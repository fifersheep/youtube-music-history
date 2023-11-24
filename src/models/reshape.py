import pandas as pd


class DataTransformer:
    def get_data(self) -> pd.DataFrame:
        return pd.read_parquet("../data/processed/listen_history.parquet.gzip")

    def data_for_timeframe(self, data: pd.DataFrame, n_months: int) -> pd.DataFrame:
        # get the most recent date
        most_recent_date = data["date"].max()

        # set a timeframe to filter the data
        timeframe = most_recent_date - pd.DateOffset(months=n_months)

        # query rows which are within the given timeframe
        return data.query("date > @timeframe").copy()
