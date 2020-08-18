from django.contrib import admin
from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('neo4j/', views.neo4j),
    path('statistics/', views.statistics),
    # path('map/', views.map),
    path('human_feature/', views.human_feature),
    path('human_edit/', views.human_edit),
    path('gait_detail/', views.gait_detail),
    path('get_welcome_data/', views.get_welcome_data),
    path('update_health/', views.update_health),
    path('healthy_table', views.healthy_table),
    path('confirmed_table', views.confirmed_table),
    path('suspected_table', views.suspected_table),
    path('get_healthy_data',views.get_healthy_data),
    path('get_suspected_data',views.get_suspected_data),
    path('get_confirmed_data',views.get_confirmed_data),
]