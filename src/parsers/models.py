from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="Название товара", max_length=250)
    sku = models.IntegerField(db_index=True, verbose_name="SKU товара")
    root = models.IntegerField(verbose_name="Id источника отзывов")
    rating = models.FloatField(verbose_name="Текущий рейтинг")

    # @property
    # def rating(self):
    #     feedbacks = self.feedbacks.all()
    #     total_summ = 0
    #     for feedback in feedbacks:
    #         total_summ += feedback.buyer_rating
    #     return round(total_summ/len(feedbacks), 1)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Feedback(models.Model):
    buyer_name = models.CharField(verbose_name="Имя покупателя", max_length=50)
    buyer_id = models.IntegerField(verbose_name="ID покупателя")
    source_id = models.CharField(
        db_index=True, verbose_name="Id отзыва на источнике", max_length=50
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name="Товар",
    )
    text = models.TextField(
        verbose_name="Отзыв",
    )
    buyer_rating = models.IntegerField(verbose_name="Оценка покупателя")
    created = models.DateTimeField(
        verbose_name="Дата создания отзыва", auto_now=False, auto_now_add=True
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
