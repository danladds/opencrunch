# Generated by Django 2.0.9 on 2018-12-15 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocaccounts', '0005_invoice_issuer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='payee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='charges', to='ocaccounts.Entity'),
        ),
    ]