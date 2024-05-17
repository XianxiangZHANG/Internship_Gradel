from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
from utils.encrypt import md5
import django_filters

class UserFilter(django_filters.FilterSet):
    # userName = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = models.User
        fields = {
            'depart': ['exact'],
            'username': ['icontains'],
        }

def user_list(request):
    """ list of user """

    # # [obj,]
    # queryset = models.User.objects.all().order_by("id")
    # # for row in queryset:
    # #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

    # return render(request, 'user_list.html', {"queryset": queryset})
    user_filter = UserFilter(request.GET, queryset=models.User.objects.all())
    return render(request, 'user/user_list.html', {'filter': user_filter})

# def user_input(request):
#     """ list of user """

#     # [obj,]
#     queryset = models.User.objects.all().order_by("id")
#     # for row in queryset:
#     #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

#     return render(request, 'user_input.html', {"queryset": queryset})

class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


UserFormSet = modelformset_factory(
    models.User,
    form=UserModelForm,
    extra=1  # 初始化时额外添加的表单数量
)


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user/user_form.html', {"form": form})

    form = UserModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'user/user_form.html', {"form": form})

    # 读取密码并更新成md5加密之后的密文
    # form.instance.password = md5(form.instance.password)

    # 保存到数据库
    form.save()
    return redirect('/user/list/')


def user_add_multiple(request):
    formset = UserFormSet(queryset=models.User.objects.none())
    # interfaceError = None

    if request.method == 'POST':
        formset = UserFormSet(request.POST)

        if formset.is_valid() : 
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('/user/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)

    return render(request, 'user/user_add_multiple.html', {
        'formset': formset,
    })



class UserEditModelForm(forms.ModelForm):
    class Meta:
        model = models.User
        # fields = ['username', 'age', 'gender', 'depart']
        fields = ['username', 'depart',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
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

    # 更新
    form.save()

    return redirect('/user/list/')


def user_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.User.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

