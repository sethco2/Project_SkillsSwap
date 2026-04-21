"""
URL patterns for the Skills app.

Mounted under /skills/ by the project router. So path('', ...) here means
"/skills/", and path('new/', ...) means "/skills/new/".

The `name=` argument lets us refer to URLs symbolically in templates and
views — e.g. {% url 'skill_detail' skill.pk %} — instead of hardcoding
strings, which break the moment the URL pattern changes.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public browsing
    path('',                 views.skill_list,    name='skill_list'),

    # User dashboard ("my skills"). Defined BEFORE the <int:pk> route so
    # that "/skills/dashboard/" doesn't accidentally try to match pk='dashboard'.
    path('dashboard/',       views.dashboard,     name='dashboard'),

    # Create — also kept above the <int:pk> route to avoid the same conflict.
    path('new/',             views.skill_create,  name='skill_create'),

    # Detail / update / delete all keyed by primary key.
    path('<int:pk>/',        views.skill_detail,  name='skill_detail'),
    path('<int:pk>/edit/',   views.skill_update,  name='skill_update'),
    path('<int:pk>/delete/', views.skill_delete,  name='skill_delete'),
]
