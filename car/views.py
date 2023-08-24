from django.shortcuts import render
from .models import *
from .serializers import CarSerializer,ReservationSerializer
from rest_framework import viewsets
# from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import IsAdminOrReadOnly
from datetime import datetime,date

# Create your views here.
class CarView(viewsets.ModelViewSet):
    queryset=Car.objects.all()
    serializer_class=CarSerializer
    # permission_classes= [IsAdminUser]  
    permission_classes= [IsAdminOrReadOnly]  

    # şu andan onceki uçuşları getirme
    # def get_queryset(self):
    #     queryset = super().get_queryset()

        # now = datetime.now()
        # current_time = now.strftime('%H:%M:%S')
        # today = date.today()
        
        # if self.request.user.is_staff: 
        #     return queryset
        # else:
        #     # print(now) 
        #     # now o anki tarih ve zamanı alıyor
        #     queryset = Reservation.objects.filter(start_date=now)
                
        #     return queryset

class ReservationView(viewsets.ModelViewSet):

    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer
    # permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

# from django.shortcuts import render

# def home_page(request):
#     return render(request, 'home.html')  # 'home.html' adlı bir template dosyasını kullanarak sayfayı oluşturuyoruz
