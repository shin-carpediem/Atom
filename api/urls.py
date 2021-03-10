from rest_framework import routers
from .views import UserViewSet


# Create your tests here.
router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
