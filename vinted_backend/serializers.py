from rest_framework import serializers
from vinted_backend.models import Users, SmartlyAPI
from django.db.models import Count


class UsersGenderSerializer(serializers.ModelSerializer):

    gender_count = serializers.SerializerMethodField()

    def get_gender_count(self, obj):
        return {
            'gender': obj[0],
            'count': obj[1]
            }

    class Meta:
        model = Users
        fields = ('gender_count', )


class UsersAgeSerializer(serializers.ModelSerializer):

    age_count = serializers.SerializerMethodField()
    
    def get_age_count(self, obj):
        return {
            'gender': obj[0],
            'ages': obj[1]
            }

    class Meta:
        model = Users
        fields = ('age_count', )    


class UsersDeviceSerializer(serializers.ModelSerializer):

    device_count = serializers.SerializerMethodField()
    
    def get_device_count(self, obj):
        return {
            'device': obj.get('registration_platform'),
            'count': obj.get('total')
            }

    class Meta:
        model = Users
        fields = ('device_count', )  

class UsersRegistrationSerializer(serializers.ModelSerializer):

    registration_count = serializers.SerializerMethodField()
    
    def get_registration_count(self, obj):
        return {
            'type': obj[0],
            'counts': obj[1]
            }

    class Meta:
        model = Users
        fields = ('registration_count', )                       


class SmartlySerializer(serializers.ModelSerializer):
    
    agg_stats = serializers.SerializerMethodField()
    def get_agg_stats(self, obj):
        return obj 

    class Meta:
        model = SmartlyAPI
        fields = ('agg_stats', ) 

        


