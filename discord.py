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

lien = "https://pornleaks.in/packs.php"

options = Options()
options.add_extension("AdGuard AdBlocker 4.3.35.0.crx")

driver = webdriver.Chrome(
   service=ChromeService(ChromeDriverManager().install()),
   options=options
   )

webhook = "https://discord.com/api/webhooks/1226783498912792637/E35M4LRIqUBzbZVIuwEMJQ3OYi8ajNULvyDX_kKm8Sk7at91avr87a2omMGGd4V4uV4_"
nomLeaks = ""
lienLeaks = ""
imageLeaks = ""
timeStop = 3600

oldName = ""

def timeClock():
   global timeStop
   if timeStop >= 0:
      timeStop -= 1
      print(timeStop)
      time.sleep(1)
      timeClock()
   else:
      timeStop = 3600
      getData()

def sendToDiscord():
   global webhook, nomLeaks, lienLeaks, imageLeaks
   data = {
      "username": "Leaks KhaosRevelation",
      "embeds": [
         {
               "title": f"{nomLeaks}",
               "fields": [

                  {"name": "lien", "value": f"{lienLeaks}", "inline": False}
               ],
               "color": 0x03b2f8,
               "image": {
                  "url": f"{imageLeaks}"
            }
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

      print(f"Le lien extrait est : {lienLeaks}")
            
      sendToDiscord()
   else:
      timeClock()

timeClock()