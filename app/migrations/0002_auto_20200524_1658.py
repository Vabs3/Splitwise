# Generated by Django 3.0.6 on 2020-05-24 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bill',
            old_name='totalAmount',
            new_name='total_amount',
        ),
        migrations.AddField(
            model_name='bill',
            name='payee',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='app.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userbill',
            name='amount',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
    ]