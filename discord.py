from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import asyncio
import random
import requests
import json
import requests
from io import BytesIO
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

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
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
   service=ChromeService(ChromeDriverManager().install()),
   options=options
   )

webhook = "https://discord.com/api/webhooks/1226579210097918124/1cQLRw8gQ_AM3dES0b2dnEX4hWBt5BKckz_2knkQyj4mL7JEdBbd6RsB5SKwTN9Tr026"
nomLeaks = ""
lienLeaks = ""
imageLeaks = ""
timeStop = 3

oldName = ""

def timeClock():
   global timeStop
   if timeStop >= 0:
      timeStop -= 1
      print(timeStop)
      time.sleep(1)
      timeClock()
   else:
      timeStop = 3
      getData()

def sendToDiscord(colorHexa):
   global webhook, nomLeaks, lienLeaks, imageLeaks
   data = {
      "username": "Leaks KhaosRevelation",
      "embeds": [
         {
               "image": {
                  "url": f"{imageLeaks}"
               },
               "fields": [
                  {"name": f"{nomLeaks}", "value": f"lien du leaks ci dessous: \n{lienLeaks}", "inline": False},
                  {"name": "Publicité", "value": f"Gagner de l'argent gratuitement et facilement : \n https://r.honeygain.me/MIGUE32364", "inline": False}
               ],
               "color": colorHexa,
         }
      ]
   }

   # Envoie l'embed via le webhook
   response = requests.post(webhook, json=data)

   if response.status_code == 204:
      pass
      print("Webhook envoyé avec succès !")
   else:
      pass
      print(f"Erreur lors de l'envoi du webhook. Code de réponse : {response.status_code}")

   timeClock()

def getData():
   global nomLeaks, lienLeaks, imageLeaks, oldName

   driver.get(lien)
   time.sleep(1)

   nom = driver.find_elements(By.CSS_SELECTOR, "[style='font-size:16px !important; overflow: hidden !important;']")
   print(nom[0].text)
   nomLeaks = nom[0].text

   if nomLeaks != oldName:
      oldName = nomLeaks
      imageLien = driver.find_elements(By.CSS_SELECTOR, '[loading="lazy"]')
      print(imageLien[0].get_attribute('src'))
      imageLeaks = imageLien[0].get_attribute('src')

      links = driver.find_elements(By.TAG_NAME, "a")
      print(links[10].get_attribute('href'))
      time.sleep(5)
      driver.get(links[10].get_attribute('href'))
      time.sleep(10)
      lienWithNoAds = driver.find_elements(By.TAG_NAME, "a")
      print(lienWithNoAds[0].get_attribute('href'))

      lienLeaks = lienWithNoAds[0].get_attribute('href')
      time.sleep(5)

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

      lienLeaks = response_json["response"]["url"]

      getColor = get_dominant_color(imageLeaks)

      print(getColor)

      print(f"Le lien extrait est : {lienLeaks}")
            
      sendToDiscord(getColor)
   else:
      timeClock()

timeClock()