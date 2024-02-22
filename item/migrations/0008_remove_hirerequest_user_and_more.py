# Generated by Django 4.2.5 on 2024-02-11 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_hirerequest_pdf_idcopy_hirerequest_pdf_other_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hirerequest',
            name='user',
        ),
        migrations.AlterField(
            model_name='hirerequest',
            name='contact_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='hirerequest',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hirerequest',
            name='postal_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='hirerequest',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]