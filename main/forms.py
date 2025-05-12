from django import forms
from .models import Contact, CourseEnrollment, Course, Student, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class EnrollmentForm(forms.Form):
    course_id = forms.IntegerField(widget=forms.HiddenInput())
