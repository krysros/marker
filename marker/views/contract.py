import logging
import datetime
from pyramid.view import view_config
import colander
import deform
from deform.schema import CSRFSchema

from babel.numbers import (
    format_currency,
    get_currency_symbol,
)
from babel.dates import (
    format_date,
    format_datetime,
)
from slownie import (
    slownie,
    slownie_zl100gr,
)
from ..models import Person
from .categories import (
    VOIVODESHIPS,
    CURRENCIES,
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

    def _prepare_template_data(self, company, appstruct):
        voivodeships = dict(VOIVODESHIPS)
        appstruct['name'] = company.name
        appstruct['street'] = company.street
        appstruct['postcode'] = company.postcode
        appstruct['city'] = company.city
        appstruct['voivodeship'] = voivodeships.get(company.voivodeship)
        appstruct['phone'] = company.phone
        appstruct['email'] = company.email
        appstruct['www'] = company.www
        appstruct['nip'] = company.nip
        appstruct['regon'] = company.regon
        appstruct['krs'] = company.krs
        appstruct['court'] = company.court
        appstruct['representation'] = self._get_persons(appstruct['representation'])
        appstruct['contacts'] = self._get_persons(appstruct['contacts'])
        penalty = 0
        for price in appstruct['contract_price']:
            price['category'] = ''.join(price['category'])
            value = price['price']
            rest = f"{str(value).split('.')[1]}/100"
            currency = price['currency']
            currency_symbol = get_currency_symbol(currency, locale='pl_PL')
            price['price'] = format_currency(value, currency, locale='pl_PL')
            if currency == 'PLN':
                price['in_words'] = slownie_zl100gr(value)
            else:
                price['in_words'] = f'{slownie(float(value))} {currency_symbol} {rest}'
            penalty += 0.005 * float(value)

        if penalty < 1000:
            # TODO: Aktualnie to przeliczenie ma sens tylko gdy wszystkie ceny wyrażone są w złotówkach
            appstruct['penalty'] = format_currency(1000.00, 'PLN', locale='pl_PL')

        periods_from = []
        periods_to = []
        for deadline in appstruct['deadlines']:
            period_from = deadline['period_from']
            period_to = deadline['period_to']
            periods_from.append(period_from)
            periods_to.append(period_to)
            deadline['period_from'] = format_datetime(period_from,
                                                      format='dd.MM.YYYY',
                                                      locale='pl_PL')
            deadline['period_to'] = format_datetime(period_to,
                                                    format='dd.MM.YYYY',
                                                    locale='pl_PL')

        today = datetime.datetime.now()
        appstruct['today'] = format_date(today,
                                         format='long',
                                         locale='pl_PL')
        appstruct['start_date'] = format_date(min(periods_from),
                                              format='long',
                                              locale='pl_PL')
        appstruct['end_date'] = format_date(max(periods_to),
                                            format='long',
                                            locale='pl_PL')
        final_date = max(periods_to) + datetime.timedelta(30)
        appstruct['final_date'] = format_date(final_date,
                                              format='long',
                                              locale='pl_PL')
        return appstruct

    @staticmethod
    def _get_people(company):
        people = []
        for p in company.people:
            people.append((p.id, p.fullname))
        return people

    @property
    def contract_form(self):

        choices = (
            ('SC', 'Podwykonawcę'),
            ('GC', 'Genralnego Wykonawcę'),
        )

        class Price(colander.Schema):
            price = colander.SchemaNode(
                colander.Decimal(),
                title='Cena',
                widget=deform.widget.MoneyInputWidget(options={'allowZero': True}),
            )
            currency = colander.SchemaNode(
                colander.String(),
                title='Waluta',
                widget=deform.widget.SelectWidget(values=CURRENCIES), 
            )
            unit = colander.SchemaNode(
                colander.String(),
                title='Jednostka',
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
                title='Wartość',
                widget=deform.widget.MoneyInputWidget(options={'allowZero': True}),
            )
            currency = colander.SchemaNode(
                colander.String(),
                title='Waluta',
                widget=deform.widget.SelectWidget(values=CURRENCIES), 
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
                colander.String(),
                title='Materiały dostarczane przez',
                widget=deform.widget.SelectWidget(values=choices),
            )
            manager = colander.SchemaNode(
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
                title='Zwrot kaucji (%)',
                validator=colander.Range(min=0, max=100),
                description='Jeżeli zero, to może zostać w całości lub w części zmieniona na gwarancję ubezpieczeniową lub bankową',
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
