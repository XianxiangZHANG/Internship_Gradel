from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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


def resin_list(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_list.html', {'filter': resin_filter, 'resins': resins, 'message':message})


def resin_list_mechanical_properties(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_list_mechanical_properties.html', {'filter': resin_filter, 'resins': resins, 'message':message})
   

def resin_list_thermophysical_toughness_properties(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_list_thermophysical_toughness_properties.html', {'filter': resin_filter, 'resins': resins, 'message':message})
  


class ResinFilterValid(django_filters.FilterSet):
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    resin = django_filters.CharFilter(field_name='resin', lookup_expr='icontains')
    hardener = django_filters.CharFilter(field_name='hardener', lookup_expr='icontains')
    accelerator = django_filters.CharFilter(field_name='accelerator', lookup_expr='icontains')

    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator', ]


def resin_valid(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilterValid(request.GET, queryset=models.Resin.objects.filter(valid=True))

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_valid.html', {'filter': resin_filter, 'resins': resins, 'message':message})

def resin_valid_mechanical_properties(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilterValid(request.GET, queryset=models.Resin.objects.filter(valid=True))

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_valid_mechanical_properties.html', {'filter': resin_filter, 'resins': resins, 'message':message})

def resin_valid_thermophysical_toughness_properties(request):
    """ list of resin """
    resins = None
    resin_filter = ResinFilterValid(request.GET, queryset=models.Resin.objects.filter(valid=True))

    message = "No resin to display. Please use the filter to load data."

    if any(request.GET.values()):
        resins = resin_filter.qs
        message = "No data found."
    elif 'filter' in request.GET:
        resins = resin_filter.qs
        message = "No data found."
    
    return render(request, 'resin/resin_valid_thermophysical_toughness_properties.html', {'filter': resin_filter, 'resins': resins, 'message':message})


def resin_input(request):
    """ list of resin """

    # [obj,]
    queryset = models.Resin.objects.all().order_by("id")
   
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
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list/')  # Replace with your redirect URL

    return render(request, 'resin/resin_add_multiple.html', {
        'formset': formset,
    })

class ResinModelFormInit(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'ratioWR', 'ratioWH', 'ratioWA', 'ratioVR', 'ratioVH', 'ratioVA',
                'potLife', 'processT', 'curingCycle', 'tg',
                'priceResin', 'priceHardener',
                'densityR', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}

class ResinModelFormM(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'flexuralStrength', 'flexuralmodulus', 'modulusElasticity', 'tensileStrength',
                'elongationBreak', 'compressionUltStrength', 'compressionModulus',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}

class ResinModelFormTT(forms.ModelForm):
    class Meta:
        model = models.Resin
        fields = ['manufacturer', 'resin', 'hardener', 'accelerator',
                'thermalExpansionCoefficient', 'charpyimpact', 'fractureToughness', 
                'fractureEnergy', 'totalShrinkage', 'hardness', 'waterAbsorption',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}

def resin_add_mechanical_properties(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelFormM, extra=0)
    
    if request.method == 'POST':
        # print("post")
        formset = ResinFormSet(request.POST)
        # print(formset)
        if formset.is_valid():
            # print("valid")
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list-mechanical-properties/')
    else:
        formset = ResinFormSet(queryset=resin_filter.qs)

    return render(request, 'resin/resin_add_mechanical_properties.html', {
        'filter': resin_filter,
        'formset': formset,
    })
  

def resin_add_thermophysical_toughness_properties(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelFormTT, extra=0)
    
    if request.method == 'POST':
        formset = ResinFormSet(request.POST)
        # print(formset)
        if formset.is_valid():
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list-thermophysical-toughness-properties/')
    else:
        formset = ResinFormSet(queryset=resin_filter.qs)

    return render(request, 'resin/resin_add_thermophysical_toughness_properties.html', {
        'filter': resin_filter,
        'formset': formset,
    })


def resin_modify_multiple(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelFormInit, extra=0)
    
    formset = None
    message = "No resin to display. Please use the filter to load data."

    if request.method == 'POST':
        formset = ResinFormSet(request.POST)
        if formset.is_valid():
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list/')
    else:
        if any(request.GET.values()):
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."
        elif 'filter' in request.GET:
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."

    return render(request, 'resin/resin_modify_multiple.html', {
        'filter': resin_filter,
        'formset': formset,
        'message': message,
    })

def resin_modify_mechanical_properties(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelFormM, extra=0)

    formset = None
    message = "No resin to display. Please use the filter to load data."
    
    if request.method == 'POST':
        # print("post")
        formset = ResinFormSet(request.POST)
        # print(formset)
        if formset.is_valid():
            # print("valid")
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list-mechanical-properties/')
    else:
        if any(request.GET.values()):
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."
        elif 'filter' in request.GET:
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."

    return render(request, 'resin/resin_modify_mechanical_properties.html', {
        'filter': resin_filter,
        'formset': formset,
        'message': message,
    })
  

def resin_modify_thermophysical_toughness_properties(request):
    # Get filtered data
    resin_filter = ResinFilter(request.GET, queryset=models.Resin.objects.all())
    
    # Define form set
    ResinFormSet = modelformset_factory(models.Resin, form=ResinModelFormTT, extra=0)

    formset = None
    message = "No resin to display. Please use the filter to load data."
    
    if request.method == 'POST':
        formset = ResinFormSet(request.POST)
        # print(formset)
        if formset.is_valid():
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/resin/list-thermophysical-toughness-properties/')
    else:
        if any(request.GET.values()):
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."
        elif 'filter' in request.GET:
            formset = ResinFormSet(queryset=resin_filter.qs)
            if not resin_filter.qs.exists():
                message = "This table is empty. You need to add the basic information of Resin first."

    return render(request, 'resin/resin_modify_thermophysical_toughness_properties.html', {
        'filter': resin_filter,
        'formset': formset,
        'message': message,
    })

def resin_add(request):
    if request.method == "GET":
        form = ResinModelForm()
        return render(request, 'resin/resin_form.html', {"form": form})

    form = ResinModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'resin/resin_form.html', {"form": form})

    # form.save()
    resin = form.save(commit=False)
    resin.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    resin.save()
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

    # form.save()
    resin = form.save(commit=False)
    resin.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    resin.save()

    return redirect('/resin/list/')


def resin_delete(request):
    aid = request.GET.get("aid")
    # models.Resin.objects.filter(id=aid).delete()
    resin = models.Resin.objects.filter(id=aid).first()
    if resin:
        resin.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        resin.delete()

    return JsonResponse({"status": True})

def resin_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        resin = models.Resin.objects.get(id=aid)
        # resin.delete()
        if resin:
            resin.user = models.User.objects.filter(id=request.info_dict['id']).first()  
            resin.delete()
        return JsonResponse({"status": True})
    except models.Resin.DoesNotExist:
        return JsonResponse({"status": False, "error": "Resin not found"})