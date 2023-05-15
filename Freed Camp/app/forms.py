import re

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app.models import Add_Lists, Tasks, Projects, Create


class CreateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput
    )
    phone_number = forms.CharField(label='Phone number')

    class Meta:
        model = Create
        fields = ('name', 'email', 'phone_number',)

    def clean_password_confirm(self):
        # Check that the two password entries match
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return password_confirm

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = re.sub(r'\D', '', phone_number)  # remove all non-numeric characters
        if len(phone_number) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Create.objects.filter(email=email).exists():
            raise ValidationError('This email is already in use')
        return email

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name must contain only letters')
        return name

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least one digit')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('Password must contain at least one letter')
        return password

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CreateAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Create
        fields = (
            'name', 'email', 'phone_number', 'password',
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions',
        )

    def clean_password(self):
        return self.initial['password']


class Add_List_Form(forms.ModelForm):
    class Meta:
        model = Add_Lists
        fields = ('name', 'description', 'project')

    widgets = {
        'name': forms.TextInput(attrs={'size': 300}),
        'description': forms.Textarea(attrs={'rows': 2}),
    }


class Project_form(forms.ModelForm):
    class Meta:
        model = Projects
        fields = '__all__'

    widgets = {
        'name': forms.TextInput(attrs={'size': 300}),
    }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if Projects.objects.filter(name=name).exists():
            raise forms.ValidationError('This name already exists')
        return cleaned_data


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('name', 'title', 'description', 'assigned_to', 'status', 'priority', 'attachment')
        widgets = {
            'attachment': forms.ClearableFileInput(attrs={'multiple': True}),
            'priority': forms.Select(attrs={'style': 'width: 500px; height: 30px;'}),
            'assigned_to': forms.Select(attrs={'style': 'width: 500px; height: 30px;'}),
            'status': forms.Select(attrs={'style': 'width: 500px; height: 30px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['priority'].initial = 'none'
        self.fields['status'].initial = 'pending'
        self.fields['attachment'].initial = 'static/assets/img/default.jpg'


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('name', 'title', 'description', 'assigned_to', 'status', 'priority', 'attachment')
        widgets = {
            'attachment': forms.ClearableFileInput(attrs={'multiple': True}),
            'priority': forms.Select(attrs={'style': 'width: 500px; height: 50px;'}),
            'assigned_to': forms.Select(attrs={'style': 'width: 500px; height: 50px;'}),
            'status': forms.Select(attrs={'style': 'width: 500px; height: 50px;'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Create
        fields = ['name', 'phone_number', 'photo']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name must contain only letters')
        return name

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = re.sub(r'\D', '', phone_number)  # remove all non-numeric characters
        if len(phone_number) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits')
        return phone_number


class AssignForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['assigned_to']

        widgets = {
            'assigned_to': forms.Select(attrs={'style': 'width: 350px; height: 40px;'}),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['status']

        widgets = {
            'status': forms.Select(attrs={'style': 'width: 350px; height: 40px;'}),
        }


class FilterForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['status', 'priority', 'assigned_to']


class PriorityForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['priority']

        widgets = {
            'priority': forms.Select(attrs={'style': 'width: 350px; height: 40px;'}),
        }