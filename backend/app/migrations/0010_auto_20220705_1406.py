# Generated by Django 3.2.3 on 2022-07-05 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20220705_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustmentitems',
            name='adjustment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aditems', to='app.adjustment'),
        ),
        migrations.AlterField(
            model_name='adjustmentitems',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aditems', to='app.inventory'),
        ),
    ]
