# Generated by Django 5.0 on 2024-11-20 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Solicitud",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rut", models.CharField(max_length=12)),
                ("nombre", models.CharField(max_length=100)),
                ("apellido", models.CharField(max_length=100)),
                ("direccion", models.CharField(max_length=200)),
                ("telefono", models.CharField(max_length=12)),
                ("comuna", models.CharField(max_length=30)),
                ("fecha_solicitud", models.DateTimeField(auto_now_add=True)),
                ("fecha_aceptacion", models.DateTimeField(blank=True, null=True)),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("pendiente", "Pendiente"),
                            ("aceptada", "Aceptada"),
                            ("rechazada", "Rechazada"),
                            ("expirada", "Expirada"),
                        ],
                        default="pendiente",
                        max_length=10,
                    ),
                ),
            ],
        ),
    ]
