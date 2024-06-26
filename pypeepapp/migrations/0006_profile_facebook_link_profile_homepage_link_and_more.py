# Generated by Django 5.0.3 on 2024-04-04 21:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pypeepapp", "0005_peep_likes"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="facebook_link",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="homepage_link",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="instagram_link",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="linkedin_link",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="profile_bio",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
