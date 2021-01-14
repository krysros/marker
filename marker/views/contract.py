import logging
import datetime
from pyramid.view import view_config
import colander
import deform
from deform.schema import CSRFSchema

from babel.numbers import format_currency
from babel.dates import (
    format_date,
    format_datetime,
)
from slownie import slownie_zl100gr
from ..models import Person
from .categories import (
    VOIVODESHIPS,
    UNITS,
    RMS,
)
from ..helpers import export_contract_to_docx


log = logging.getLogger(__name__)


class ContractView(object):
    def __init__(self, request):
        self.request = request

    def _get_persons(self, ids):
        persons = self.request.dbsession.query(Person).filter(Person.id.in_(ids)).all()
        result = []
        for p in persons:
            result.append(
                {
                    'fullname': p.fullname,
                    'position': p.position,
                    'phone': p.phone,
                    'email': p.email,
                }
            )
        return result

    def _insert_dots(self, appstruct):
        DOTS = '..............................'
        for k, v in appstruct.items():
            if v == '':
                appstruct[k] = DOTS
        return appstruct

    def _fmt_datetime(self, dt):
        return format_datetime(dt, format='dd.MM.YYYY', locale='pl_PL')

    def _fmt_date(self, d):
        return format_date(d, format='long', locale='pl_PL')

    def _fmt_currency(self, c):
        return format_currency(c, 'PLN', locale='pl_PL')


    def _prepare_template_data(self, company, appstruct):
        voivodeships = dict(VOIVODESHIPS)
        voivodeship = voivodeships.get(company.voivodeship)
        representation = self._get_persons(appstruct['representation'])
        contacts = self._get_persons(appstruct['contacts'])

        appstruct['name'] = company.name
        appstruct['street'] = company.street
        appstruct['postcode'] = company.postcode
        appstruct['city'] = company.city
        appstruct['voivodeship'] = voivodeship
        appstruct['phone'] = company.phone
        appstruct['email'] = company.email
        appstruct['www'] = company.www
        appstruct['nip'] = company.nip
        appstruct['regon'] = company.regon
        appstruct['krs'] = company.krs
        appstruct['court'] = company.court
        appstruct['representation'] = representation
        appstruct['contacts'] = contacts

        penalty = 0
        for price in appstruct['contract_price']:
            value = price['price']
            price['category'] = ''.join(price['category'])
            price['price'] = self._fmt_currency(value)
            price['in_words'] = slownie_zl100gr(value)
            penalty += 0.005 * float(value)

        if penalty < 1000:
            appstruct['penalty'] = self._fmt_currency(1000.00)

        total = 0
        appstruct['labels'] = ['Zakres', 'Od', 'Do', 'Wartość']
        periods_from = []
        periods_to = []
        for deadline in appstruct['deadlines']:
            value = deadline['value']
            period_from = deadline['period_from']
            period_to = deadline['period_to']
            periods_from.append(period_from)
            periods_to.append(period_to)
            deadline['period_from'] = self._fmt_datetime(period_from)
            deadline['period_to'] = self._fmt_datetime(period_to)
            deadline['value'] = self._fmt_currency(value)
            total += value
        appstruct['total'] = self._fmt_currency(total)

        today = datetime.datetime.now()
        start_date = min(periods_from)
        end_date = max(periods_to)
        final_date = end_date + datetime.timedelta(30)
        appstruct['today'] = self._fmt_date(today)
        appstruct['start_date'] = self._fmt_date(start_date)
        appstruct['end_date'] = self._fmt_date(end_date)
        appstruct['final_date'] = self._fmt_date(final_date)
        appstruct = self._insert_dots(appstruct)
        return appstruct

    @staticmethod
    def _get_people(company):
        people = []
        for person in company.people:
            people.append((person.id, person.fullname))
        return people

    @property
    def contract_form(self):

        class Price(colander.Schema):
            price = colander.SchemaNode(
                colander.Decimal(),
                title='Cena (PLN)',
                widget=deform.widget.MoneyInputWidget(options={'allowZero': True}),
            )
            unit = colander.SchemaNode(
                colander.String(),
                title='Jednostka',
                missing='',
                widget=deform.widget.SelectWidget(values=UNITS),
            )
            category = colander.SchemaNode(
                colander.List(),
                title='Kategoria',
                widget=deform.widget.CheckboxChoiceWidget(
                    values=RMS, inline=True
                ),
                validator=colander.Length(min=1),
            )
            description = colander.SchemaNode(
                colander.String(),
                title='Opis',
            )

        class Deadline(colander.Schema):
            scope = colander.SchemaNode(
                colander.String(),
                title='Zakres',
            )
            period_from = colander.SchemaNode(
                colander.Date(),
                title='Termin (od)',
            )
            period_to = colander.SchemaNode(
                colander.Date(),
                title='Termin (do)',
            )
            value = colander.SchemaNode(
                colander.Decimal(),
                title='Wartość (PLN)',
                widget=deform.widget.MoneyInputWidget(options={'allowZero': True}),
            )

        class ContractPrice(colander.SequenceSchema):
            price = Price(title='Cena')

        class Deadlines(colander.SequenceSchema):
            deadline = Deadline(title='Termin')

        class Schema(CSRFSchema):
            representation = colander.SchemaNode(
                colander.List(),
                title='Reprezentacja',
                widget=deform.widget.Select2Widget(
                    values=self.people, multiple=True
                ),
            )
            contacts = colander.SchemaNode(
                colander.List(),
                title='Osoby do kontaktu',
                widget=deform.widget.Select2Widget(
                    values=self.people, multiple=True
                ),
            )
            subject = colander.SchemaNode(
                colander.String(),
                title='Przedmiot umowy',
                )
            materials = colander.SchemaNode(
                colander.Boolean(),
                description='Zaznacz, jeśli materiały dostarcza Podwykonawca',
                widget=deform.widget.CheckboxWidget(),
                title='Materiały',
            )
            works_manager = colander.SchemaNode(
                colander.Boolean(),
                description='Zaznacz, jeśli wymagany jest kierownik robót z uprawnieniami w danej specjalności',
                widget=deform.widget.CheckboxWidget(),
                title='Kierownik robót',
            )
            payment_deadline = colander.SchemaNode(
                colander.Integer(),
                default=30,
                title='Termin płatności (dni)',
                validator=colander.Range(min=0),
            )
            utilities = colander.SchemaNode(
                colander.Decimal(),
                default=1,
                title='Media (%)',
                validator=colander.Range(min=0, max=100),
            )
            deposit = colander.SchemaNode(
                colander.Decimal(),
                default=5,
                title='Kaucja (%)',
                validator=colander.Range(min=0, max=100),
            )
            refund = colander.SchemaNode(
                colander.Integer(),
                default=40,
                missing=0,
                title='Zwrot kaucji (%)',
                validator=colander.Range(min=0, max=100),
                description='Domyślnie w całości lub w części zmieniona na gwarancję ubezpieczeniową lub bankową',
            )
            guarantee = colander.SchemaNode(
                colander.Integer(),
                default=66,
                title='Gwarancja (miesiące)',
                validator=colander.Range(min=0),
            )
            warranty = colander.SchemaNode(
                colander.Integer(),
                default=66,
                title='Rękojmia (miesiące)',
                validator=colander.Range(min=0),
            )
            contract_price = ContractPrice(title='Wynagrodzenie')
            deadlines = Deadlines(title='Terminy')

        schema = Schema().bind(request=self.request)
        submit_btn = deform.form.Button(name='submit', title='Pobierz')
        form = deform.Form(schema, buttons=(submit_btn,))
        form.set_widgets({'subject': deform.widget.TextAreaWidget()})
        form.set_widgets({'contract_price': deform.widget.SequenceWidget(min_len=1)})
        form.set_widgets({'deadlines': deform.widget.SequenceWidget(min_len=1)})
        return form

    @view_config(
        route_name='contract',
        renderer='form.mako',
        permission='view'
    )
    def prepare(self):
        company = self.request.context.company
        self.people = self._get_people(company)
        form = self.contract_form
        appstruct = {}
        rendered_form = None

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except deform.exception.ValidationFailure as e:
                rendered_form = e.render()
            else:
                fields = self._prepare_template_data(company, appstruct)
                response = export_contract_to_docx(fields)
                log.info(f'Użytkownik {self.request.user.username} wygenerował wzór umowy dla firmy {company.name}')
                return response

        if rendered_form is None:
            rendered_form = form.render(appstruct=appstruct)
        reqts = form.get_widget_resources()

        return dict(
            heading=f'Wzór umowy dla firmy {company.name}',
            rendered_form=rendered_form,
            css_links=reqts['css'],
            js_links=reqts['js'],
            )
