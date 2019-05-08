from .real_estate_form import RealEstateFiltersForm
from agency.models import Garage


class GarageForm(RealEstateFiltersForm):

    def filter(self):
        lands = super().filter(Garage)
        return lands
