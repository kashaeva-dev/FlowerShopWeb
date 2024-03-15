from django import forms
from .models import DeliveryInterval, Order, Bouquet


class OrderForm(forms.Form):
    fname = forms.CharField(label='Имя', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': 'Введите Имя'}))
    tel = forms.CharField(label='Телефон', max_length=15,
                          widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': '+ 7 (999) 000 '
                                                                                                     '00 00'}))
    adres = forms.CharField(label='Адрес доставки', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'order__form_input', 'placeholder': 'Адрес доставки'}))
    orderTime = forms.ModelChoiceField(label='Время заказа',
                                       queryset=DeliveryInterval.objects.all(),
                                       empty_label=None,
                                       widget=forms.RadioSelect(attrs={'class': 'order__form_radio'}))

    def __init__(self, *args, **kwargs):
        self.bouquet_id = kwargs.pop('bouquet_id', None)
        super(OrderForm, self).__init__(*args, **kwargs)

    def save_order(self):
        cleaned_data = self.cleaned_data
        fname = cleaned_data['fname']
        tel = cleaned_data['tel']
        adres = cleaned_data['adres']
        orderTime = cleaned_data['orderTime']

        bouquet = Bouquet.objects.get(id=self.bouquet_id)

        order = Order.objects.create(
            contact_name=fname,
            contact_phone=tel,
            delivery_address=adres,
            delivery_interval=orderTime,
            bouquet=bouquet
        )
        return order
