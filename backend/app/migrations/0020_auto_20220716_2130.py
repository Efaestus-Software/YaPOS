# Generated by Django 3.2.3 on 2022-07-16 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_salesitems_unitcost'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='seniorID',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]