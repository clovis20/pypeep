# Generated by Django 5.0.3 on 2024-04-03 23:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pypeepapp", "0003_peep"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="profile_img",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]