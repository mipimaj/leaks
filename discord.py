from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import datetime
import asyncio
import random
import requests
import json
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os
import pytz

webhook = ""
webhook2 = ""
takeLeaks = 100

nomLeaks = ""
lienLeaks = ""
lienLeaksWithAds = ""
LienLeaksTrue = False
imageLeaks = ""

oldName = ""
nameAndImage = -1
link = 7

loaded_data = {"leaks": []}

# Vérifier si le fichier 'database.json' existe déjà
if os.path.exists('database.json'):
   # Si le fichier existe, charger les données existantes
   with open('database.json', 'r') as f:
      loaded_data = json.load(f)
else:
   # Si le fichier n'existe pas, créer un nouveau dictionnaire
   # Écrire les données initiales dans le fichier JSON
   with open('database.json', 'w') as f:
      json.dump(loaded_data, f)


def get_dominant_color(image_url, num_clusters=3):
   # Télécharger l'image à partir du lien
   response = requests.get(image_url)
   image = Image.open(BytesIO(response.content))

   # Le reste du script reste le même
   image_np = np.asarray(image.resize((100, 100)), dtype=np.float32)
   pixels = image_np.reshape(-1, 3)

   # Utiliser KMeans pour trouver les couleurs les plus dominantes
   kmeans = KMeans(n_clusters=num_clusters)
   kmeans.fit(pixels)

   # Trouver l'étiquette la plus courante (c'est-à-dire la couleur la plus dominante)
   labels = kmeans.labels_
   counts = np.bincount(labels)
   dominant_color = kmeans.cluster_centers_[np.argmax(counts)]

   # Convertir la couleur dominante en hexadécimal
   dominant_color = dominant_color.astype(int)
   hex_color = '0x{:02x}{:02x}{:02x}'.format(*dominant_color)

   # Convertir la couleur hexadécimale en entier
   int_color = int(hex_color, 16)

   return int_color

lien = "https://pornleaks.in/packs.php"

options = Options()
options.add_extension("AdGuard AdBlocker 4.3.35.0.crx")
# options.add_argument("--headless=new")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
   service=ChromeService(ChromeDriverManager().install()),
   options=options
   )


def timeClock():
   global nameAndImage, link
   print("ok")
   nameAndImage = -1
   link = 7
   time.sleep(600)
   dataToReceive()

def sendToDiscord(colorHexa):
   global webhook, nomLeaks, lienLeaks, imageLeaks, lienLeaksWithAds, LienLeaksTrue
   if LienLeaksTrue == False:
      data = {
         "username": "Leaks KhaosRevelation",
         "embeds": [
            {
                  "image": {
                     "url": f"{imageLeaks}"
                  },
                  "fields": [
                     {"name": f"{nomLeaks}", "value": f"lien du leaks ci dessous: \n{lienLeaksWithAds if LienLeaksTrue == False else lienLeaks}", "inline": False},
                     {"name": "Publicité", "value": f"Gagner de l'argent gratuitement et facilement : \n https://r.honeygain.me/MIGUE32364", "inline": False},
                     {"name": "Nous soutenir", "value": f"Vous pouvez faire des dons PayPal ci dessous \n https://www.paypal.com/paypalme/khaosrevelation \n merci à tous ceux qui nous soutienne", "inline": False}
                  ],
                  "color": colorHexa,
                  "timestamp": str(datetime.datetime.utcnow().isoformat()) + "Z"    # Format ISO 8601
            }
         ]
      }
   else:
      data = {
         "username": "Leaks KhaosRevelation",
         "embeds": [
            {
                  "image": {
                     "url": f"{imageLeaks}"
                  },
                  "fields": [
                     {"name": f"{nomLeaks}", "value": f"lien du leaks ci dessous: \n{lienLeaks}", "inline": False}
                  ],
                  "color": colorHexa,
                  "timestamp": str(datetime.datetime.utcnow().isoformat()) + "Z"    # Format ISO 8601
            }
         ]
      }

   # Envoie l'embed via le webhook
   response = requests.post(webhook if LienLeaksTrue == False else webhook2, json=data)

   if response.status_code == 204:
      pass
      print("Webhook envoyé avec succès !")
   else:
      pass
      print(f"Erreur lors de l'envoi du webhook. Code de réponse : {response.status_code}")

   LienLeaksTrue = True


def getData(nameAndImage, link):
   global nomLeaks, lienLeaks, imageLeaks, oldName, loaded_data, lienLeaksWithAds, LienLeaksTrue

   LienLeaksTrue = False

   nom = driver.find_elements(By.CSS_SELECTOR, "[style='font-size:16px !important; overflow: hidden !important;']")
   print(nom[nameAndImage].text)
   nomLeaks = nom[nameAndImage].text

   # Vérifier si nomLeaks existe déjà dans les données chargées
   if nomLeaks in loaded_data["leaks"]:
      print("leaks déjà existant")
   else:
      driver.get(lien)
      time.sleep(5)
      # Ajouter la nouvelle valeur au début de la liste
      loaded_data["leaks"].insert(0, nomLeaks)

      if nomLeaks != oldName:

         with open('database.json', 'w') as f:
            json.dump(loaded_data, f)
         
         oldName = nomLeaks
         imageLien = driver.find_elements(By.CSS_SELECTOR, '[loading="lazy"]')
         print(imageLien[nameAndImage].get_attribute('src'))
         imageLeaks = imageLien[nameAndImage].get_attribute('src')

         links = driver.find_elements(By.TAG_NAME, "a")
         print(links[link].get_attribute('href'))
         time.sleep(1)
         driver.get(links[link].get_attribute('href'))
         time.sleep(1)
         lienWithNoAds = driver.find_elements(By.TAG_NAME, "a")
         print(lienWithNoAds[0].get_attribute('href'))

         lienLeaks = lienWithNoAds[0].get_attribute('href')
         time.sleep(1)

         url = "https://dash-api.work.ink/v1/link"

         payload = {
            "title": f"{nomLeaks}",
            "destination": f"{lienLeaks}",
            "custom": f"{nomLeaks + str(random.randint(10000, 99999))}"
         }
         headers = {
            "X-Api-Key": "fef9f2ad-1bbf-4913-ae51-8190d4b1a70b",
            "Content-Type": "application/json"
         }

         response = requests.request("POST", url, json=payload, headers=headers)

         print(response.text)

         response_json = json.loads(response.text)

         lienLeaksWithAds = response_json["response"]["url"]

         getColor = get_dominant_color(imageLeaks)

         print(getColor)

         print(f"Le lien extrait est : {lienLeaks}")

         sendToDiscord(getColor)
         sendToDiscord(getColor)

def dataToReceive():
   global nameAndImage, link, takeLeaks
   for i in range(takeLeaks):
      link += 3
      nameAndImage += 1
      getData(nameAndImage, link)
      time.sleep(1)

   timeClock()


timeClock()