import pandas as pd

def data_for_timeframe(listen_history, n_months):
    # get the most recent date
    most_recent_date = listen_history["date"].max()
    
    # set a timeframe to filter the data
    timeframe = most_recent_date - pd.DateOffset(months=n_months)
    
    # query rows which are within the given timeframe
    data = listen_history.query("date > @timeframe").copy()
    
    return data

