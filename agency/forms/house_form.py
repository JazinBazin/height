from django import forms
from .real_estate_form import RealEstateFiltersForm
from agency.models import House


class HouseForm(RealEstateFiltersForm):

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
            ('a', 'Не важно'),
            ('h', 'Дом'),
            ('c', 'Дача')),
        initial='a',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def filter(self):
        houses = super().filter(House)

        if self.cleaned_data['rooms_from']:
            houses = houses.filter(
                number_of_rooms__gte=self.cleaned_data['rooms_from'])
        if self.cleaned_data['rooms_to']:
            houses = houses.filter(
                number_of_rooms__lt=self.cleaned_data['rooms_to'])
        if self.cleaned_data['floors_count_from']:
            houses = houses.filter(
                number_of_floors__gte=self.cleaned_data['floors_count_from'])
        if self.cleaned_data['floors_count_to']:
            houses = houses.filter(
                number_of_floors__lt=self.cleaned_data['floors_count_to'])
        if self.cleaned_data['house_type'] != 'a':
            houses = houses.filter(
                house_type=self.cleaned_data['house_type'])

        return houses
