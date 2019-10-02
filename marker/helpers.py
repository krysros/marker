import io
import xlsxwriter
from pyramid.response import Response


def export_to_xlsx(companies):
    # Create an in-memory output file for the new workbook.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
    worksheet = workbook.add_worksheet()

    # Write rows.
    header = ['Firma', 'Miasto', 'Województwo', 'Rekomendacje',
              'Imię i nazwisko', 'Stanowisko', 'Telefon', 'Email', 'WWW']

    for j, col in enumerate(header):
        worksheet.write(0, j, col)

    i = 1
    for company in companies:
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
    response.content_disposition = 'attachment; filename="export.xlsx"'
    return response
