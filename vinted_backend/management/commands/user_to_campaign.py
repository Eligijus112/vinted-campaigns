from vinted_backend.models import Users, UsersCampaign, AdwordsAPI, SmartlyAPI
from vinted_backend.utils import parse_date, check_if_nan

from django.core.management.base import BaseCommand
import pandas as pd
from tqdm import tqdm

class Command(BaseCommand):
    """
    A command to attribute a user to campaign
    """
    def handle(self, *args, **kwargs):
        # Iterating through the plans of adwords
        google_campaigns = AdwordsAPI.objects.values_list('campaign_name', flat=True).distinct()

        # Searching for users
        for campaign in google_campaigns:
            users = Users.objects.filter(registration_full_utm__contains=campaign).values_list('id', flat=True)    
            for user in users:
                UsersCampaign.objects.update_or_create(
                    user_id=user,
                    defaults={
                        'campaign_name': campaign,
                        'campaign_type': 'adwords'
                    }
                )    

        # Iterating through the plans of smartly
        fb_campaigns = SmartlyAPI.objects.values_list('campaign_name', flat=True).distinct()

        # Searching for users
        for campaign in fb_campaigns:
            users = Users.objects.filter(registration_full_utm__contains=campaign).values_list('id', flat=True)    
            for user in users:
                UsersCampaign.objects.update_or_create(
                    user_id=user,
                    defaults={
                        'campaign_name': campaign,
                        'campaign_type': 'smartly'
                        }
                )         