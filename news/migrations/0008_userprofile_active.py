# Generated by Django 4.2.18 on 2025-01-26 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_rename_author_comment_commenter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
