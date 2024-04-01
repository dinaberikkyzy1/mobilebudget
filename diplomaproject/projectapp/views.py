import csv
import os
import re
import PyPDF2
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def convert_pdf_to_json(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file:
            # Save the PDF file temporarily
            temp_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, 'temp.pdf'), ContentFile(pdf_file.read()))

            # Extract tables from PDF
            tables = extract_tables_from_pdf(temp_path)

            # Convert tables to JSON
            json_data = convert_tables_to_json(tables)

            # Export JSON data to CSV
            csv_file_path = os.path.join(settings.MEDIA_ROOT, 'output.csv')
            csv_exported_path = export_json_to_csv(json_data, csv_file_path)

            # Return CSV file path
            return JsonResponse({'data': json_data})

    return JsonResponse({'error': 'Invalid request'}, status=400, safe=False)


def extract_tables_from_pdf(temp_path):
    pdf_file = open(temp_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    tables = []

    for page_number in range(num_pages):
        page_text = pdf_reader.pages[page_number].extract_text()
        page_tables = extract_tables_from_page_text(page_text)
        if page_number == 0:
            continue
        tables.extend(page_tables)

    pdf_file.close()

    tables.sort(key=lambda x: x[0].split()[0])

    return tables



def extract_tables_from_page_text(page_text):
    tables = []

    lines = page_text.split('\n')

    current_table = []

    for line in lines:
        current_table.append(line.strip())

    tables.append(current_table)

    return tables

def convert_tables_to_json(tables):
    json_data = []
    del (tables[0][0])
    for table in tables:
        for row in table:
            if '₸' not in row: continue
            if "JSC" in row: continue

            date = row[:8]
            comma_index = row.find(",")

            amount = "".join([i for i in row][9:comma_index])

            transaction_type = ""

            if "+" in row:
                transaction_type = "Income"
            elif "-" in row:
                transaction_type = "Outcome"

            json_entry = {
                "date": date,
                "amount": int(''.join(re.findall('\d+', amount))),
                "type": transaction_type,
                "category": re.sub(' +', ' ', row.split('₸', 1)[1].strip()).split(' ', 1)[0]
            }

            json_data.append(json_entry)
    return json_data


def export_json_to_csv(json_data, csv_file_path):
    fieldnames = ['date', 'amount', 'type', 'category']

    with open(csv_file_path, mode='w', newline='',encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(json_data)

    return csv_file_path

