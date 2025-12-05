# Google API Credentials Setup Guide

This guide will walk you through obtaining all the necessary Google API credentials for the Google Fit Data import scripts.

## Prerequisites

- A Google account
- Access to Google Cloud Console

## Step-by-Step Instructions

### Step 1: Create or Select a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click **"New Project"** (or select an existing project)
4. Enter a project name (e.g., "Google Fit Data Import")
5. Click **"Create"**
6. Wait for the project to be created, then select it from the dropdown

**Note:** Your **Project ID** is displayed in the project dropdown. It's usually in the format: `your-project-name-123456`. You'll need this later.

### Step 2: Enable Google Fitness API

1. In the Google Cloud Console, go to **"APIs & Services"** > **"Library"**
2. Search for **"Fitness API"**
3. Click on **"Fitness API"**
4. Click **"Enable"**
5. Wait for the API to be enabled

### Step 3: Create OAuth 2.0 Client ID Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"OAuth client ID"**
4. If prompted, configure the OAuth consent screen:
   - Choose **"External"** (unless you have a Google Workspace account)
   - Click **"Create"**
   - Fill in the required fields:
     - **App name**: "Google Fit Data Import" (or any name)
     - **User support email**: Your email
     - **Developer contact information**: Your email
   - Click **"Save and Continue"**
   - On the Scopes page, click **"Save and Continue"** (no need to add scopes here)
   - On the Test users page, add your email address, then click **"Save and Continue"**
   - Review and click **"Back to Dashboard"**

5. Now create the OAuth Client ID:
   - **Application type**: Select **"Web application"**
   - **Name**: "Google Fit Data Import Client" (or any name)
   - **Authorized redirect URIs**: Add one of these:
     - `http://localhost` (for local development)
     - `https://developers.google.com/oauthplayground` (alternative)
   - Click **"Create"**

6. A popup will appear with your credentials:
   - **Your Client ID**: Copy this (looks like: `1)
   - **Your Client Secret**: Copy this (looks like: ``)

**⚠️ Important:** Save these credentials securely. You won't be able to see the client secret again after closing this popup.

### Step 4: Create API Key

1. Still in **"APIs & Services"** > **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** again
3. Select **"API key"**
4. A popup will appear with your API key (looks like: ``)
5. Click **"Restrict key"** (recommended for security):
   - Under **"API restrictions"**, select **"Restrict key"**
   - Check **"Fitness API"**
   - Click **"Save"**

**⚠️ Important:** Copy and save your API key.

### Step 5: Get Your Project ID

1. In Google Cloud Console, click on the project dropdown at the top
2. Your **Project ID** is displayed there (it's different from the Project Name)
3. It usually looks like: `health-data-transfer-480313`

### Step 6: Create the secrets.yml File

1. In your project root directory (`/Users/smit.mirani/repos/google-fit-data/`), create a file named `secrets.yml`
2. Copy the template below and fill in your actual credentials:

```yaml
client_id: 'YOUR_CLIENT_ID_HERE'
client_secret: 'YOUR_CLIENT_SECRET_HERE'
fitness_api_key: 'YOUR_API_KEY_HERE'
redirect_uri: 'http://localhost'
project_id: 'YOUR_PROJECT_ID_HERE'
```

### Step 7: Verify Your Setup

1. Make sure `secrets.yml` is in the root directory: `/Users/smit.mirani/repos/google-fit-data/secrets.yml`
2. Verify the file format is correct (YAML syntax, proper indentation)
3. Make sure all values are in quotes (single or double quotes are fine)

## Security Notes

- **Never commit `secrets.yml` to version control!** It contains sensitive credentials.
- The `.gitignore` file should include `secrets.yml` (check if it exists)
- Keep your credentials secure and don't share them publicly
- If you accidentally commit credentials, rotate them immediately in Google Cloud Console

## Troubleshooting

### "Invalid credentials" error
- Double-check that you copied the credentials correctly (no extra spaces)
- Make sure the Fitness API is enabled in your project
- Verify the redirect_uri matches what you configured in OAuth Client ID

### "API key not valid" error
- Make sure the API key is not restricted incorrectly
- Verify the Fitness API is enabled
- Check that the API key has access to Fitness API

### "Project not found" error
- Verify your Project ID is correct (not the Project Name)
- Make sure you're using the Project ID, not the Project Number

## Quick Reference: What Goes Where

| Credential | Where to Find It | Format Example |
|------------|------------------|----------------|
| `client_id` | OAuth 2.0 Client ID credentials | `123456789-abc...apps.googleusercontent.com` |
| `client_secret` | OAuth 2.0 Client ID credentials | `GOCSPX-abc...` |
| `fitness_api_key` | API Key credentials | `AIzaSyAbC...` |
| `redirect_uri` | You configure this | `http://localhost` |
| `project_id` | Project dropdown in Cloud Console | `my-project-123456` |

## Need Help?

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Fit API Documentation](https://developers.google.com/fit/rest)
- [OAuth 2.0 Setup Guide](https://developers.google.com/identity/protocols/oauth2)

