import os, datetime, logging
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.files import File
from .config import *
from .model import *
from .app import SirbaForecast
from netCDF4 import *
import pandas as pd
import datetime as datetime

logging.basicConfig(filename=sirba_log,level=logging.INFO)

def run_historical(request):

    """
    Controller to call nasaaccess R functions.
    """
    # Get selected parameters and pass them into nasaccess R scripts
    try:
        start = request.POST.get('startDate')
        d_start = str(datetime.datetime.strptime(start, '%b %d, %Y').strftime('%Y-%m-%d'))
        end = request.POST.get(str('endDate'))
        d_end = str(datetime.datetime.strptime(end, '%b %d, %Y').strftime('%Y-%m-%d'))
        select_comid = request.POST.get('select_comid')
        d_comid = select_comid
        #d_comid = int(select_comid)
        select_variable = request.POST.get('select_variable')
        #unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        #unique_path = os.path.join(user_workspaces, 'outputs', unique_id, 'historical_data')
        #unique_path='C:/Users/minou/tethysdev/tethysapp-sirba_forecast/tethysapp/sirba_forecast/workspaces/user_workspaces/outputs'
        #os.makedirs(unique_path) 
        #os.chmod(unique_path, 0o777)
        email = request.POST.get('email')
        result = historical_run(select_variable,d_comid, d_start, d_end, email)
        #result=historical_run(select_variable,d_comid, d_start, d_end, unique_path)
        return JsonResponse({'Result': str(result)})
    except Exception as e:
        #return JsonResponse({'Error': "Il retrouve la fonction"})
        return JsonResponse({'Error': str(e)})

def download_data(request):
    """
    Controller to download data using a unique access code emailed to the user when their data is ready
    """
    if request.method == 'POST':
        #get access code from form
        access_code = request.POST['access_code']

        #identify user's file path on the server
        unique_path = os.path.join(user_workspaces, 'outputs', access_code, 'historical_data')
        #unique_path = os.path.join(data_path, 'outputs', access_code)

        #compress the entire directory into a .zip file
        def zipfolder(foldername, target_dir):
            zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
            #zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_STORED)
            rootlen = len(target_dir) + 1
            for base, dirs, files in os.walk(target_dir):
                for file in files:
                    fn = os.path.join(base, file)
                    zipobj.write(fn, fn[rootlen:])

        zipfolder(unique_path, unique_path)

        #open the zip file
        path_to_file = os.path.join(user_workspaces, 'outputs', access_code, 'historical_data.zip')
        #f = open(path_to_file, 'r')
        f = open(path_to_file, 'r', encoding="ISO-8859-1")
        #f = open(path_to_file, 'r', errors="ignore")
        myfile = File(f)

        #download the zip file using the browser's download dialogue box
        response = HttpResponse(myfile, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=historical_data.zip'
        return response