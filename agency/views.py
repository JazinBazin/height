from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models, serializers, forms


def index(request):
    return render(request, 'agency/pages/index.html', {
        'advantages': models.Advantage.objects.all(),
        'real_estate_types': models.RealEstateType.objects.all(),
        # 'contacts': models.Contact.objects.first(),
    })


def services(request):
    return render(request, 'agency/pages/services.html', {
        'services': models.Service.objects.all(),
        'real_estate_types': models.RealEstateType.objects.all(),
    })


def about(request):
    return render(request, 'agency/pages/about.html', {
        'descriptions': models.Description.objects.all(),
    })


def contacts(request):
    return render(request, 'agency/pages/contacts.html', {
        # 'contacts': models.Contact.objects.first(),
    })


def user_request(request):
    if request.method == 'POST':
        user_requst_form = forms.UserRequestForm(request.POST)
        if user_requst_form.is_valid():
            user_requst_form.send_email()
            return HttpResponseRedirect(reverse('agency:success_users_request'))

    return render(request, 'agency/pages/user_request.html', {
        'form': forms.UserRequestForm(),
    })


def success_users_request(request):
    return render(request, 'agency/pages/success_users_request.html', {
        'real_estate_types': models.RealEstateType.objects.all(),
    })


@api_view(['POST'])
def user_response(request):
    form = forms.UserResponseForm(request.data.get('formData'))

    if form.is_valid():
        form.send_mail(request.data.get('vendorCode'))
        return Response('ok')
    else:
        return Response('error')


def real_estate_data(request, RealEstate, Form, Serializer):
    offset = int(request.data.get('offset'))
    count = int(request.data.get('count'))
    form = Form(request.data.get('formData'))

    if form.is_valid():
        all_real_estate = form.filter()
    else:
        all_real_estate = RealEstate.objects.filter(status='p')

    response_real_estate = all_real_estate[offset:offset + count]
    serializer = Serializer(response_real_estate, many=True)
    return serializer.data


@api_view(['POST'])
def apartments_list(request):
    return Response(real_estate_data(request, models.Apartment, forms.ApartmentsForm,
                                     serializers.ApartmentSerializer))


@api_view(['POST'])
def houses_list(request):
    return Response(real_estate_data(request, models.House, forms.HouseForm,
                                     serializers.HouseSerializer))


@api_view(['POST'])
def lands_list(request):
    return Response(real_estate_data(request, models.Land, forms.LandForm,
                                     serializers.LandSerializer))


@api_view(['POST'])
def garages_list(request):
    return Response(real_estate_data(request, models.Garage, forms.GarageForm,
                                     serializers.GarageSerializer))


@api_view(['POST'])
def commercial_list(request):
    return Response(real_estate_data(request, models.Commercial, forms.CommercialForm,
                                     serializers.CommercialtSerializer))


forms_template_name_prefix = 'agency/forms/'
unique_params_template_name_prefix = 'agency/pages/real_estate/'
description_template_name_prefix = 'agency/pages/real_estate/'


def real_estate_description(request, pk, RealEstate, template_name):
    real_estate = get_object_or_404(RealEstate, pk=pk)
    if real_estate.status != 'p':
        raise Http404
    return render(request, description_template_name_prefix + template_name, {
        'real_estate': real_estate,
        'form': forms.UserResponseForm(),
    })


def apartments(request):
    return render(request, 'agency/pages/real_estate/real_estate.html', {
        'page_title': 'Квартиры',
        'page_description': 'Продажа, покупка, аренда и обмен квартир. Список предложений.',
        'real_estate_description_page_url': 'apartment_description',
        'real_estate_list_url': '/apartments_list/',
        'form': forms.ApartmentsForm(),
        'form_template': forms_template_name_prefix + 'apartments_form.html',
        'description_page': 'agency:apartment_description',
        'unique_params_template': unique_params_template_name_prefix + 'apartments.html',
        'best_ads': models.Apartment.objects.filter(status='p', is_best_offer=True),
        'unique_params_component_name': 'apartment'
    })


def apartment_description(request, pk):
    return real_estate_description(request, pk, models.Apartment, 'apartment_description.html')


