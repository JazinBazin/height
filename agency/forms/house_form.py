from django import forms
from .real_estate_form import RealEstateFiltersForm
from agency import models


class HouseForm(RealEstateFiltersForm):

    district = forms.ModelChoiceField(
        queryset=models.District.objects.filter(id__in=(
            estate.district.id for estate in models.House.objects.exclude(district=None))).order_by('name'),
        empty_label='Все',
        to_field_name='name',
        label='Район:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    populated_area = forms.ModelChoiceField(
        queryset=models.PopulatedArea.objects.filter(id__in=(
            estate.populated_area.id for estate in models.House.objects.exclude(populated_area=None))).order_by('name'),
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

    house_type = forms.ChoiceField(
        label='Тип жилья:',
        choices=(
            ('a', 'Неважно'),
            ('h', 'Дом'),
            ('c', 'Дача')),
        initial='a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def filter(self):
        houses = super().filter(models.House)

        if self.cleaned_data['rooms_from']:
            houses = houses.filter(
                number_of_rooms__gte=self.cleaned_data['rooms_from'])
        if self.cleaned_data['rooms_to']:
            houses = houses.filter(
                number_of_rooms__lte=self.cleaned_data['rooms_to'])
        if self.cleaned_data['floors_count_from']:
            houses = houses.filter(
                number_of_floors__gte=self.cleaned_data['floors_count_from'])
        if self.cleaned_data['floors_count_to']:
            houses = houses.filter(
                number_of_floors__lte=self.cleaned_data['floors_count_to'])
        if self.cleaned_data['house_type'] != 'a':
            houses = houses.filter(
                house_type=self.cleaned_data['house_type'])

        return houses
