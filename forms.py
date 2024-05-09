from datetime import date
from django import forms
from .models import BookInformation,student_purchase,student_register

        
class student_register_form(forms.ModelForm):
    class Meta:
        model= student_register
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class OTPForm(forms.Form):
    email = forms.EmailField()

class OTPValidationForm(forms.Form):
    otp = forms.CharField(max_length=6)
    
class BookInformationForm(forms.ModelForm):
    class Meta:
        model = BookInformation
        fields = ['book_name', 'author_name', 'department_name','count']

        

class student_purchase_form(forms.ModelForm):
    class Meta:
        model = student_purchase
        fields = "__all__"
        
class BookForm(forms.ModelForm):
    class Meta:
        model = BookInformation
        fields = ['book_name', 'author_name', 'department_name', 'count']
