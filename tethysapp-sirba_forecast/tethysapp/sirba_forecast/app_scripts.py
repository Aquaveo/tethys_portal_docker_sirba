from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#import smtplib, sys, shapely, rasterio, netCDF4, datetime, georaster, requests, os, shutil, warnings, logging
import smtplib, sys, datetime, requests, os, shutil, warnings, logging
import numpy as np
#import rasterio.mask
import pandas as pd
#import geopandas as gpd
#import xarray as xr
#from rasterio import features
#from shapely.geometry import box

#logging.basicConfig(filename='/home/ubuntu/subprocess/nasaaccess.log',level=logging.INFO)

def send_email(to_email, unique_id):

    from_email = 'bernard.minoungou.bfa@gmail.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Your VIC output data is ready'

    msg['From'] = from_email
    msg['To'] = to_email

    #email content
    message = """\
        <html>
            <head></head>
            <body>
                <p>Hello,
                   <br>
                   Your historical VIC data is ready for download at 
                   <a href="http://tethys-agrhymet/apps/historical_data_service">
                        http://tethys-agrhymet/apps/historical_data_service
                   </a>
                   <br>
                   Your unique access code is: <strong>""" + unique_id + """</strong><br>
                </p>
            </body>
        <html>
    """

    part1 = MIMEText(message, 'html')
    msg.attach(part1)

    gmail_user = 'bernard.minoungou.bfa@gmail.com'
    gmail_pwd = 'XXXXXXXXXXX'
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_pwd)
    smtpserver.sendmail(gmail_user, to_email, msg.as_string())
    smtpserver.close()

#  read in file paths and arguments from subprocess call in model.py
email = sys.argv[1]
unique_id=sys.argv[2]



#  when data is ready, send the user an email with their unique access code
send_email(email, unique_id)

#logging.info("Complete!!!")