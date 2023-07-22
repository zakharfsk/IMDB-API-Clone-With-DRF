from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 10
    page_size_query_param = 'size'
    last_page_strings = ('end_page',)


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'
    last_page_strings = ('end_page',)


class WatchListCPagination(CursorPagination):
    page_size = 10
    ordering = '-created'
    cursor_query_param = 'record'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = ('end_page',)