def houses(request):
    return render(request, 'agency/pages/real_estate/real_estate.html', {
        'page_title': 'Дома и дачи',
        'page_description': 'Продажа, покупка, аренда и обмен домов и дач. Список предложений.',
        'real_estate_description_page_url': 'house_description',
        'real_estate_list_url': '/houses_list/',
        'form': forms.HouseForm(),
        'form_template': forms_template_name_prefix + 'houses_form.html',
        'description_page': 'agency:house_description',
        'unique_params_template': unique_params_template_name_prefix + 'houses.html',
        'best_ads': models.House.objects.filter(status='p', is_best_offer=True),
        'unique_params_component_name': 'house'
    })


def house_description(request, pk):
    return real_estate_description(request, pk, models.House, 'house_description.html')


def lands(request):
    return render(request, 'agency/pages/real_estate/real_estate.html', {
        'page_title': 'Земельные участки',
        'real_estate_description_page_url': 'land_description',
        'page_description': 'Продажа, покупка, аренда и обмен земельных участков. Список предложений.',
        'real_estate_list_url': '/lands_list/',
        'form': forms.LandForm(),
        'form_template': forms_template_name_prefix + 'lands_form.html',
        'description_page': 'agency:land_description',
        'unique_params_template': unique_params_template_name_prefix + 'lands.html',
        'best_ads': models.Land.objects.filter(status='p', is_best_offer=True),
        'unique_params_component_name': 'land'
    })


def land_description(request, pk):
    return real_estate_description(request, pk, models.Land, 'land_description.html')


def garages(request):
    return render(request, 'agency/pages/real_estate/real_estate.html', {
        'page_title': 'Гаражи',
        'page_description': 'Продажа, покупка, аренда и обмен гаражей. Список предложений.',
        'real_estate_description_page_url': 'garage_description',
        'real_estate_list_url': '/garages_list/',
        'form': forms.GarageForm(),
        'form_template': forms_template_name_prefix + 'garages_form.html',
        'description_page': 'agency:garage_description',
        'unique_params_template': unique_params_template_name_prefix + 'garages.html',
        'best_ads': models.Garage.objects.filter(status='p', is_best_offer=True),
        'unique_params_component_name': 'garage'
    })


def garage_description(request, pk):
    return real_estate_description(request, pk, models.Garage, 'garage_description.html')


def commercial(request):
    return render(request, 'agency/pages/real_estate/real_estate.html', {
        'page_title': 'Коммерческая недвижимость',
        'page_description': 'Продажа, покупка, аренда и обмен коммерческой недвижимости. Список предложений.',
        'real_estate_description_page_url': 'commercial_description',
        'real_estate_list_url': '/commercial_list/',
        'form': forms.CommercialForm(),
        'form_template': forms_template_name_prefix + 'commercial_form.html',
        'description_page': 'agency:commercial_description',
        'unique_params_template': unique_params_template_name_prefix + 'commercial.html',
        'best_ads': models.Commercial.objects.filter(status='p', is_best_offer=True),
        'unique_params_component_name': 'commercial'
    })


def commercial_description(request, pk):
    return real_estate_description(request, pk, models.Commercial, 'commercial_description.html')


def get_best_offers(*list_of_real_estate):
    serialized_best_offers = []
    for RealEstateModel, RealEstateSerializer in list_of_real_estate:
        best_real_estate = RealEstateModel.objects.filter(
            status='p', is_best_offer=True)
        if best_real_estate:
            serializer = RealEstateSerializer(best_real_estate, many=True)
            serialized_best_offers.append({
                'tab_name': RealEstateModel._meta.model_name,
                'verbose_tab_name': RealEstateModel._meta.verbose_name_plural,
                'description_page': RealEstateModel.description_page,
                'ads': serializer.data
            })
    return serialized_best_offers


@api_view(['GET'])
def best_offers(request):
    return Response(get_best_offers((models.Apartment, serializers.ApartmentSerializer),
                                    (models.House, serializers.HouseSerializer),
                                    (models.Land, serializers.LandSerializer),
                                    (models.Garage, serializers.GarageSerializer),
                                    (models.Commercial, serializers.CommercialtSerializer)))
