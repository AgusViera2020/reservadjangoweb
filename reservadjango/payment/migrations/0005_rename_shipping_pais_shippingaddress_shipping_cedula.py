# Generated by Django 4.2.10 on 2024-05-04 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='shipping_pais',
            new_name='shipping_cedula',
        ),
    ]
