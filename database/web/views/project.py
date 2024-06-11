from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from openpyxl import load_workbook
from datetime import datetime

from web import models
from utils.encrypt import md5
import django_filters

class ProjectFilter(django_filters.FilterSet):
    projectName = django_filters.CharFilter(field_name='projectName', lookup_expr='icontains')
    program = django_filters.CharFilter(field_name='program', lookup_expr='icontains')
    equipment = django_filters.CharFilter(field_name='equipment', lookup_expr='icontains')
    customer = django_filters.CharFilter(field_name='customer', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Project
        fields = ['projectName', 'program', 'equipment', 'customer','valid']

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
    program = django_filters.CharFilter(field_name='program', lookup_expr='icontains')
    equipment = django_filters.CharFilter(field_name='equipment', lookup_expr='icontains')
    customer = django_filters.CharFilter(field_name='customer', lookup_expr='icontains')
    
    class Meta:
        model = models.Project
        fields = ['projectName', 'program', 'equipment', 'customer',]


def project_valid(request):
    """ list of project """

    project_filter = ProjectFilterValid(request.GET, queryset=models.Project.objects.filter(valid=True))
    return render(request, 'project/project_valid.html', {'filter': project_filter})


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['projectName', 'program', 'equipment', 'customer', 'projectNo', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def project_add(request):
    if request.method == "GET":
        form = ProjectModelForm()
        return render(request, 'project/project_add.html', {"form": form})

    form = ProjectModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'project/project_add.html', {"form": form})


    form.save()
    return redirect('/project/list/')
    


class ProjectEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = ['projectName', 'program', 'equipment', 'customer', 'projectNo', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate','valid']

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

class UploadFileForm(forms.Form):
    file = forms.FileField()


def handle_uploaded_file_project(f):
    # 加载Excel文件
    wb = load_workbook(filename=f, data_only=True)
    if 'CoverPage' not in wb.sheetnames:
        return {'error': 'CoverPage sheet not found'}
    
    sheet = wb['CoverPage']

    # 获取项目数据
    project_data = {}
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value == "Program : ":
                project_data['program'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Equipment : ":
                project_data['equipment'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Customer : ":
                project_data['customer'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Project No:":
                project_data['projectNo'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Relative design:":
                project_data['relativeDesign'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Structure drawing nb:":
                project_data['structureDrawingNb'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Document Nr. : ":
                project_data['documentNb'] = sheet.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Revision: ":
                project_data['revision'] = sheet.cell(row=cell.row, column=cell.column + 1).value
            elif cell.value == "Last update :":
                last_update = sheet.cell(row=cell.row, column=cell.column + 1).value
                if isinstance(last_update, datetime):
                    project_data['lastUpdate'] = last_update.strftime('%m/%d/%Y')
                else:
                    project_data['lastUpdate'] = last_update
    
    project_data['projectName'] = project_data['projectNo'] +' - '+ project_data['customer'] +' - '+ project_data['program']
    print(project_data['projectName'])
    return project_data

def upload_file_project(request):
    if request.method == 'POST' and 'file' in request.FILES:
        project_data = handle_uploaded_file_project(request.FILES['file'])
        if 'error' in project_data:
            return JsonResponse(project_data, status=400)
        return JsonResponse(project_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
