import httplib2
import pandas as pd
import time

from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from requests.exceptions import HTTPError

#On renseigne ID_client, le code secret client, et le nom du fichier XLS se trouvant
#dans le meme repertoire que le projet Python
clientId = 'ID_client'
clientSecret = 'Code_Secret_Du_Client'
listLocation = 'FICHIER.xls'


df = pd.read_excel(listLocation, sheet_name='sheeet') # Nom de la feuille xls
website_list = df['Complete URL'].tolist() # on recup la colonne
website_list_clean = [website for website in website_list if str(website) != "nan"]

OAUTH_SCOPE = 'https://www.googleapis.com/auth/webmasters'

REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

flow = OAuth2WebServerFlow(clientId, clientSecret, OAUTH_SCOPE, REDIRECT_URI)
authorize_url = flow.step1_get_authorize_url()
print('Copier/Collez le lien suivant sur votre navigateur: ' + authorize_url)
code = input('Entrez le code de verification donné par Google: ').strip()
credentials = flow.step2_exchange(code)

http = httplib2.Http()
http = credentials.authorize(http)

webmasters_service = build('webmasters', 'v3', http=http)

for website in website_list_clean:
  try:
    webmasters_service.sites().add(siteUrl=website).execute()
  except Exception as err:
    print(f'Other error occurred: {err}')
  else:
    print(website+" a été ajouté à votre GSC!")
    time.sleep(5)
