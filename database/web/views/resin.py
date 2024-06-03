from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
import django_filters

class ResinFilter(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    resin = django_filters.CharFilter(field_name='resin', lookup_expr='icontains')
    hardener = django_filters.CharFilter(field_name='hardener', lookup_expr='icontains')
    accelerator = django_filters.CharFilter(field_name='accelerator', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator', 'valid']

    # class Meta:
    #     model = models.Resin
    #     valid = django_filters.BooleanFilter(field_name='valid')  
    #     fields = {
    #         'manufacturer': ['icontains'], 
    #         'resin': ['icontains'],
    #         'hardener': ['icontains'],
    #         'accelerator': ['icontains'],
    #         'valid':['']
    #     }

def resin_list(request):
    """ list of resin """

    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    return render(request, 'resin/resin_list.html', {'filter': resin_filter})



def resin_input(request):
    """ list of resin """

    # [obj,]
    queryset = models.Resin.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'resin/resin_input.html', {"queryset": queryset})


class ResinModelForm(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'ratioWR', 'ratioWH', 'ratioWA', 'ratioVR', 'ratioVH', 'ratioVA',
                'potLife', 'processT', 'curingCycle', 'tg',
                'priceResin', 'priceHardener',
                'densityR', 'flexuralStrength', 'flexuralmodulus', 'modulusElasticity', 'tensileStrength',
                'elongationBreak', 'compressionUltStrength', 'compressionModulus','thermalExpansionCoefficient',
                'charpyimpact', 'fractureToughness', 'fractureEnergy', 'totalShrinkage', 'hardness', 'waterAbsorption', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

class ResinForm(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'ratioWR', 'ratioWH', 'ratioWA', 'ratioVR', 'ratioVH', 'ratioVA',
                'potLife', 'processT', 'curingCycle', 'tg',
                'priceResin', 'priceHardener',
                'densityR', 'flexuralStrength', 'flexuralmodulus', 'modulusElasticity', 'tensileStrength',
                'elongationBreak', 'compressionUltStrength', 'compressionModulus','thermalExpansionCoefficient',
                'charpyimpact', 'fractureToughness', 'fractureEnergy', 'totalShrinkage', 'hardness', 'waterAbsorption', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


ResinFormSet = modelformset_factory(
    models.Resin,
    form=ResinModelForm,
    extra=1  # The number of additional forms added during initialization
)

ResinMultFormSet = modelformset_factory(
    models.Resin,
    form=ResinForm,
    extra=1  # The number of additional forms added during initialization
)

def resin_add_multiple(request):
    formset = ResinFormSet(queryset=models.Resin.objects.none())
   
    # resinError = None

    if request.method == 'POST':
        formset = ResinFormSet(request.POST)
       
        # resinName = request.POST.get('resinName')
        # if not resinName:
        #     resinError = "Required"
        if formset.is_valid() :
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('/resin/list/')  # Replace with your redirect URL

    return render(request, 'resin/resin_add_multiple.html', {
        'formset': formset,
    })


def resin_modify_multiple(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelForm, extra=0)
    
    if request.method == 'POST':
        formset = ResinFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/resin/list/')
    else:
        formset = ResinFormSet(queryset=resin_filter.qs)

    return render(request, 'resin/resin_modify_multiple.html', {
        'filter': resin_filter,
        'formset': formset,
    })


def resin_add(request):
    if request.method == "GET":
        form = ResinModelForm()
        return render(request, 'resin/resin_form.html', {"form": form})

    form = ResinModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'resin/resin_form.html', {"form": form})

    form.save()
    return redirect('/resin/list/')


class ResinEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'ratioWR', 'ratioWH', 'ratioWA', 'ratioVR', 'ratioVH', 'ratioVA',
                'potLife', 'processT', 'curingCycle', 'tg',
                'priceResin', 'priceHardener',
                'densityR', 'flexuralStrength', 'flexuralmodulus', 'modulusElasticity', 'tensileStrength',
                'elongationBreak', 'compressionUltStrength', 'compressionModulus','thermalExpansionCoefficient',
                'charpyimpact', 'fractureToughness', 'fractureEnergy', 'totalShrinkage', 'hardness', 'waterAbsorption','valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def resin_edit(request, aid):
    resin_object = models.Resin.objects.filter(id=aid).first()

    if request.method == "GET":
        form = ResinEditModelForm(instance=resin_object)
        return render(request, 'resin/resin_form.html', {"form": form})

    form = ResinEditModelForm(instance=resin_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'resin/resin_form.html', {"form": form})

    form.save()

    return redirect('/resin/list/')


def resin_delete(request):
    aid = request.GET.get("aid")
    models.Resin.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

def resin_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        resin = models.Resin.objects.get(id=aid)
        resin.delete()
        return JsonResponse({"status": True})
    except models.Resin.DoesNotExist:
        return JsonResponse({"status": False, "error": "Resin not found"})