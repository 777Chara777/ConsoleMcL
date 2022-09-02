import sys
import os
import json
import requests

from datetime import datetime

def _platform_minecraft():
    if (sys.platform == "linux" or sys.platform == "linux2"):
        return "natives-linux"
    elif sys.platform == "win32":
        return "natives-windows"
    elif sys.platform == "darwin":
        return "natives-macos"
    
def _platform_minecraft_v2():
    if (sys.platform == "linux" or sys.platform == "linux2"):
        return "linux"
    elif sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "osx"

def __cls_or_clear_platform():
    if sys.platform == 'win32':
        return "cls"
    elif sys.platform == 'linux' or sys.platform == 'linux2':
        return "clear"
    elif sys.platform == 'darwin':
        return "clear"

def title_os_platform(name):
    if sys.platform == 'win32':
        os.system(f"title {name}")
    # elif sys.platform == 'linux' or sys.platform == 'linux2':
    #     return "clear"
    elif sys.platform == 'darwin':
        os.system(f"title {name}")

def MDowloadFiles(link: str, paths: list,):
    for filepath in paths:
        if misfile(f"{filepath}/{link.split('/')[-1]}") != True:
            resp = requests.get(link)
            if link.split('.')[-1] == 'json':
                baits = json.loads(resp.text)
                with open(f"{filepath}/{link.split('/')[-1]}", 'w', encoding="UTF-8") as f:
                    json.dump(baits, f, indent=2, ensure_ascii=False)   
            else:
                open(f"{filepath}/{link.split('/')[-1]}", 'wb').write(resp.content)

mcls = lambda : os.system(__cls_or_clear_platform())

mplatform_min = lambda : _platform_minecraft()

mplatform_min_v2 = lambda : _platform_minecraft_v2()

mplatform = lambda : sys.platform

mtitle = lambda name : title_os_platform(name)

misfile = lambda path : os.path.isfile(path) 

misdir = lambda path : os.path.isdir(path)

mcdir = lambda path : os.mkdir(path)

mexists = lambda path : os.path.exists(path)

mwhatinfile = lambda path : os.listdir(path)

msystem = lambda command : os.system(command)

def load_json(derictory, Name, Name2=None):
    try:
        with open(derictory, encoding="utf-8") as config_file:
            data = json.load(config_file)
            config_file.close()
        Num = data[str(Name)]
        if Name2 != None:
            Num2 = data[str(Name2)]
        else:
            return "!", Num, None
        return "!", Num, Num2
    except:
        return None,None,None

def input_json(derictory, Data):
    try:
        with open(derictory, 'w', encoding="UTF-8") as f:
            json.dump(Data, f, indent=2, ensure_ascii=False)
        return "!"
    except:
        return None

def loadall_json(derictory) -> dict:
    with open(derictory, encoding="utf-8") as config_file:
        data = json.load(config_file)
    return data

def file_size(file_path):
    def convert_bytes(num):
        # for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        for x in [0, 1, 2, 3, 4]:
            if num < 1024.0:
                return x
                # return "%s" % (x)
            num /= 1024.0
    if misfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def Time(num=0):
    if num == 0:
        return datetime.today().strftime("%d-%m-%Y %H:%M")
    elif num == 1:
        return datetime.today().strftime("%d-%m-%Y")
    elif num == 2:
        return datetime.today().strftime("%H:%M")
    elif num == 3:
        return datetime.today().strftime("%d-%m-%Y %H:%M:%S")
    elif num == 4:
        return datetime.today().strftime("%H:%M:%S")
    elif num == 5:
        return int(datetime.today().strftime("%H%M%S"))

def LogError(ctx, Type=0, *, send_message=False):
    """ 
    * 0 - None
    * 1 - Log
    * 2 - Warning
    * 3 - ERROR
    * 4 - Crash ERROR
    """
    if send_message == True:
        print("\nError please check the log!\n")

    if misfile("./logs/last.log"):
        save = file_size("./logs/last.log")
        if save >= 2:

            with open("./logs/last.log", 'r', encoding="UTF-8") as save_file_to_zit:
                file_to_zip = save_file_to_zit.read()
            open("./logs/last.log", 'w')
            zipped = file_to_zip
            with open(f"./logs/last-{Time(0)}.gz", 'w') as zip_save:
                zip_save.write(zipped)
                zip_save.close()
    else:
        with open("./logs/last.log", "w") as create:
            create.write(f"[UTC: {Time(0)}] File Create")
            create.close()

    with open("./logs/last.log", 'a', encoding="UTF-8") as L:
        if Type == 0:
            L.write(f"\n[UTC: {Time(0)}]: {ctx}")
        elif Type == 1:
            L.write(f"\nLog: [UTC: {Time(0)}]: {ctx}")
        elif Type == 2:
            L.write(f"\nWarning: [UTC: {Time(0)}]: {ctx}")
        elif Type == 3:
            L.write(f"\nERROR: [UTC: {Time(0)}]: {ctx}")
        elif Type == 4:
            L.write(f"\nCrash ERROR: [UTC: {Time(0)}]: {ctx}")
            L.close(); os.system("pause")
            exit(1)
        L.close()



