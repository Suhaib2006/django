# Generated by Django 4.2.23 on 2025-06-17 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projet_Page', '0005_alter_datainfo_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='trialinfo',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
