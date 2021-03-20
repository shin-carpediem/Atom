from rest_framework import routers
from .views import UserViewSet, HouseViewSet, HouseChoreViewSet


# Create your tests here.
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'house', HouseViewSet)
router.register(r'housechore', HouseChoreViewSet)
