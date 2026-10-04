import tkinter as tk
from tkinter import filedialog, END
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from string import punctuation
from nltk.corpus import stopwords
import folium
from folium.plugins import HeatMap
import random
def clean_tweet(tweet):
    tokens = tweet.split()

    table = str.maketrans("", "", punctuation)
    tokens = [word.translate(table) for word in tokens]

    tokens = [word for word in tokens if word.isalpha()]

    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word.lower() not in stop_words]

    tokens = [word for word in tokens if len(word) > 1]

    return " ".join(tokens)
def analyze_sentiment(tweets):
    positive = 0
    negative = 0
    neutral = 0
    results = []

    for tweet in tweets:
        blob = TextBlob(tweet)
        polarity = blob.polarity

        if polarity > 0.1:
            sentiment = "POSITIVE"
            positive += 1
        elif polarity < -0.1:
            sentiment = "NEGATIVE"
            negative += 1
        else:
            sentiment = "NEUTRAL"
            neutral += 1

        results.append({
            "tweet": tweet,
            "sentiment": sentiment,
            "polarity": polarity
        })

    return results, positive, negative, neutral
def load_dataset():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return None

    try:
        data = pd.read_csv(file_path, encoding="iso-8859-1")

        if "Text" not in data.columns:
            print("Error: 'Text' column not found in dataset.")
            return None

        return data

    except Exception as e:
        print("Error reading dataset:", e)
        return None
def show_sentiment_graph(positive, negative, neutral):
    labels = ["Positive", "Negative", "Neutral"]
    values = [positive, negative, neutral]

    plt.figure(figsize=(7, 5))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%"
    )
    plt.title("Women Safety & Sentiment Graph")
    plt.axis("equal")
    plt.show()
def generate_heatmap(tweet_count):
    locations = [
        (random.uniform(12, 28), random.uniform(72, 88))
        for _ in range(tweet_count)
    ]

    if not locations:
        print("No data available for heatmap.")
        return

    india_map = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    HeatMap(locations).add_to(india_map)

    india_map.save("heatmap.html")

    print("Heatmap generated! Open heatmap.html")
def run_project():
    data = load_dataset()

    if data is None:
        return

    tweets = data["Text"].dropna().astype(str).tolist()

    cleaned_tweets = [clean_tweet(tweet.lower()) for tweet in tweets]

    results, positive, negative, neutral = analyze_sentiment(cleaned_tweets)

    print("\n--- Women Safety Sentiment Analysis ---")
    print("Total Tweets :", len(tweets))
    print("Positive     :", positive)
    print("Negative     :", negative)
    print("Neutral      :", neutral)

    show_sentiment_graph(positive, negative, neutral)

    generate_heatmap(len(tweets))


run_project()