from rest_framework.routers import DefaultRouter
from .views import RechargeViewSet

router = DefaultRouter()
router.register("recharge",RechargeViewSet)
urlpatterns = router.urls

