# Generated by Django 5.0.3 on 2024-03-30 05:40

import any_urlfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='received_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook_link',
            field=any_urlfield.models.fields.AnyUrlField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram_link',
            field=any_urlfield.models.fields.AnyUrlField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin_link',
            field=any_urlfield.models.fields.AnyUrlField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter_link',
            field=any_urlfield.models.fields.AnyUrlField(blank=True, max_length=300),
        ),
    ]
