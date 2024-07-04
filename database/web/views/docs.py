from django.shortcuts import render
from django.http import HttpResponse, Http404
import os
from django.conf import settings

def serve_docs(request, path):
    document_root = os.path.join(settings.STATICFILES_DIRS[0], 'docs')
    full_path = os.path.join(document_root, path)

    if os.path.isdir(full_path):
        index_file = os.path.join(full_path, 'index.html')
        if os.path.exists(index_file):
            with open(index_file, 'rb') as f:
                return HttpResponse(f.read(), content_type='text/html')
        else:
            raise Http404("Directory index file not found")
    elif os.path.exists(full_path):
        with open(full_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='text/html')
    else:
        raise Http404("File not found")
