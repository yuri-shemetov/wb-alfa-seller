## Задание: 
В группу Телеграмм должны поступать уведомления о негативном отзыве на товар в Wildberries.

Входные данные: файл Exel (пример: Книга111.xlsx) со списком SKU товаров. (SKU - основной id товаров в WB. Используется, например, в адресе карточки товара: https://www.wildberries.ru/catalog/642...etail.aspx)

Сообщение следующего содержания (ориентировочно): "Негативный отзыв/название товара/SKU товара/столько-то звезд (от 4х до 1ой)/ текст отзыва/Текущий рейтинг товара."

Методы мониторинга (на выбор, можно сделать по-своему):
1) парсинг страниц карточек товара.
2) использование API WB. Описания нужных запросов нет, но через инспектор кода в браузере их можно изучить (POST: https://public-feedbacks.wildberries.r...backs/site)

Выполнять: регулярно по расписанию (достаточно предложить и описать метод запуска).

Задание выполнить на Python.

## Запуск приложения
Клонируем ссылку
```bash
git clone https://github.com/yuri-shemetov/wb-alfa-seller.git
```

Приложение использует инструмент poetry для управления зависимостями. Вам необходимо его установить, до начала работы
```bash
pip install --user poetry
poetry install
poetry --version
```

Запустить Reddis из docker-compose:
```bash
sudo docker compose -f docker-compose.yml up --build
```

Переходим в папку SRC: cd src. Вам необходимо будет настроить вашу копию .env для работы с приложением. Хорошим стартом будет копирование файла .env.dist в .env.

Запускаем миграции
```bash
poetry run manage.py makemigrate
```

Запускаем локальный сервер, а также Celery (worker - тот, кто выполняет задачу; beat - тот, кто следит за графиком)
```bash
poetry run ./manage.py runserver
poetry run celery -A project_settings worker -l INFO
poetry run celery -A project_settings beat -l INFO
```