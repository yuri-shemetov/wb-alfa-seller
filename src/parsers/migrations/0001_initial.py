# Generated by Django 4.2.4 on 2023-09-01 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                (
                    "name",
                    models.CharField(max_length=250, verbose_name="Название товара"),
                ),
                ("sku", models.IntegerField(db_index=True, verbose_name="SKU товара")),
                ("root", models.IntegerField(verbose_name="Id источника отзывов")),
                ("rating", models.FloatField(verbose_name="Текущий рейтинг")),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
        migrations.CreateModel(
            name="Feedback",
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
                (
                    "buyer_name",
                    models.CharField(max_length=50, verbose_name="Имя покупателя"),
                ),
                ("buyer_id", models.IntegerField(verbose_name="ID покупателя")),
                (
                    "source_id",
                    models.CharField(
                        db_index=True,
                        max_length=50,
                        verbose_name="Id отзыва на источнике",
                    ),
                ),
                ("text", models.TextField(verbose_name="Отзыв")),
                ("buyer_rating", models.IntegerField(verbose_name="Оценка покупателя")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания отзыва"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedbacks",
                        to="parsers.product",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
    ]
