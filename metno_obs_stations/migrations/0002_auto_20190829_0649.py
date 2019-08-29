# Generated by Django 2.2.4 on 2019-08-29 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20190626_1313'),
        ('metno_obs_stations', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StandardMeteorologicalBuoy',
        ),
        migrations.CreateModel(
            name='MetObsStation',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('catalog.dataset',),
        ),
    ]
