# Generated by Django 4.2.23 on 2025-06-14 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Projet_Page', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codeinfo',
            old_name='Code',
            new_name='code',
        ),
    ]
