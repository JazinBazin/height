from django import forms
from django.db.models import Q
from agency import models


class RealEstateFiltersForm(forms.Form):

    sort_type = forms.ChoiceField(
        label='Сортировка:',
        choices=(
            ('n', 'Не сортировать'),
            ('price', 'По цене'),
            ('area', 'По площади')),
        initial='n',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    sort_order = forms.ChoiceField(
        label='Тип сортировки:',
        choices=(
            ('a', 'По возрастанию'),
            ('d', 'По убыванию')),
        initial='a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    transaction_type = forms.ChoiceField(
        label='Вид сделки:',
        choices=(
            ('a', 'Любой'),
            ('p', 'Покупка'),
            ('r', 'Аренда'),
            ('e', 'Обмен')),
        initial='any',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    price_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )

    price_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )

    area_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )

    area_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )

    district = forms.ModelChoiceField(
        queryset=None,
        empty_label='Все',
        to_field_name='name',
        label='Район:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    populated_area = forms.ModelChoiceField(
        queryset=None,
        empty_label='Все',
        to_field_name='name',
        label='Населённый пункт:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def filter(self, RealEstate):
        real_estate = RealEstate.objects.filter(status='p')

        if self.cleaned_data['price_from']:
            real_estate = real_estate.filter(
                price__gte=self.cleaned_data['price_from'])
        if self.cleaned_data['price_to']:
            real_estate = real_estate.filter(
                price__lt=self.cleaned_data['price_to'])
        if self.cleaned_data['area_from']:
            real_estate = real_estate.filter(
                area__gte=self.cleaned_data['area_from'])
        if self.cleaned_data['area_to']:
            real_estate = real_estate.filter(
                area__lt=self.cleaned_data['area_to'])
        if self.cleaned_data['transaction_type'] != 'a':
            real_estate = real_estate.filter(
                transaction_type=self.cleaned_data['transaction_type'])

        district = self.cleaned_data['district']
        populated_area = self.cleaned_data['populated_area']

        if populated_area:
            if district:
                if populated_area.is_city:
                    real_estate = real_estate.filter(
                        Q(populated_area=populated_area) | Q(district=district))
                else:
                    real_estate = real_estate.filter(
                        populated_area=populated_area, district=district)
            else:
                real_estate = real_estate.filter(
                    populated_area=populated_area)
        elif district:
            real_estate = real_estate.filter(
                district=district
            )

        if self.cleaned_data['sort_type'] != 'n':
            if self.cleaned_data['sort_order'] == 'a':
                real_estate = real_estate.order_by(
                    self.cleaned_data['sort_type'])
            else:
                real_estate = real_estate.order_by(
                    "-" + self.cleaned_data['sort_type'])

        return real_estate
