from django.conf.urls import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	(r'^accounts/', include('registration.urls')),
    url(r'^$', 'evmev.ilan.views.home', name='home'),
    url(r'^hakkinda', 'evmev.ilan.views.hakkinda', name='hakkinda'),
	url(r'^iletisim', 'evmev.ilan.views.iletisim', name='iletisim'),
    url(r'^ilan/ekle', 'evmev.ilan.views.ekle', name='ilan'),
	url(r'^ilan/kaydet', 'evmev.ilan.views.kaydet', name='kaydet'),
	url(r'^ilan/upload', 'evmev.ilan.views.upload', name='upload'),

	url(r'^ilan/ara', 'evmev.ilan.views.ara', name='ara'),
	url(r'^ilan/getir', 'evmev.ilan.views.getir', name='getir'),
	url(r'^ilan/goster/(?P<ilan_id>.*)$', 'evmev.ilan.views.goster', name='goster'),

	url(r'', include('social_auth.urls')),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT}),
    # url(r'^evmev/', include('evmev.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
