from io import BytesIO
from django.core.paginator import Paginator
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ValidationError
import django_filters

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
    request.session.set_expiry(60 * 60 * 13)

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

class LogFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset=models.Log.objects.values_list('user', flat=True).distinct())
    action = django_filters.ChoiceFilter(choices=[(action, action) for action in models.Log.objects.values_list('action', flat=True).distinct()])
    model = django_filters.ChoiceFilter(choices=[(model, model) for model in models.Log.objects.values_list('model', flat=True).distinct()])
    object_id = django_filters.CharFilter(field_name='object_id', lookup_expr='exact')
    timestamp = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = models.Log
        fields = ['user', 'action', 'model', 'object_id', 'timestamp']

def home(request):
    # log_filter = LogFilter(request.GET, queryset=models.Log.objects.all().order_by('-timestamp'))
    # paginator = Paginator(log_filter.qs, 20)  # Display 20 logs per page
    # page_number = request.GET.get('page')   
    # page_obj = paginator.get_page(page_number)
    
    # return render(request, 'account/home.html', {'page_obj': page_obj, 'filter': log_filter})
    logs = models.Log.objects.all().order_by('-timestamp')

    user_filter = request.GET.get('user')
    if user_filter:
        logs = logs.filter(user__username=user_filter)

    action_filter = request.GET.get('action')
    if action_filter:
        logs = logs.filter(action=action_filter)

    table_filter = request.GET.get('table')
    if table_filter:
        logs = logs.filter(model=table_filter)

    object_id_filter = request.GET.get('object_id')
    if object_id_filter:
        logs = logs.filter(object_id=object_id_filter)

    timestamp_filter = request.GET.get('timestamp')
    if timestamp_filter:
        logs = logs.filter(timestamp__icontains=timestamp_filter)

    paginator = Paginator(logs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = models.Log.objects.values_list('user__username', flat=True).distinct()
    actions = models.Log.objects.values_list('action', flat=True).distinct()
    tables = models.Log.objects.values_list('model', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'users': users,
        'actions': actions,
        'tables': tables,
    }
    return render(request, 'account/home.html', context)

    # print(request.info_dict)
    # request.info_dict['name']
    # return render(request, 'account/home.html')

class LogFilterUser(django_filters.FilterSet):
    action = django_filters.ChoiceFilter(choices=[(action, action) for action in models.Log.objects.values_list('action', flat=True).distinct()])
    model = django_filters.ChoiceFilter(choices=[(model, model) for model in models.Log.objects.values_list('model', flat=True).distinct()])
    object_id = django_filters.CharFilter(field_name='object_id', lookup_expr='exact')
    timestamp = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = models.Log
        fields = ['timestamp', 'action', 'model', 'object_id', ]

def user_log(request):
    user = models.User.objects.filter(id=request.info_dict['id']).first()
    user_logs = LogFilterUser(request.GET, queryset=models.Log.objects.filter(user=user).order_by('-timestamp')) 
    paginator = Paginator(user_logs.qs, 10)  # Display 10 logs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'account/log.html', {'page_obj': page_obj, 'filter': user_logs})

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'depart']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}



def upload(request):
    user = models.User.objects.filter(id=request.info_dict['id']).first()

    
    # print(user)
    return render(request, 'account/upload.html', {'user': user})
    # return render(request, 'account/upload.html')



def check(request):
    user = models.User.objects.filter(id=request.info_dict['id']).first()

    
    # print(user)
    return render(request, 'account/check.html', {'user': user})

    # print(user.username, user.depart)
    # return render(request, 'account/check.html', {'depart': user.depart})
    # return render(request, 'account/check.html')


