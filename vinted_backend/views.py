from rest_framework import generics
from django.db.models import Count
from django.db import connection

from vinted_backend.serializers import UsersGenderSerializer, SmartlySerializer
from vinted_backend.serializers import UsersAgeSerializer, UsersDeviceSerializer
from vinted_backend.serializers import UsersRegistrationSerializer

from vinted_backend.models import Users, SmartlyAPI, AdwordsAPI, UsersCampaign

from datetime import datetime
from collections import Counter 
import numpy as np
import pandas as pd


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
        
        ages = (
            ('all', np.histogram(all_genders, 30)),
            ('M', np.histogram(M, 30)), 
            ('F',  np.histogram(F, 30))
            )

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


class SmartlyAggView(generics.ListAPIView):

     serializer_class = SmartlySerializer
     def get_queryset(self):
        stats = SmartlyAPI.objects.filter(fb_objective__in=['APP_INSTALLS']).values('impressions', 'clicks', 'cost')

        # Extracting statistics
        impressions = np.sum([x.get('impressions') for x in stats])
        clicks = np.sum([x.get('clicks') for x in stats])
        cost = np.sum([x.get('cost') for x in stats])
        ctr = round(clicks * 100 / impressions, 3)
        cpc = round(clicks / cost, 3)

        return (
            ('impressions', impressions), 
            ('clicks', clicks),
            ('cost', cost),
            ('ctr', ctr),
            ('cpc', cpc)
            )


class SmartlyGranularView(generics.ListAPIView):

     serializer_class = SmartlySerializer
     def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select campaign_name, sum(impressions) impressions, sum(clicks) clicks, sum(cost) total_cost
            from smartly_api 
            group by campaign_name;
            """,
            connection
        )

        stats['ctr'] = stats['clicks'] * 100/stats['impressions']
        stats['cpc'] = stats['clicks']/stats['total_cost']

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('campaign_name', row['campaign_name']),
                    ('impressions', row['impressions'],),
                    ('clicks', row['clicks']),
                    ('cost', row['total_cost']),
                    ('ctr', round(row['ctr'], 3)),
                    ('cpc', round(row['cpc'], 3))
                ]
            )

        return list_stats


class AdWordsAggView(generics.ListAPIView):

    serializer_class = SmartlySerializer
    def get_queryset(self):
        stats = AdwordsAPI.objects.values('impressions', 'clicks', 'cost')

        impressions = np.sum([x.get('impressions') for x in stats])
        clicks = np.sum([x.get('clicks') for x in stats])
        cost = np.sum([x.get('cost') for x in stats])
        ctr = round(clicks * 100 / impressions, 3)
        cpc = round(clicks / cost, 3)

        return (
            ('impressions', impressions), 
            ('clicks', clicks),
            ('cost', cost),
            ('ctr', ctr),
            ('cpc', cpc)
            )

class AdWordsGranularView(generics.ListAPIView):

     serializer_class = SmartlySerializer
     def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select campaign_name, sum(impressions) impressions, sum(clicks) clicks, sum(cost) total_cost
            from adwords_api
            where cost > 0
            group by campaign_name
            """,
            connection
        )

        stats['ctr'] = stats['clicks'] * 100/stats['impressions']
        stats['cpc'] = stats['clicks']/stats['total_cost']

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('campaign_name', row['campaign_name']),
                    ('impressions', row['impressions'],),
                    ('clicks', row['clicks']),
                    ('cost', row['total_cost']),
                    ('ctr', round(row['ctr'], 3)),
                    ('cpc', round(row['cpc'], 3))
                ]
            )

        return list_stats            


