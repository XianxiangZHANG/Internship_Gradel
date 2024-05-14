# from django.shortcuts import render, redirect
# from django.forms import modelformset_factory
# from web.models import Bushing, Project
# from web.views.bushing import BushingModelForm

# def bushing_add_multiple(request):
#     BushingFormSet = modelformset_factory(Bushing, form=BushingModelForm, extra=1)
#     if request.method == "POST":
#         formset = BushingFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             project = request.POST.get('project')
#             part = request.POST.get('part')
#             for instance in instances:
#                 instance.project_id = project
#                 instance.part_id = part
#                 instance.save()
#             return redirect('/bushing/list/')
#     else:
#         formset = BushingFormSet(queryset=Bushing.objects.none())
#     projects = Project.objects.all()
#     return render(request, 'bushing_add_multiple.html', {'formset': formset, 'projects': projects})
