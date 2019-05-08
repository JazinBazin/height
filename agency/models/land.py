from .real_estate import RealEstate


class Land(RealEstate):
    class Meta:
        verbose_name = 'земелный участок'
        verbose_name_plural = 'Земельные участки'

    description_page = 'land_description'