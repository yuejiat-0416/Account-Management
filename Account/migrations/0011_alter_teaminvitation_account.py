# Generated by Django 4.2.3 on 2023-08-10 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0010_remove_teaminvitation_account_tea_role_id_74c378_idx'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teaminvitation',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Account.account'),
        ),
    ]
