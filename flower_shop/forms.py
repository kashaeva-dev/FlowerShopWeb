from django import forms

class ConsultationForm(forms.ModelForm):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.PhoneField(label='Телефон', max_length=15)
    agree = forms.BooleanField(label='Согласие', required=False)