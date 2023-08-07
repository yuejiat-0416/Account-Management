# Generated by Django 4.2.3 on 2023-08-05 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('company_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('account_status', models.CharField(choices=[('active', 'Active'), ('expired', 'Expired'), ('fraud', 'Fraud')], max_length=255)),
                ('company_summary', models.TextField(blank=True, null=True)),
                ('company_industry', models.CharField(blank=True, max_length=255, null=True)),
                ('company_size_range', models.CharField(blank=True, choices=[('1-50', '1-50'), ('51-200', '51-200'), ('201-500', '201-500'), ('501-1000', '501-1000'), ('1001+', '1001+')], max_length=255, null=True)),
                ('company_website', models.URLField(blank=True, max_length=255, null=True)),
                ('company_location', models.CharField(blank=True, max_length=255, null=True)),
                ('company_domain', models.CharField(max_length=255, unique=True)),
                ('logo_url', models.URLField(blank=True, max_length=255, null=True)),
                ('company_linkedin', models.URLField(blank=True, max_length=255, null=True)),
                ('company_facebook', models.URLField(blank=True, max_length=255, null=True)),
                ('company_twitter', models.URLField(blank=True, max_length=255, null=True)),
                ('company_video_url', models.URLField(blank=True, max_length=255, null=True)),
                ('viewed_employer_welcome', models.TextField(blank=True, null=True)),
                ('viewed_employer_tutorial', models.TextField(blank=True, null=True)),
                ('stripe_customer_id', models.CharField(max_length=255, unique=True)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('trial_starts_at', models.DateTimeField()),
                ('trial_end_at', models.DateTimeField()),
                ('is_free_trial', models.BooleanField(default=True)),
                ('payg_credit', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=255, unique=True)),
                ('role_type', models.CharField(choices=[('admin', 'Admin'), ('hiring_manager', 'Hiring_Manager'), ('recruiter', 'Recruiter'), ('coordinator', 'Coordinator'), ('sourcer', 'Sourcer'), ('external_reviewer', 'External_Reviewer'), ('sub_reviewer', 'Sub_Reviewer')], max_length=255)),
                ('role_description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invited_email', models.EmailField(max_length=254)),
                ('is_accepted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.account')),
                ('invited_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_invitations', to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_invitations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='role',
            index=models.Index(fields=['role_type'], name='Account_rol_role_ty_4ef254_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['company_name'], name='Account_acc_company_856c6a_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['account_status'], name='Account_acc_account_7614f8_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['company_industry'], name='Account_acc_company_60d1ab_idx'),
        ),
        migrations.AddIndex(
            model_name='account',
            index=models.Index(fields=['company_domain'], name='Account_acc_company_9ced45_idx'),
        ),
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['user'], name='Account_tea_user_id_358661_idx'),
        ),
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['account'], name='Account_tea_account_459e53_idx'),
        ),
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['invited_email'], name='Account_tea_invited_fedefd_idx'),
        ),
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['is_accepted'], name='Account_tea_is_acce_941aa5_idx'),
        ),
        migrations.AddIndex(
            model_name='teaminvitation',
            index=models.Index(fields=['role'], name='Account_tea_role_id_74c378_idx'),
        ),
    ]