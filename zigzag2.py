import numpy as np
import plotly.graph_objects as go
import pandas as pd

PEAK, VALLEY = 1, -1


def _identify_initial_pivot(X, up_thresh, down_thresh):
    """Quickly identify the X[0] as a peak or valley."""
    x_0 = X[0]
    max_x = x_0
    max_t = 0
    min_x = x_0
    min_t = 0
    up_thresh += 1
    down_thresh += 1

    for t in range(1, len(X)):
        x_t = X[t]

        if x_t / min_x >= up_thresh:
            return VALLEY if min_t == 0 else PEAK

        if x_t / max_x <= down_thresh:
            return PEAK if max_t == 0 else VALLEY

        if x_t > max_x:
            max_x = x_t
            max_t = t

        if x_t < min_x:
            min_x = x_t
            min_t = t

    t_n = len(X) - 1
    return VALLEY if x_0 < X[t_n] else PEAK


def peak_valley_pivots_candlestick(close, high, low, up_thresh, down_thresh):
    """
    Finds the peaks and valleys of a series of HLC (open is not necessary).
    TR: This is modified peak_valley_pivots function in order to find peaks and valleys for OHLC.
    Parameters
    ----------
    close : This is series with closes prices.
    high : This is series with highs  prices.
    low : This is series with lows prices.
    up_thresh : The minimum relative change necessary to define a peak.
    down_thesh : The minimum relative change necessary to define a valley.
    Returns
    -------
    an array with 0 indicating no pivot and -1 and 1 indicating valley and peak
    respectively
    Using Pandas
    ------------
    For the most part, close, high and low may be a pandas series. However, the index must
    either be [0,n) or a DateTimeIndex. Why? This function does X[t] to access
    each element where t is in [0,n).
    The First and Last Elements
    ---------------------------
    The first and last elements are guaranteed to be annotated as peak or
    valley even if the segments formed do not have the necessary relative
    changes. This is a tradeoff between technical correctness and the
    propensity to make mistakes in data analysis. The possible mistake is
    ignoring data outside the fully realized segments, which may bias analysis.
    """
    if down_thresh > 0:
        raise ValueError('The down_thresh must be negative.')

    initial_pivot = _identify_initial_pivot(close, up_thresh, down_thresh)

    t_n = len(close)
    pivots = np.zeros(t_n, dtype='i1')
    pivots[0] = initial_pivot

    # Adding one to the relative change thresholds saves operations. Instead
    # of computing relative change at each point as x_j / x_i - 1, it is
    # computed as x_j / x_1. Then, this value is compared to the threshold + 1.
    # This saves (t_n - 1) subtractions.
    up_thresh += 1
    down_thresh += 1

    trend = -initial_pivot
    last_pivot_t = 0
    last_pivot_x = close[0]
    for t in range(1, len(close)):

        if trend == -1:
            x = low[t]
            r = x / last_pivot_x
            if r >= up_thresh:
                pivots[last_pivot_t] = trend  #
                trend = 1
                # last_pivot_x = x
                last_pivot_x = high[t]
                last_pivot_t = t
            elif x < last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t
        else:
            x = high[t]
            r = x / last_pivot_x
            if r <= down_thresh:
                pivots[last_pivot_t] = trend
                trend = -1
                # last_pivot_x = x
                last_pivot_x = low[t]
                last_pivot_t = t
            elif x > last_pivot_x:
                last_pivot_x = x
                last_pivot_t = t

    if last_pivot_t == t_n - 1:
        pivots[last_pivot_t] = trend
    elif pivots[t_n - 1] == 0:
        pivots[t_n - 1] = trend

    return pivots


file_path = r"data.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

pivots = peak_valley_pivots_candlestick(df.Close, df.High, df.Low, 0.0006, -0.0006)
df['Pivots'] = pivots
df['Pivot Price'] = np.nan  # This line clears old pivot prices
df.loc[df['Pivots'] == 1, 'Pivot Price'] = df.High
df.loc[df['Pivots'] == -1, 'Pivot Price'] = df.Low

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'])])

df_diff = df['Pivot Price'].dropna().diff().copy()

fig.add_trace(
    go.Scatter(mode="lines+markers",
               x=df['Date'],
               y=df["Pivot Price"]
               ))

fig.update_layout(
    autosize=False,
    width=1600,
    height=800, )

fig.add_trace(go.Scatter(x=df['Date'],
                         y=df['Pivot Price'].interpolate(),
                         mode='lines',
                         line=dict(color='black')))


# def annot(value):
#     if np.isnan(value):
#         return ''
#     else:
#         return value
#
#
# j = 0
# for i, p in enumerate(df['Pivot Price']):
#     if not np.isnan(p):
#         fig.add_annotation(dict(font=dict(color='rgba(0,0,200,0.8)', size=12),
#                                 x=df['Date'].iloc[i],
#                                 y=p,
#                                 showarrow=False,
#                                 text=annot(round(abs(df_diff.iloc[j]), 3)),
#                                 textangle=0,
#                                 xanchor='right',
#                                 xref="x",
#                                 yref="y"))
#         j = j + 1

fig.update_xaxes(type='category')
fig.write_html("./file.html", auto_open=True)