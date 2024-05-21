from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms

from web import models
from utils.encrypt import md5
import django_filters

class PartFilter(django_filters.FilterSet):

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

    part_filter = PartFilter(request.GET, queryset=models.Part.objects.all())
    return render(request, 'part/part_list.html', {'filter': part_filter})

def part_input(request):
    """ list of part """

    queryset = models.Part.objects.all().order_by("id")
    
    return render(request, 'part/part_input.html', {"queryset": queryset})

class PartModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName', 'resinName', 'resinDensity', 'fiberName', 'totalTowNumber', 'fiberDensity', 'fiberVolumeRatio', 'windingDensity', 'fiberSectionCalc',
                  'fiberSectionAcc', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'defaultCycleNumber', 'tensileYoungModulus', 'tensileUtimateStress', 'tensileYieldStress',
                  'compressionYoungModulus', 'flexuralModulus', 'numberLink', 'numberBushing', 'totalMassLink', 'totalMassAccumulation', 'totalMassWinding',
                  'totalMassBushing', 'additionalMass', 'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def part_add(request):
    if request.method == "GET":
        form = PartModelForm()
        return render(request, 'part/part_form.html', {"form": form})

    form = PartModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'part/part_form.html', {"form": form})


    form.save()
    return redirect('/part/list/')


class PartEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName', 'resinName', 'resinDensity', 'fiberName', 'totalTowNumber', 'fiberDensity', 'fiberVolumeRatio', 'windingDensity', 'fiberSectionCalc',
                  'fiberSectionAcc', 'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'defaultCycleNumber', 'tensileYoungModulus', 'tensileUtimateStress', 'tensileYieldStress',
                  'compressionYoungModulus', 'flexuralModulus', 'numberLink', 'numberBushing', 'totalMassLink', 'totalMassAccumulation', 'totalMassWinding',
                  'totalMassBushing', 'additionalMass', 'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def part_edit(request, aid):
    part_object = models.Part.objects.filter(id=aid).first()

    if request.method == "GET":
        form = PartEditModelForm(instance=part_object)
        return render(request, 'part/part_form.html', {"form": form})

    form = PartEditModelForm(instance=part_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'part/part_form.html', {"form": form})

    form.save()

    return redirect('/part/list/')


def part_delete(request):
    aid = request.GET.get("aid")
    models.Part.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

