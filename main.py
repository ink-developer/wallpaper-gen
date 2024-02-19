import requests
import ctypes
import os
import winreg
from colorama import Fore
import shutil
import asyncio
import config

headars = {
    "x-api-key": config.CAT_API
}

header2 = {
    "X-Api-Key": config.NINJAS_API,
    "Accept": "image/jpg"
}

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX

# TODO: more logs
# TODO: linux support

gen = True

width = config.WIDTH
height = config.HEIGHT

SPI_SETDESKWALLPAPER = 0x14
SPIF_UPDATEINIFILE = 0x2 

#53463

async def ninjas(type: str):
    try:
        os.remove("./images/wallpaper.jpg")
    except FileNotFoundError:
        print("Can't delete picture")

    try:
        resp = requests.get(f"https://api.api-ninjas.com/v1/randomimage?category={type}&width={width}&height={height}", headers=header2, stream=True)
    except requests.RequestsJSONDecodeError:
        print("Json error. Can be rate limit or ban")

    with open('./images/wallpaper.jpg', 'wb') as file:
        shutil.copyfileobj(resp.raw, file)
        file.close()
        path = os.path.abspath("./images/wallpaper.jpg")
        key = r"Control Panel\Desktop"
        value_name = "Wallpaper"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, path)
        
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path , SPIF_UPDATEINIFILE)
        print(f"Successfully\nwidth {width}, height {height}")
        await asyncio.sleep(3)


    

async def cats():

    global gen
    while gen == True:
        
        try:
            os.remove("./images/wallpaper.jpg")
        except FileNotFoundError:
            print("Can't delete picture")
            
        try:
            resp = requests.get("https://api.thecatapi.com/v1/images/search?limit=1", headers=headars).json()
        except requests.RequestsJSONDecodeError:
            print("Json error (can be limit or ban)")
        print("Got answer")
        img = resp[0]["url"]
        width1 = resp[0]["width"]
        height1 = resp[0]["height"]
        img2 = requests.get(img)
        if width1 == round(config.RATIO * height1) and not img.endswith(".gif"):
                with open("./images/" + img.split("/")[-1], "wb") as file:
                    img3 = img.split("/")[-1]
                    file.write(img2.content)
                    file.close()
                    os.rename("./images/" + img.split("/")[-1]  , "./images/wallpaper.jpg")
                    gen = False
                    path = os.path.abspath("./images/wallpaper.jpg")
                    key = r"Control Panel\Desktop"
                    value_name = "Wallpaper"
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE) as reg_key:
                        winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, path)
                    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path , SPIF_UPDATEINIFILE)
                    print(f"Successfully\nWidth {width1}, Height {height1}")
                    await asyncio.sleep(3)
        else:
            print("The picture doesn't fit")


async def main():
    while True:
        print(f"""{magenta}
    ____      __      _       __      ____                                
   /  _/___  / /__   | |     / /___ _/ / /___  ____ _____  ___  __________
   / // __ \/ //_/   | | /| / / __ `/ / / __ \/ __ `/ __ \/ _ \/ ___/ ___/
 _/ // / / / ,<      | |/ |/ / /_/ / / / /_/ / /_/ / /_/ /  __/ /  (__  ) 
/___/_/ /_/_/|_|     |__/|__/\__,_/_/_/ .___/\__,_/ .___/\___/_/  /____/  
                                     /_/         /_/                    
        """)
        print(f"""{reset}{cyan}
        Choose variant
          
      1. Cats (not stable idk)
      2. Nature
      3. City
      4. Technology
      5. Food
      6. Still life
      7. Abstract
      8. Wildlife
      (1-8)
{reset}""")
        clear = lambda: os.system('cls')
        

        choose = input()

        if choose == "1":
            await cats()
            clear()
        elif choose == "2":
            await ninjas("nature")
            clear()
        elif choose == "3":
            await ninjas("city")
            clear()
        elif choose == "4":
            await ninjas("technology")
            clear()
        elif choose == "5": 
            await ninjas("food")
            clear()
        elif choose == "6":
            await ninjas("still_life")
            clear()
        elif choose == "7":
            await ninjas("abstract")
            clear()
        elif choose == "8":
            await ninjas("wildlife")
            clear()
        else:
            print(f"{red}Choose from 1 to 8!{reset}")
            await asyncio.sleep(1)

            
asyncio.run(main())
