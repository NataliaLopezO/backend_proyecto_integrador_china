# Generated by Django 4.2 on 2023-06-21 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("finding_china", "0003_customuser_progreso_historia"),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
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
                ("pregunta", models.CharField(max_length=200)),
                ("categoria", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name="customuser",
            name="progreso_contribuciones",
            field=models.JSONField(
                default={
                    "acupuntura": 0,
                    "brujula": 0,
                    "datos_contribuciones": 0,
                    "imprenta": 0,
                    "papel": 0,
                    "polvora": 0,
                }
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="progreso_cultura",
            field=models.JSONField(
                default={
                    "artesanias": 0,
                    "creencias": 0,
                    "datos_cultura": 0,
                    "festividades": 0,
                    "tradiciones": 0,
                    "vestimenta": 0,
                }
            ),
        ),
        migrations.CreateModel(
            name="Option",
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
                ("es_respuesta_correcta", models.BooleanField(default=False)),
                ("texto_opcion", models.CharField(max_length=200)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finding_china.question",
                    ),
                ),
            ],
        ),
    ]
