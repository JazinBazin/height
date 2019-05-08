from .real_estate_form import RealEstateFiltersForm
from agency.models import Land


class LandForm(RealEstateFiltersForm):

    def filter(self):
        lands = super().filter(Land)
        return lands
