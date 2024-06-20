from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from web import models
import django_filters

class SequenceTypeFilter(django_filters.FilterSet):
    sequenceType = django_filters.CharFilter(field_name='sequenceType', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Resin
        fields = ['sequenceType', 'description', 'valid']


def sequenceType_list(request):
    """ list of sequenceType """

    sequenceType_filter = SequenceTypeFilter(request.GET, queryset=models.SequenceType.objects.all())
    return render(request, 'sequenceType/sequenceType_list.html', {'filter': sequenceType_filter})


class SequenceTypeFilterValid(django_filters.FilterSet):
    sequenceType = django_filters.CharFilter(field_name='sequenceType', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
   
    class Meta:
        model = models.Resin
        fields = ['sequenceType', 'description', ]

def sequenceType_valid(request):
    """ list of sequenceType """

    sequenceType_filter = SequenceTypeFilterValid(request.GET, queryset=models.SequenceType.objects.filter(valid=True))
    return render(request, 'sequenceType/sequenceType_valid.html', {'filter': sequenceType_filter})


class SequenceTypeModelForm(forms.ModelForm):
    class Meta:
        model = models.SequenceType
        fields = ['sequenceType', 'description', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


SequenceTypeFormSet = modelformset_factory(
    models.SequenceType,
    form=SequenceTypeModelForm,
    extra=1  
)


def sequenceType_add(request):
    if request.method == "GET":
        form = SequenceTypeModelForm()
        return render(request, 'sequenceType/sequenceType_form.html', {"form": form})

    form = SequenceTypeModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'sequenceType/sequenceType_form.html', {"form": form})

    # form.save()
    sequenceType = form.save(commit=False)
    sequenceType.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    sequenceType.save()
    return redirect('/sequenceType/list/')


def sequenceType_add_multiple(request):
    formset = SequenceTypeFormSet(queryset=models.SequenceType.objects.none())
    # interfaceError = None

    if request.method == 'POST':
        formset = SequenceTypeFormSet(request.POST)

        if formset.is_valid() : 
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/sequenceType/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)

    return render(request, 'sequenceType/sequenceType_add_multiple.html', {
        'formset': formset,
    })

def sequenceType_modify_multiple(request):
    # Get filtered data
    sequenceType_filter = SequenceTypeFilter(request.GET, queryset=models.SequenceType.objects.all())
    
    # Define form set
    SequenceTypeFormSet = modelformset_factory(models.SequenceType, form=SequenceTypeModelForm, extra=0)
    
    if request.method == 'POST':
        formset = SequenceTypeFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/sequenceType/list/')
    else:
        formset = SequenceTypeFormSet(queryset=sequenceType_filter.qs)

    return render(request, 'sequenceType/sequenceType_modify_multiple.html', {
        'filter': sequenceType_filter,
        'formset': formset,
    })

class SequenceTypeEditModelForm(forms.ModelForm):
    class Meta:
        model = models.SequenceType
        fields = ['sequenceType', 'description', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def sequenceType_edit(request, aid):
    sequenceType_object = models.SequenceType.objects.filter(id=aid).first()

    if request.method == "GET":
        form = SequenceTypeEditModelForm(instance=sequenceType_object)
        return render(request, 'sequenceType/sequenceType_form.html', {"form": form})

    form = SequenceTypeEditModelForm(instance=sequenceType_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'sequenceType/sequenceType_form.html', {"form": form})

    # form.save()
    sequenceType = form.save(commit=False)
    sequenceType.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    sequenceType.save()

    return redirect('/sequenceType/list/')


def sequenceType_delete(request):
    aid = request.GET.get("aid")
    # models.SequenceType.objects.filter(id=aid).delete()
    sequenceType = models.SequenceType.objects.filter(id=aid).first()
    if sequenceType:
        sequenceType.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        sequenceType.delete()

    return JsonResponse({"status": True})


def sequenceType_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        sequenceType = models.SequenceType.objects.get(id=aid)
        # sequenceType.delete()
        if sequenceType:
            sequenceType.user = models.User.objects.filter(id=request.info_dict['id']).first()  
            sequenceType.delete()

        return JsonResponse({"status": True})
    except models.SequenceType.DoesNotExist:
        return JsonResponse({"status": False, "error": "sequenceType not found"})