# Generated by Django 5.0.3 on 2024-03-28 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_article_article_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articlestype', to='base.articletype'),
            preserve_default=False,
        ),
    ]
