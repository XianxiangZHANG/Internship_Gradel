from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

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

    # # [obj,]
    # queryset = models.Department.objects.all().order_by("id")
    # # for row in queryset:
    # #     print(row.departmentname, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

    # return render(request, 'department_list.html', {"queryset": queryset})
    department_filter = DepartmentFilter(request.GET, queryset=models.Department.objects.all())
    return render(request, 'department/department_list.html', {'filter': department_filter})

# def department_input(request):
#     """ list of department """

#     # [obj,]
#     queryset = models.Department.objects.all().order_by("id")
#     # for row in queryset:
#     #     print(row.departmentname, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)

#     return render(request, 'department_input.html', {"queryset": queryset})

class DepartmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        # fields = ['departmentname', 'password', 'age', 'gender', 'depart']
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


DepartmentFormSet = modelformset_factory(
    models.Department,
    form=DepartmentModelForm,
    extra=1  # 初始化时额外添加的表单数量
)


def department_add(request):
    if request.method == "GET":
        form = DepartmentModelForm()
        return render(request, 'department/department_form.html', {"form": form})

    form = DepartmentModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'department/department_form.html', {"form": form})

    # 读取密码并更新成md5加密之后的密文
    # form.instance.password = md5(form.instance.password)

    # 保存到数据库
    form.save()
    return redirect('/department/list/')


def department_add_multiple(request):
    formset = DepartmentFormSet(queryset=models.Department.objects.none())
    # interfaceError = None

    if request.method == 'POST':
        formset = DepartmentFormSet(request.POST)

        if formset.is_valid() : 
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('/department/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)

    return render(request, 'department/department_add_multiple.html', {
        'formset': formset,
    })



class DepartmentEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Department
        # fields = ['departmentname', 'age', 'gender', 'depart']
        fields = ['title',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 自定义操作，找到所有的字段
        # print(self.fields)
        for name, filed_object in self.fields.items():
            # print(name, filed_object)
            filed_object.widget.attrs = {"class": "form-control"}


def department_edit(request, aid):
    department_object = models.Department.objects.filter(id=aid).first()

    if request.method == "GET":
        form = DepartmentEditModelForm(instance=department_object)
        return render(request, 'department/department_form.html', {"form": form})

    form = DepartmentEditModelForm(instance=department_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'department/department_form.html', {"form": form})

    # 更新
    form.save()

    return redirect('/department/list/')


def department_delete(request):
    aid = request.GET.get("aid")
    # print("要删除的ID:", aid)
    models.Department.objects.filter(id=aid).delete()

    # return JsonResponse({"status": False, 'error': "ID不能为空"})
    return JsonResponse({"status": True})

