from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet

router = DefaultRouter()
router.register(r'hoteis', HotelViewSet, basename='hotel')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]
