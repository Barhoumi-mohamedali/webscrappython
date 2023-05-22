import requests
from bs4 import BeautifulSoup
import mysql.connector
import json

# Connexion à la base de données MySQL
cnx = mysql.connector.connect(user='root', password='barhoumi@0011',
                              port=3306,
                              host='192.168.94.131',
                              database='webscraping')
cursor = cnx.cursor()


# Extraction des données du site Web
url = 'https://www.usine-digitale.fr/cybersecurite/'

headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

response = requests.get(url,headers=headers).text
soup = BeautifulSoup(response, 'html.parser')
data = []
data_appended =[]
my_array=[]
page=soup.find_all('div', class_='editoCardType10__content')

# Parcourez les éléments HTML pour extraire les données souhaitées
for item in page:
    try:
        valtitre= item.find('h2', class_='editoCardType10__title').text

    except:
        valtitre = 'no titte found!'
    try:
        valarticle= item.find('p', class_='editoCardType10__text is-noMobile').text
        
    except:
           valtitre = 'no titte found!'
      
   # put data in dictionnary format
    data = {
        "valtitre":valtitre.strip(),
        "valarticle" : valarticle.strip()
     }
    #append data 
    data_appended=data_appended+ [data]
    
    for dictionary in [data]:
    # Step 4: Append each dictionary to the array
          my_array.append(dictionary)
         
          my_array_dumps=json.dumps(my_array,ensure_ascii=False)
          titre = dictionary["valtitre"]
          article = dictionary["valarticle"]
          
          query = "INSERT INTO webscrappingdata(titre, article) VALUES (%s, %s)"
          cursor.execute(query, (titre, article))
          # for key, value in dictionary.items():
          #   print(f"Ceci est la clé : {key} et ceci est la valeur : {value}")
         
print(my_array_dumps)

# Enregistrement des modifications et fermeture de la connexion
cnx.commit()
cursor.close()
cnx.close()     
