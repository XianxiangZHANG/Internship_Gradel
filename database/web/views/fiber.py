from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
import django_filters

class FiberFilter(django_filters.FilterSet):
    material = django_filters.CharFilter(field_name='material', lookup_expr='icontains')
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    distributor = django_filters.CharFilter(field_name='distributor', lookup_expr='icontains')
    grade = django_filters.CharFilter(field_name='grade', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Fiber
        fields = ['material', 'manufacturer', 'distributor', 'grade', 'valid']
    # class Meta:
    #     model = models.Fiber
    #     fields = {
    #         'material': ['icontains'], 
    #         'manufacturer': ['icontains'],
    #         'distributor': ['icontains'],
    #         'grade': ['icontains'],
    #     }

class FiberFilterValid(django_filters.FilterSet):
    material = django_filters.CharFilter(field_name='material', lookup_expr='icontains')
    manufacturer = django_filters.CharFilter(field_name='manufacturer', lookup_expr='icontains')
    distributor = django_filters.CharFilter(field_name='distributor', lookup_expr='icontains')
    grade = django_filters.CharFilter(field_name='grade', lookup_expr='icontains')

    class Meta:
        model = models.Fiber
        fields = ['material', 'manufacturer', 'distributor', 'grade', ]

def fiber_list(request):
    """ list of fiber """

    fiber_filter = FiberFilter(request.GET, queryset=models.Fiber.objects.all())
    return render(request, 'fiber/fiber_list.html', {'filter': fiber_filter})

def fiber_valid(request):
    """ list of fiber """

    fiber_filter = FiberFilterValid(request.GET, queryset=models.Fiber.objects.filter(valid=True))
    return render(request, 'fiber/fiber_valid.html', {'filter': fiber_filter})

def fiber_input(request):
    """ list of fiber """

    # [obj,]
    queryset = models.Fiber.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'fiber/fiber_input.html', {"queryset": queryset})


class FiberModelForm(forms.ModelForm):
    class Meta:
        model = models.Fiber
        fields = ['material', 'manufacturer', 'distributor', 'grade',
                'singleFilamentDiameter', 'tow', 'towInThousands', 
                'tex', 'density', 'theoreticalDrySection', 'tensileStrength', 'tensileModulus',
                'price21', 'price22', 'price23', 'price24', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

class FiberForm(forms.ModelForm):
    class Meta:
        model = models.Fiber
        fields = ['material', 'manufacturer', 'distributor', 'grade',
                'singleFilamentDiameter', 'tow', 'towInThousands', 
                'tex', 'density', 'theoreticalDrySection', 'tensileStrength', 'tensileModulus',
                'price21', 'price22', 'price23', 'price24', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


FiberFormSet = modelformset_factory(
    models.Fiber,
    form=FiberModelForm,
    extra=1  # The number of additional forms added during initialization
)

FiberMultFormSet = modelformset_factory(
    models.Fiber,
    form=FiberForm,
    extra=1  # The number of additional forms added during initialization
)

def fiber_add_multiple(request):
    formset = FiberFormSet(queryset=models.Fiber.objects.none())
   
    # fiberError = None

    if request.method == 'POST':
        formset = FiberFormSet(request.POST)
       
        # fiberName = request.POST.get('fiberName')
        # if not fiberName:
        #     fiberError = "Required"
        if formset.is_valid() :
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/fiber/list/')  # Replace with your redirect URL

    return render(request, 'fiber/fiber_add_multiple.html', {
        'formset': formset,
    })


def fiber_modify_multiple(request):
    # Get filtered data
    fiber_filter = FiberFilter(request.GET, queryset=models.Fiber.objects.all())
    
    # Define form set
    FiberFormSet = modelformset_factory(models.Fiber, form=FiberModelForm, extra=0)
    
    if request.method == 'POST':
        formset = FiberFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/fiber/list/')
    else:
        formset = FiberFormSet(queryset=fiber_filter.qs)

    return render(request, 'fiber/fiber_modify_multiple.html', {
        'filter': fiber_filter,
        'formset': formset,
    })


def fiber_add(request):
    if request.method == "GET":
        form = FiberModelForm()
        return render(request, 'fiber/fiber_form.html', {"form": form})

    form = FiberModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'fiber/fiber_form.html', {"form": form})

    # form.save()
    fiber = form.save(commit=False)
    fiber.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    fiber.save()
    return redirect('/fiber/list/')


class FiberEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Fiber
        fields = ['material', 'manufacturer', 'distributor', 'grade',
                'singleFilamentDiameter', 'tow', 'towInThousands', 
                'tex', 'density', 'theoreticalDrySection', 'tensileStrength', 'tensileModulus',
                'price21', 'price22', 'price23', 'price24', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def fiber_edit(request, aid):
    fiber_object = models.Fiber.objects.filter(id=aid).first()

    if request.method == "GET":
        form = FiberEditModelForm(instance=fiber_object)
        return render(request, 'fiber/fiber_form.html', {"form": form})

    form = FiberEditModelForm(instance=fiber_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'fiber/fiber_form.html', {"form": form})

    # form.save()
    fiber = form.save(commit=False)
    fiber.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    fiber.save()

    return redirect('/fiber/list/')


def fiber_delete(request):
    aid = request.GET.get("aid")
    # models.Fiber.objects.filter(id=aid).delete()
    fiber = models.Fiber.objects.filter(id=aid).first()
    if fiber:
        fiber.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        fiber.delete()

    return JsonResponse({"status": True})

def fiber_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        fiber = models.Fiber.objects.get(id=aid)
        # fiber.delete()
        if fiber:
            fiber.user = models.User.objects.filter(id=request.info_dict['id']).first()  
            fiber.delete()

        return JsonResponse({"status": True})
    except models.Fiber.DoesNotExist:
        return JsonResponse({"status": False, "error": "Fiber not found"})