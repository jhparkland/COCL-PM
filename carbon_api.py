import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

import requests
import os
import json

class CarbonIntensityAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api-access.electricitymaps.com/2w97h07rvxvuaa1g"

    def get_carbon_intensity(self, zone='KR', data='intensity', format='history'):
        url = f"{self.base_url}/carbon-{data}/{format}"
        params = {'zone': zone}
        headers = {'auth-token': self.api_key}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            # request output
            data = json.dumps(response.json())
            data = {"carbon_intensity": json.loads(data)['history'][-1]['carbonIntensity']}
            return data
        else:
            # failed request
            print("Error:", response.status_code, response.text)
            return None

# Usage
api_key = os.getenv("CABONTOKEN")
result = CarbonIntensityAPI(api_key).get_carbon_intensity(zone='KR', data='intensity', format='history')
if result:
    print(result)