from django import forms
from django.core import mail
from .user_basic_form import UserBasicForm


class UserRequestForm(UserBasicForm):

    users_message = forms.CharField(
        label='Сообщение:',
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Ваши пожелания',
            'rows': '10'
        })
    )

    def send_email(self):
        message = 'Имя: ' + self.cleaned_data['users_name'] + '\n' + \
            'Номер телефона: ' + self.cleaned_data['users_phone'] + '\n' + \
            'Почта: ' + self.cleaned_data['users_email'] + '\n'

        if self.cleaned_data['users_message']:
            message += 'Сообщение: ' + self.cleaned_data['users_message']

        mail.send_mail(
            'Заявка от пользователя ' + self.cleaned_data['users_name'],
            message,
            'visota-agency@rambler.ru',
            ['visota-agency@rambler.ru'],
            fail_silently=False,
        )
