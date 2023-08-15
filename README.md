# Data Analysis of My Own YouTube Music History

## Data Processing

1. Data downloaded using [Google Takeout](https://takeout.google.com/settings/takeout) on 4 Aug 2023, filtering for "YouTube and YouTube Music"
1. Stored as `watch-history.json` under `/data/raw` (excluded from source control)
1. Extracted the music history with `python3 ./src/data/make_dataset.py`
   1. Loads the data into a dataframe
   1. Filters for music by targeting looking for "YouTube Music" as the value of `header`
   1. Cleans the data and adds a few helper columns (see comments for details)
   1. Saves this dataframe to a parquet file

## Environment

Create an environment
`conda env create -f environment.yml`

Update the environment, pruning any removed dependencies
`conda env update -f environment.yml --prune`

Activate environment
`conda activate youtube_music_env`
