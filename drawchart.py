import zigzag2
import numpy as np
import pandas as pd



def draw_chart(close, high, low):
    pivots = zigzag2.peak_valley_pivots_candlestick(close, high, low, .01, -.01)
    pivotPrice = np.nan  # This line clears old pivot prices
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
        width=1000,
        height=800, )

    fig.add_trace(go.Scatter(x=df['Date'],
                             y=df['Pivot Price'].interpolate(),
                             mode='lines',
                             line=dict(color='black')))


    def annot(value):
        if np.isnan(value):
            return ''
        else:
            return value


    j = 0
    for i, p in enumerate(df['Pivot Price']):
        if not np.isnan(p):
            fig.add_annotation(dict(font=dict(color='rgba(0,0,200,0.8)', size=12),
                                    x=df['Date'].iloc[i],
                                    y=p,
                                    showarrow=False,
                                    text=annot(round(abs(df_diff.iloc[j]), 3)),
                                    textangle=0,
                                    xanchor='right',
                                    xref="x",
                                    yref="y"))
            j = j + 1

    fig.update_xaxes(type='category')
    fig.show()