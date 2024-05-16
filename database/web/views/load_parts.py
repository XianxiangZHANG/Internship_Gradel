from django.http import JsonResponse
from web import models

def load_parts(request):
    project_id = request.GET.get('project_id')
    parts = models.Part.objects.filter(project_id=project_id).order_by('partName')
    part_list = list(parts.values('id', 'partName'))
    return JsonResponse(part_list, safe=False)

def load_interfaces(request):
    part_id = request.GET.get('part_id')
    interfaces = models.interface.objects.filter(part_id=part_id).order_by('interfaceName')
    interface_list = list(interfaces.values('id', 'interfaceName'))
    return JsonResponse(interface_list, safe=False)