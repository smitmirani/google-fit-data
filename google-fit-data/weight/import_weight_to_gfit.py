# -------------------------------------------------------------------------------
# Purpose: Load weights.csv and import to a Google Fit account
# Some codes refer to:
# 1. https://github.com/tantalor/fitsync
# 2. http://www.ewhitling.com/2015/04/28/scrapping-data-from-google-fitness/
import json
import os
import yaml
import httplib2
from googleapiclient.discovery import build

from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from read_weight_csv import read_weights_csv_with_gfit_format
from googleapiclient.errors import HttpError

# Setup for Google API:
# Steps:
# 1. Go https://console.developers.google.com/apis/credentials
# 2. Create credentials => OAuth Client ID
# 3. Set Redirect URI to your URL or the playground https://developers.google.com/oauthplayground
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (google-fit-data root)
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
SECRETS_FILE = os.path.join(PARENT_DIR, 'secrets.yml')

try:
    with open(SECRETS_FILE, 'r') as f:
        secrets = yaml.safe_load(f)
    if secrets is None:
        raise ValueError("secrets.yml file is empty or invalid")
    CLIENT_ID = secrets['client_id']
    CLIENT_SECRET = secrets['client_secret']
    # Redirect URI to google Fit, See Steps 3 above
    #REDIRECT_URI='https://developers.google.com/oauthplayground'
    REDIRECT_URI = secrets['redirect_uri']
    PROJECT_ID = secrets['project_id']
except FileNotFoundError:
    raise FileNotFoundError(
        f"secrets.yml file not found at {SECRETS_FILE}. "
        f"Please create this file with your Google API credentials."
    )
except KeyError as e:
    raise KeyError(
        f"Missing required key in secrets.yml: {e}. "
        f"Required keys: client_id, client_secret, redirect_uri, project_id, fitness_api_key"
    )

# See scope here: https://developers.google.com/fit/rest/v1/authorization
SCOPE = 'https://www.googleapis.com/auth/fitness.body.write'

# API Key
# Steps:
# 1. Go https://console.developers.google.com/apis/credentials
# 2. Create credentials => API Key => Server Key
try:
    API_KEY = secrets['fitness_api_key']
except KeyError:
    raise KeyError("Missing 'fitness_api_key' in secrets.yml")

def import_weight_to_gfit():
    # first step of auth
    # only approved IP is my Digital Ocean Server
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    auth_uri = flow.step1_get_authorize_url()
    print ("Copy this url to web browser for authorization: ")
    print (auth_uri)

    # hmm, had to manually pull this as part of a Google Security measure.
    # there must be a way to programatically get this, but this exercise doesn't need it ... yet...
    token = input("Copy the token from URL and input here: ")
    cred = flow.step2_exchange(token)
    http = httplib2.Http()
    http = cred.authorize(http)
    fitness_service = build('fitness','v1', http=http, developerKey=API_KEY)

    # init the fitness objects
    fitusr = fitness_service.users()
    fitdatasrc = fitusr.dataSources()

    data_source = dict(
        type='raw',
        application=dict(name='weight_import'),
        dataType=dict(
          name='com.google.weight',
          field=[dict(format='floatPoint', name='weight')]
        ),
        device=dict(
          type='scale',
          manufacturer='withings',
          model='smart-body-analyzer',
          uid='ws-50',
          version='1.0',
        )
      )

    def get_data_source_id(dataSource):
      return ':'.join((
        dataSource['type'],
        dataSource['dataType']['name'],
        PROJECT_ID,
        dataSource['device']['manufacturer'],
        dataSource['device']['model'],
        dataSource['device']['uid']
        ))

    data_source_id = get_data_source_id(data_source)

    print ('datasourceID')
    print(data_source_id)

    # Try to find existing data sources for weight
    try:
        list_response = fitness_service.users().dataSources().list(userId='me').execute()
        existing_sources = list_response.get('dataSource', [])

        # Look for an existing weight data source
        weight_source_id = None
        for source in existing_sources:
            if source.get('dataType', {}).get('name') == 'com.google.weight':
                weight_source_id = source.get('dataStreamId')
                print(f'Found existing weight data source: {weight_source_id}')
                break

        if weight_source_id:
            data_source_id = weight_source_id
        else:
            # Create new data source if none exists
            fitness_service.users().dataSources().create(
                userId='me',
                body=data_source).execute()
            print(f'Created new data source: {data_source_id}')
    except HttpError as error:
        print(f'Error checking data sources: {error}')
        # Try to use the computed data_source_id anyway
        pass

    weights = read_weights_csv_with_gfit_format()
    print('got weights...')
    min_log_ns = weights[0]["startTimeNanos"]
    max_log_ns = weights[-1]["startTimeNanos"]
    dataset_id = '%s-%s' % (min_log_ns, max_log_ns)

    # patch data to google fit
    fitness_service.users().dataSources().datasets().patch(
      userId='me',
      dataSourceId=data_source_id,
      datasetId=dataset_id,
      body=dict(
        dataSourceId=data_source_id,
        maxEndTimeNs=max_log_ns,
        minStartTimeNs=min_log_ns,
        point=weights,
      )).execute()

    # read data to verify
    print(fitness_service.users().dataSources().datasets().get(
        userId='me',
        dataSourceId=data_source_id,
        datasetId=dataset_id).execute())

if __name__=="__main__":
    import_weight_to_gfit()
