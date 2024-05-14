from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms

from web import models
from utils.encrypt import md5
import django_filters

class BushingFilter(django_filters.FilterSet):
    class Meta:
        model = models.Bushing
        fields = []

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

class BushingModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        # fields = ['username', 'password', 'age', 'gender', 'depart']
        # fields = ['partName', 'equipment', 'customer', 'partNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']
        fields = ['part', 'bushingName', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def bushing_add(request):
    if request.method == "GET":
        form = BushingModelForm()
        return render(request, 'bushing_form.html', {"form": form})

    form = BushingModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing_form.html', {"form": form})


    # 保存到数据库
    form.save()
    return redirect('/bushing/list/')


class BushingEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        # fields = ['username', 'age', 'gender', 'depart']
        # fields = ['partName', 'equipment', 'customer', 'partNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']
        fields = ['part', 'bushingName', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
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

