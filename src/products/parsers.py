import requests
import json
import logging
from products.models import Feedback, Product
from django.utils import timezone
from project_settings import settings

URL_FEEDBACK = "https://feedbacks2.wb.ru/feedbacks/v1/%(root)s"
URL_PRODUCT = "https://card.wb.ru/cards/detail?nm=%(sku)s"


def send_message(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token:
        return
    url_req = (
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    )
    response = requests.post(url_req)
    if response.status_code != 200:
        logging.info(
            f"Error message not sent to chat_id={chat_id}, status code={response.status}"
        )
    else:
        logging.info(f"Notification sent successfully!")


def fetch_text(url):
    if settings.PROXIES:
        response = requests.get(url, proxies=settings.PROXIES)
    else:
        response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        logging.info(f"Status code: {response.status_code} ")


def new_feedback(feedback, product):
    Feedback.objects.create(
        buyer_name=feedback.get("wbUserDetails").get("name"),
        buyer_id=feedback.get("wbUserId"),
        source_id=feedback.get("id"),
        product=product,
        text=feedback.get("text"),
        buyer_rating=feedback.get("productValuation"),
        created=timezone.now(),
    )
    logging.info("New feedback!")
    context = fetch_text(URL_PRODUCT % {"sku": product.sku})
    product_json = json.loads(context, strict=False).get("data").get("products")[0]
    text = f"{product.name}\n{product.sku}\
        \nОценка покупателя: {feedback.get('productValuation')}\
        \nОбщий рейтинг: {product_json['reviewRating']}\
        \n{feedback.get('text')}"
    send_message(text)


def new_product(product_sku):
    context = fetch_text(URL_PRODUCT % {"sku": product_sku})
    product_json = json.loads(context, strict=False).get("data").get("products")[0]
    product = Product.objects.create(
        name=product_json["name"],
        sku=product_sku,
        root=product_json["root"],
        rating=product_json["reviewRating"],
    )
    logging.info("New product!")

    return product


def parse_feedback(product_sku):
    product = Product.objects.filter(sku=product_sku).first()
    context = fetch_text(URL_FEEDBACK % {"root": product.root})
    data = json.loads(context, strict=False)
    if data.get("feedbacks"):
        for feedback in data.get("feedbacks"):
            if (
                feedback.get("productValuation")
                and int(feedback.get("productValuation")) < 5
            ):
                exists_feedback = Feedback.objects.filter(
                    source_id=feedback.get("id")
                ).first()
                if not exists_feedback:
                    new_feedback(feedback, product)
    else:
        logging.info("No product feedbacks!")


def parse_product(product_sku):
    product = Product.objects.filter(sku=product_sku).first()
    if not product:
        product = new_product(product_sku)
