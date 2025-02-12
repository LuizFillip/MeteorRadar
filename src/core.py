import os 
import base as b
import datetime as dt 
import pandas as pd 

def replace_files():
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
    
    for f in lines:
        
        reader = f[:6].strip()
        
        line = f[6:].split()
        
        keys = list(data.keys())
        if reader in keys:
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
    df.drop(columns=['dt', 'times'], inplace = True)
    df.rename(columns = {'k, ht': 'ht'}, inplace = True)
    
    df = df.replace(999.0, float('nan'))
    
    return df

root = 'MeteorRadar/data/Cariri'

def run_process():

    for year in range(2019, 2023):
        dates = pd.date_range(
            f'{year}-01-01', 
            freq= '1M', periods = 12)
        
        out = []
        for dn in dates:
            mon = dn.strftime('%m')
            infile = f'{root}/{dn.year}/{mon}/'
           
            for fn in os.listdir(infile):
                if fn.endswith('hwd'): 
                   out.append(MeteorData(infile, fn))
         
        df = pd.concat(out)
        
        df.to_csv(f'{year}')
