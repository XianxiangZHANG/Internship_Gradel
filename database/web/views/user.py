from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = models.User
        fields = {
            'depart': ['exact'],
            'username': ['icontains'],
        }

def user_list(request):
    """ list of user """

    user_filter = UserFilter(request.GET, queryset=models.User.objects.all())
    return render(request, 'user/user_list.html', {'filter': user_filter})

class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


UserFormSet = modelformset_factory(
    models.User,
    form=UserModelForm,
    extra=1  
)


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user/user_form.html', {"form": form})

    form = UserModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'user/user_form.html', {"form": form})

    form.save()
    return redirect('/user/list/')

def user_add_multiple(request):
    UserFormSet = modelformset_factory(models.User, form=UserModelForm, extra=1)

    if request.method == 'POST':
        formset = UserFormSet(request.POST, queryset=models.User.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect('/user/list/')  
    else:
        formset = UserFormSet(queryset=models.User.objects.none())

    return render(request, 'user/user_add_multiple.html', {'formset': formset})

def user_modify_multiple(request):
    # Get filtered data
    user_filter = UserFilter(request.GET, queryset=models.User.objects.all())
    
    # Define form set
    UserFormSet = modelformset_factory(models.User, form=UserModelForm, extra=0)
    
    if request.method == 'POST':
        formset = UserFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/user/list/')
    else:
        formset = UserFormSet(queryset=user_filter.qs)

    return render(request, 'user/user_modify_multiple.html', {
        'filter': user_filter,
        'formset': formset,
    })

class UserEditModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'depart',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def user_edit(request, aid):
    user_object = models.User.objects.filter(id=aid).first()

    if request.method == "GET":
        form = UserEditModelForm(instance=user_object)
        return render(request, 'user/user_form.html', {"form": form})

    form = UserEditModelForm(instance=user_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'user/user_form.html', {"form": form})

    form.save()

    return redirect('/user/list/')


def user_delete(request):
    aid = request.GET.get("aid")
    models.User.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

