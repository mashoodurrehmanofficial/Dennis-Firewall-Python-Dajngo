# Generated by Django 4.0.1 on 2022-07-01 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_iptable_delete_categorytable_delete_weblistingtable'),
    ]

    operations = [
        migrations.AddField(
            model_name='iptable',
            name='waiting',
            field=models.BooleanField(default=False),
        ),
    ]
