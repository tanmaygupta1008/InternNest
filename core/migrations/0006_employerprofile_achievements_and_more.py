# Generated by Django 5.1.1 on 2025-02-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_applicationcounter_job_jobapplication_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employerprofile',
            name='achievements',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='company_size',
            field=models.CharField(blank=True, choices=[('1-50', '1-50 employees'), ('51-200', '51-200 employees'), ('201-1000', '201-1000 employees'), ('1000+', '1000+ employees')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='employerprofile',
            name='social_links',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
