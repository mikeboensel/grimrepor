from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_refresh_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',  # Download this from Google Cloud Console
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    
    # Save credentials for future use
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    print(f"Refresh Token: {creds.refresh_token}")

if __name__ == '__main__':
    get_refresh_token()