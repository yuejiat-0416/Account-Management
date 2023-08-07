# Generated by Django 4.2.3 on 2023-08-05 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='company_domain',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='stripe_customer_id',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='trial_end_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='trial_starts_at',
            field=models.DateTimeField(null=True),
        ),
    ]