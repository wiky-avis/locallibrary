import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Book

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату между сейчас и 4 недели (по умолчанию 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Проверьте, если дата не в прошлом.
        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата - продление в прошлом'))

        # Проверьте, является ли дата в допустимом диапазоне (+4 недели с сегодняшнего дня).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата - обновление более 4 недель впереди'))

        # Не забудьте всегда вернуть очищенные данные.
        return data
