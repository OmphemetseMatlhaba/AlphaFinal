# Generated by Django 4.2.5 on 2024-02-07 22:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('emergency', '0002_alter_soscall_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='DesignatedContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_information', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.RenameField(
            model_name='soscall',
            old_name='additional_info',
            new_name='additional_details',
        ),
        migrations.RemoveField(
            model_name='soscall',
            name='user',
        ),
        migrations.AddField(
            model_name='soscall',
            name='emergency_type',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='soscall',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='soscall',
            name='user_contact',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='soscall',
            name='user_name',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
    ]
