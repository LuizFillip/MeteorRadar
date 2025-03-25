import pandas as pd
import base as b 
import spectral as sp
import numpy as np 

infile = 'VM01A12D23.csv'
# df = b.load(infile)

df = pd.read_csv('VM01A12D23.csv', sep=';', decimal=',', encoding='latin1', low_memory=False)
df = df.T.reset_index(drop=True).T
df = df.rename(columns={0: "TIME", 2: "VVINST", 7: "VVMIN", 8: "VVMAX", 9: "DIRV", 16: "RAJV"})
df["TIME"] = pd.to_datetime(df["TIME"], format="%d/%m/%Y %H:%M", dayfirst=True)
df['VVINST'] = pd.to_numeric(df['VVINST'], errors='coerce')
df['VVMIN'] = pd.to_numeric(df['VVMIN'], errors='coerce')
df['VVMAX'] = pd.to_numeric(df['VVMAX'], errors='coerce')
df['DIRV'] = pd.to_numeric(df['DIRV'], errors='coerce')
df['RAJV'] = pd.to_numeric(df['RAJV'], errors='coerce')
df = df[['TIME', 'VVINST', 'VVMIN', 'VVMAX', 'DIRV', 'RAJV']]

df.set_index('TIME', inplace = True)

df.to_csv('test_1')

#%%%
import datetime as dt 

df = b.load('test_1')
ds = df.loc[df.index.date == dt.date(2023, 1, 17)]

ds['doy'] = ds.index.hour + (ds.index.minute / 60)

parameter = 'VVINST'

wave, spec = sp.quick_plot(ds, parameter, j1 = 7.5)

spec.ax_sst.set(
    ylabel = f'{parameter.title()} wind (m/s)',
    ylim = [0, 10]
    )

#%%%

# ds1 = pd.DataFrame(
#     wave.power, 
#     columns = wave.time, 
#     index = wave.period)

# ds2 = ds1.loc[
#     ((ds1.index > 2.5) & (ds1.index < 5)), 
#     ((ds1.columns > 5) & (ds1.columns < 10))
#     ]


# ds2.index

