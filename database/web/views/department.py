from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory
from django.db.models import Count

from web import models
from utils.encrypt import md5
import django_filters

class DepartmentFilter(django_filters.FilterSet):
    # departmentName = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.Department
        fields = {
            'title': ['icontains'],
        }

def department_list(request):
    """ list of department """

    departments = models.Department.objects.annotate(employee_count=Count('user'))
    return render(request, 'department/department_list.html', {'departments': departments})

def department_list_read(request):
    """ list of department """

    departments = models.Department.objects.annotate(employee_count=Count('user'))
    return render(request, 'department/department_list_read.html', {'departments': departments})

# def department_list(request):
#     """ list of department """

#     department_filter = DepartmentFilter(request.GET, queryset=models.Department.objects.all())
#     return render(request, 'department/department_list.html', {'filter': department_filter})

class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


DepartmentFormSet = modelformset_factory(
    models.Department,
    form=DepartmentModelForm,
    extra=1  
)


def department_add(request):
    if request.method == "GET":
        form = DepartmentModelForm()
        return render(request, 'department/department_form.html', {"form": form})

    form = DepartmentModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'department/department_form.html', {"form": form})

    # form.save()
    department = form.save(commit=False)
    department.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    department.save()
    return redirect('/department/list/')


def department_add_multiple(request):
    formset = DepartmentFormSet(queryset=models.Department.objects.none())
    # interfaceError = None

    if request.method == 'POST':
        formset = DepartmentFormSet(request.POST)

        if formset.is_valid() : 
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/department/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)

    return render(request, 'department/department_add_multiple.html', {
        'formset': formset,
    })

def department_modify_multiple(request):
    # Get filtered data
    department_filter = DepartmentFilter(request.GET, queryset=models.Department.objects.all())
    
    # Define form set
    DepartmentFormSet = modelformset_factory(models.Department, form=DepartmentModelForm, extra=0)
    
    if request.method == 'POST':
        formset = DepartmentFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/department/list/')
    else:
        formset = DepartmentFormSet(queryset=department_filter.qs)

    return render(request, 'department/department_modify_multiple.html', {
        'filter': department_filter,
        'formset': formset,
    })


class DepartmentEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def department_edit(request, aid):
    department_object = models.Department.objects.filter(id=aid).first()

    if request.method == "GET":
        form = DepartmentEditModelForm(instance=department_object)
        return render(request, 'department/department_form.html', {"form": form})

    form = DepartmentEditModelForm(instance=department_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'department/department_form.html', {"form": form})

    # form.save()
    department = form.save(commit=False)
    department.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    department.save()

    return redirect('/department/list/')


def department_delete(request):
    aid = request.GET.get("aid")
    # models.Department.objects.filter(id=aid).delete()
    department = models.Department.objects.filter(id=aid).first()
    if department:
        department.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        department.delete()

    return JsonResponse({"status": True})


def department_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        department = models.Department.objects.get(id=aid)
        # department.delete()
        if department:
            department.user = models.User.objects.filter(id=request.info_dict['id']).first()  
            department.delete()

        return JsonResponse({"status": True})
    except models.Department.DoesNotExist:
        return JsonResponse({"status": False, "error": "Department not found"})
