import pandas as pd

def export_to_csv(dataframe, filename):
    return dataframe.to_csv(index=False).encode("utf-8")