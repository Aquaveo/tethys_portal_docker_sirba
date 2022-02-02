from django.db import models
import os, random, string, subprocess, requests, shutil, logging, zipfile
from .config import *
from tethys_sdk.services import get_spatial_dataset_engine
from netCDF4 import *
import pandas as pd
import datetime as datetime

logging.basicConfig(filename=sirba_log,level=logging.INFO)



# Model for data access form
class accessCode(models.Model):
    access_code = models.CharField(max_length=6)


def historical_run(select_variable,comid, start, end, email):
    if(select_variable=='Discharge'):
        try:
            data_dir= os.path.join(app_workspace,  'Qout_riv_pfaf_sirba_1981_2010_bon.nc')
            #data_dir= 'C:/Users/minou/tethysdev/Qout_riv_pfaf_sirba_1981_2010_bon.nc'
            r1 = Dataset(data_dir)
            rr1 = r1.variables['rivid'][:].tolist()
            #Le COMID de l'exutoire vaut 14032264
            #basin_index=rr1.index(comid)
            basin_index=rr1.index(14032264)
            sim=r1.variables['Qout'][:,basin_index]
            obstimes = pd.date_range('1981-01-01','2010-12-31',freq='D')
            sim = pd.Series(sim)
            obstimes = pd.Series(obstimes)
            frame = { 'Dates': obstimes, 'Qsim': sim }
            result = pd.DataFrame(frame)
            result.set_index('Dates')
            mask = result.loc[(result['Dates']>=start) & (result['Dates']<=end)]
            #create a new folder to store the user's requested data
            unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            unique_path = os.path.join(user_workspaces, 'outputs', unique_id, 'historical_data')
            os.makedirs(unique_path) 
            os.chmod(unique_path, 0o777)
            mask.to_csv(unique_path+'/'+'output.csv',index = False)
            
            run = subprocess.call([nasaaccess_py3, nasaaccess_script, email, unique_id])
            return "The historical discharge is saved"
            
        except Exception as e:
            logging.info(str(e))
            return str(e)