# Generated by Django 4.2.23 on 2025-06-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projet_Page', '0009_alter_questionpaper_pdf_alter_questionpaper_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaper',
            name='pdf',
            field=models.FileField(upload_to='Question/'),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='uploaded',
            field=models.BooleanField(verbose_name=False),
        ),
    ]
