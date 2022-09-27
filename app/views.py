import os.path

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
import csv

from .models import UploadSync
from CsvProcessing.csvprocessing import CsvProcessing

"""using the decorator sync_to_async This means that the synchronous function, http_call_sync, will be run in a new thread. Review the docs for more 
info. as we need interact with the db is not posible to use only library asyncIO without to use sync_to_async"""


@sync_to_async
def upload(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for img in images:
            # if file is not , return
            if not img.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return HttpResponseRedirect(reverse("myapp:upload_csv"))
            # if file is too large, return
            if img.multiple_chunks():
                messages.error(request, "Uploaded file is too big (%.2f MB)." % (images.size / (1000 * 1000),))
                return HttpResponseRedirect(reverse("myapp:upload_csv"))

            file_data = img.read().decode("utf-8")
            lines = file_data.split("\n")
            load_files = []
            for line in lines[1:]:
                fields = line.split(",")
                data_dict = {"Song": fields[0], "Date": fields[1], "Number of Plays": fields[2]}
                load_files.append(data_dict)
            # here is called the function from the module created
            c = CsvProcessing()
            c.read_csv(payload_files_test=load_files)
            dict_processed = c.process_csv()
            plays_info = ['Song', 'Date', 'Total Number of Plays for Date']
            UploadSync.objects.create(images=img)

            with open(f'input/{img}', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=plays_info)
                writer.writeheader()
                writer.writerows(dict_processed)

    images = UploadSync.objects.all()

    return render(request, "index.html", {'images': images})


@sync_to_async
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(file_path)
            return response
    raise Http404
