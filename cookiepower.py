import json
import math
import datetime
import aiohttp
import asyncio
import base64
import tkinter as tk
from tkinter import filedialog

config = {
  "Cookies": None,
  "SuperCookies": None,
  "Structures": None,
  "SuperStructures": None,
  "ShowcaseItems": None,
  "ShowcaseShelves": None,
  "Milkshakes": None,
  "Bakeries": None,
  "Achievements": None,
  "MaximumValues": None
}

def GetKeys(data):
  return data.keys()

INFO = {"TITLE": "Python", "VERSIONBUILD": "3.9.1"}

async def async_fetch(session, url, data=None, requires_content_type=False):
  if requires_content_type:
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'User-agent': '{0[TITLE]} {0[VERSIONBUILD]}'.format(INFO)}
  else:
    headers = {'User-agent': '{0[TITLE]} {0[VERSIONBUILD]}'.format(INFO)}

  if not data:
    async with session.get(url, headers=headers) as response:
      return await response.text()
  else:
    async with session.post(url, headers=headers, data=data) as response:
      return await response.text()

async def DownloadSave(save_md5):
  async with aiohttp.ClientSession() as session:
    save_data = await async_fetch(session, 'https://ccprodapi.pixelcubestudios.com/Backup/Load/{}'.format(save_md5))
    save_data = json.loads(save_data)
    
    if not save_data['data']:
      print("No such save code.")
      return None
    
    else:
      save_data = json.loads( base64.b64decode(save_data['data']) )
      return save_data

'''
  Cookies
  
  Cookie Power Sources
    Gilding: Costs 4,000,000 rainbow cookies per gild and provides a variable amount of cookie power.
    Homemade Cookie: Costs one homemade cookie and provides 100 cookie power.
    Rainbow Mastery: Indirectly from achievements.
    Cosmic Cupcake: Requires gilding, homemade cookie, and rainbow mastery; provides 100 cookie power.
'''
def GetCookies():
  dict = {}
  
  for i in config['Cookies']:
    dict[i["InternalName"]] = {
      "RainbowMastery": False,
      "Gilded": False,
      "CookiePowerIfGilded": ((i['Id'] - 1) % 8) + 2 + math.floor((i['Id'] - 1) / 8),
      "HomemadeCookie": False
    }
  
  return dict

