from django.http import JsonResponse
from web import models

def load_parts(request):
    project_id = request.GET.get('project_id')
    if project_id:
        parts = models.Part.objects.filter(project_id=project_id).order_by('partName')
        part_list = list(parts.values('id', 'partName'))
        return JsonResponse(part_list, safe=False)
    else:
        return JsonResponse({'error': 'Project ID is required.'}, status=400)

def load_interfaces(request):
    part_id = request.GET.get('part_id')
    if part_id:
        interfaces = models.Interface.objects.filter(part_id=part_id).order_by('interfaceName')
        interface_list = list(interfaces.values('id', 'interfaceName'))
        return JsonResponse(interface_list, safe=False)
    else:
        return JsonResponse({'error': 'Part ID is required.'}, status=400)

def load_links(request):
    part_id = request.GET.get('part_id')
    if part_id:
        links = models.Link.objects.filter(part_id=part_id).order_by('linkName')  # Note the change here: 'linkName'
        link_list = list(links.values('id', 'linkName'))
        return JsonResponse(link_list, safe=False)
    else:
        return JsonResponse({'error': 'Part ID is required.'}, status=400)
