from django.urls import path,include
from rest_framework import routers
from .views import CarView,ReservationView

router=routers.DefaultRouter()
router.register("cars",CarView)
router.register("resv",ReservationView)

urlpatterns = [
    path('', include(router.urls)),

]