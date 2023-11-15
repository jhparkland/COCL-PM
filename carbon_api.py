import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

def carbon_intensity(zone='KR', data='intensity', format='history'):
    '''
    - parameters -
    zone : region code (zone list : https://docs.google.com/document/d/e/2PACX-1vTdYp8E5E3fNogL54ICf_UxfA_rZ_RPO4WKWI4ZANPSX25jCbvHtAxc-VrJt9HymeRHFcSGWXjhVHS0/pub)
    lon : Longitude (if querying with a geolocation)
    lat : Latitude (if querying with a geolocation)
    - format -
    history : carbon intensity data during 24 hours (each 1 hours => total 24 data)
    latest : carbon intensity real-time data (1 data)
    forecast : the forecasted carbon intensity (in gCO2eq/kWh) of an area. It can either be queried by zone identifier or by geolocation.
    - output(json) -
    zone : region code
    carbonIntensity : carbon intensity (gCo2eq/kWh)
    datatime : data measure/estimate time
    updataedAt : data generation time
    emissionFactorType : type of emission factors used for computing the carbon intensity (lifecycle)
    estimatinMethod : if not estimated, value is null (null / Time slice average)
    '''
    # API endpoint URL
    url = f"https://api-access.electricitymaps.com/2w97h07rvxvuaa1g/carbon-{data}/{format}"
    # request parameter
    params = {
        'zone': zone
    }
    # Add API key to header
    headers = {
        'auth-token': os.getenv("CABONTOKEN")
    }
    # GET request
    response = requests.get(url, headers=headers, params=params)
    # Sucess request
    if response.status_code == 200:
        # request output
        data = json.dumps(response.json())
        data = {"carbon_intensity": json.loads(data)['history'][-1]['carbonIntensity']}
        return data
    else:
        # failed request
        print("Error:", response.status_code, response.text)
        return None

# carbon_intensity()