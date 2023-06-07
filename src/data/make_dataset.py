# import os
import pandas as pd
import json

def load_dataset():
    with open("data/raw/watch-history.json") as json_file:
        data = json.load(json_file)
        return pd.json_normalize(data)

def extract_listen_history(data):
    # query rows which have the "YouTube Music" header and are within the given timeframe
    listen_history = data.query('header == "YouTube Music"')[
        ["title", "subtitles", "time"]
    ].copy()

    # remove rows which have no subtitles value, as this is where the artist is stored
    listen_history = listen_history.dropna(subset=["subtitles"])

    # removed 'Watched ' from the title
    listen_history["title"] = listen_history["title"].map(lambda x: x.lstrip("Watched "))

    # create the artist column by extracting name from subtitles and removing ' - Topic' from the end
    listen_history["artist"] = listen_history["subtitles"].map(
        lambda x: x[0]["name"].rstrip(" - Topic")
    )

    # use the time column to create a date, day, month, and year column
    listen_history["time"] = pd.to_datetime(listen_history["time"])
    listen_history["date"] = pd.to_datetime(listen_history["time"].dt.date)
    listen_history["day"] = listen_history["time"].dt.day
    listen_history["month"] = listen_history["time"].dt.month
    listen_history["year"] = listen_history["time"].dt.year
    listen_history.dtypes

    # some artists are reported with varying names, combine them manually
    listen_history["artist"] = listen_history["artist"].replace(
        "Caramell", "Caramella Girls"
    )
    return listen_history

def save_df(data, filename):
    data.to_parquet(f"data/processed/{filename}", index=False)
    

if __name__ == '__main__':
    dataset = load_dataset()
    listen_history = extract_listen_history(dataset)
    save_df(listen_history, "listen_history.parquet.gzip")


