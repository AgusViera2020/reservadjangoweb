# Generated by Django 4.2.10 on 2024-04-05 20:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservadjango', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='imagen',
            field=models.ImageField(blank=True, default='', upload_to='media/servicios/'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='contacto',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='precio',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('direccion', models.CharField(blank=True, default='', max_length=100)),
                ('telefono', models.CharField(blank=True, default='', max_length=15)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
                ('status', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservadjango.servicio')),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='reservadjango.categoria'),
        ),
    ]