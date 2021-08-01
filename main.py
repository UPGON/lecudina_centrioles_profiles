import re

import numpy as np
import pandas as pd
from scipy import interpolate

from matplotlib import pyplot as plt


def main():
    data_raw = pd.read_excel('data/Lecudina.xlsx', sheet_name='Sheet2')
    data = data_raw.copy()
    data = data.drop('Picture ID', axis=1)
    picture_id_row = data.columns
    container = {}

    col_curr = None
    l1, l2, l3 = -1, -1, -1
    roi_type = ''
    roi_id = -1
    for c, col in enumerate(picture_id_row):
        print(c, col)
        if not col.startswith('Unnamed'):
            print(f'\nCreating new sub df from {c, col}')
            col_curr = col
            l1, l2, l3 = [int(l) for l in col_curr.split('_')]
            container[(l1, l2, l3, 'x')] = data.iloc[1:, c].to_numpy()
        else:
            print(f'...adding new roi to sub df {col_curr}')
            roi = data.iloc[0, c]

            if type(roi) != str:
                continue
            match = re.match(r'^([Aa]xonema|[Bb]asal [Bb]ody) ([MCIVX]+)$', roi)
            if len(match.groups()) == 2:
                roi_type, roi_id = match.groups()
                profile = data.iloc[1:, c].dropna().to_numpy()
                interpolated = profile
                container[(l1, l2, l3, roi_type, roi_id)] = interpolated

    fig, ax = plt.subplots(1, 1)
    for k, v in container.items():
        ax.plot(v)
    fig.savefig('out/fig.pdf')

    print(0)


if __name__ == '__main__':
    main()
