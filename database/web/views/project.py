from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms

from web import models
from utils.encrypt import md5
import django_filters

class ProjectFilter(django_filters.FilterSet):
    # projectName = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Project
        fields = {
            'projectName': ['icontains'],
            'equipment': ['icontains'],
            'customer': ['icontains'],
        }

def project_list(request):
    """ list of project """

    # # [obj,]
    # queryset = models.Project.objects.all().order_by("id")
    # # for row in queryset:
    # #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

    # return render(request, 'project_list.html', {"queryset": queryset})
    project_filter = ProjectFilter(request.GET, queryset=models.Project.objects.all())
    return render(request, 'project/project_list.html', {'filter': project_filter})

# def project_input(request):
#     """ list of project """

#     # [obj,]
#     queryset = models.Project.objects.all().order_by("id")
#     # for row in queryset:
#     #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

#     return render(request, 'project_input.html', {"queryset": queryset})

class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        # fields = ['username', 'password', 'age', 'gender', 'depart']
        fields = ['projectName', 'equipment', 'customer', 'projectNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def project_add(request):
    if request.method == "GET":
        form = ProjectModelForm()
        return render(request, 'project/project_form.html', {"form": form})

    form = ProjectModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'project/project_form.html', {"form": form})

    # 读取密码并更新成md5加密之后的密文
    # form.instance.password = md5(form.instance.password)

    # 保存到数据库
    form.save()
    return redirect('/project/list/')


class ProjectEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Project
        # fields = ['username', 'age', 'gender', 'depart']
        fields = ['projectName', 'equipment', 'customer', 'projectNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def project_edit(request, aid):
    project_object = models.Project.objects.filter(id=aid).first()

    if request.method == "GET":
        form = ProjectEditModelForm(instance=project_object)
        return render(request, 'project/project_form.html', {"form": form})

    form = ProjectEditModelForm(instance=project_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'project/project_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/project/list/')


def project_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Project.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

