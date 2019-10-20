# Generated by Django 2.2.3 on 2019-10-19 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinted_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinted_backend.Users')),
            ],
            options={
                'db_table': 'users_to_campaign',
            },
        ),
    ]