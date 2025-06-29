# Generated by Django 4.2.23 on 2025-06-15 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home_Page', '0004_alter_projectinfo_project'),
        ('Projet_Page', '0002_rename_code_codeinfo_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrialInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=10)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Trials', to='Home_Page.projectinfo')),
            ],
        ),
    ]
