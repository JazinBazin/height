from django.contrib import admin
from django import forms
from django import db
from . import models
from .filters import RangeInputFilter
from django.utils.safestring import mark_safe

# admin.site.disable_action('delete_selected')
admin.site.site_header = 'Агентство недвижимости "Высота"'
admin.site.site_title = 'Агентство недвижимости "Высота"'


class AdvantageAdmin(admin.ModelAdmin):
    list_display = ('headline', 'order_number',)
    list_editable = ['order_number', ]


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('headline', 'order_number',)
    list_editable = ['order_number', ]


class RealEstateTypeAdmin(admin.ModelAdmin):
    exclude = ['link']
    list_display = ('headline', 'order_number',)
    list_editable = ['order_number', ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ServiceListItemInline(admin.TabularInline):
    model = models.ServiceListItem
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceListItemInline]
    list_display = ('headline', 'order_number',)
    list_editable = ['order_number', ]


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('headline', 'order_number',)
    list_editable = ['order_number', ]


class ContactPhoneInline(admin.StackedInline):
    model = models.ContactPhone
    extra = 0


class ContactAdmin(admin.ModelAdmin):
    inlines = [ContactPhoneInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RealEstateImageInline(admin.StackedInline):
    model = models.RealEstateImage
    extra = 0
    exclude = ['thumbnail']
    classes = ('collapse',)
    readonly_fields = ['thumbnail_image', ]

    def has_add_permission(self, request, obj):
        return False

    def thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" style="box-shadow: 0 0 10px rgba(0,0,0,0.5);"/>'.format(
            url=instance.thumbnail.url,
            width=instance.thumbnail.width,
            height=instance.thumbnail.height,
        ))

    thumbnail_image.short_description = 'Изображение'


basic_required_fields = ('headline', 'image', 'description', 'vendor_code',
                         'transaction_type', 'price', 'currency', 'area',
                         'area_units', 'address', 'phone')
basic_optional_fields = ('locality', 'district', 'documents',)
basic_list_filters = (('status', admin.ChoicesFieldListFilter),
                      ('is_best_offer', admin.BooleanFieldListFilter),
                      ('transaction_type', admin.ChoicesFieldListFilter),
                      ('price', RangeInputFilter),
                      ('area', RangeInputFilter))


class RealEstateAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'agency/admin/css/range_input_filter.css',
            )
        }

    inlines = [RealEstateImageInline]
    search_fields = ['headline', 'vendor_code']
    list_display = ('headline', 'vendor_code', 'status',
                    'is_best_offer', 'last_edit_date')
    exclude = ['thumbnail']
    list_filter = basic_list_filters
    list_per_page = 10
    actions = ['publish', 'archive',
               'add_to_best_offers', 'remove_from_best_offers']
    formfield_overrides = {
        db.models.PositiveIntegerField: {'widget': forms.NumberInput},
    }
    list_editable = ['status', 'is_best_offer']
    fieldsets = (
        (None, {
            'fields': basic_required_fields + ('status', 'is_best_offer',)
        }),
        ('Необязательные параметры', {
            'classes': ('collapse',),
            'fields': basic_optional_fields
        }),
    )
    date_hierarchy = 'creation_date'
    ordering = ('-last_edit_date',)

    def view_on_site(self, obj):
        if obj.status == 'p':
            return '/' + str(obj.id) + obj.description_page + '/'

    def publish(self, request, queryset):
        queryset.update(status='p')

    def archive(self, request, queryset):
        queryset.update(status='a')

    def add_to_best_offers(self, request, queryset):
        queryset.update(is_best_offer=True)

    def remove_from_best_offers(self, request, queryset):
        queryset.update(is_best_offer=False)

    publish.short_description = 'Опубликовать'
    archive.short_description = 'Архивировать'
    add_to_best_offers.short_description = 'Добавить в \"Лучшие предложения\"'
    remove_from_best_offers.short_description = 'Удалить из \"Лучших предложений\"'

    def save_model(self, request, obj, form, change):
        obj.save()
        for afile in request.FILES.getlist('multiple_images'):
            obj.images.create(image=afile)


class ApartmentAdmin(RealEstateAdmin):
    list_filter = basic_list_filters + (('number_of_rooms', RangeInputFilter),
                                        ('floor_number', RangeInputFilter),
                                        ('number_of_floors', RangeInputFilter),
                                        ('balcony', admin.BooleanFieldListFilter),
                                        ('bathroom', admin.ChoicesFieldListFilter))

    fieldsets = (
        (None, {
            'fields': basic_required_fields +
            ('number_of_rooms', 'floor_number', 'number_of_floors',
             'balcony', 'bathroom', 'status', 'is_best_offer',),
        }),
        ('Необязательные параметры', {
            'classes': ('collapse',),
            'fields': basic_optional_fields + ('decoration', 'building_type')
        }),
    )


class HouseAdmin(RealEstateAdmin):
    list_filter = basic_list_filters + (('number_of_rooms', RangeInputFilter),
                                        ('number_of_floors', RangeInputFilter),
                                        ('house_type', admin.ChoicesFieldListFilter),)

    fieldsets = (
        (None, {
            'fields': basic_required_fields +
            ('house_type', 'number_of_floors',
             'number_of_rooms', 'status', 'is_best_offer',)
        }),
        ('Необязательные параметры', {
            'classes': ('collapse',),
            'fields': basic_optional_fields + ('decoration',)
        }),
    )


class CommercialAdmin(RealEstateAdmin):
    list_filter = basic_list_filters + \
        (('commercial_type', admin.AllValuesFieldListFilter),)
    fieldsets = (
        (None, {
            'fields': basic_required_fields + ('commercial_type', 'status', 'is_best_offer',)
        }),
        ('Необязательные параметры', {
            'classes': ('collapse',),
            'fields': basic_optional_fields +
            ('number_of_rooms', 'number_of_floors',
             'decoration',)
        }),
    )


admin.site.register(models.RealEstateType, RealEstateTypeAdmin)
admin.site.register(models.Advantage, AdvantageAdmin)
admin.site.register(models.Apartment, ApartmentAdmin)
admin.site.register(models.House, HouseAdmin)
admin.site.register(models.Land, RealEstateAdmin)
admin.site.register(models.Garage, RealEstateAdmin)
admin.site.register(models.Commercial, CommercialAdmin)
admin.site.register(models.Contact, ContactAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Description, DescriptionAdmin)
admin.site.register(models.Certificate, CertificateAdmin)
