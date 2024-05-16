from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class InterfaceFilter(django_filters.FilterSet):
    class Meta:
        model = models.Interface
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
            'interfaceName': ['icontains'],
        }

def interface_list(request):
    """ list of interface """

    interface_filter = InterfaceFilter(request.GET, queryset=models.Interface.objects.all())
    return render(request, 'interface/interface_list.html', {'filter': interface_filter})

def interface_input(request):
    """ list of interface """

    # [obj,]
    queryset = models.Interface.objects.all().order_by("id")
  
    return render(request, 'interface/interface_input.html', {"queryset": queryset})

   
class InterfaceModelForm(forms.ModelForm):
    class Meta:
        model = models.Interface
        fields = ['interfaceName', 'height', 'intDiameter', 'totalLink', 'totalArm', 'totalSection',
                'extDiameter', 'theoHeight', 'accMass', 'finODiam', 'finAccSection', 'safetyFactor',
                'interfaceCenterX', 'interfaceCenterY', 'interfaceCenterZ',
                'directionVectorX', 'directionVectorY', 'directionVectorZ',
                'divisionStep',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)
    

InterfaceFormSet = modelformset_factory(
    models.Interface,
    form=InterfaceModelForm,
    extra=1  # 初始化时额外添加的表单数量
)

def interface_add_multiple(request):
    projects = models.Project.objects.all()
    formset = InterfaceFormSet(queryset=models.Interface.objects.none())
    project_part_form = ProjectPartForm()
    # interfaceError = None

    if request.method == 'POST':
        formset = InterfaceFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)
        # interfaceName = request.POST.get('bushingName')
        # print("aaaaaaaa",interfaceName)
        # if not interfaceName:
        #     interfaceError = "Required"

        if formset.is_valid() and project_part_form.is_valid(): 
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/interface/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(project_part_form.errors)

    return render(request, 'interface/interface_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        # 'interfaceError': interfaceError,
    })



def interface_add(request):
    if request.method == "GET":
        form = InterfaceModelForm()
        return render(request, 'interface/interface_form.html', {"form": form})

    form = InterfaceModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'interface/interface_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/interface/list/')


class InterfaceEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Interface
        fields = ['project', 'part', 'interfaceName', 'height', 'intDiameter', 'totalLink', 'totalArm', 'totalSection',
                'extDiameter', 'theoHeight', 'accMass', 'finODiam', 'finAccSection', 'safetyFactor',
                'interfaceCenterX', 'interfaceCenterY', 'interfaceCenterZ',
                'directionVectorX', 'directionVectorY', 'directionVectorZ',
                'divisionStep',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def interface_edit(request, aid):
    interface_object = models.Interface.objects.filter(id=aid).first()

    if request.method == "GET":
        form = InterfaceEditModelForm(instance=interface_object)
        return render(request, 'interface/interface_form.html', {"form": form})

    form = InterfaceEditModelForm(instance=interface_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'interface/interface_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/interface/list/')


def interface_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Interface.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

