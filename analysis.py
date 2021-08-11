import pandas as pd
from matplotlib import pyplot as plt


def main():
    data = pd.read_excel('out/profiles_interp.xlsx', index_col=[0, 1, 2], header=0)

    summarised = data.groupby(['picture', 'roi']).std()
    plt.pcolor(summarised.sort_index(level='roi'), cmap='cividis')
    plt.xlabel('Distance [0-1 um]')
    plt.ylabel('Profile')
    plt.savefig('out/heatmap.png')

    picture_names = data.index.get_level_values(0).unique()
    roi_names = data.index.get_level_values(1).unique()

    fig, axs = plt.subplots(nrows=len(picture_names),
                            ncols=len(roi_names),
                            figsize=(5, 15))

    for p, pic in enumerate(picture_names):
        ax = axs[p, :]
        sub = data.loc[pic, :]

        for r, roi in enumerate(roi_names):
            sax = ax[r]
            ssub = sub.loc[roi, :]
            sax.plot(ssub.mean(), color='blue', lw=1, ls='-', alpha=1)

            for _, prof in ssub.iterrows():
                sax.plot(prof, color='blue', lw=.5, ls='-', alpha=.2)
                sax.set_xlim(0, 1)
                # sax.set_ylim(0, 50)
                sax.spines['top'].set_visible(False)
                sax.spines['right'].set_visible(False)
                sax.spines['bottom'].set_visible(False)
                sax.xaxis.set_visible(False)
                sax.set_title(f'{pic} {roi.lower()}')

    fig.tight_layout()
    fig.savefig('out/plot.png', dpi=300)
    print(0)


if __name__ == '__main__':
    main()
