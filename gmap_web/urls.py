from django.urls import include, re_path

import gmap_web.views as views

urlpatterns = [
    re_path(r'^admin$', views.home, name='home'),
    re_path(r'^admin/reload/$', views.rld, name='rld'),
    re_path(r'^', include(('maps.urls', 'display_map'), namespace="display_map")),
    # re_path(r'^accounts/login/$', 'django.contrib.auth.views.login'),
]
