# Generated by Django 4.2.10 on 2024-04-29 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='ciudad',
            new_name='shipping_ciudad',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='direccion',
            new_name='shipping_direccion',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='email',
            new_name='shipping_email',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='full_name',
            new_name='shipping_nombre',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='pais',
            new_name='shipping_pais',
        ),
    ]