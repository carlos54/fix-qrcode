import requests
import json
import os
import sys
import shutil
import datetime
base_url = 'http://localhost:5000'
#base_url = 'https://mailing-api-test.statec.etat.lu/v1'


 

def get():
    r = requests.get(f'{base_url}/data')
    response = json.loads(r.content.decode("utf-8"))
    print(response)



def post():
    
    utc_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H%MZ")
    shutil.copyfile('data.json', f'backupdata_{utc_datetime}.json')#pour ne pas perdre les données si le POST passe
    file = {'data': open('./test/data_test.json','rb')}
    values = {"empty":"value"}
    r = requests.post(f'{base_url}/data', files=file,  data=values)
    if r.status_code == 200:
        response = json.loads(r.content.decode("utf-8"))
        print(response)
    else:
        print(r.content)
    


if __name__ == "__main__":
    run_fn = f'{sys.argv[1]}()'
    #print(os.getenv('FLASK_ENV', "vide"))
    exec(run_fn)


 
