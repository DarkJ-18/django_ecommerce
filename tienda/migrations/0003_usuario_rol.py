# Generated by Django 5.1.1 on 2025-03-24 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='rol',
            field=models.IntegerField(choices=[(1, 'Administrador')], default=1),
        ),
    ]
