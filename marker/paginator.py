import paginate


def get_paginator(request, query, page=1):
    query_params = request.GET.mixed()

    def url_maker(page_number):
        query_params['page'] = page_number
        return request.current_route_url(_query=query_params)
    return SqlalchemyOrmPage(query, page,
                             items_per_page=50,
                             url_maker=url_maker)


def paginate_link_tag(item):
    """
    Create an A-HREF tag that points to another page usable in paginate.
    """
    a_tag = paginate.Page.default_link_tag(item)
    if item['type'] == 'current_page':
        return paginate.make_html_tag('li', a_tag, **{'class': 'active'})
    return paginate.make_html_tag('li', a_tag)


class SqlalchemyOrmWrapper(object):
    """Wrapper class to access elements of a collection."""
    def __init__(self, obj):
        self.obj = obj

    def __getitem__(self, range):
        # Return a range of objects of an sqlalchemy.orm.query.Query object
        return self.obj[range]

    def __len__(self):
        # Count the number of objects in an sqlalchemy.orm.query.Query object
        return self.obj.count()


class SqlalchemyOrmPage(paginate.Page):
    """A pagination page that deals with SQLAlchemy ORM objects."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, wrapper_class=SqlalchemyOrmWrapper, **kwargs)

    def pager(self):
        return super().pager(
            '$link_previous ~2~ $link_next',
            curpage_attr={'class': 'current_page'},
            dotdot_attr={'class': 'spacer'},
            symbol_first='<i class="fa fa-chevron-circle-left" aria-hidden="true"></i>',
            symbol_last='<i class="fa fa-chevron-circle-right" aria-hidden="true"></i>',
            symbol_previous='<i class="fa fa-chevron-left" aria-hidden="true"></i>',
            symbol_next='<i class="fa fa-chevron-right" aria-hidden="true"></i>',
            link_tag=paginate_link_tag
        )
