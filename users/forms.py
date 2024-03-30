import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import ModelForm

from .models import User, Professor

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

RANK_CHOICES = [
    ('I', 'Instructor'),
    ('A1', 'Assistant Professor'),
    ('A2', 'Associate Professor'),
    ('P', 'Professor')
]


class UserForm(ModelForm):
    gender = forms.CharField(max_length=1, widget=forms.Select(choices=GENDER_CHOICES))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'national_id', 'gender', 'birth_date',
                  'user_code']

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if len(username) < 5:
                raise forms.ValidationError("Username must be at least 5 characters long.")
            if username.isdigit():
                raise forms.ValidationError("Username cannot consist of only numbers.")
            if not username.isascii():
                raise forms.ValidationError("Username must contain English characters only.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name:
            if not first_name.isalpha():
                raise forms.ValidationError("Your first name must contain only letters.")
            if not first_name.isascii():
                raise forms.ValidationError("Your first name must be in English.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name:
            if not last_name.isalpha():
                raise forms.ValidationError("Your last name must contain only letters.")
            if not last_name.isascii():
                raise forms.ValidationError("Your last name must be in English.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number:
            if not re.match(r"^(09)([0-9]{9})$", phone_number):
                raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if national_id:
            if not national_id.isdigit() or len(national_id) != 10:
                raise forms.ValidationError("National ID must be a valid 10-digit number.")
        return national_id

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender:
            if gender not in [item[0] for item in GENDER_CHOICES]:
                raise forms.ValidationError("Gender Must be M or F.")
        return gender

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.match(r"^.{8,255}$", password):
            raise forms.ValidationError("Password should be at least 8 characters long.")
        if not re.search(r"(.*[!@#$%^&*()_+\-=\[\]{};':\"\\,.<>?].*)+", password):
            raise forms.ValidationError("Password should have at least one special character.")
        if not re.search(r"(.*[A-Z].*)+", password):
            raise forms.ValidationError("Password should have at least one uppercase letter")
        if not re.search(r"(.*\d.*){2,}", password):
            raise forms.ValidationError("Password should have at least two digits")
        return password


class UpdateUserForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False


class ProfessorForm(ModelForm):
    rank = forms.CharField(max_length=2, widget=forms.Select(choices=RANK_CHOICES))

    def __init__(self, *args, **kwargs):
        super(ProfessorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Professor
        fields = ['specialization', 'rank']

    def clean_specialization(self):
        specialization = self.cleaned_data['specialization']
        if specialization:
            if specialization.isdigit():
                raise forms.ValidationError("Specialization cannot consist of only numbers.")
            if not specialization.isalpha():
                raise forms.ValidationError("Specialization must contain English characters only.")
        return specialization

    def clean_rank(self):
        rank = self.cleaned_data['rank']
        if rank:
            if rank not in [item[0] for item in RANK_CHOICES]:
                raise forms.ValidationError(f"Rank Must be {' or '.join([item[0] for item in RANK_CHOICES])}")
        return rank


class UpdateProfessorForm(ProfessorForm):
    def __init__(self, *args, **kwargs):
        super(UpdateProfessorForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = False
