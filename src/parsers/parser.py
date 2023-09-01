import requests
import json
from parsers.models import Feedback, Product
from django.utils import timezone

URL_FEEDBACK = "https://feedbacks2.wb.ru/feedbacks/v1/%(root)s"
URL_PRODUCT = "https://card.wb.ru/cards/detail?nm=%(sku)s"


def fetch_feedback(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text


def new_feedback(feedback, product):
    Feedback.objects.create(
        buyer_name=feedback.get("wbUserDetails").get("name"),
        buyer_id=feedback.get("globalUserId"),
        source_id=feedback.get("id"),
        product=product,
        text=feedback.get("text"),
        buyer_rating=feedback.get("productValuation"),
        created=timezone.now(),
    )


def new_product(product_sku):
    context = fetch_feedback(URL_PRODUCT % {"sku": product_sku})
    product_json = json.dump(context).get("products")[0]
    product = Product.objects.create(
        name=product_json["name"],
        sku=product_sku,
        root=product_json["root"],
        raiting=product_json["reviewRating"],
    )

    return product


def parse(product_sku):
    product = Product.objects.get(sku=product_sku)
    if not product:
        product = new_product(product_sku)
    context = fetch_feedback(URL_FEEDBACK % {"root": product.root})
    data = json.dump(context)
    for feedback in data.get("feedbacks"):
        exists_feedback = Feedback.objects.get(source_id=feedback.get("id"))
        if not exists_feedback:
            new_feedback(feedback, product)
