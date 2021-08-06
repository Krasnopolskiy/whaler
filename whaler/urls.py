from main.views import IndexView, ReportsView
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('reports/', ReportsView.as_view(), name='reports'),
]
