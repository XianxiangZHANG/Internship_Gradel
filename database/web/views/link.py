from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = models.Link
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
            'linkName': ['icontains'],
        }

def link_list(request):
    """ list of link """

    link_filter = LinkFilter(request.GET, queryset=models.Link.objects.all())
    return render(request, 'link_list.html', {'filter': link_filter})

def link_input(request):
    """ list of link """

    # [obj,]
    queryset = models.Link.objects.all().order_by("id")
  
    return render(request, 'link_input.html', {"queryset": queryset})

   
class LinkModelForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ['linkName', 'interface', 'length', 'linkType', 'armDiam', 'armSection', 
                  'cycle', 'sequence', 'finArmSection', 'finArmDiam', 'finArmRadius',
                'mass', 'angle',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)
    

LinkFormSet = modelformset_factory(
    models.Link,
    form=LinkModelForm,
    extra=1  # 初始化时额外添加的表单数量
)

def link_add_multiple(request):
    projects = models.Project.objects.all()
    formset = LinkFormSet(queryset=models.Link.objects.none())
    project_part_form = ProjectPartForm()
    # linkError = None

    if request.method == 'POST':
        formset = LinkFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)
        # linkName = request.POST.get('bushingName')
        # print("aaaaaaaa",linkName)
        # if not linkName:
        #     linkError = "Required"

        if formset.is_valid() and project_part_form.is_valid(): 
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/link/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(project_part_form.errors)

    return render(request, 'link_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        # 'linkError': linkError,
    })



def link_add(request):
    if request.method == "GET":
        form = LinkModelForm()
        return render(request, 'link_form.html', {"form": form})

    form = LinkModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'link_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/link/list/')


class LinkEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ['linkName', 'interface', 'length', 'linkType', 'armDiam', 'armSection', 
                  'cycle', 'sequence', 'finArmSection', 'finArmDiam', 'finArmRadius',
                'mass', 'angle',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def link_edit(request, aid):
    link_object = models.Link.objects.filter(id=aid).first()

    if request.method == "GET":
        form = LinkEditModelForm(instance=link_object)
        return render(request, 'link_form.html', {"form": form})

    form = LinkEditModelForm(instance=link_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'link_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/link/list/')


def link_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Link.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

