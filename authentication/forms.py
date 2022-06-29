from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from authentication.models import CustomUser, Worker, WorkerCategory

class WorkerSignUpForm(UserCreationForm):
    category_name = forms.ModelChoiceField(
        queryset=WorkerCategory.objects.all(),
        # to_field_name="category_name",
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser    
        fields= ('name', 'email','phone_number', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_worker = True
        user.save()
        worker = Worker.objects.create(user=user)
        worker.category_name = self.cleaned_data.get('category_name')
        worker.save()
        return user

    def __init__(self, *args, **kwargs):
        super(WorkerSignUpForm, self).__init__(*args, **kwargs)
        for field_name in ('name', 'email', 'password1', 'password2'):
            self.fields[field_name].help_text = ''

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser    
        fields= ('name','phone_number', 'address', 'profile_image')


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('experience','id_proof', 'id_image')


class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser    
        fields= ('name', 'email','phone_number', 'address')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        for field_name in ('name', 'email', 'password1', 'password2'):
            self.fields[field_name].help_text = ''