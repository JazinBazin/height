from django import forms

class UserBasicForm(forms.Form):

    users_name = forms.CharField(
        label='Ваше имя:',
        min_length=2,
        max_length=100,
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    users_phone = forms.CharField(
        min_length=10,
        max_length=100,
        label='Номер телефона:',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    users_email = forms.EmailField(
        label='Ваш email:',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )