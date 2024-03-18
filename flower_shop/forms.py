import datetime

from django import forms
from .models import DeliveryInterval, Order, Bouquet, Consulting, PaymentType
from phonenumber_field.formfields import PhoneNumberField



class OrderForm(forms.Form):
    current_time = datetime.datetime.now().time()
    fname = forms.CharField(label='Имя', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': 'Введите Имя'}))
    tel = forms.CharField(label='Телефон', max_length=15,
                          widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': '+ 7 (999) 000 '
                                                                                                     '00 00'}))
    adres = forms.CharField(label='Адрес доставки', max_length=100,
                            widget=forms.TextInput(
                                attrs={'class': 'order__form_input', 'placeholder': 'Адрес доставки'}))
    orderTime = forms.ModelChoiceField(label='Время заказа',
                                       queryset=DeliveryInterval.objects.filter(start_time__gte=current_time),
                                       empty_label=None,
                                       widget=forms.RadioSelect(attrs={'class': 'order__form_radio'}))
    online_payment = forms.BooleanField(label='Оплата онлайн', initial=True, required=False)

    def __init__(self, *args, **kwargs):
        self.bouquet_id = kwargs.pop('bouquet_id', None)
        super(OrderForm, self).__init__(*args, **kwargs)

    def save_order(self):
        cleaned_data = self.cleaned_data
        fname = cleaned_data['fname']
        tel = cleaned_data['tel']
        adres = cleaned_data['adres']
        order_time = cleaned_data['orderTime']
        online_payment = cleaned_data['online_payment']

        if online_payment:
            payment_type = PaymentType.objects.get(name='онлайн')
        else:
            payment_type = PaymentType.objects.get(name='наличными курьеру')

        bouquet = Bouquet.objects.get(id=self.bouquet_id)

        order = Order.objects.create(
            contact_name=fname,
            contact_phone=tel,
            delivery_address=adres,
            delivery_interval=order_time,
            bouquet=bouquet,
            payment_type=payment_type
        )
        return order


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
                                   error_messages={
                                       'required': 'Пожалуйста, подтвердите согласие на обработку персональных'
                                                   ' данных.'},
                                   widget=forms.CheckboxInput(attrs={'checked': 'checked',
                                                                     }))

    class Meta:
        model = Consulting
        fields = ['client_name', 'contact_phone', 'agreement']
