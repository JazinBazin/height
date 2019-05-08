from .real_estate_form import RealEstateFiltersForm
from agency.models import Commercial


class CommercialForm(RealEstateFiltersForm):

    def filter(self):
        commercial = super().filter(Commercial)
        return commercial
