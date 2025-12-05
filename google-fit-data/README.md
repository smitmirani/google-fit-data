# google-fit-data
Load bulk weight/steps data to a Google Fit account

# Secrets

Create a file named `secrets.yml` in the root directory (`google-fit-data/`) with your Google API credentials in YAML format:

```yaml
client_id: 'YOUR CLIENT ID'
client_secret: 'YOUR CLIENT SECRET'
fitness_api_key: 'YOUR FITNESS API KEY'
redirect_uri: 'http://localhost'
project_id: 'YOUR PROJECT ID'
```

**📖 Detailed Setup Instructions:** See [GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md) for step-by-step instructions on how to obtain all Google API credentials.

**Note:** The `secrets.yml` file should be in the root directory of the project (same level as `requirements.txt`). This file is already in `.gitignore` to keep your credentials secure.

## Download and installation
```
git clone https://github.com/ryanpconnors/google-fit-data.git
cd google-fit-data
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Import weight data into Google Fit
```
python weight/import_weight_to_gfit.py
```

## Import steps data into Google Fit
```
python steps/import_steps_to_gfit.py
```
