from main.views import IndexView, ReportAcceptView, ReportDeclineView, ReportListView, ReportView
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('report/', ReportView.as_view(), name='report'),
    path('report/list', ReportListView.as_view(), name='report_list'),
    path('report/accept/<int:pk>', ReportAcceptView.as_view(), name='report_accept'),
    path('report/decline/<int:pk>', ReportDeclineView.as_view(), name='report_decline'),
]
