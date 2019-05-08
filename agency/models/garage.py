from .real_estate import RealEstate


class Garage(RealEstate):
    class Meta:
        verbose_name = 'гараж'
        verbose_name_plural = 'Гаражи'

    description_page = 'garage_description'