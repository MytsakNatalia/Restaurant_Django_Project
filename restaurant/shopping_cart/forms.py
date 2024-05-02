from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    total_price = forms.DecimalField(disabled=True, max_digits=8, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ('address', 'total_price', 'status')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control py-4'})
        self.fields['status'].widget.attrs.update({'class': 'form-control py-4'})
