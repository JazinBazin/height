from .real_estate_form import RealEstateFiltersForm
from django import forms
from agency import models


class LandForm(RealEstateFiltersForm):

    district = forms.ModelChoiceField(
        queryset=models.District.objects.filter(id__in=(
            estate.district.id for estate in models.Land.objects.exclude(district=None))).order_by('name'),
        empty_label='Все',
        to_field_name='name',
        label='Район:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    populated_area = forms.ModelChoiceField(
        queryset=models.PopulatedArea.objects.filter(id__in=(
            estate.populated_area.id for estate in models.Land.objects.exclude(populated_area=None))).order_by('name'),
        empty_label='Все',
        to_field_name='name',
        label='Населённый пункт:',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def filter(self):
        lands = super().filter(models.Land)
        return lands
