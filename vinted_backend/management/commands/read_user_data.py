from vinted_backend.models import Users
from vinted_backend.utils import parse_date, check_if_nan

from django.core.management.base import BaseCommand
import pandas as pd
from tqdm import tqdm

class Command(BaseCommand):
    """
    A command to write adwords data to database
    """
    def handle(self, *args, **kwargs):
        # Reading the data
        d = pd.read_csv('vinted_backend/input_data/UsersData.txt')

        # Writing to database
        for _, row in tqdm(d.iterrows()):

            data = {
                'portal': row['portal'],
                'language': row['language'],
                'gender': check_if_nan(row['gender']),
                'age_at_registration': check_if_nan(row['age_at_registration']),
                'registration_platform': row['registration_platform'],
                'registration_local_time': parse_date(row['registration_local_time']),
                'first_visit_local_time': parse_date(row['first_visit_local_time']),
                'first_listing_local_time': parse_date(row['first_listing_local_time']),
                'first_sale_local_time': parse_date(row['first_sale_local_time']),
                'first_purchase_local_time': parse_date(row['first_purchase_local_time']),
                'registration_full_utm': row['registration_full_utm'],
                'first_visit_full_utm': row['first_visit_full_utm']
            }

            Users.objects.update_or_create(
                user_id = row['user_id'],
                defaults=data
            )
