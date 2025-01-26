import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from textblob import TextBlob
from transformers import pipeline
import numpy as np

# -------------------------------
# 1. Сбор данных с помощью Steam
# -------------------------------

def get_steam_top_games():
    """
    Получает список популярных игр на Steam через веб-скрейпинг.
    :return: список игр с названием и количеством игроков.
    """
    url = "https://store.steampowered.com/stats/"
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка при получении данных с сайта Steam.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    games = []
    for row in soup.find_all("tr")[1:11]:  # Топ-10 игр
        cols = row.find_all("td")
        game_name = cols[1].text.strip()
        players = int(cols[0].text.replace(",", "").strip())
        games.append({"name": game_name, "players": players})

    return games

# -------------------------------
# 2. Анализ данных
# -------------------------------

def analyze_sentiment(reviews):
    """
    Анализирует тональность отзывов об играх.
    :param reviews: список строк с отзывами
    :return: список тональностей
    """
    sentiment_analysis = pipeline("sentiment-analysis")
    sentiments = []
    for review in reviews:
        result = sentiment_analysis(review)
        sentiments.append(result[0])
    return sentiments

def analyze_popularity(games):
    """
    Строит график популярности игр.
    :param games: список игр с названием и количеством игроков
    """
    names = [game["name"] for game in games]
    players = [game["players"] for game in games]

    plt.barh(names, players, color="skyblue")
    plt.xlabel("Число игроков")
    plt.title("Топ-10 игр на Steam")
    plt.gca().invert_yaxis()
    plt.show()

# -------------------------------
# 3. Генерация идей нейросетью
# -------------------------------

def generate_game_idea():
    """
    Генерирует идею для игры на основе анализа трендов.
    """
    generator = pipeline("text-generation", model="gpt-2")
    prompt = (
        "Создай идею для популярной инди-игры. Это должен быть платформер с уникальной механикой, "
        "ориентированный на текущие тренды. Например, с элементами процедурной генерации уровней "
        "и интересным визуальным стилем."
    )
    ideas = generator(prompt, max_length=100, num_return_sequences=1)
    return ideas[0]["generated_text"]

# -------------------------------
# 4. Объединение всего
# -------------------------------

def main():
    print("Сбор данных о популярных играх на Steam...")
    top_games = get_steam_top_games()

    if not top_games:
        print("Не удалось получить данные о популярных играх.")
        return

    print("\nАнализ популярных игр:")
    for game in top_games:
        print(f"Игра: {game['name']}, Число игроков: {game['players']}")

    # Построение графика популярности
    analyze_popularity(top_games)

    # Анализ тональности (упрощённый пример)
    sample_reviews = [
        "This game is incredibly addictive and fun!",
        "The graphics are amazing, but the gameplay is too slow.",
        "I love the multiplayer mechanics, they're so well done.",
    ]
    print("\nАнализ тональности отзывов:")
    sentiments = analyze_sentiment(sample_reviews)
    for review, sentiment in zip(sample_reviews, sentiments):
        print(f"Отзыв: {review}\nТональность: {sentiment}\n")

    # Генерация идеи
    print("Генерация идеи для игры...")
    game_idea = generate_game_idea()
    print("\nСгенерированная идея:")
    print(game_idea)

# -------------------------------
# Запуск программы
# -------------------------------

if __name__ == "__main__":
    main()
