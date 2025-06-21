from django.urls import path, re_path

from maps import views

app_name="maps"

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^description$', views.description, name='description'),
    re_path(r'^datasets$', views.datasets, name='datasets'),
    re_path(r'^about$', views.about, name='about'),
    re_path(r'^recent$', views.recent, name='recent'),
    path('map/<int:task_id>/', views.display_map, name='display_map'),
    re_path(r'^map/(\d*)/(\w*)$', views.display_map, name='display_map'),
    re_path(r'^get_map/(\d*)/$', views.get_map, name='get_map'),
    re_path(r'^get_map_zoomed/(\d*)$', views.get_map_zoomed, name='get_map_zoomed'),
    re_path(r'^get_task_metadata/(\d*)/$', views.get_task_metadata, name='get_task_metadata'),
    re_path(r'^get_json/(\d*)/$', views.get_json, name='get_json'),
    # re_path(r'^get_adjacency_matrix/(\d*)/$', views.get_adjacency_matrix, name='get_adjacency_matrix'),
    # re_path(r'^get_mds$', views.get_mds, name='get_mds'),
    re_path(r'^request_map/$', views.request_map, name='request_map')
    # re_path(r'^test$', views.test, name='test')
]
