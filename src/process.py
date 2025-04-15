import base as b 
import spectral as sp
import numpy as np 
import matplotlib.pyplot as plt


def plot(df):
   
    
    df['doy'] = df.index.day_of_year + (df.index.hour / 24)
    
    parameter = 'merid'
    
    spec = sp.quick_plot(df, parameter, j1 = 5.5)
    
    spec.ax_sst.set(
        ylabel = f'{parameter.title()} wind (m/s)',
        ylim = [-200, 200]
        )
    
    spec.ax_spec.set(yticks = np.arange(2, 12, 2))


year = 2018

def meteor_data(year):
    
    fname = f'MeteorRadar/data/proc/{year}'
    
    df = b.load(fname)
    
    df = df[(df["ht"] >= 88) & (df["ht"] <= 92)]
     
    df = df.resample('3H').mean().interpolate()
    
    df['doy'] = df.index.day_of_year + (df.index.hour / 24)
    return df 

def main():

    for year in range(2018, 2023):
        
        df = meteor_data(year)
        
        for p in ['zonal', 'merid']:
    
            wv = sp.quick_plot(df, p, j1 = 5.5)
            
            path = f'SpectralData/Meteor/{year}_{p}'
            
            wv.fig.savefig(path)
