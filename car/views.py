from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CarSerializer,ReservationSerializer
from .models import Car,Reservation
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import IsAdminOrReadOnly
from django.db.models import Q, OuterRef, Exists
# Create your views here.

# OuterRef = tablolar arasindaki iliksiyi kurar

class CarView(ModelViewSet):
    serializer_class=CarSerializer
    queryset=Car.objects.all()
    permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        
        if self.request.user.is_staff:
            queryset=super().get_queryset().filter()
        else:
            queryset=super().get_queryset().filter(availability=True)
      

        start=self.request.query_params.get('start')
        end=self.request.query_params.get('end')
        # if start is not None and end is not None:   
        if start and end:      
            #select id from reservation where end_date>start and start_date<end

            # not_available=Reservation.objects.filter(
            #     end_date__gt=start,start_date__lt=end
            #     ).values_list('id',flat=True) 

            #flat true id leri [1,3,7] listeye çeviriyor
            # queryset=self.queryset.exclude(id__in=not_available)

            # not_available=Reservation.objects.filter(
            #     Q(end_date__gt=start) & Q(start_date__lt=end)
            #     ).values_list('id',flat=True) 
            c1=Q(end_date__gt=start)
            c2=Q(start_date__lt=end)
            # not_available=Reservation.objects.filter(
            #     c1 & c2 
            #     ).values_list('id',flat=True) 

            # queryset=queryset.exclude(id__in=not_available)

            #! annotete yapisi
            queryset=queryset.annotate(
                is_available= ~Exists(Reservation.objects.filter(
                    Q(car=OuterRef('pk')) & c1 & c2
                    )
                )
            )

            return queryset
    

class ReservationView(ModelViewSet):
    serializer_class=ReservationSerializer
    queryset=Reservation.objects.all()
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)