from django import forms
from .real_estate_form import RealEstateFiltersForm
from agency import models


class ApartmentsForm(RealEstateFiltersForm):

    district = forms.ModelChoiceField(
        queryset=models.District.objects.filter(id__in=(
            estate.district.id for estate in models.Apartment.objects.exclude(district=None))).order_by('name'),
        empty_label='Все',
        to_field_name='name',
        label='Район:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    populated_area = forms.ModelChoiceField(
        queryset=models.PopulatedArea.objects.filter(id__in=(
            estate.populated_area.id for estate in models.Apartment.objects.exclude(populated_area=None))).order_by('name'),
        empty_label='Все',
        to_field_name='name',
        label='Населённый пункт:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    rooms_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )

    rooms_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )

    floor_number_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )

    floor_number_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )

    floors_count_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От'
        })
    )

    floors_count_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'До'
        })
    )

    balcony = forms.ChoiceField(
        label='Балкон:',
        choices=(
            ('a', 'Неважно'),
            (True, 'Есть'),
            (False, 'Нет')),
        initial='a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    bathroom = forms.ChoiceField(
        label='Санузел:',
        choices=(
            ('a', 'Неважно'),
            ('c', 'Совмещённый'),
            ('s', 'Раздельный')),
        initial='a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def filter(self):
        apartments = super().filter(models.Apartment)

        if self.cleaned_data['rooms_from']:
            apartments = apartments.filter(
                number_of_rooms__gte=self.cleaned_data['rooms_from'])
        if self.cleaned_data['rooms_to']:
            apartments = apartments.filter(
                number_of_rooms__lt=self.cleaned_data['rooms_to'])
        if self.cleaned_data['floor_number_from']:
            apartments = apartments.filter(
                floor_number__gte=self.cleaned_data['floor_number_from'])
        if self.cleaned_data['floor_number_to']:
            apartments = apartments.filter(
                floor_number__lt=self.cleaned_data['floor_number_to'])
        if self.cleaned_data['floors_count_from']:
            apartments = apartments.filter(
                number_of_floors__gte=self.cleaned_data['floors_count_from'])
        if self.cleaned_data['floors_count_to']:
            apartments = apartments.filter(
                number_of_floors__lt=self.cleaned_data['floors_count_to'])
        if self.cleaned_data['balcony'] != 'a':
            apartments = apartments.filter(
                balcony=self.cleaned_data['balcony'])
        if self.cleaned_data['bathroom'] != 'a':
            apartments = apartments.filter(
                bathroom=self.cleaned_data['bathroom'])

        return apartments
