import pandas as pd
import numpy as np
import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from requests.exceptions import HTTPError
from tabulate import tabulate  # Для красивого вывода таблиц

# Функция для получения данных с Alpha Vantage
def get_investing_data(pair_id):
    try:
        # Ваш личный ключ API от Alpha Vantage
        api_key = 'WFSDFCPP8XHCMB6R'
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={pair_id}&interval=5min&apikey={api_key}"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'An error occurred: {err}')
        return None

# Функция для преобразования полученных данных в формат списка списков
def convert_to_list_of_lists(data):
    # Проверяем, что данные содержат временные ряды
    if 'Time Series (5min)' not in data:
        print("Данные не содержат временных рядов.")
        return []

    # Извлекаем временные ряды
    time_series = data['Time Series (5min)']

    # Преобразуем данные в список списков
    formatted_data = []
    for date, values in time_series.items():
        # Извлекаем дату и время
        date_time = date.split()
        date = date_time[0]
        time = date_time[1]

        # Извлекаем цену закрытия
        close_price = values['4. close']

        # Добавляем данные в список
        formatted_data.append([date, time, close_price])

    return formatted_data

# Функция для расчета уровней Фибоначчи
def calculate_fib_levels(high, low):
    levels = [0.236, 0.382, 0.5, 0.618, 0.786]
    return {level: high - (high - low) * level for level in levels}

# Функция для получения экономических новостей
def get_economic_news():
    url = 'https://ru.investing.com/economic-calendar/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('tr', class_='js-event-item')
    news = []
    for item in news_items:
        time_element = item.find('td', class_='time')
        currency_element = item.find('td', class_='flagCur')
        impact_element = item.find('td', class_='sentiment')
        event_element = item.find('td', class_='event')
        actual_element = item.find('td', class_='actual')
        forecast_element = item.find('td', class_='forecast')
        previous_element = item.find('td', class_='previous')

        news.append({
            'time': time_element.text.strip() if time_element else 'Нет данных',
            'currency': currency_element.text.strip() if currency_element else 'Нет данных',
            'impact': impact_element.get('title').strip() if impact_element else 'Нет данных',
            'event': event_element.text.strip() if event_element else 'Нет данных',
            'actual': actual_element.text.strip() if actual_element else 'Нет данных',
            'forecast': forecast_element.text.strip() if forecast_element else 'Нет данных',
            'previous': previous_element.text.strip() if previous_element else 'Нет данных'
        })
    return news

# Функция для анализа влияния новостей на рынок
def analyze_news_impact(news):
    impact_dict = {
        'positive': ['рост', 'увеличение', 'повышение'],
        'negative': ['падение', 'снижение', 'кризис']
    }
    for article in news:
        for word in impact_dict['positive']:
            if word in article['event']:
                return 'positive'
        for word in impact_dict['negative']:
            if word in article['event']:
                return 'negative'
    return 'neutral'

# Функция для определения сигнала на основе фундаментального анализа
def fundamental_analysis_signal(news_impact, ema_short, ema_long):
    if news_impact == 'positive' and ema_short > ema_long:
        return 'Strong Buy'
    elif news_impact == 'negative' and ema_short < ema_long:
        return 'Strong Sell'
    else:
        return 'Hold'

# Функция для определения сигнала с учетом EMA и уровней Фибоначчи
def signal(ema_short, ema_long, price, fib_levels):
    if ema_short > ema_long and price > fib_levels[0.618]:
        return 'Sell'
    elif ema_short < ema_long and price < fib_levels[0.382]:
        return 'Buy'
    else:
        return 'Hold'

# Функция для определения выхода из сделки с использованием уровней Фибоначчи и EMA
def exit_trade_fibonacci_ema(current_price, ema_50, ema_100, fib_levels):
    for level, fib_price in fib_levels.items():
        if abs(current_price - fib_price) < 0.0001:
            return 'Exit', f'Fib.Level {level}'
    if (ema_50 < ema_100 and current_price > ema_50) or (ema_50 > ema_100 and current_price < ema_50):
        return 'Exit', 'EMA Crossover'
    return 'Hold', 'No Exit'

# Функция для расчета True Range
def calculate_true_range(high, low, prev_close):
    return max(high - low, abs(high - prev_close), abs(low - prev_close))

# Функция для расчета ATR
def calculate_atr(closes, highs, lows, n):
    tr_values = []
    for i in range(1, len(closes)):
        tr = calculate_true_range(highs[i], lows[i], closes[i - 1])
        tr_values.append(tr)

    atr = sum(tr_values[-n:]) / n
    return atr

# Функция для генерации случайных Волн Эллиота (для примера)
def elliot_waves(data):
    waves = ['Up', 'Down']
    elliot_waves = []
    for i in range(len(data)):
        elliot_waves.append(random.choice(waves))
    return elliot_waves

# Функция для определения точек входа и выхода из сделок на основе Волн Эллиота и EMA
def enter_exit_trade_elliot_ema(data, elliot_waves):
    entry_point = None
    exit_point = None

    for i in range(len(data)):
        if elliot_waves[i] == 'Up' and data['EMA_50'].iloc[i] > data['EMA_100'].iloc[i]:
            entry_point = i
        elif elliot_waves[i] == 'Down' and data['EMA_50'].iloc[i] < data['EMA_100'].iloc[i]:
            exit_point = i

    return entry_point, exit_point

