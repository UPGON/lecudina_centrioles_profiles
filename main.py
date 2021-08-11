import re

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def main():
    data_raw = pd.read_excel('data/Lecudina.xlsx', sheet_name='Sheet2')
    data = data_raw.copy()
    data = data.drop('Picture ID', axis=1)
    picture_id_row = data.columns
    container = {}

    length_target = 112

    col_curr = None
    roi_type = ''
    roi_id = -1
    profile = None

    x = np.linspace(0, 1, length_target, endpoint=True)

    for c, col in enumerate(picture_id_row):
        print(c)
        if not col.startswith('Unnamed'):
            col_curr = col
            profile = data.iloc[1:, c].dropna().to_numpy()
        else:
            roi = data.iloc[0, c]
            if type(roi) != str:
                continue
            match = re.match(r'^([Aa]xonema|[Bb]asal [Bb]ody) ([MCIVX]+)$', roi)

            if len(match.groups()) == 2:
                roi_type, roi_id = match.groups()

            intensities = data.iloc[1:, c].dropna().to_numpy()
            f = interp1d(profile, intensities, fill_value='extrapolate')

            container[(col_curr, roi_type, roi_id)] = f(x).astype(np.uint8)

    profile_df = pd.DataFrame(container, index=x.round(3))
    profile_df = profile_df.T
    profile_df.index.set_names(['picture', 'roi', 'replicate'], inplace=True)
    profile_df = profile_df.reset_index()
    profile_df.to_excel('out/profiles_interp.xlsx', index=False)


if __name__ == '__main__':
    main()
