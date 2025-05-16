from django import forms
from .models import StudyMaterial ,University, Course, YearSemester ,Student ,QuestionPaper
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StudyMaterialForm(forms.ModelForm):
    class Meta:
        model = StudyMaterial
        fields = [
            'title', 'university', 'course', 'year_or_semester',
            'semester',  # NEW FIELD
            'subject', 'file_upload', 'drive_link', 'description'
        ]


class StudentSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already taken.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Passwords do not match.')

        return cleaned_data

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'university', 'course', 'year_or_semester']


class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = [
            'title', 'university', 'course', 'year_or_semester','semester',
            'subject', 'file_upload', 'drive_link', 'description'
        ]

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    university = forms.ModelChoiceField(queryset=University.objects.all(), required=False)

    class Meta:
        model = Student
        fields = ['university']

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            student.save()
        return student

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        required=False
    )