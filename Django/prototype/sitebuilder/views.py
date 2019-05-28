from django.shortcuts import render
from django.template import Template, Context
from django.http import HttpResponse, Http404
from django.conf import settings
import os
import json
from django.template.loader_tags import BlockNode

def get_page_or_404(name):
    '''Return page content as a Django template or raise 404 error.'''
    try:
        file_path = os.path.join(settings.SITE_PAGES_DIRECTORY, name)
    except ValueError as e:
        raise Http404('Page not found (Value error: ' + e.reason + '.) ' + 'Path=' + file_path)
    else:
        if not os.path.exists(file_path):
            raise Http404('Page not found (Nonexistent path)')
    with open(file_path, 'r', encoding = 'utf-8') as f:
        page = Template(f.read())
    meta = None
    for i, node in enumerate(list(page.nodelist)):
        if isinstance(node, BlockNode) and node.name == 'context':
            meta = page.nodelist.pop(i)
            break
    page._meta = meta
    return page

def page(request, slug = 'index'):
    '''Render the requested page if found.'''
    file_name = '{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug' : slug,
        'page' : page,
    }
    if page._meta is not None:
        meta = page._meta.render(Context())
        extra_context = json.loads(meta)
        context.update(extra_context)
    return render(request, 'page.html', context)