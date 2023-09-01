import openpyxl

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from products.parsers import parse_product
from products.models import Product


def home(request):
    products = Product.objects.all().order_by("sku")
    context = {
        "products": products,
    }
    return render(request, "products/index.html", context=context)


def upload_excel(request):
    data = {}
    if "GET" == request.method:
        return render(request, "products/upload.html", data)

    try:
        excel_file = request.FILES["excel_file"]
        if not excel_file.name.endswith(".xlsx"):
            messages.error(request, "File is not a XLSX")
            return HttpResponseRedirect(reverse("products:upload_excel"))
        if excel_file.multiple_chunks():
            messages.error(
                request,
                "Uploaded file is too big (%.2f MB). "
                % (excel_file.size / (1000 * 1000),),
            )
            return HttpResponseRedirect(reverse("products:upload_excel"))
        file_data = openpyxl.load_workbook(excel_file)
        worksheet = file_data["Лист1"]
        errors = False
        for row in worksheet.iter_rows():
            for cell in row:
                try:
                    parse_product(int(cell.value))
                except Exception as e:
                    messages.error(request, "Unable to upload file. " + repr(e))
                    errors = True
                    pass
        if not errors:
            messages.success(request, "All data uploaded successfully!")
    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))
    return HttpResponseRedirect(reverse("products:upload_excel"))
