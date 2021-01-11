import io
import xlsxwriter
from pyramid.response import Response
from pyramid.path import AssetResolver
from docxtpl import DocxTemplate


def export_companies_to_xlsx(items):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    # Write rows.
    header = ['Firma', 'Miasto', 'Województwo', 'Rekomendacje',
              'Imię i nazwisko', 'Stanowisko', 'Telefon', 'Email', 'WWW']

    for j, col in enumerate(header):
        worksheet.write(0, j, col, bold)

    i = 1
    for company in items:
        cols = [company.name, company.city, company.voivodeship,
                company.upvote_count, '', 'BIURO',
                company.phone, company.email, company.www]
        for j, col in enumerate(cols):
            worksheet.write(i, j, col)
        i += 1
        for person in company.people:
            cols = [company.name, company.city,
                    company.voivodeship, company.upvote_count,
                    person.fullname, person.position,
                    person.phone, person.email, company.www]
            for j, col in enumerate(cols):
                worksheet.write(i, j, col)
            i += 1

    # Close the workbook before streaming the data.
    workbook.close()
    # Rewind the buffer.
    output.seek(0)
    # Construct a server response.
    response = Response()
    response.body_file = output
    response.content_type = 'application/vnd.openxmlformats-' \
                            'officedocument.spreadsheetml.sheet'
    response.content_disposition = 'attachment; filename="firmy.xlsx"'
    return response


def export_offers_to_xlsx(items, query):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True, 'default_date_format': 'dd/mm/yyyy'})
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    if query == 'edited':
        date_header = 'Zmodyfikowano'
    else:
        date_header = 'Utworzono'

    # Write rows.
    header = ['Firma', 'Przetarg', 'Kategoria', 'Jedn.',
              'Cena', 'Waluta', date_header]

    for j, col in enumerate(header):
        worksheet.write(0, j, col, bold)

    i = 1
    for offer in items:
        cols = [offer.company.name, offer.tender.name, offer.category,
                offer.unit, offer.cost, offer.currency]
        for j, col in enumerate(cols):
            worksheet.write(i, j, col)
        if query == 'edited':
            worksheet.write_datetime(i, j + 1, offer.edited)
        else:
            worksheet.write_datetime(i, j + 1, offer.added)
        i += 1

    # Close the workbook before streaming the data.
    workbook.close()
    # Rewind the buffer.
    output.seek(0)
    # Construct a server response.
    response = Response()
    response.body_file = output
    response.content_type = 'application/vnd.openxmlformats-' \
                            'officedocument.spreadsheetml.sheet'
    response.content_disposition = 'attachment; filename="oferty.xlsx"'
    return response


def export_contract_to_docx(fields):
    a = AssetResolver('marker')
    resolver = a.resolve('templates/draft_contract.docx')
    template = resolver.abspath()
    docx = DocxTemplate(template)
    docx.render(fields)
    output = io.BytesIO()
    docx.save(output)
    output.seek(0)
    response = Response()
    response.body_file = output
    response.content_type = 'application/vnd.openxmlformats-' \
                            'officedocument.wordprocessingml.document'
    response.content_disposition = 'attachment; filename="umowa.docx"'
    return response
