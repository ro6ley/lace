from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TemplateCreateView, TemplateDetailsView

urlpatterns = {
    path('templates/', TemplateCreateView.as_view(), name="templates"),
    path('templates/<int:pk>/', TemplateDetailsView.as_view(), name="template_detail")
}

urlpatterns = format_suffix_patterns(urlpatterns)
