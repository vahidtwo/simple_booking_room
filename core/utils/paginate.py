from django.core.paginator import Paginator, EmptyPage, InvalidPage


def paginate(data, page=None, limit=None, url='', serializer=None, serializer_kwargs=None):
    next_page_url, previous_page_url, next_page, previous_page, count, pages = None, None, None, None, 0, 0
    page = int(page) if page else 1
    limit = int(limit) if limit else 10
    try:
        data = Paginator(data, limit)
        pages = data.num_pages
        count = data.count
        data = data.page(page)
        if data.has_next():
            next_page_url = '{}&page={}&limit={}'.format(url, page + 1, limit)
            next_page = page + 1
        if data.has_previous():
            previous_page_url = '{}&page={}&limit={}'.format(url, page - 1, limit)
            previous_page = page - 1
        if serializer:
            serializer_kwargs = serializer_kwargs if serializer_kwargs else {}
            data = serializer(data, many=True, **serializer_kwargs).data
        else:
            data = list(data)
    except EmptyPage or InvalidPage:
        data = []
    return {
        'data': data,
        'pagination': {
            'count': count,
            'pages': pages,
            'page': page,
            'limit': limit,
            'next': next_page, 'next_url': next_page_url,
            'previous': previous_page, 'previous_url': previous_page_url
        }
    }
