# -*- coding: UTF-8 -*-

import json
import urllib2
import urlparse
from django import template
from django.conf import settings

register = template.Library()

ASSETS = {}

def get_assets(url):
    if not settings.DEBUG and ASSETS.has_key(url):
        return ASSETS[url]
    assets_url = '%s?url=%s' % (settings.SPROCKETS_GET_ASSET_URL, url)
    req = urllib2.Request(assets_url)
    resp = urllib2.urlopen(req)
    assets = ASSETS[url] = json.loads(resp.read())
    return assets

@register.simple_tag
def stylesheet_tag(url, media='screen'):
    assets = get_assets(url)
    return '\n'.join(['<link href="%s%s" media="%s" rel="stylesheet" type="text/css" />' % \
            (settings.SPROCKETS_ASSETS_URL, asset, media) \
            for asset in assets])

@register.simple_tag
def javascript_tag(url):
    assets = get_assets(url)
    return '\n'.join(['<script src="%s%s" type="text/javascript"></script>' % \
            (settings.SPROCKETS_ASSETS_URL, asset)
            for asset in assets])

@register.simple_tag
def image_tag(url, **kwargs):
    assets = get_assets(url)
    attributes = ' '.join(['%s="%s"' % (k, v) for k, v in kwargs.items()])
    return '\n'.join(['<img src="%s%s" %s />' % \
            (settings.SPROCKETS_ASSETS_URL, asset, attributes)
            for asset in assets])

@register.simple_tag
def asset_url(url):
    return urlparse.urljoin(settings.SPROCKETS_ASSETS_URL, url)
