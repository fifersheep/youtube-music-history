# import os
import pandas as pd
import json


def load_dataset():
    with open("../../data/raw/watch-history.json", encoding='UTF-8') as json_file:
        data = json.load(json_file)
        return pd.json_normalize(data)


def extract_listen_history(data):
    # query rows which have the "YouTube Music" header and are within the given timeframe
    youre_losing_me_title_matcher = ('title.str.contains("losing me", case=False) '
                                     '& ~title.str.contains("Therapist", case=False)'
                                     '& ~title.str.contains("fanmade", case=False)')
    listen_history_df = \
        data.query(f'(header == "YouTube Music") | (header == "YouTube" & {youre_losing_me_title_matcher})')[
            ["title", "subtitles", "time"]
        ].copy()

    # remove rows which have no subtitles value, as this is where the artist is stored
    listen_history_df = listen_history_df.dropna(subset=["subtitles"])

    # removed 'Watched ' from the title
    listen_history_df["title"] = listen_history_df["title"].map(lambda x: x.lstrip("Watched "))

    # create the artist column by extracting name from subtitles and removing ' - Topic' from the end
    listen_history_df["artist"] = listen_history_df["subtitles"].map(
        lambda x: x[0]["name"].rstrip(" - Topic")
    )

    # use the time column to create a date, day, month, and year column
    listen_history_df["time"] = pd.to_datetime(listen_history_df["time"])
    listen_history_df["date"] = pd.to_datetime(listen_history_df["time"].dt.date)
    listen_history_df["month"] = listen_history_df["date"].to_numpy().astype('datetime64[M]')

    # some artists are reported with varying names, combine them manually
    listen_history_df["artist"] = listen_history_df["artist"].replace(
        {
            "Caramell": "Caramella Girls",
            "TaylorSwiftVEVO": "Taylor Swift",
            "Teller 13 Taylor": "Taylor Swift",
        }
    )

    # combine Taylor Swift "You're Losing Me" tracks
    youre_losing_me_listens = listen_history_df.query(youre_losing_me_title_matcher)
    listen_history_df.loc[youre_losing_me_listens.index, 'title'] = "You’re Losing Me (From The Vault)"

    return listen_history_df


def save_df(data, filename):
    data.to_parquet(f"../../data/processed/{filename}", index=False)


if __name__ == '__main__':
    dataset = load_dataset()
    listen_history = extract_listen_history(dataset)
    save_df(listen_history, "listen_history.parquet.gzip")
