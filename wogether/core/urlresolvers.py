# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import urlresolvers


__real_reverse = urlresolvers.reverse


def reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None):
    try:
        return __real_reverse(viewname, urlconf, args, kwargs, current_app)
    except urlresolvers.NoReverseMatch as no_match:
        external_urlconfs = getattr(settings, 'EXTERNAL_URLCONFS', [])
        for p, c in external_urlconfs:
            urlconf = c
            try:
                return p + __real_reverse(viewname, urlconf, args, kwargs, current_app)
            except urlresolvers.NoReverseMatch:
                pass
        raise no_match

urlresolvers.reverse = reverse
