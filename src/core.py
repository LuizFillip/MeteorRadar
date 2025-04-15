import os 
import base as b
import datetime as dt 
import pandas as pd 
from tqdm import tqdm 

root = 'MeteorRadar/data/Cariri'

def replace_files(path_in):
    path_in = 'MeteorRadar/data/Cariri/'
    
    for fn in os.listdir(path_in):
        
        if fn.endswith('hwd'):    
            dn = dt.datetime.strptime(fn[2:10], '%Y%m%d')
        
            path_year = f'{path_in}{dn.year}'
            b.make_dir(path_year)
            month = dn.strftime('%m')
            path_month = f'{path_year}/{month}'
            b.make_dir(path_month)
            
            src = path_in + fn
            dst = f'{path_month}/{fn}'
            
            os.replace(src, dst)
    return None 
            
def fn2dn(fn):
    return dt.datetime.strptime(fn[2:10], '%Y%m%d')


def raw_file(infile):

    lines = open(infile).readlines()
    
    data = {
            'times': [], 
            'zonal': [], 
            'merid': [],
            'k, ht': []
            }
    
    for ln in lines:
        
        reader = ln[:6].strip()
        line = ln[6:].split()
   
        if reader in list(data.keys()):
            if len(line) == 24:
                data[reader].extend(line)
            else:
                data[reader].extend([line[2]] * 24)
                
    return data 

def MeteorData(infile, fn):
        
    df = pd.DataFrame(raw_file(infile + fn)) 
    
    df = df.astype(float)
    
    df['dt'] = fn2dn(fn)
    
    df['datetime'] = df['dt'] + pd.to_timedelta(
        df['times'], unit = 'h')
    
    df.set_index('datetime', inplace = True)
    df.drop(columns = ['dt', 'times'], inplace = True)
    df.rename(columns = {'k, ht': 'ht'}, inplace = True)
    df.replace(999.0, float('nan'), inplace = True)
    
    return df


def run_process(year):

    path_yr = f'{root}/{year}'
    
    out = []
    for folder in os.listdir(path_yr):
       
        infile = f'{path_yr}/{folder}/'
       
        for fn in tqdm(os.listdir(infile), folder):
            if fn.endswith('hwd'): 
                try:
                    out.append(MeteorData(infile, fn))
                except:
                    # print(fn)
                    continue 
    df = pd.concat(out).sort_index()
    
    df.to_csv(f'MeteorRadar/data/proc/{year}')
    
    return df

def main():
    
    for year in range(2019, 2023):
        
        run_process(year)
        

# year = 2018
# df = run_process(year)

# df 