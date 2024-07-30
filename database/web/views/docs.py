from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404, JsonResponse
import os
from django.conf import settings
import mimetypes
import shutil
import zipfile

def serve_docs(request, path):
    document_root = os.path.join(settings.STATICFILES_DIRS[0], 'docs/site')
    full_path = os.path.join(document_root, path)

    if os.path.isdir(full_path):
        index_file = os.path.join(full_path, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'rb') as f:
                return HttpResponse(f.read(), content_type='text/html')
        else:
            raise Http404("Directory index file not found")
    elif os.path.exists(full_path):
        mime_type, _ = mimetypes.guess_type(full_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'
        with open(full_path, 'rb') as f:
            return HttpResponse(f.read(), content_type=mime_type)
    else:
        raise Http404("File not found")

def upload_docs(request):
    if request.method == 'POST' and request.FILES['zip_file']:
        uploaded_file = request.FILES['zip_file']
        docs_dir = os.path.join(settings.STATICFILES_DIRS[0], 'docs')

        # clean /docs
        for filename in os.listdir(docs_dir):
            file_path = os.path.join(docs_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        # make sure a zip file
        if not uploaded_file.name.endswith('.zip'):
            return JsonResponse({'status': 'error', 'message': 'Uploaded file is not a zip file'}, status=400)

        temp_zip_path = os.path.join(settings.BASE_DIR, 'temp.zip')
        with open(temp_zip_path, 'wb+') as temp_zip:
            for chunk in uploaded_file.chunks():
                temp_zip.write(chunk)

        try:
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                zip_ref.extractall(docs_dir)
        except zipfile.BadZipFile:
            return JsonResponse({'status': 'error', 'message': 'Invalid zip file'}, status=400)
        finally:
            os.remove(temp_zip_path)

        return JsonResponse({'status': 'success', 'message': 'Files uploaded successfully'})

    return render(request, 'doc/updateDoc.html')