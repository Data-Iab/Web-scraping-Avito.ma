from bs4 import BeautifulSoup
import requests
import urllib3
import pandas as pd
import numpy as np

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def make_soup(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    return BeautifulSoup(r.data,'html.parser')

def get_urls(soup):
    code = soup.find_all(lambda tag: tag.get('class') == ['fs14'])
    for i in range(len(code)):
        code[i] = code[i].a['href']
    return code

def get_title(soup):
    item = soup.find_all(class_='page-header mbm')
    return item[0].text

def get_price(soup):
    prix = soup.find_all(class_='amount value')
    try:
        return prix[0].text
    except:
        return np.nan

def get_info_generale(soup):
    info_generale = soup.find_all(class_ = 'font-normal fs12 no-margin ln22')
    info_generale_list = []
    for x in info_generale:
        info_generale_list.append(x.text)
    return info_generale_list

def get_info_detaille(soup):
    info_detaille_class = soup.find_all(class_ = 'span10')
    info_detaille_list = info_detaille_class[0].find_all('li')
    info_detaille_list2 = []
    for x in info_detaille_list:
        info_detaille_list2.append(x.text)
    return info_detaille_list2

def get_info_supp(soup):
    info_supp = soup.find_all(class_='ul-flex-column')
    info_supp_list = []
    for x in info_supp:
        info_supp_list.append(x.text)
    return info_supp_list

data = pd.DataFrame(columns=['Titre','Prix', 'Info generales', 'Info Detailles', 'Info Supplimentaires'])

premiere_page = 300
derniere_page = 400

for page in range(premiere_page,derniere_page):
    k=0
    soup = make_soup('https://www.avito.ma/fr/maroc/immobilier-%C3%A0_vendre?o='+str(page))
    urls = get_urls(soup)
    for url in urls:
        print('Scraping page: ')
        soup = make_soup(url)
        data = pd.concat([data,pd.DataFrame([[get_title(soup),get_price(soup),get_info_generale(soup),get_info_detaille(soup),
                                              get_info_supp(soup)]],
                        columns=['Titre','Prix', 'Info generales', 'Info Detailles', 'Info Supplimentaires'])])
        k+=1


def find_nombre_piece(listx):
    for x in listx:
        if 'Nombre de pièces' in x :
            if (x[23:len(x)-3] == '-'):
                return np.nan
            else:
                return x[23:len(x)-3]
    return np.nan

def find_surface_totale(listx):
    for x in listx:
        if 'Surface totale' in x:
            return x[19:len(x)-5]
    return np.nan

def find_secteur(listx):
    for x in listx:
        if 'Secteur' in x:
            return x[12:len(x)-3]
    return np.nan

def find_adresse(listx):
    for x in listx:
        if 'Adresse' in x:
            if (x[10:len(x)-1] == ' -'):
                return np.nan
            else :
                return x[10:len(x)-1]
    return np.nan

def find_type(listx):
    for x in listx:
        if 'Type' in x:
            return x[9:]
    return np.nan


data['Info generales'] = data['Info generales'].apply(str).apply(str.split,args=(','))

data['Nombre de pieces'] = data['Info generales'].apply(find_nombre_piece)
data['Type'] = data['Info generales'].apply(find_type)
data['Adresse'] = data['Info generales'].apply(find_adresse)
data['Secteur'] = data['Info generales'].apply(find_secteur)
data['Surface totale en m^2'] = data['Info generales'].apply(find_surface_totale)
del data['Info generales']

def find_salon(listx):
    for x in listx:
        if 'Salons' in x :
            return x[11:len(x)-2]
    return np.nan

def find_salle_bain(listx):
    for x in listx:
        if 'Salles de bain' in x :
            return x[20:len(x)-2]
    return np.nan

def find_Superficie_habitable(listx):
    for x in listx:
        if 'Superficie habitable' in x :
            return x[26:len(x)-4]
    return np.nan

def find_age_bien(listx):
    for x in listx:
        if 'Âge du bien' in x :
            return x[17:len(x)-2]
    return np.nan

def find_etage(listx):
    for x in listx:
        if 'Étage' in x :
            return x[10:len(x)-1]
    return np.nan

def find_frais_syndic(listx):
    for x in listx:
        if 'Frais de syndic / mois' in x :
            return x[27:len(x)-4]
    return '0'

data['Info Detailles'] = data['Info Detailles'].apply(str).apply(str.split,args=(','))

data['Salons'] = data['Info Detailles'].apply(find_salon)
data['Salles de bain'] = data['Info Detailles'].apply(find_salle_bain)
data['Etage'] = data['Info Detailles'].apply(find_etage)
data['Age du bien'] = data['Info Detailles'].apply(find_age_bien)
data['Superficie habitable'] = data['Info Detailles'].apply(find_Superficie_habitable)
data['Frais de syndic / mois'] = data['Info Detailles'].apply(find_frais_syndic)
del data['Info Detailles']



def Ascenseur(string):
    if 'Ascenseur' in string:
        return 'Oui'
    else:
        return 'Non'

def Balcon(string):
    if 'Balcon' in string:
        return 'Oui'
    else:
        return 'Non'


def Terrasse(string):
    if 'Terrasse' in string:
        return 'Oui'
    else:
        return 'Non'

def Cuisine_equipee (string):
    if 'Cuisine équipée ' in string:
        return 'Oui'
    else:
        return 'Non'

def Loti(string):
    if 'Loti' in string:
        return 'Oui'
    else:
        return 'Non'

def Jardin(string):
    if 'Jardin' in string:
        return 'Oui'
    else:
        return 'Non'

def Piscine(string):
    if 'Piscine' in string:
        return 'Oui'
    else:
        return 'Non'

def Concierge(string):
    if 'Concierge' in string:
        return 'Oui'
    else:
        return 'Non'

def Parking(string):
    if 'Parking' in string:
        return 'Oui'
    else:
        return 'Non'

def Chauffage(string):
    if 'Chauffage' in string:
        return 'Oui'
    else:
        return 'Non'

def Climatisation(string):
    if 'Climatisation' in string:
        return 'Oui'
    else:
        return 'Non'

def Meuble(string):
    if 'Meublé' in string:
        return 'Oui'
    else:
        return 'Non'

def Securite(string):
    if 'Sécurité' in string:
        return 'Oui'
    else:
        return 'Non'

def Garage(string):
    if 'Garage' in string:
        return 'Oui'
    else:
        return 'Non'

data['Info Supplimentaires'] = data['Info Supplimentaires'].apply(str)

data['Garage'] = data['Info Supplimentaires'].apply(Garage)
data['Securite'] = data['Info Supplimentaires'].apply(Securite)
data['Meuble'] = data['Info Supplimentaires'].apply(Meuble)
data['Climatisation'] = data['Info Supplimentaires'].apply(Climatisation)
data['Chauffage'] = data['Info Supplimentaires'].apply(Chauffage)
data['Parking'] = data['Info Supplimentaires'].apply(Parking)
data['Concierge'] = data['Info Supplimentaires'].apply(Concierge)
data['Piscine'] = data['Info Supplimentaires'].apply(Piscine)
data['Jardin'] = data['Info Supplimentaires'].apply(Jardin)
data['Loti'] = data['Info Supplimentaires'].apply(Loti)
data['Cuisine equipee'] = data['Info Supplimentaires'].apply(Cuisine_equipee)
data['Terrasse'] = data['Info Supplimentaires'].apply(Terrasse)
data['Ascenseur'] = data['Info Supplimentaires'].apply(Ascenseur)
data['Balcon'] = data['Info Supplimentaires'].apply(Balcon)

del data['Info Supplimentaires']

def regler_entier(x):
    try:
        return int(x)
    except:
        return np.nan

def remove_space(string):
    try:
        return string.replace(" ","")
    except:
        return np.nan

def nan(string):
    if string == 'nan':
        return np.nan
    else:
        return string

def fix_rez(element):
    try:
        return int(element)
    except:
        if type(element)==str:
            return 0
        return np.nan

def fix_pieces(element):
    try:
        if element == '10+':
            return 11
        else:
            return int(element)
    except:
        return np.nan


data.index = [i for i in range(len(data))]

import unidecode

data['Age du bien'] = data['Age du bien'].apply(str).apply(unidecode.unidecode).apply(nan)
data['Adresse'] = data['Adresse'].apply(str).apply(unidecode.unidecode).apply(nan)
data['Secteur'] = data['Secteur'].apply(str).apply(unidecode.unidecode).apply(nan)
data['Titre'] = data['Titre'].apply(str.split,args = ('\n')).apply(lambda x : x[1])
data['Nombre de pieces'] = data['Nombre de pieces'].apply(fix_pieces)
data['Prix'] = data['Prix'].apply(remove_space).apply(regler_entier)
data['Etage'] = data['Etage'].apply(fix_rez)


data = data[(data['Prix'] > 150000)]
data.to_csv("C:\\Workplace\\Mini projet inpt\\Données Avito.ma2.csv")