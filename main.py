import numpy as np
import pandas as pd
import plotly.graph_objects as go
import zigzag
import binance

# file_path = r"DOTUSDT-1m-2022-05.xlsx"
# df = pd.read_excel(file_path, engine='openpyxl')
#
# high = np.array(df['High'])
# low = np.array(df['Low'])

data = binance.get_data(market='NEARUSDT', tick_interval='1h')
(date, open, high, low, close) = data

if __name__ == '__main__':
    fig = go.Figure(data=[go.Candlestick(
                            x=date,
                            open=open,
                            high=high,
                            low=low,
                            close=close
                        )])

    fig.update_layout(
        width=1600,
        height=900, )

    fig.write_html("./file.html")
    for (i_h, p_h),(i_l, p_l) in zigzag.zigzag(high, low, depth=2, dev_threshold=6):
        print(f'PEAK Index: {i_h}, price: {p_h}, DATE: {list(reversed(date))[i_h]} - VALLEY Index: {i_l}, price: {p_l}, DATE: {list(reversed(date))[i_l]}')