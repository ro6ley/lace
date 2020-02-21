from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import TemplateViewSet

router = SimpleRouter()
router.register('templates', TemplateViewSet, basename="templates")  # try basename instead of base_name

urlpatterns = router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
