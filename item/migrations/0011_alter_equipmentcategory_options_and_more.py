# Generated by Django 4.2.5 on 2024-02-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_hirerequest_total_cost_hirerequest_total_days_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipmentcategory',
            options={'ordering': ('name',), 'verbose_name_plural': 'Equipment Categories'},
        ),
        migrations.AlterField(
            model_name='equipmentcategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
