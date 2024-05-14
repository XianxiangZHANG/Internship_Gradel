# forms.py
from django import forms
from django.forms import modelformset_factory
from web import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'password', 'depart']

UserFormSet = modelformset_factory(models.User, form=UserForm, extra=1)  # extra=1 表示默认显示一个空表单
