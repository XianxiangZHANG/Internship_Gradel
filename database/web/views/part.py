from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms

from web import models
from utils.encrypt import md5
import django_filters

class PartFilter(django_filters.FilterSet):
    # projectName = django_filters.CharFilter(field_name='project__projectName', lookup_expr='icontains')
    # projectName = django_filters.CharFilter(field_name='project__projectName', lookup_expr='exact')

    class Meta:
        model = models.Part
        fields = {
            'project': ['exact'], 
            'partName': ['icontains'],
            'resinName': ['icontains'],
            'fiberName': ['icontains'],
        }
def part_list(request):
    """ list of part """

    # # [obj,]
    # queryset = models.Part.objects.all().order_by("id")
    # # for row in queryset:
    # #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    # # for row in queryset:
    # #     print(row.project.projectName)

    # return render(request, 'part_list.html', {"queryset": queryset})
    part_filter = PartFilter(request.GET, queryset=models.Part.objects.all())
    return render(request, 'part_list.html', {'filter': part_filter})

def part_input(request):
    """ list of part """

    # [obj,]
    queryset = models.Part.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'part_input.html', {"queryset": queryset})

class PartModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        # fields = ['username', 'password', 'age', 'gender', 'depart']
        # fields = ['partName', 'equipment', 'customer', 'partNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']
        fields = ['project', 'partName', 'resinName', 'resinDensity', 'fiberName', 'totalTowNumber', 'fiberDensity', 'fiberVolumeRatio', 'windingDensity', 'fiberSectionCalc',
                  'fiberSectionAcc', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'defaultCycleNumber', 'tensileYoungModulus', 'tensileUtimateStress', 'tensileYieldStress',
                  'compressionYoungModulus', 'flexuralModulus', 'numberLink', 'numberBushing', 'totalMassLink', 'totalMassAccumulation', 'totalMassWinding',
                  'totalMassBushing', 'additionalMass', 'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def part_add(request):
    if request.method == "GET":
        form = PartModelForm()
        return render(request, 'part_form.html', {"form": form})

    form = PartModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'part_form.html', {"form": form})


    # 保存到数据库
    form.save()
    return redirect('/part/list/')


class PartEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        # fields = ['username', 'age', 'gender', 'depart']
        # fields = ['partName', 'equipment', 'customer', 'partNo', 'partsNumber', 'relativeDesign', 'structureDrawingNb', 'documentNb', 'revision', 'lastUpdate']
        fields = ['project', 'partName', 'resinName', 'resinDensity', 'fiberName', 'totalTowNumber', 'fiberDensity', 'fiberVolumeRatio', 'windingDensity', 'fiberSectionCalc',
                  'fiberSectionAcc', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'defaultCycleNumber', 'tensileYoungModulus', 'tensileUtimateStress', 'tensileYieldStress',
                  'compressionYoungModulus', 'flexuralModulus', 'numberLink', 'numberBushing', 'totalMassLink', 'totalMassAccumulation', 'totalMassWinding',
                  'totalMassBushing', 'additionalMass', 'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def part_edit(request, aid):
    part_object = models.Part.objects.filter(id=aid).first()

    if request.method == "GET":
        form = PartEditModelForm(instance=part_object)
        return render(request, 'part_form.html', {"form": form})

    form = PartEditModelForm(instance=part_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'part_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/part/list/')


def part_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Part.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})


# def search_projects(request):
#     if request.is_ajax():
#         query = request.GET.get('term', '')  # "term" 是 jQuery UI Autocomplete 发送的默认参数
#         projects = models.Project.objects.filter(name__icontains=query)[:10]  # 返回最多10个结果
#         results = [{'id': project.id, 'label': project.name, 'value': project.name} for project in projects]
#         return JsonResponse(results, safe=False)
#     return JsonResponse([], safe=False)
