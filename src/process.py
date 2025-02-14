import base as b 
import spectral as sp
import numpy as np 

year = 2022

fname = f'MeteorRadar/data/proc/{year}'

df = b.load(fname)

df = df[(df["ht"] >= 88) & (df["ht"] <= 92)]


df = df.resample('3H').mean().interpolate()
# df = df.rolling('3H').mean().interpolate()

df['doy'] = df.index.day_of_year + (df.index.hour / 24)


parameter = 'merid'

spec = sp.quick_plot(df, parameter, j1 = 5.5)

spec.ax_sst.set(
    ylabel = f'{parameter.title()} wind (m/s)',
    ylim = [-200, 200]
    )

spec.ax_spec.set(yticks = np.arange(2, 12, 2))