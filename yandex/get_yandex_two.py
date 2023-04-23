# -*- coding: utf-8 -*-
import json
import random
# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys
from time import sleep

import requests
from requests.exceptions import ConnectionError

from config import load_config

# проверка версии пайтона
if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf-8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf-8')
        else:
            return x

# --- Входные данные ---
config = load_config(".env")

# какие столбцы подгрузить
column = ['Date', 'CampaignName', 'AdGroupName', 'AdGroupId', 'AdNetworkType', 'Placement', 'Criteria', 'CriteriaType',
          'MatchType', 'RlAdjustmentId', 'LocationOfPresenceName', 'Device', 'Gender', 'Age', 'Impressions', 'Clicks',
          'Cost', 'AvgEffectiveBid', 'AvgTrafficVolume', 'AvgImpressionPosition', 'AvgClickPosition', 'Bounces',
          'BounceRate', 'Conversions']

# ID цели
goal_id = ['282393785', '120846175', '208408852', '209436928', '208415434']
# даты отчета
first_date = "2023-03-19"
second_date = "2023-03-19"

# --- Подготовка запроса ---
# Создание HTTP-заголовков запроса

headers_one = {"Authorization": f'{config.reports.token_type} ' + config.yandex_token.token_two,
               "Client-Login": config.yandex_login.login_two,
               "Accept-Language": "ru",
               "processingMode": "auto",
               "returnMoneyInMicros": "false",
               "skipReportHeader": "true",
               # "skipColumnHeader": "true",
               "skipReportSummary": "true"
               }

# Создание тела запроса
body = {"params": {"SelectionCriteria": {"DateFrom": first_date, "DateTo": second_date}, "Goals": goal_id,
                   "FieldNames": column, "ReportName": f"Отчет {random.randint(1, 10000)}",
                   "ReportType": "CRITERIA_PERFORMANCE_REPORT", "DateRangeType": "CUSTOM_DATE", "Format": "TSV",
                   "IncludeVAT": "YES", "IncludeDiscount": "NO"}}

# Кодирование тела запроса в JSON
body = json.dumps(body, indent=4)

# --- Запуск цикла для выполнения запросов ---
# Если получен HTTP-код 200, то выводится содержание отчета
# Если получен HTTP-код 201 или 202, выполняются повторные запросы
while True:
    try:
        request_one = requests.post(config.reports.reports_url, body, headers=headers_one)
        request_one.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
        if request_one.status_code == 400:
            print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
            print("RequestId: {}".format(request_one.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(u(body)))
            print("JSON-код ответа сервера: \n{}".format(u(request_one.json())))
            break
        elif request_one.status_code == 200:
            print("Отчет создан успешно")
            print("RequestId: {}".format(request_one.headers.get("RequestId", False)))
            break
        elif request_one.status_code == 201:
            print("Отчет успешно поставлен в очередь в режиме офлайн")
            retryIn = int(20)
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId: {}".format(request_one.headers.get("RequestId", False)))
            sleep(retryIn)
        elif request_one.status_code == 202:
            print("Отчет формируется в режиме офлайн")
            retryIn = int(request_one.headers.get("retryIn", 60))
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId:  {}".format(request_one.headers.get("RequestId", False)))
            sleep(retryIn)
        elif request_one.status_code == 500:
            print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
            print("RequestId: {}".format(request_one.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(request_one.json())))
            break
        elif request_one.status_code == 502:
            print("Время формирования отчета превысило серверное ограничение.")
            print(
                "Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
            print("JSON-код запроса: {}".format(body))
            print("RequestId: {}".format(request_one.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(request_one.json())))
            break
        else:
            print("Произошла непредвиденная ошибка")
            print("RequestId:  {}".format(request_one.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(body))
            print("JSON-код ответа сервера: \n{}".format(u(request_one.json())))
            break

    # Обработка ошибки, если не удалось соединиться с сервером API Директа
    except ConnectionError:
        # В данном случае мы рекомендуем повторить запрос позднее
        print("Произошла ошибка соединения с сервером API")
        # Принудительный выход из цикла
        break

    # Если возникла какая-либо другая ошибка
    except:
        # В данном случае мы рекомендуем проанализировать действия приложения
        print("Произошла непредвиденная ошибка")
        # Принудительный выход из цикла
        break

    # создаем csv файл и записываем в него ответ

    with open("./excel/yandex_data_two.csv", 'w', encoding='utf-8') as file_one:
        file_one.write(request_one.text)
