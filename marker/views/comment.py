import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import deform
from deform.schema import CSRFSchema
import colander

from ..models import Comment


log = logging.getLogger(__name__)


class CommentView(object):
    def __init__(self, request):
        self.request = request

    @property
    def comment_form(self):
        class Schema(CSRFSchema):
            comment = colander.SchemaNode(
                colander.String(),
                title='Komentarz',
                )
        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Dodaj')
        form = deform.Form(schema, buttons=(submit_btn,))
        form.set_widgets({'comment': deform.widget.TextAreaWidget()})
        return form

    @view_config(
        route_name='comment_add',
        renderer='form.mako',
        permission='edit'
    )
    def add(self):
        company = self.request.context.company
        form = self.comment_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                comment = Comment(
                    comment=appstruct['comment'],
                    )
                comment.added_by = self.request.user
                company.comments.append(comment)
                self.request.dbsession.add(comment)
                self.request.session.flash('success:Dodano do bazy danych')
                log.info(f'Użytkownik {self.request.user.username} dodał komentarz {comment.comment}')
                return HTTPFound(location=self.request.route_url('company_view', company_id=company.id, slug=company.slug))

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading=f'Komentarz dot. firmy {company.name}',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )

    @view_config(
        route_name='comment_delete',
        request_method='GET',
        permission='edit'
    )
    def delete(self):
        company = self.request.context.company
        comment = self.request.context.comment
        self.request.dbsession.delete(comment)
        self.request.session.flash('success:Usunięto z bazy danych')
        log.info(f'Użytkownik {self.request.user.username} usunął komentarz dot. firmy {company.name}')
        return HTTPFound(location=self.request.route_url('company_view', company_id=company.id, slug=company.slug))
