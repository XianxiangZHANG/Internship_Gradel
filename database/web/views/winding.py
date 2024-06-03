from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class WindingFilter(django_filters.FilterSet):
    class Meta:
        model = models.Winding
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
        }

def winding_list(request):
    """ list of winding """

    winding_filter = WindingFilter(request.GET, queryset=models.Winding.objects.all())
    return render(request, 'winding/winding_list.html', {'filter': winding_filter})

def winding_valid(request):
    """ list of winding """

    winding_filter = WindingFilter(request.GET, queryset=models.Winding.objects.filter(part__valid=True))
    return render(request, 'winding/winding_valid.html', {'filter': winding_filter})

def winding_input(request):
    """ list of winding """

    # [obj,]
    queryset = models.Winding.objects.all().order_by("id")
  
    return render(request, 'winding/winding_input.html', {"queryset": queryset})

   
class WindingModelForm(forms.ModelForm):
    class Meta:
        model = models.Winding
        fields = ['link', 'interface1','interface2','interface3', 'sequence',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)
    # link = forms.ModelChoiceField(queryset=models.Link.objects.all(), required=True)
    

WindingFormSet = modelformset_factory(
    models.Winding,
    form=WindingModelForm,
    extra=1 
)

def winding_add_multiple(request):
    projects = models.Project.objects.all()
    formset = WindingFormSet(queryset=models.Winding.objects.none())
    project_part_form = ProjectPartForm()


    if request.method == 'POST':
        formset = WindingFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)

        if formset.is_valid() and project_part_form.is_valid(): 
            print("valid")
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            # link = project_part_form.cleaned_data['link']
            for instance in instances:
                instance.project = project
                instance.part = part
                # instance.link = link
                instance.save()
            return redirect('/winding/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(project_part_form.errors)

    return render(request, 'winding/winding_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
    })

def winding_modify_multiple(request):
    # Get filtered data
    winding_filter = WindingFilter(request.GET, queryset=models.Winding.objects.all())
    
    # Define form set
    WindingFormSet = modelformset_factory(models.Winding, form=WindingModelForm, extra=0)
    
    if request.method == 'POST':
        formset = WindingFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/winding/list/')
    else:
        formset = WindingFormSet(queryset=winding_filter.qs)

    return render(request, 'winding/winding_modify_multiple.html', {
        'filter': winding_filter,
        'formset': formset,
    })

def winding_add(request):
    if request.method == "GET":
        form = WindingModelForm()
        return render(request, 'winding_form.html', {"form": form})

    form = WindingModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'winding_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/winding/list/')


class WindingEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Winding
        fields = ['project', 'part', 'link', 'interface1','interface2','interface3',  'sequence',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def winding_edit(request, aid):
    winding_object = models.Winding.objects.filter(id=aid).first()

    if request.method == "GET":
        form = WindingEditModelForm(instance=winding_object)
        return render(request, 'winding/winding_form.html', {"form": form})

    form = WindingEditModelForm(instance=winding_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'winding/winding_form.html', {"form": form})

    form.save()

    return redirect('/winding/list/')


def winding_delete(request):
    aid = request.GET.get("aid")
    models.Winding.objects.filter(id=aid).delete()
    
    return JsonResponse({"status": True})

