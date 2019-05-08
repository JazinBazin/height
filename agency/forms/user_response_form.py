from django.core import mail
from .user_basic_form import UserBasicForm


class UserResponseForm(UserBasicForm):

    def send_mail(self, vendor_code):
        message = 'Артикул: ' + vendor_code + '\n' + \
            'Имя: ' + self.cleaned_data['users_name'] + '\n' + \
            'Номер телефона: ' + self.cleaned_data['users_phone'] + '\n' + \
            'Почта: ' + self.cleaned_data['users_email'] + '\n'

        mail.send_mail(
            'Пользователь ' +
            self.cleaned_data['users_name'] + ' откликнулся на объявление',
            message,
            'visota-agency@rambler.ru',
            ['visota-agency@rambler.ru'],
            fail_silently=False,
        )
