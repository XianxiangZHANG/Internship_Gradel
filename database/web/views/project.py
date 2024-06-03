from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms

from web import models
from utils.encrypt import md5
import django_filters

class ProjectFilter(django_filters.FilterSet):
    projectName = django_filters.CharFilter(field_name='projectName', lookup_expr='icontains')
    equipment = django_filters.CharFilter(field_name='equipment', lookup_expr='icontains')
    customer = django_filters.CharFilter(field_name='customer', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Project
        fields = ['projectName', 'equipment', 'customer','valid']

    # class Meta:
    #     model = models.Project
    #     fields = {
    #         'projectName': ['icontains'],
    #         'equipment': ['icontains'],
    #         'customer': ['icontains'],
    #     }

def project_list(request):
    """ list of project """

    project_filter = ProjectFilter(request.GET, queryset=models.Project.objects.all())
    return render(request, 'project/project_list.html', {'filter': project_filter})

class ProjectFilterValid(django_filters.FilterSet):
    projectName = django_filters.CharFilter(field_name='projectName', lookup_expr='icontains')
    equipment = django_filters.CharFilter(field_name='equipment', lookup_expr='icontains')
    customer = django_filters.CharFilter(field_name='customer', lookup_expr='icontains')
    
    class Meta:
        model = models.Project
        fields = ['projectName', 'equipment', 'customer',]


def project_valid(request):
    """ list of project """

    project_filter = ProjectFilterValid(request.GET, queryset=models.Project.objects.filter(valid=True))
    return render(request, 'project/project_valid.html', {'filter': project_filter})


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['projectName', 'equipment', 'customer', 'projectNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def project_add(request):
    if request.method == "GET":
        form = ProjectModelForm()
        return render(request, 'project/project_form.html', {"form": form})

    form = ProjectModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'project/project_form.html', {"form": form})

    form.save()
    return redirect('/project/list/')


class ProjectEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['projectName', 'equipment', 'customer', 'projectNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate','valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def project_edit(request, aid):
    project_object = models.Project.objects.filter(id=aid).first()

    if request.method == "GET":
        form = ProjectEditModelForm(instance=project_object)
        return render(request, 'project/project_form.html', {"form": form})

    form = ProjectEditModelForm(instance=project_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'project/project_form.html', {"form": form})

    form.save()

    return redirect('/project/list/')


def project_delete(request):
    aid = request.GET.get("aid")
    models.Project.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

