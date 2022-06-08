import numpy as np
import pandas as pd
import zigzag

file_path = r"DOTUSDT-1m-2022-05.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

high = np.array(df['High'])
low = np.array(df['Low'])

if __name__ == '__main__':
    print(high, low, zigzag.zigzag(high, low))
    for (i_h, p_h),(i_l, p_l) in zigzag.zigzag(high, low):
        print(f'PEAK Index: {i_h}, price: {p_h}, VALLEY Index: {i_l}, price: {p_l}')