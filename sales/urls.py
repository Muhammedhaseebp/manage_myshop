from rest_framework.routers import DefaultRouter
from .views import SaleViewset


router = DefaultRouter()
router.register("sales",SaleViewset)
urlpatterns = router.urls

