import sys
import os
import yaml
import httplib2
from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from googleapiclient.errors import HttpError

# Get secrets
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_FILE = os.path.join(SCRIPT_DIR, 'secrets.yml')

with open(SECRETS_FILE, 'r') as f:
    secrets = yaml.safe_load(f)
    CLIENT_ID = secrets['client_id']
    CLIENT_SECRET = secrets['client_secret']
    REDIRECT_URI = secrets['redirect_uri']
    PROJECT_ID = secrets['project_id']
    API_KEY = secrets['fitness_api_key']

SCOPE = 'https://www.googleapis.com/auth/fitness.body.write'

def delete_weight_data(authorization_code):
    # Authorize
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    auth_uri = flow.step1_get_authorize_url()
    print("Copy this url to web browser for authorization: ")
    print(auth_uri)

    cred = flow.step2_exchange(authorization_code)
    http = httplib2.Http()
    http = cred.authorize(http)
    fitness_service = build('fitness','v1', http=http, developerKey=API_KEY)

    # List existing data sources
    list_response = fitness_service.users().dataSources().list(userId='me').execute()
    existing_sources = list_response.get('dataSource', [])

    # Find weight data source
    weight_source_id = None
    for source in existing_sources:
        if source.get('dataType', {}).get('name') == 'com.google.weight':
            weight_source_id = source.get('dataStreamId')
            print(f'Found weight data source: {weight_source_id}')
            break

    if not weight_source_id:
        print('No weight data source found')
        return

    # Delete all data from this data source
    # Use a very large time range to delete all data
    dataset_id = '0-9999999999000000000'  # From epoch to far future

    try:
        fitness_service.users().dataSources().datasets().delete(
            userId='me',
            dataSourceId=weight_source_id,
            datasetId=dataset_id).execute()
        print('Successfully deleted weight data')
    except HttpError as error:
        print(f'Error deleting data: {error}')

if __name__ == "__main__":
    auth_code = "4/0ATX87lPHnJ7tvWWwGojbBM7K2aUmSX7sMiWoubsqWaumZ06-RIOwmqb2IjpgZuW82qnTfw"
    delete_weight_data(auth_code)
