from django import forms
from crispy_forms.helper import FormHelper
from .models import *
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user = User.objects.filter(username=username).first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user no longer active.")

        return super(UserLoginForm,self).clean(*args, **kwargs)


class UserRegisterFoam(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'email2',
            'password',
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Email must match")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This Email has already been registered")

        return email


class PostJob(forms.ModelForm):

    class Meta:
        model = Job
        fields = [
            'title',
            'description',
            'category',
            'company',
            'location',
            'salary',
        ]

    def __init__(self, *args, **kwargs):
        super(PostJob, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id_intake_form'
        self.helper.form_method = 'POST'
        self.helper.form_tag = True


class CreateCategory(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]


class CreateCompany(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'name',
            'description',
            'location',
        ]


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = [
            'description',
            'document',
        ]


class RateApplyForm(forms.ModelForm):
    class Meta:
        model = RateApply
        fields = [
            'rate',
            'comment',
        ]
        widgets = {
            'rate': forms.HiddenInput()
        }

        def clean_rate(self):
            rate = self.get('rate')
            if rate is None:
                raise forms.ValidationError("Rate required")