# %%
# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
from time import sleep
import json
import pandas as pd

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

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
# %%
# --- Входные данные ---
# Адрес сервиса Reports для отправки JSON-запросов (регистрозависимый)
ReportsURL = 'https://api.direct.yandex.com/json/v5/reports'

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = 'y0_AgAAAABf82q1AAZAOQAAAADOqyOFZIope4xMQBi3iWMw37Q0wvHflGE'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = 'ivan-poisk-bm'

# какие столбцы подгрузить
stolbec = ['Date', 'CampaignName', 'AdGroupName', 'AdGroupId', \
           'AdNetworkType', 'Criteria', 'CriteriaType', 'MatchType', 'RlAdjustmentId', \
           'LocationOfPresenceName', 'Device', 'Gender', 'Age', 'Impressions', 'Clicks', 'Cost', 'AvgEffectiveBid', \
           'AvgTrafficVolume', 'AvgImpressionPosition', 'AvgClickPosition', 'BounceRate', 'Conversions']

# ID цели
goalID = ['282393785']
# даты отчета
firstDate = "2023-02-28"
secondDate = "2023-02-28"
# %%

# --- Подготовка запроса ---
# Создание HTTP-заголовков запроса
headers = {
    # OAuth-токен. Использование слова Bearer обязательно
    "Authorization": "Bearer " + token,
    # Логин клиента рекламного агентства
    "Client-Login": clientLogin,
    # Язык ответных сообщений
    "Accept-Language": "ru",
    # Режим формирования отчета
    "processingMode": "auto",
    # Формат денежных значений в отчете
    "returnMoneyInMicros": "false",
    # Не выводить в отчете строку с названием отчета и диапазоном дат
    # "skipReportHeader": "true",
    # Не выводить в отчете строку с названиями полей
    # "skipColumnHeader": "true",
    # Не выводить в отчете строку с количеством строк статистики
    "skipReportSummary": "true"
}

# Создание тела запроса
body = {
    "params": {
        "SelectionCriteria": {
            "DateFrom": firstDate,
            "DateTo": secondDate
        },
        "Goals": goalID,
        "FieldNames": stolbec,
        "ReportName": f"Отчет 9",
        "ReportType": "CRITERIA_PERFORMANCE_REPORT",
        "DateRangeType": "CUSTOM_DATE",
        "Format": "TSV",
        "IncludeVAT": "YES",
        "IncludeDiscount": "NO"
    }
}

# Кодирование тела запроса в JSON
body = json.dumps(body, indent=4)

# %%

# --- Запуск цикла для выполнения запросов ---
# Если получен HTTP-код 200, то выводится содержание отчета
# Если получен HTTP-код 201 или 202, выполняются повторные запросы
while True:
    try:
        req = requests.post(ReportsURL, body, headers=headers)

        req.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
        if req.status_code == 400:
            print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(u(body)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        elif req.status_code == 200:
            print("Отчет создан успешно")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            break
        elif req.status_code == 201:
            print("Отчет успешно поставлен в очередь в режиме офлайн")
            retryIn = int(20)
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 202:
            print("Отчет формируется в режиме офлайн")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Повторная отправка запроса через {} секунд".format(retryIn))
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 500:
            print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        elif req.status_code == 502:
            print("Время формирования отчета превысило серверное ограничение.")
            print(
                "Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
            print("JSON-код запроса: {}".format(body))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
            break
        else:
            print("Произошла непредвиденная ошибка")
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            print("JSON-код запроса: {}".format(body))
            print("JSON-код ответа сервера: \n{}".format(u(req.json())))
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
# %%
# создаем csv файл и записываем в него ответ
with open("./cashe.csv", 'w', encoding='utf-8') as file:
    file.write(req.text)

# превращаем ответ в таблицу
df = pd.read_csv("cashe.csv", header=1, sep='\t', index_col=0, encoding="utf-8")

# меняем значения в конверсиях - на 0, переводит в int

for col in df.columns:
    if 'Conversions' in col:
        df[col] = df[col].replace('--', '0').astype(int)
        conv = col

# проверка таблицы
df.groupby('CampaignName', as_index=False).agg({'Clicks': 'sum', 'Cost': 'sum', conv: 'sum'}).sort_values(conv)
# %%

# %%

# %%

# %%
