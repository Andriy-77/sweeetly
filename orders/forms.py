from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(label='Імʼя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Прізвище', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адреса доставки', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))