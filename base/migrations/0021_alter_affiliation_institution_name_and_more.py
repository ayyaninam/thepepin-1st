# Generated by Django 5.0.3 on 2024-03-30 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_alter_affiliation_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliation',
            name='institution_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affiliation', to='base.institution'),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='affiliation',
            name='state',
            field=models.CharField(blank=True, choices=[('Current', 'Current'), ('Past', 'Past')], max_length=20, null=True),
        ),
    ]
