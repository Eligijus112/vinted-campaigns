from vinted_backend.models import AdwordsAPI

from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd

class Command(BaseCommand):
    """
    A command to write adwords data to database
    """
    def handle(self, *args, **kwargs):
        # Truncating old data 
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE adwords_api")

        # Reading the data
        d = pd.read_csv('vinted_backend/input_data/AdwordsAPIData.csv')

        # Writing to database
        for _, row in d.iterrows():
            data = {
                'account': row['account'],
                'campaign_name': row['campaign_name'],
                'adgroup_name': row['adgroup_name'],
                'keyword': row['keyword'],
                'local_date': row['local_date'],
                'impressions': row['impressions'],
                'clicks': row['clicks'],
                'cost': row['cost'],
                'currency': row['currency'],
                'media_source': row['media_source'],
                'portal': row['portal']
            }
            
            AdwordsAPI.objects.create(**data)