# Функция для печати данных в виде таблицы с заголовками
def print_data_in_columns(data, headers):
    # Определяем ширину столбцов по самому длинному элементу в каждом из них
    column_widths = [max(len(str(item)) for item in column) for column in zip(*data, headers)]
    column_widths = [max(width, len(header)) for width, header in zip(column_widths, headers)]  # Учитываем заголовки

    # Функция для печати строки данных, выровненной по ширине столбцов
    def print_row(row, widths):
        print(" ".join(str(item).ljust(width) for item, width in zip(row, widths)))

    # Печать заголовков
    print_row(headers, column_widths)

    # Печать разделителя
    print("-" * (sum(column_widths) + len(column_widths) - 1))

    # Печать данных
    for row in data:
        print_row(row, column_widths)

def calculate_rsi(close_prices, n):
    gains = [0]  # Приросты
    losses = [0]  # Убытки

    for i in range(1, len(close_prices)):
        diff = close_prices[i] - close_prices[i - 1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))

    avg_gain = sum(gains[:n]) / n
    avg_loss = sum(losses[:n]) / n

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def get_session_time():
    """
    Функция для определения времени суток (сессии) на основе текущего времени.
    Возвращает строку с названием сессии.
    """
    current_hour = datetime.now().hour

    if 0 <= current_hour < 9:
        return 'Азиатская'
    elif 9 <= current_hour < 16:
        return 'Европейская'
    elif 16 <= current_hour < 24:
        return 'Американская'
    else:
        return 'Тихоокеанская'

async def main(pair_id, chat_id):
    # Получение данных с Alpha Vantage
    data = get_investing_data(pair_id)
    if not data:
        await bot.send_message(chat_id, "Произошла ошибка при получении данных. Пожалуйста, попробуйте позже.")
        return

    list_of_lists = convert_to_list_of_lists(data)

    # Преобразование данных в DataFrame
    df = pd.DataFrame(list_of_lists, columns=['Дата', 'Время', 'Цена'])
    df['Дата'] = pd.to_datetime(df['Дата'] + ' ' + df['Время'])
    df.sort_values('Дата', inplace=True)

    # Убедимся, что столбец 'Цена' содержит числа с плавающей точкой
    df['Цена'] = df['Цена'].astype(float)

    # Рассчитываем EMA
    df['EMA_50'] = df['Цена'].ewm(span=50, adjust=False).mean()
    df['EMA_100'] = df['Цена'].ewm(span=100, adjust=False).mean()
    df['EMA_600'] = df['Цена'].ewm(span=600, adjust=False).mean()
    df['EMA_25'] = df['Цена'].ewm(span=25, adjust=False).mean()

    # Получаем и анализируем экономические новости
    news = get_economic_news()
    news_impact = analyze_news_impact(news)

    # Получаем текущую сессию
    current_session = get_session_time()

    # Выводим информацию о времени сессии и влиянии новостей
    message = f"Текущая сессия: {current_session} сессия\n"
    message += "Влияние новостей на рынок: " + news_impact + "\n\n"

    # Получаем максимальную и минимальную цены для расчета уровней Фибоначчи
    high_price = df['Цена'].max()
    low_price = df['Цена'].min()
    fib_levels = calculate_fib_levels(high_price, low_price)

    # Прогнозируем сигналы на следующий день
    last_date = df['Дата'].iloc[-1]
    predicted_signals = []

    for minute in range(0, 24 * 60, 60):  # Прогноз каждый час
        next_time = last_date + pd.Timedelta(minutes=minute + 60)
        ema_50 = df['EMA_50'].iloc[-1]
        ema_100 = df['EMA_100'].iloc[-1]
        ema_600 = df['EMA_600'].iloc[-1]
        ema_25 = df['EMA_25'].iloc[-1]
        price_change = random.uniform(-0.0001, 0.0001)
        predicted_price = round(df['Цена'].iloc[-1] + price_change, 6)

        if ema_600 is not None:
            if predicted_price > ema_600:
                predicted_signal = 'Buy'
            elif predicted_price < ema_600:
                predicted_signal = 'Sell'
            else:
                predicted_signal = 'Hold'
        else:
            predicted_signal = 'Hold'

        exit_signal, reason = exit_trade_fibonacci_ema(predicted_price, ema_50, ema_100, fib_levels)

        if predicted_price > ema_25:
            exit_signal = 'Exit'
            reason = 'EMA 25 Crossover'

        # Добавляем процент точности
        actual_price = df['Цена'].iloc[-1]
        accuracy = round((predicted_price / actual_price - 1) * 100, 2)

        predicted_signals.append([next_time.strftime("%Y-%m-%d %H:%M"), predicted_signal, predicted_price, exit_signal, reason, f"{accuracy}%"])

    # Выводим прогноз в виде таблицы с заголовками
    headers = ["Дата", "Сигнал", "Цена", "Выход", "Причина", "Точность"]
    table = tabulate(predicted_signals, headers=headers, tablefmt="pretty")
    message += f"<pre>{table}</pre>"

    await bot.send_message(chat_id, message, parse_mode='HTML')

if __name__ == "__main__":
    import asyncio
    from aiogram import Bot, Dispatcher, types
    from aiogram.contrib.middlewares.logging import LoggingMiddleware
    from aiogram.dispatcher.webhook import SendMessage
    from aiogram.types import ParseMode

    # Токен бота
    API_TOKEN = '7187020122:AAGvfF_RRItJ5PALFujIIg6HEUqzNIRXmAM'

    # Инициализация бота и диспетчера
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        await message.reply("Привет! Для получения прогноза на следующий час введите команду /forecast <валютная_пара>.")
        
    @dp.message_handler(commands=['forecast'])
    async def send_forecast(message: types.Message):
        try:
            currency_pair = message.text.split()[1]
            await main(currency_pair.upper(), message.chat.id)
        except IndexError:
            await message.reply("Вы не указали валютную пару. Пожалуйста, попробуйте снова.")

    # Запуск бота
    executor = dp.start_polling()
    asyncio.run(executor)
