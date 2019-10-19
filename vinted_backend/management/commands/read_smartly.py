from vinted_backend.models import SmartlyAPI

from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd


class Command(BaseCommand):
    """
    A command to write smartly data to database
    """
    def handle(self, *args, **kwargs):
        # Truncating old data 
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE smartly_api")

        # Reading the data
        d = pd.read_csv('vinted_backend/input_data/SmartlyAPIData.csv')

        # Writing to database
        for _, row in d.iterrows():
            data = {
                'account_name': row['account_name'],
                'campaign_name': row['campaign_name'],
                'adgroup_name': row['adgroup_name'],
                'name': row['name'],
                'fb_objective': row['fb_objective'],
                'local_date': row['local_date'],
                'campaign_start_date': row['campaign_start_date'],
                'impressions': row['impressions'],
                'clicks': row['clicks'],
                'cost': row['cost'],
                'currency': row['currency'],
                'portal': row['portal']
            }
            
            SmartlyAPI.objects.create(**data)