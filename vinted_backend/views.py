from rest_framework import generics
from django.db.models import Count

from vinted_backend.serializers import UsersGenderSerializer, SmartlySerializer
from vinted_backend.serializers import UsersAgeSerializer, UsersDeviceSerializer
from vinted_backend.serializers import UsersRegistrationSerializer

from vinted_backend.models import Users, SmartlyAPI

from datetime import datetime
from collections import Counter 


class UserGenderView(generics.ListAPIView):

    serializer_class = UsersGenderSerializer
    def get_queryset(self):
        genders = Users.objects.filter(gender__in=['M', 'F']).values('gender')
        
        M = [x for x in genders if x.get('gender')=='M'] 
        F = [x for x in genders if x.get('gender')=='F'] 
        
        distribution = (('M', len(M)), ('F', len(F)))

        return distribution


class UserAgeView(generics.ListAPIView):

    serializer_class = UsersAgeSerializer
    def get_queryset(self):
        ages = Users.objects.filter(gender__in=['M', 'F']).values('gender', 'age_at_registration')
        ages = [x for x in ages if x.get('age_at_registration')]

        all_genders = [x.get('age_at_registration') for x in ages]
        M = [x.get('age_at_registration') for x in ages if x.get('gender')=="M"]
        F = [x.get('age_at_registration') for x in ages if x.get('gender')=="F"] 
        
        ages = (('all', all_genders), ('M', M), ('F', F))

        return ages

class UserDeviceView(generics.ListAPIView):

    serializer_class = UsersDeviceSerializer
    def get_queryset(self):
        return Users.objects.all().values('registration_platform').annotate(total=Count('registration_platform'))      


class UserRegistrationView(generics.ListAPIView):

    serializer_class = UsersRegistrationSerializer
    def get_queryset(self):
        time_frames = Users.objects.exclude(registration_local_time__isnull=True).values_list('registration_local_time', flat=True)

        # Extracting days of week and hours per day
        weekdays = []
        hours = []
        for time in time_frames:
            weekdays.append(time.weekday())
            hours.append(time.hour)

        weekdays = list(zip([x + 1 for x in Counter(weekdays).keys()], Counter(weekdays).values()))
        hours = list(zip([x + 1 for x in Counter(hours).keys()], Counter(hours).values()))

        return (('weekdays', weekdays), ('hours', hours))  


class SmartlyView(generics.ListAPIView):

     serializer_class = SmartlySerializer
     queryset = SmartlyAPI.objects.all()
