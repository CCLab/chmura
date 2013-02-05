from django.conf.urls.defaults import *

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^api/words/(?P<speech_id>\d+)/$', 'chmura.word.views.api_count'),
    (r'^word/(?P<object_id>\d+)/$', 'chmura.word.views.word'),    
    (r'^word/cache/$', 'chmura.word.views.cache'),
    (r'^word/context/(?P<speech_id>\d+)/(?P<lemma_id>\d+)/?$', 'chmura.word.views.context'),
    
    (r'^year/(?P<object_id>\d+)/(?P<width>\d)/$', 'chmura.word.views.year'),    

    # Example:
    (r'^speech/', include('chmura.speech.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )
                