import os
from Module.BaseModule import *

def DetectLanguegFile():
    Url_langueg = "https://raw.githubusercontent.com/777Chara777/MinecarftLauncher/main/Launcher/Languages/"
    if not mexists('./Languages'):
        os.mkdir('./Languages')

    for url in ['en.json','ru.json']:
        if not misfile(f'./Languages/{url}'):
            MDowloadFiles(Url_langueg+url,['./Languages'])

class launch:
    def __init__(self) -> None:
        DetectLanguegFile()
        self.Language_list = [x for x in os.listdir("./Languages") if not __file__.split("\\")[-1] == x and x.endswith(".json")]
        self.speck = self.logick()

    def logick(self):
        if misfile("./UserSettings.json"):
            data = loadall_json("./UserSettings.json")
            if len(self.Language_list) == 0:
                LogError("Error Language: No languages installed!", 2)
            num = 0; languech = ''
            for x in self.Language_list:
                if x == data['Info-User'].get("Language")+".json":
                    num+=1
                    languech = loadall_json(f"./Languages/{x}")
            if num != 1:
                for num, x in enumerate(self.Language_list):
                    self.Language_list[num] = x.split(".")[0]

                LogError(f"Error Language: There is no such language! '{data['Info-User'].get('Language')}'.\n * please select a language from the list `{' , '.join(self.Language_list)}`", 2)
            else:
                return languech

