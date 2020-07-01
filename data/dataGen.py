import pandas as pd
import dask.dataframe as dd
from dask.distributed import Client


#Load inventory file text file, compute as pandas, remove estraneous spaces, split into columns
if __name__ == 'dataGen':
    client = Client()

inventory = dd.read_csv('s3://noaa-ghcn-pds/ghcnd-inventory.txt',storage_options={'anon':True},
                    header=None,names=['Data']).compute()

inventory['Data'] = inventory['Data'].apply(lambda x: ' '.join(x.split()))

inventory = inventory['Data'].str.split(' ',expand=True)

inventory.columns=['station','latitude','longitude','measure','begin','end']

inventory = inventory.astype({'latitude':'float64','longitude':'float64','begin':'int64', 'end':'int64'})




