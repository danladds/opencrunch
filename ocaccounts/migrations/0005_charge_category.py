# Generated by Django 2.0.9 on 2018-12-17 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocaccounts', '0004_auto_20181217_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='Category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='ocaccounts.Category'),
            preserve_default=False,
        ),
    ]
