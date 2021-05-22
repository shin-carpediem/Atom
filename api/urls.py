from rest_framework import routers
from .views import HouseViewSet, UserViewSet, InquireViewSet, RequestChHouseViewSet, RequestHouseOwnerViewSet, HouseChoreViewSet


# Create your tests here.
router = routers.DefaultRouter()
router.register(r'house', HouseViewSet)
router.register(r'user', UserViewSet)
router.register(r'inquire', InquireViewSet)
router.register(r'request_ch_house', RequestChHouseViewSet)
router.register(r'request_house_owner', RequestHouseOwnerViewSet)
router.register(r'housechore', HouseChoreViewSet)
