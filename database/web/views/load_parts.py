from django.http import JsonResponse
from web import models

def load_parts(request):
    project_id = request.GET.get('project_id')
    parts = models.Part.objects.filter(project_id=project_id).order_by('partName')
    part_list = list(parts.values('id', 'partName'))
    return JsonResponse(part_list, safe=False)
