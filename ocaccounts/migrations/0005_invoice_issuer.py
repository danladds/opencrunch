# Generated by Django 2.0.9 on 2018-12-15 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocaccounts', '0004_auto_20181215_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='issuer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ocaccounts.Entity'),
            preserve_default=False,
        ),
    ]