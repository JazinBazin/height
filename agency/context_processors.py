from . import models


def contacts(request):
    if not request.path.startswith('/admin/'):
        return {
            'contacts': models.Contact.objects.first(),
        }
    else:
        return {}
