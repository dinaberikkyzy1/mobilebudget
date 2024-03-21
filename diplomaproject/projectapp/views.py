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

            # Return the JSON response
            tables = extract_tables_from_pdf(temp_path)
            print(tables)
            json_response = convert_tables_to_json(tables)

            return JsonResponse(json_response, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400, safe=False)

def extract_tables_from_pdf(temp_path):
    pdf_file = open(temp_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    print(num_pages)
    tables = []
    for page_number in range(num_pages):
        page_text = pdf_reader.pages[page_number].extract_text()
        page_tables = extract_tables_from_page_text(page_text)
        tables.extend(page_tables)
    pdf_file.close()
    return tables

def extract_tables_from_page_text(page_text):
    # Regular expression to identify simple table-like structures
    # This is just a basic example and might need to be adjusted based on the actual PDF structure
    #table_regex = r'\d+\s+[A-Za-z]+\s+\d+\s+'  # Example: 1   Item A    100
    table_regex = r'\d+\s+[A-Za-z]+\s+Replenishment\s+\d+\s+'

    tables = []
    # lines = page_text.split('\n')
    # current_table = []
    # for line in lines:
    #     if re.match(table_regex, line):
    #         current_table.append(line.strip())
    #     elif current_table:
    #         tables.append(current_table)
    #         current_table = []
    # if current_table:
    #     tables.append(current_table)
    ##################
    lines = page_text.split('\n')
    current_table = []
    for line in lines:
        # if re.match(table_regex, line):
        if 'Replenishment' in line:

            current_table.append(line.strip())
        # elif current_table:
        #     tables.append(current_table)
    # if current_table:
    tables.append(current_table)

    ###########
    return tables

def convert_tables_to_json(tables):
    json_data = []
    del (tables[0][0])
    for table in tables:
        for row in table:
                # Extracting relevant information from the table row
            date = row[:8]
            amount = "".join([i for i in row if i.isnumeric()][6:-2])

            if "Income" in row:
                category = "Income"
            elif "Outcome" in row:
                category = "Outcome"
            elif "Replenishment" in row:
                category = "Replenishment"


            if "+" in row:
               type = "Income"
            elif "-" in row:
               type = "Outcome"

            json_entry = {
                "date": date,
                "amount": amount,
                "type": type,
                "category": category
            }
            json_data.append(json_entry)
    return json_data

    return JsonResponse({'error': 'Invalid request'}, status=400,safe=False)
