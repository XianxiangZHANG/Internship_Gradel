import hashlib
from io import BytesIO

from django import forms
from django.core.validators import RegexValidator
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError


from web import models
from utils.encrypt import md5
from utils.helper import check_code


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Please enter your username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': "Please enter your passwaord"}, render_value=True),
    )

    code = forms.CharField(
        label="Code",
        widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Please enter the code"}),
    )

class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'class': 'input__field', 'placeholder': "Please enter your old passwaord"}, render_value=True)
    )
    
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'class': 'input__field', 'placeholder': "Please enter your new passwaord"}, render_value=True)
    )
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'class': 'input__field', 'placeholder': "Please enter your new passwaord again"}, render_value=True)
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = md5(self.cleaned_data.get('old_password'))
        print(old_password)
        if old_password != self.user.password:
            # print(self.user.password)
            raise ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "New passwords must match.")



def login(request):
    """ User Login """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'account/login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'account/login.html', {"form": form})

    # Determine whether the verification code is correct
    image_code = request.session.get("image_code")
    if not image_code:
        form.add_error("code", "The code has expired")
        return render(request, 'account/login.html', {"form": form})
    if image_code.upper() != form.cleaned_data['code'].upper():
        form.add_error("code", "The code error")
        return render(request, 'account/login.html', {"form": form})

    # The verification code is correct, go to the database to verify the username and password
    user = form.cleaned_data['username']
    pwd = form.cleaned_data['password']
    encrypt_pasword = md5(pwd)
    # print(user, encrypt_pasword)
    User_object = models.User.objects.filter(username=user, password=encrypt_pasword).first()
    if not User_object:
        return render(request, 'account/login.html', {"form": form, 'error': "Wrong username or password"})

    request.session['info'] = {"id": User_object.id, 'name': User_object.username}
    request.session.set_expiry(60 * 60 * 24 * 7)

    return redirect("/home/")



def changePassword(request, aid):
    user = models.User.objects.filter(id=request.info_dict['id']).first()

    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            encrypt_pasword = md5(new_password)
            user.password = encrypt_pasword
            user.save()
            return render(request, 'account/password_changed.html')
    else:
        form = ChangePasswordForm(user)
    return render(request, 'account/change_password.html', {'form': form})


def img_code(request):
    # 1.Generate Image
    image_object, code_str = check_code()

    # 2.The image content is returned and written to the memory, read from the memory and returned
    stream = BytesIO()
    image_object.save(stream, 'png')

    # 3.The content of the image is written to the session + 60s
    request.session['image_code'] = code_str
    request.session.set_expiry(60)

    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.clear()
    return redirect('login/')


def home(request):
    print(request.info_dict)
    # request.info_dict['name']
    return render(request, 'account/home.html')

def upload(request):
    return render(request, 'account/upload.html')

def check(request):
    return render(request, 'account/check.html')


