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

    bushing_filter = BushingFilter(request.GET, queryset=models.Bushing.objects.all())
    return render(request, 'bushing/bushing_list.html', {'filter': bushing_filter})

def bushing_input(request):
    """ list of bushing """

    # [obj,]
    queryset = models.Bushing.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'bushing/bushing_input.html', {"queryset": queryset})

   
class BushingModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}

class BushingForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['project', 'part', 'bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)

BushingFormSet = modelformset_factory(
    models.Bushing,
    form=BushingModelForm,
    extra=1  # The number of additional forms added during initialization
)

BushingMultFormSet = modelformset_factory(
    models.Bushing,
    form=BushingForm,
    extra=1  # The number of additional forms added during initialization
)

def bushing_add_multiple(request):
    projects = models.Project.objects.all()
    formset = BushingFormSet(queryset=models.Bushing.objects.none())
    project_part_form = ProjectPartForm()
    # bushingError = None

    if request.method == 'POST':
        formset = BushingFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)
        # bushingName = request.POST.get('bushingName')
        # if not bushingName:
        #     bushingError = "Required"
        if formset.is_valid() and project_part_form.is_valid():
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/bushing/list/')  # Replace with your redirect URL

    return render(request, 'bushing/bushing_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        # 'bushingError': bushingError,
    })


def bushing_modify_multiple(request):
    # Get filtered data
    bushing_filter = BushingFilter(request.GET, queryset=models.Bushing.objects.all())
    
    # Define form set
    BushingFormSet = modelformset_factory(models.Bushing, form=BushingModelForm, extra=0)
    
    if request.method == 'POST':
        formset = BushingFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/bushing/list/')
    else:
        formset = BushingFormSet(queryset=bushing_filter.qs)

    return render(request, 'bushing/bushing_modify_multiple.html', {
        'filter': bushing_filter,
        'formset': formset,
    })



def bushing_add(request):
    if request.method == "GET":
        form = BushingModelForm()
        return render(request, 'bushing/bushing_form.html', {"form": form})

    form = BushingModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing/bushing_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/bushing/list/')


class BushingEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Bushing
        fields = ['project', 'part', 'bushingName', 'numberInterface', 'bushingDrawNb', 'AccOnBushing', 'bushingMass', 'totalBushingMass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def bushing_edit(request, aid):
    bushing_object = models.Bushing.objects.filter(id=aid).first()

    if request.method == "GET":
        form = BushingEditModelForm(instance=bushing_object)
        return render(request, 'bushing/bushing_form.html', {"form": form})

    form = BushingEditModelForm(instance=bushing_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'bushing/bushing_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/bushing/list/')


def bushing_delete(request):
    aid = request.GET.get("aid")
    models.Bushing.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

def bushing_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        bushing = models.Bushing.objects.get(id=aid)
        bushing.delete()
        return JsonResponse({"status": True})
    except models.Bushing.DoesNotExist:
        return JsonResponse({"status": False, "error": "Bushing not found"})