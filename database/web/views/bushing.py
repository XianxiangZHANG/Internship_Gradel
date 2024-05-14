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
    return render(request, 'bushing_list.html', {'filter': bushing_filter})

def bushing_input(request):
    """ list of bushing """

    # [obj,]
    queryset = models.Bushing.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'bushing_input.html', {"queryset": queryset})

# class BushingModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Bushing
#         fields = ['project', 'part', 'bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    # add one
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['part'].queryset = models.Part.objects.none()

    #     if 'project' in self.data:
    #         try:
    #             project_id = int(self.data.get('project'))
    #             self.fields['part'].queryset = models.Part.objects.filter(project_id=project_id).order_by('partName')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['part'].queryset = self.instance.project.part_set.order_by('partName')

    #     for name, field_object in self.fields.items():
    #         field_object.widget.attrs = {"class": "form-control"}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['part'].queryset = models.Part.objects.none()

    #     if 'project' in self.data:
    #         try:
    #             project_id = int(self.data.get('project'))
    #             self.fields['part'].queryset = models.Part.objects.filter(project_id=project_id).order_by('partName')
    #         except (ValueError, TypeError):
    #             pass
    #     elif self.instance.pk:
    #         self.fields['part'].queryset = self.instance.project.part_set.order_by('partName')
        
    #     for name, field_object in self.fields.items():
    #         field_object.widget.attrs = {"class": "form-control"}
   
class BushingModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


BushingFormSet = modelformset_factory(
    models.Bushing, 
    form=BushingModelForm, 
    extra=1  # 可以根据需要调整额外表单的数量
)

# def bushing_add_multiple(request):
#     BushingFormSet = modelformset_factory(models.Bushing, form=BushingModelForm, extra=1)
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
#         formset = BushingFormSet(queryset=models.Bushing.objects.none())
#     return render(request, 'bushing_add_multiple.html', {'formset': formset})
def bushing_add_multiple(request):
    BushingFormSet = modelformset_factory(models.Bushing, form=BushingModelForm, extra=1)
    if request.method == "POST":
        formset = BushingFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            project = request.POST.get('project')
            part = request.POST.get('part')
            for instance in instances:
                instance.project_id = project
                instance.part_id = part
                instance.save()
            return redirect('/bushing/list/')
    else:
        formset = BushingFormSet(queryset=models.Bushing.objects.none())
    projects = models.Project.objects.all()
    return render(request, 'bushing_add_multiple.html', {'formset': formset, 'projects': projects})


def bushing_add(request):
    if request.method == "GET":
        form = BushingModelForm()
        return render(request, 'bushing_form.html', {"form": form})

    form = BushingModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing_form.html', {"form": form})


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
        return render(request, 'bushing_form.html', {"form": form})

    form = BushingEditModelForm(instance=bushing_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/bushing/list/')


def bushing_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Bushing.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

