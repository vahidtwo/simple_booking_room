import inspect

from django.contrib import admin
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase


class AbstractBaseAdmin(admin.ModelAdmin):
    default_list_display = ('created_at',)
    list_display = ('id', '__str__') + default_list_display
    default_list_filter = ('created_at', 'updated_at')
    list_filter = default_list_filter
    default_search_fields = ('id',)
    search_fields = default_search_fields
    readonly_fields = ('created_at', 'updated_at')
    default_fieldset = (None, {'fields': (('created_at', 'updated_at'),)})

    def changelist_view(self, request, extra_context=None):
        actions = self.get_actions(request)
        if actions and request.method == 'POST' and 'index' in request.POST and '_save' not in request.POST:
            response = self.response_action(request, queryset=self.get_queryset(request))
            if response:
                return response
        return super().changelist_view(request, extra_context)

    def response_action(self, request, queryset):
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            pass

        action_form = self.action_form(data, auto_id=None)
        action_form.fields['action'].choices = self.get_action_choices(request)

        if action_form.is_valid():
            action = action_form.cleaned_data['action']
            select_across = action_form.cleaned_data['select_across']
            func = self.get_actions(request)[action][0]
            has_queryset = 'queryset' in inspect.signature(func).parameters
            selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
            if not selected and not select_across and has_queryset:
                return None

            if not select_across:
                queryset = queryset.filter(pk__in=selected)

            if has_queryset:
                response = func(self, request, queryset)
            else:
                response = func(self, request)

            if isinstance(response, HttpResponseBase):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            return None
