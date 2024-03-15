from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Consulting


class CustomPhoneNumberField(PhoneNumberField):
    def to_python(self, value):
        if value and not value.startswith('+'):
            value = '+7' + value
        return super(CustomPhoneNumberField, self).to_python(value)


class ConsultingForm(forms.ModelForm):
    client_name = forms.CharField(label='Имя клиента',
                           max_length=100,
                           widget=forms.TextInput(attrs={'placeholder': 'Введите Имя', 'required': 'required'}))
    contact_phone = CustomPhoneNumberField(label='Телефон',
                                     max_length=15,
                                     error_messages={'invalid': 'Введите корректный номер телефона.'},
                                     widget=forms.TextInput(attrs={'placeholder': 'Введите Имя',
                                                                   'required': 'required'}))
    agreement = forms.BooleanField(required=True,
                                   error_messages={'required': 'Пожалуйста, подтвердите согласие на обработку персональных данных.'},
                                   widget=forms.CheckboxInput(attrs={'checked': 'checked',
                                                                     }))

    class Meta:
        model = Consulting
        fields = ['client_name', 'contact_phone', 'agreement']
