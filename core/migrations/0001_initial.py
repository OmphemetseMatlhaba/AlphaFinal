# Generated by Django 4.2.5 on 2024-02-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CropPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nitrogen', models.FloatField()),
                ('phosphorus', models.FloatField()),
                ('potassium', models.FloatField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('pH', models.FloatField()),
                ('rainfall', models.FloatField()),
                ('predicted_crop', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
