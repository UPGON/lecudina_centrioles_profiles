import re

import cv2
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


def main():
    data_raw = pd.read_excel('data/Lecudina.xlsx', sheet_name='Sheet2')
    data = data_raw.copy()
    data = data.drop('Picture ID', axis=1)
    picture_id_row = data.columns
    container = {}

    length_target = 32

    col_curr = None
    l1, l2, l3 = -1, -1, -1
    roi_type = ''
    roi_id = -1
    pic_n = len([i for i in picture_id_row if i.startswith('Unnamed')])
    image_profiles = np.zeros((pic_n, length_target), dtype=np.uint8)
    profile_inc = 0

    for c, col in enumerate(picture_id_row):
        if not col.startswith('Unnamed'):
            col_curr = col
            # l1, l2, l3 = [int(l) for l in col_curr.split('_')]
            profile = data.iloc[1:, c].dropna().to_numpy()
            print(profile.max())
        else:
            roi = data.iloc[0, c]

            if type(roi) != str:
                continue
            match = re.match(r'^([Aa]xonema|[Bb]asal [Bb]ody) ([MCIVX]+)$', roi)

            if len(match.groups()) == 2:
                roi_type, roi_id = match.groups()

            intensities = data.iloc[1:, c].dropna().to_numpy()

            intensities_int = intensities.astype(np.uint8)
            resampled = cv2.resize(intensities_int, (1, length_target))
            resampled = resampled.flatten().T
            image_profiles[profile_inc, :] = resampled
            profile_inc += 1
            container[(col_curr, roi_type, roi_id)] = resampled

    cv2.imwrite('out/profile.png', image_profiles)

    print(0)


if __name__ == '__main__':
    main()
