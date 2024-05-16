from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class BushingFilter(django_filters.FilterSet):
    class Meta:
        model = models.Bushing
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
            'bushingName': ['icontains'],
        }

def bushing_list(request):
    """ list of bushing """

    # # [obj,]
    # queryset = models.Bushing.objects.all().order_by("id")
    # # for row in queryset:
    # #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    # # for row in queryset:
    # #     print(row.project.projectName)

    # return render(request, 'bushing_list.html', {"queryset": queryset})
    bushing_filter = BushingFilter(request.GET, queryset=models.Bushing.objects.all())
    return render(request, 'bushing/bushing_list.html', {'filter': bushing_filter})

def bushing_input(request):
    """ list of bushing """

    # [obj,]
    queryset = models.Bushing.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'bushing/bushing_input.html', {"queryset": queryset})

   
class BushingModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}

class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)

BushingFormSet = modelformset_factory(
    models.Bushing,
    form=BushingModelForm,
    extra=1  # 初始化时额外添加的表单数量
)


# def bushing_add_multiple(request):
#     BushingFormSet = modelformset_factory(models.Bushing, form=BushingModelForm, extra=1)

    
#     # formset = BushingFormSet(queryset=models.Bushing.objects.none())
#     project_error = part_error = bushing_error = None

#     if request.method == 'POST':
#         formset = BushingFormSet(request.POST)
#         project_s = request.POST.get('project')
#         part_s = request.POST.get('part')
#         bushingName = request.POST.get('bushingName')

#         if not project_s:
#             project_error = 'Project is required.'
                
#         if not part_s:
#             part_error = 'Part is required.'
        
#         if not bushingName:
#             bushing_error = 'Required.'
            
#         if formset.is_valid() and project_s and part_s and bushingName:
#             instances = formset.save(commit=False)
#             project = models.Project.objects.get(id=project_s)
#             part = models.Part.objects.get(id=part_s)
#             for instance in instances:
#                 instance.project_id = project
#                 instance.part_id = part
#                 instance.save()
#             return redirect('/bushing/list/')  # 替换为你的重定向URL

#     else:
#         formset = BushingFormSet(queryset=models.Bushing.objects.none())

#     projects = models.Project.objects.all()
#     return render(request, 'bushing_add_multiple.html', {
#         'projects': projects,
#         'formset': formset,
#         'project_error': project_error,
#         'part_error': part_error,
#         'bushing_error': bushing_error,
#     })
def bushing_add_multiple(request):
    projects = models.Project.objects.all()
    formset = BushingFormSet(queryset=models.Bushing.objects.none())
    project_part_form = ProjectPartForm()
    # bushingError = None

    if request.method == 'POST':
        formset = BushingFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)
        # bushingName = request.POST.get('bushingName')
        # if not bushingName:
        #     bushingError = "Required"
        if formset.is_valid() and project_part_form.is_valid():
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/bushing/list/')  # Replace with your redirect URL

    return render(request, 'bushing/bushing_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        # 'bushingError': bushingError,
    })


def bushing_add(request):
    if request.method == "GET":
        form = BushingModelForm()
        return render(request, 'bushing/bushing_form.html', {"form": form})

    form = BushingModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing/bushing_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/bushing/list/')


class BushingEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['project', 'part', 'bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def bushing_edit(request, aid):
    bushing_object = models.Bushing.objects.filter(id=aid).first()

    if request.method == "GET":
        form = BushingEditModelForm(instance=bushing_object)
        return render(request, 'bushing/bushing_form.html', {"form": form})

    form = BushingEditModelForm(instance=bushing_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing/bushing_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/bushing/list/')


def bushing_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Bushing.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

