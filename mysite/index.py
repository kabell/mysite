# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.defaulttags import register
from django.template.loader import get_template
from django.template import Context, Template
from django.core.exceptions import ObjectDoesNotExist
from time import time
import datetime
import os
import random
import glob
import codecs
import sys
from mysite.models import MenuItem, Page, BlogPost

def parse_args(s):
    return dict(x.split('=') for x in s.split('&'))



def blog(request,args):
    posts = BlogPost.objects.all().order_by('-id')[:10]
    template = get_template('blog.html')
    html = template.render(Context(locals()))
    return html

def blog_add(request,args):
    if request.POST:
        title = request.POST.get(key="title")
        trailer = request.POST.get(key='trailer')
        content = request.POST.get(key='content')

        post = BlogPost(title=title, trailer=trailer, content=content, date=datetime.datetime.now().date())
        post.save()

    id = -1
    template = get_template('blog_edit.html')
    html = template.render(Context(locals()))
    return html

def blog_edit(request,args):
    if request.POST:
        id = request.POST.get(key='id')
        title = request.POST.get(key="title")
        trailer = request.POST.get(key='trailer')
        content = request.POST.get(key='content')

        post = BlogPost.objects.get(id=id)
        post.title = title
        post.trailer = trailer
        post.content = content
        post.save()

    args = parse_args(args)

    post = BlogPost.objects.get(id=args['id'])
    template = get_template('blog_edit.html')
    html = template.render(Context(locals()))
    return html

def blog_post(request,args):
    postid = parse_args(args)['post']
    post = BlogPost.objects.get(id=postid)

    template = get_template('blogpost.html')
    html = template.render(Context(locals()))
    return html

def menu_edit(request,args):
    if request.POST:
        id = request.POST.get(key='id')
        page = request.POST.get(key='page')
        sk = request.POST.get(key='sk')
        en = request.POST.get(key='en')
        deleted = request.POST.get(key='deleted')
        if deleted == None:
            deleted = False
        item = MenuItem.objects.get(id=id)
        item.page = page
        item.sk = sk
        item.en = en
        item.deleted = deleted
        item.save()

    args = parse_args(args)
    id = args['id'];
    item = MenuItem.objects.get(id=id)
    template = get_template('menuedit.html')
    html = template.render(Context(locals()))
    return html

def menu_show(request,args):
    items = MenuItem.objects.all()
    template = get_template('menushow.html')
    html = template.render(Context(locals()))
    return html


def change_language(request):
    language = request.session.get('language', "sk")
    if language == "sk":
        request.session['language'] = "en"
    else:
        request.session['language'] = "sk"
    return HttpResponse("OK")

def page(request, id = 1, args=""):

        id=str(id)
        try:
            if id.isdigit():
                page_item = Page.objects.get(id=id,deleted=False)
            else:
                page_item = Page.objects.get(page=id,deleted=False)
        except ObjectDoesNotExist:
            return page(request, 0)
        id = page_item.id
        title = page_item.title
        content = page_item.content
        generator = page_item.generator
        date = page_item.date
        visible = page_item.visible
        language = request.session.get('language', 'sk')

        #generate page by generator
        if generator != "":
            try:
                html = eval(generator+"(request,args)")
            except AttributeError:
                html = Template(content).render(Context(locals()))
        else:
            html = Template(content).render(Context(locals()))


        #generate full page
        menu = MenuItem.objects.filter(deleted=False)
        template = get_template('index.html')

        html = template.render(Context(locals()))
        return HttpResponse(html)

def page_add(request,args):

    if request.POST:
        ppage = request.POST.get(key="page")
        title = request.POST.get(key="title")
        content = request.POST.get(key="content")
        generator = request.POST.get(key="generator")
        visible = request.POST.get(key="visible")

        #print title, content, generator, visible
        page = Page(page=ppage,title=title, content=content, generator=generator, visible=visible, deleted=False, date=datetime.datetime.now().date())
        page.save()

    template = get_template('page_edit.html')
    html = template.render(Context(locals()))
    return html

def page_edit(request,args):

    args = parse_args(args)
    if request.POST:
        id = request.POST.get(key="id")
        ppage = request.POST.get(key="page")
        title = request.POST.get(key="title")
        content = request.POST.get(key="content")
        generator = request.POST.get(key="generator")
        visible = request.POST.get(key="visible")
        deleted = request.POST.get(key="deleted")
        if visible == None:
            visible = False
        if deleted == None:
            deleted = False


        #print title, content, generator, visible
        page = Page.objects.get(id=id)
        page.page = ppage
        page.title = title
        page.content = content
        page.generator = generator
        page.visible = visible
        page.deleted = deleted
        page.save()

    page = Page.objects.get(id=args['id'])

    template = get_template('page_edit.html')

    html = template.render(Context(locals()))
    return html



