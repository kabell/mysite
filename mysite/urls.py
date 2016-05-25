from django.conf.urls import patterns, include, url
from mysite.index import page, change_language

urlpatterns = patterns('',
    url(r'^change_language',change_language),
	url(r'^$', page),
    url(r'^page=(\w+)$',page),
    url(r'^page=(\w+)&(.+)',page),
    #url(r'^(\w+)$', index),

)