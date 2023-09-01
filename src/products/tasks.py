import logging

from celery import shared_task
from products.parsers import parse_feedback
from products.models import Product


@shared_task
def parse_feedbacks():
    try:
        products = [product.sku for product in Product.objects.all()]
        count_process_parsing = 0
        if products != []:
            for product_sku in products:
                parse_feedback(product_sku)
                logging.info(f"Parsed an sku: {product_sku}. Success!")
                count_process_parsing += 1
            return f"Finish. Count products = {count_process_parsing}"
    except Exception as ex:
        logging.info(f"Error! {ex}")
