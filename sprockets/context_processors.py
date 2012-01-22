# -*- coding: UTF-8 -*-

from django.conf import settings

def sprockets(request):
    return {
        'SPROCKETS_ASSETS_URL': settings.SPROCKETS_ASSETS_URL,
    }
