import datetime
import numpy as np
import math
import pandas as pd

file_path = r"data.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

dev_threshold = 0.6
depth = 2
line_color = '#2962FF'
extend_to_last_bar = True
display_reversal_price = True
display_cumulative_volume = True
display_reversal_price_change = True
difference_price = "Absolute"
# difference_price = "Percent"


bar_index = len(df)
df['DateTime'] = pd.to_datetime(df['Date'])
df['TimeStamp'] = df.DateTime.astype('int64') // 10 ** 9
time = np.array(df['TimeStamp'])



def pivots (src, length, isHigh):
    isFound = False
    p = np.array(src)[length]
    src = list(reversed(src))
    bar_index = list(range(len(src)))
    if length == 0:
        yield 0, p
    else:
        isFound = True
        for i in range (abs(length - 1)) :
            if isHigh and src[i] > p:
                isFound = False
            if not isHigh and src[i] < p:
                isFound = False
        for i in range(length + 1, 2 * length):
            if isHigh and src[i] >= p:
                isFound = False
            if not isHigh and src[i] <= p:
                isFound = False
        if isFound and length * 2 <= len(src):
            yield [bar_index[length], p]
        else:
            yield [int(np.nan), float(np.nan)]

high = np.array(df['High'])
low = np.array(df['Low'])
[iH, pH] = pivots(high, math.floor(depth / 2), True)
[iL, pL] = pivots(low, math.floor(depth / 2), False)

def calc_dev(base_price, price):
    100 * (price - base_price) / base_price

def price_rotation_aggregate(price_rotation, pLast, cum_volume):
    str = ""
    if display_reversal_price:
        str += str.tostring(pLast, format.mintick) + " "
    if display_reversal_price_change:
        str += price_rotation + " "
    if display_cumulative_volume:
        str += "\n" + cum_volume
    return str

def caption(isHigh, iLast, pLast, price_rotation, cum_volume):
    price_rotation_str = price_rotation_aggregate(price_rotation, pLast, cum_volume)
    if display_reversal_price or display_reversal_price_change or display_cumulative_volume:
        if not isHigh:
            # label.new(iLast, pLast, text=price_rotation_str, style=label.style_none, xloc=xloc.bar_time, yloc=yloc.belowbar, textcolor=color.red)
            print('')
        else:
            # label.new(iLast, pLast, text=price_rotation_str, style=label.style_none, xloc=xloc.bar_time, yloc=yloc.abovebar, textcolor=color.green)
            print('')

def price_rotation_diff(pLast, price):
    if display_reversal_price_change:
        tmp_calc = price - pLast

        if difference_price == "Absolute":
            if np.sign(tmp_calc) > 0:
                src = "+"
            else:
                src = ""
            src += str.tostring(tmp_calc, format.mintick)
        else:
            if  np.sign(tmp_calc) > 0:
                src = "+"
            else:
                src = "-"
            src += str.tostring((math.abs(tmp_calc) * 100)/pLast, format.percent)


        str = "(" + str  + ")"
        return str
    else:
        ""

if __name__ == '__main__':
    print([iH, pH], [iL, pL])