def Cookies(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  cookies = GetCookies()
  
  # Data Collection
  for i in keys:
    if "AncientCookie" in i:
      cookies[i[13:]]['HomemadeCookie'] = True
    
    if "BoughtGold" in i:
      cookies[i[10:]]['Gilded'] = True
    
    if "Collected" in i and i.index("Collected") == 0 and data[i] >= 40000000:
      cookies[i[9:]]['RainbowMastery'] = True
  
  # Calculation
  for j in cookies:
    if cookies[j]['Gilded']:
      interimTotal += cookies[j]['CookiePowerIfGilded']
    
    if cookies[j]['HomemadeCookie']:
      interimTotal += 100
    
    if cookies[j]['RainbowMastery'] and cookies[j]['Gilded'] and cookies[j]['HomemadeCookie']:
      interimTotal += 100
  
  return interimTotal

'''
  Super Cookies
  
  Cookie Power Sources
    Gilding: Not applicable.
    Upgrading: Up to level 250, not including achievements.
'''
def GetSuperCookies():
  dict = {}
  
  for i in config['SuperCookies']:
    dict[i["InternalName"]] = {
      "Coefficient": int(i['Id']),
      "ComputedQuantity": 0
    }
  
  return dict

def SuperCookies(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  superCookies = GetSuperCookies()
  
  # Data Collection
  for i in keys:
    if "OwnedSuper" in i and "OwnedSuperCookie" in i:
      superCookies[i[10:]]['ComputedQuantity'] = data[i] if data[i] <= 250 else 250
  
  # Calculation
  for j in superCookies:
    interimTotal += superCookies[j]['ComputedQuantity'] * superCookies[j]['Coefficient']
  
  return interimTotal

'''
  Structures
  
  Cookie Power Sources
    Gilding: Costs 7,000,000 rainbow cookie per gild and provides a variable amount of cookie power.
    Mastery: Costs light cookies and yields a variable amount of cookie power.
    Homemade Cookie: Costs one homemade cookie and provides 100 cookie power.
    Cosmic Cupcake: Requires gilding, homemade cookie, and rainbow mastery; provides 100 cookie power.
'''
def GetStructures():
  dict = {}
  
  for i in config['Structures']:
    dict[i["InternalName"]] = {
      "Coefficient": int(i['Id']),
      "Gilded": False,
      "MasteryLevel": 0,
      "HomemadeCookie": False
    }
  
  return dict

def Structures(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  structures = GetStructures()
  
  # Data Collection
  for i in keys:
    if "AncientStruct" in i:
      structures[i[13:]]['HomemadeCookie'] = True
      
    if "Bought" in i and "Gold" in i and not "BoughtGold" in i and not "Super" in i:
      structures[i[6:-4]]['Gilded'] = True
    
    if "PrestigeStruct" in i:
      structures[i[14:]]['MasteryLevel'] = data[i] - 1
  
  # Calculation
  for j in structures:
    if structures[j]['Gilded']:
      interimTotal += structures[j]['Coefficient']
      
    if structures[j]['HomemadeCookie']:
      interimTotal += 100
    
    interimTotal += structures[j]['MasteryLevel'] * structures[j]['Coefficient']
    
    if structures[j]['MasteryLevel'] == 10 and structures[j]['HomemadeCookie'] and structures[j]['Gilded']:
      interimTotal += 100
  
  return interimTotal

'''
  Super Structures
  
  Cookie Power Sources
    Gilding: Not applicable.
    Upgrading: Up to level 250, not including achievements.
'''
def GetSuperStructures():
  dict = {}
  
  for i in config['SuperStructures']:
    dict[i["InternalName"]] = {
      "Coefficient": int(i['Id']),
      "ComputedQuantity": 0
    }
  
  return dict

def SuperStructures(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  superStructures = GetSuperStructures()
  
  # Data Collection
  for i in keys:
    if "OwnedSuper" in i and "OwnedSuperCookie" not in i:
      superStructures[i[10:]]['ComputedQuantity'] = data[i] if data[i] <= 250 else 250
  
  # Calculation
  for j in superStructures:
    interimTotal += superStructures[j]['ComputedQuantity'] * superStructures[j]['Coefficient']
  
  return interimTotal

'''
  Showcase Items
  
  Cookie Power Sources
    Unlocking: Variable amount.
    Mastery: Variable amount.
    Homemade Cookie: Costs one homemade cookie and provides 100 cookie power.
    Cosmic Cupcake: Requires homemade cookie and full mastery; provides 100 cookie power.
'''
def GetShowcaseUnlockValue(i):
  n = int(i['Id'])

  if n > 112:
    return (n - 112) * 10
  else:
    if n > 96:
      return (math.floor(((n+32)-1)/16)+1)*n
    else:
      return (math.floor((n-1)/16)+1)*n

def GetShowcaseItems():
  dict = {}
  
  for i in config['ShowcaseItems']:
    dict[i["InternalName"]] = {
      "Unlock": GetShowcaseUnlockValue(i),
      "Coefficient": ((int(i['Id'])-1) % 112) + 1,
      "MasteryLevel": 0,
      "HomemadeCookie": False,
    }
  
  return dict

def ShowcaseItems(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  showcaseItems = GetShowcaseItems()
  
  # Data Collection
  for i in keys:
    if "AncientShowcase" in i:
      showcaseItems[i[15:]]['HomemadeCookie'] = True
    
    if "ShowcaseLevel" in i and i != "ShowcaseLevel":
      showcaseItems[i[13:]]['MasteryLevel'] = data[i]
  
  # Calculation
  x_iter = 0
  
  for j in showcaseItems:
    if x_iter <= data['ShowcaseLevel'] and x_iter <= 112:
      interimTotal += showcaseItems[j]['Unlock']
    elif x_iter > 112:
      if 'BoughtShowcase{}'.format(j) in data:
        interimTotal += showcaseItems[j]['Unlock']
      
    if showcaseItems[j]['HomemadeCookie']:
      interimTotal += 100
    
    interimTotal += showcaseItems[j]['MasteryLevel'] * showcaseItems[j]['Coefficient']
    
    if showcaseItems[j]['MasteryLevel'] == 10 and showcaseItems[j]['HomemadeCookie']:
      interimTotal += 100
     
    x_iter += 1
  
  return interimTotal

'''
  Showcase Shelves
  
  Cookie Power Sources
    Upgrading: Variable amount; constant between levels. The Lost Items and Mystery III showcase shelves are bugged and do not award Cookie Power.
'''
def GetShowcaseShelves():
  dict = {}
  
  for i in config['ShowcaseShelves']:
    dict[i["Id"]] = {
      "Coefficient": i['Coefficient']
    }
  
  return dict

def ShowcaseShelves(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  showcaseShelves = GetShowcaseShelves()
  
  # Calculation
  for i in keys:
    if "ShowcaseSet" in i:
      interimTotal += data[i] * showcaseShelves[i[11:-7]]['Coefficient']
  
  return interimTotal

'''
  Milkshakes
  
  Cookie Power Sources
    Unlocking: Cookie Power corresponds to the milkshake ID.
    Upgrading: One Cookie Power per milkshake level.
'''
def GetMilkshakes():
  dict = {}
  
  for i in config['Milkshakes']:
    dict[i["InternalName"]] = {
      "Id": int(i['Id']),
      "Levels": 85
    }
  
  return dict

def Milkshakes(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  milkshakes = GetMilkshakes()
  
  # Calculation
  for i in keys:
    if 'Level' in i and 'Milk' in i and i.index("Level") == 0:
      interimTotal += milkshakes[i[5:-4]]['Id']
      interimTotal += data[i] - 1
  
  return interimTotal

'''
  Bakeries
  
  Cookie Power Sources
    Unlocking: Variable amount.
    Mastery: Variable amount.
    Homemade Cookie: Costs one homemade cookie and provides 100 cookie power.
    Cosmic Cupcake: Requires homemade cookie and full mastery; provides 100 cookie power.
'''
def GetBakeries():
  dict = {}
  
  for i in config['Bakeries']:
    dict[i["InternalName"]] = {
      "Coefficient": int(i['Id']),
      "MasteryLevel": 0,
      "HomemadeCookie": False
    }
  
  return dict

def Bakeries(data):
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  bakeries = GetBakeries()
  
  # Data Collection
  for i in keys:
    if 'Bakery' in i and 'PrestigeLevel' in i:
      bakeries[i[6:-13]]['MasteryLevel'] = data[i] - 1
    
    if 'AncientBakery' in i:
      bakeries[i[13:]]['HomemadeCookie'] = True
    
  # Calculation
  for j in bakeries:
    if 'Bakery{}Date'.format(j) in data:
      interimTotal += bakeries[j]['Coefficient']
      interimTotal += bakeries[j]['Coefficient'] * bakeries[j]['MasteryLevel']
      
      if bakeries[j]['HomemadeCookie']:
        interimTotal += 100
      
      if bakeries[j]['HomemadeCookie'] and bakeries[j]['MasteryLevel'] == 10:
        interimTotal += 100
  
  return interimTotal

'''
  Achievements
  
  Cookie Power Sources
    Unlocking: One Cookie Power per achievement.
'''

def Achievements():
  # Variables
  interimTotal = 0
  keys = GetKeys(data)
  
  # Data Collection
  for i in keys:
    if 'ACH' in i:
      if i.index("ACH") == 0:
        # verify if achievement still exists
        if 'septuagintillion' in i:
          pass
        elif 'Octogintillion' in i:
          pass
        elif 'octogintillion' in i:
          pass
        elif 'Cupcake' in i:
          if int(i[10:]) % 200000 == 0:
            interimTotal += 1
        elif 'Login' in i:
          if int(i[8:]) <= 100:
            interimTotal += 1
        elif 'ACHOven' in i:
          pass
        elif 'ACHDispose' in i:
          pass
        elif 'ACHLeague' in i:
          pass
        elif 'ACHShowcase-' in i:
          pass
        elif 'ACHTheme' in i:
          pass
        elif i.endswith('200') or i.endswith('300') or i.endswith('400'):
          if 'Login' in i:
            interimTotal += 1
          elif 'Bakery' in i:
            interimTotal += 1
          elif 'Super' in i:
            interimTotal += 1
          elif 'Set' in i:
            interimTotal += 1
        elif (i[-2:] == '20' or i[-2:] == '40' or i[-2:] == '60' or i[-2:] == '80') and 'ACHSet' in i:
          pass
        else:
          interimTotal += 1
  
  return interimTotal

if __name__ == "__main__":
  data = None
  loop = True
  option = -1
  total = 0
  
  with open("maxima.json", "r") as f1:
    config['MaximumValues'] = json.load(f1)
  
  with open("cookies.json", "r") as f2:
    config['Cookies'] = json.load(f2)
  
  with open("supercookies.json", "r") as f3:
    config['SuperCookies'] = json.load(f3)
  
  with open("structures.json", "r") as f4:
    config['Structures'] = json.load(f4)
  
  with open("superstructures.json", "r") as f5:
    config['SuperStructures'] = json.load(f5)
  
  with open("showcaseitems.json", "r") as f6:
    config['ShowcaseItems'] = json.load(f6)
  
  with open("showcaseshelves.json", "r") as f7:
    config['ShowcaseShelves'] = json.load(f7)
  
  with open("milkshakes.json", "r") as f8:
    config['Milkshakes'] = json.load(f8)
  
  with open("bakeries.json", "r") as f9:
    config['Bakeries'] = json.load(f9)
  
  print("All data loaded.\r\n")
  
  while loop:
    selection = input("Please input a save code or select a file [S/F]: ")
    
    if selection.strip().upper()[0:1] == "S":
      option = 0
      loop = False
    elif selection.strip().upper()[0:1] == "F":
      option = 1
      loop = False
    elif selection.strip().upper()[0:1] == "X":
      exit()
    else:
      print("Please try again or exit by typing \"X\".\r\n")
  
  if option == 0:
    save_md5 = input("Please enter an existing save code: ")
  
    loop = asyncio.get_event_loop() 
    data = loop.run_until_complete( DownloadSave(save_md5) )
    
    if data:
      print("Successfully downloaded save.")
    else:
      exit()
    
  if option == 1:
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    
    with open(file_path, "r") as f:
      try:
        data = json.load(f)
        print("Successfully opened save file.")
      except:
        print("Error while accessing or parsing file.")
  
  print("\r\nPlayer Name: {}".format(data['BakeryName']))
  print("Time of Backup: {}Z\r\n".format(datetime.datetime.utcfromtimestamp(data['LatestPlayTime']).isoformat()))
  
  print("Calculating COOKIES ...")
  result = Cookies(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['Cookies'], result/config['MaximumValues']['Cookies']))
  
  print("Calculating SUPER COOKIES ...")
  result = SuperCookies(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['SuperCookies'], result/config['MaximumValues']['SuperCookies']))
  
  print("Calculating STRUCTURES ...")
  result = Structures(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['Structures'], result/config['MaximumValues']['Structures']))
  
  print("Calculating SUPER STRUCTURES ...")
  result = SuperStructures(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['SuperStructures'], result/config['MaximumValues']['SuperStructures']))
  
  print("Calculating SHOWCASE ITEMS ...")
  result = ShowcaseItems(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['ShowcaseItems'], result/config['MaximumValues']['ShowcaseItems']))
  
  print("Calculating SHOWCASE SHELVES ...")
  result = ShowcaseShelves(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['ShowcaseShelves'], result/config['MaximumValues']['ShowcaseShelves']))
  
  print("Calculating MILKSHAKES ...")
  result = Milkshakes(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['Milkshakes'], result/config['MaximumValues']['Milkshakes']))
  
  print("Calculating BAKERIES ...")
  result = Bakeries(data)
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['Bakeries'], result/config['MaximumValues']['Bakeries']))
  
  print("Calculating ACHIEVEMENTS ...")
  result = Achievements()
  total += result
  print("  {:,} / {:,} ({:.2%})\r\n".format(result, config['MaximumValues']['Achievements'], result/config['MaximumValues']['Achievements']))
  
  print("Total Cookie Power: {:,} / {:,} ({:.2%})".format(total, config['MaximumValues']['Total'], total/config['MaximumValues']['Total']))