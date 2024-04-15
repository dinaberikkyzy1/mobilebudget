
import os
from pydoc import doc
import re

import PyPDF2
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import tabulate
import os
import json

from .forms import IncomeForm, ReviewForm, SpendingForm


@csrf_exempt
# def convert_pdf_to_json(request):
#     if request.method == 'POST':
#         # Get the uploaded file from the request
#         pdf_file = request.FILES.get('pdf_file')

#         if pdf_file:
            
#             pdf_path = default_storage.save(os.path.join(settings.MEDIA_ROOT, 'test.pdf'),pdf_file)

#             # Extract tables from PDF
#             tables = extract_tables_from_pdf(pdf_path)

#             # Convert tables to JSON
#             json_data = convert_tables_to_json(tables)

#             return JsonResponse({'data': json_data})

#     return JsonResponse({'error': 'Invalid request'}, status=400, safe=False)


def convert_pdf_to_json(request):
    if request.method == 'POST':
        # Get the uploaded file from the request
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file:
            # Get the path to the permanent file
            permanent_pdf = os.path.join(settings.MEDIA_ROOT, 'permanent.pdf')

            # Open the permanent file in append mode and write the contents of the uploaded PDF
            with default_storage.open(permanent_pdf, 'ab') as permanent_file:
                for chunk in pdf_file.chunks():
                    permanent_file.write(chunk)

            # Extract tables from PDF
            tables = extract_tables_from_pdf(permanent_pdf)

            # Convert tables to JSON
            json_data = convert_tables_to_json(tables)

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

@csrf_exempt
def onboarding_step1(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('onboarding_step2')
    else:
        form = IncomeForm()
    return render(request, 'onboarding_step1.html', {'form': form})

def onboarding_step2(request):
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            spending = form.save(commit=False)
            spending.user = request.user
            spending.save()
            return redirect('onboarding_step3')
    else:
        form = SpendingForm()
    return render(request, 'onboarding_step2.html', {'form': form})

def onboarding_step3(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('onboarding_complete')
    else:
        form = ReviewForm()
    return render(request, 'onboarding_step3.html', {'form': form})

def onboarding_complete(request):
    return render(request, 'onboarding_complete.html')


# def convert_tables_to_json(tables):
#     json_data = []
#     del (tables[0][0])
#     for table in tables:
#         for row in table:
            
#             if '₸' not in row: continue
#             if "JSC" in row: continue

#             date = row[:8]
#             comma_index = row.find(",")
         
#             amount = "".join([i for i in row][9:comma_index])

#             transaction_type = ""

#             if "+" in row:
#                 transaction_type = "Income"
#             elif "-" in row:
#                 print(row)
#                 transaction_type = "Outcome"

#             json_entry = {
#                 "date": date,
#                 "amount": int(''.join(re.findall('\d+', amount))),
#                 "type": transaction_type,
#                 "category": re.sub(' +', ' ', row.split('₸', 1)[1].strip()).split(' ', 1)[0]
#             }

#             json_data.append(json_entry)
#     return json_data


@csrf_exempt
def export_to_pdf(request):
    if request.method == 'POST':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="data.pdf"'
        
        json_file = request.FILES.get('json_file')
        
        if not json_file:
            return HttpResponse("No JSON file provided", status=400)
        
        try:
            json_data = json.load(json_file)
        except json.JSONDecodeError as e:
            return HttpResponse(f"Error reading JSON file: {e}", status=400)
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        header = json_data[0].keys()
        rows =  [list(x.values()) for x in json_data]
        
        table_data = [header] + rows
        
        table = Table(table_data)
        table.setStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        
        doc.build([table])
        
        # Save the PDF directly to the permanent location
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'data.pdf')
        with open(pdf_file_path, 'wb') as pdf_file:
            pdf_file.write(response.content)

        return HttpResponse(f"PDF saved to {pdf_file_path}")
    else:
        return HttpResponse("Method not allowed", status=405)