class InstallationTotal(generics.ListAPIView):
    serializer_class = SmartlySerializer

    def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select campaign_type, count(*) 
            from users_to_campaign 
            group by campaign_type;
            """, connection
        )

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('campaign_name', row['campaign_type']),
                    ('no_installs', row['count'],)
                ]
            )

        return list_stats

class InstallationCampaign(generics.ListAPIView):
    serializer_class = SmartlySerializer

    def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select campaign_type, campaign_name, count(*) 
            from users_to_campaign 
            group by campaign_type, campaign_name
            order by campaign_type, count desc;
            """, connection
        )

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('campaign_name', row['campaign_name']),
                    ('campaign_type', row['campaign_type']),
                    ('no_installs', row['count'],)
                ]
            )

        return list_stats    


class UserBehaviour(generics.ListAPIView):
    serializer_class = SmartlySerializer

    def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select campaign_type, campaign_name, 
            sum(first_listing_local_time) users_list, 
            sum(first_sale_local_time) users_sale, 
            sum(first_purchase_local_time) users_purchase,
            count(*) total_installs
            from
            (select campaign_name, campaign_type,
            CASE 
                when first_listing_local_time is null then 0
                else 1
            end AS first_listing_local_time,
            CASE 
                when first_sale_local_time is null then 0
                else 1
            end AS first_sale_local_time,
            CASE 
                when first_purchase_local_time is null then 0
                else 1
            end AS first_purchase_local_time
            from 
                (select *
                from users_to_campaign) campaigns
            left join 
                (select id user_id, first_listing_local_time, first_sale_local_time, first_purchase_local_time
                from users) users
            using(user_id)) events
            group by campaign_type, campaign_name;
            """, connection
        )

        stats['share_users_list'] = round(stats['users_list'] * 100 / stats['total_installs'], 3)
        stats['share_users_sale'] = round(stats['users_sale'] * 100 / stats['total_installs'], 3)
        stats['share_users_purchase'] = round(stats['users_purchase'] * 100 / stats['total_installs'], 3)

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('campaign_name', row['campaign_name']),
                    ('campaign_type', row['campaign_type']),
                    ('no_users_list', row['users_list'],),
                    ('no_users_sale', row['users_sale']),
                    ('no_users_purchase', row['users_purchase']),
                    ('share_users_list', row['share_users_list']),
                    ('share_users_sale', row['share_users_sale']),
                    ('share_users_purchase', row['share_users_purchase']),
                    ('total_installs', row['total_installs']),
                ]
            )

        return list_stats               


class UserAgeBehaviour(generics.ListAPIView):
    serializer_class = SmartlySerializer

    def get_queryset(self):
        stats = pd.read_sql_query(
            """
            select age_at_registration,
            sum(first_listing_local_time) users_list, 
            sum(first_sale_local_time) users_sale, 
            sum(first_purchase_local_time) users_purchase,
            count(*) total_installs
            from
            (select age_at_registration,
             CASE 
             when first_listing_local_time is null then 0
             else 1
             end AS first_listing_local_time,
             CASE 
             when first_sale_local_time is null then 0
             else 1
             end AS first_sale_local_time,
             CASE 
             when first_purchase_local_time is null then 0
             else 1
             end AS first_purchase_local_time
             from users 
            where age_at_registration is not null and age_at_registration <= 60) user_data
            group by age_at_registration
            order by age_at_registration desc;
            """, connection
        )

        stats['share_users_list'] = round(stats['users_list'] * 100 / stats['total_installs'], 3)
        stats['share_users_sale'] = round(stats['users_sale'] * 100 / stats['total_installs'], 3)
        stats['share_users_purchase'] = round(stats['users_purchase'] * 100 / stats['total_installs'], 3)

        list_stats = []
        for _, row in stats.iterrows():
            list_stats.append(
                [
                    ('age_at_registration', row['age_at_registration']),
                    ('no_users_list', row['users_list'],),
                    ('no_users_sale', row['users_sale']),
                    ('no_users_purchase', row['users_purchase']),
                    ('share_users_list', row['share_users_list']),
                    ('share_users_sale', row['share_users_sale']),
                    ('share_users_purchase', row['share_users_purchase']),
                    ('total_installs', row['total_installs']),
                ]
            )

        return list_stats               