from django.db import models
from django.db.models.aggregates import Count
from random import randint


class AdwordsAPI(models.Model):
    """
    A class to store adwords API data
    """  
    account = models.TextField(null=True, blank=True)
    campaign_name = models.TextField(null=True, blank=True)
    adgroup_name = models.TextField(null=True, blank=True)
    keyword = models.TextField(null=True, blank=True)
    local_date = models.DateField()
    impressions = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    media_source = models.TextField(null=True, blank=True)
    portal = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "adwords_api"


class SmartlyAPI(models.Model):
    account_name = models.TextField(null=True, blank=True)
    campaign_name = models.TextField(null=True, blank=True)
    adgroup_name = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    fb_objective = models.TextField(null=True, blank=True)
    local_date = models.DateField()
    campaign_start_date = models.DateTimeField()
    impressions = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    currency = models.TextField(null=True, blank=True)
    portal = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "smartly_api"


class Users(models.Model):

    portal = models.TextField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True, db_index=True) 
    language = models.TextField(null=True, blank=True)
    gender = models.TextField(null=True, blank=True) 
    age_at_registration = models.IntegerField(null=True, blank=True)
    registration_platform = models.TextField(null=True, blank=True)
    registration_local_time = models.DateTimeField(null=True, blank=True)
    first_visit_local_time = models.DateTimeField(null=True, blank=True) 
    first_listing_local_time = models.DateTimeField(null=True, blank=True)
    first_sale_local_time = models.DateTimeField(null=True, blank=True)
    first_purchase_local_time = models.DateTimeField(null=True, blank=True)
    registration_full_utm = models.TextField(null=True, blank=True) 
    first_visit_full_utm = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "users"


class UsersCampaign(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE) 
    campaign_name = models.TextField(null=True, blank=True)
    campaign_type = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "users_to_campaign"
   