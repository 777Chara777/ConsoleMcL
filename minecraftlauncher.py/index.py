import asyncio
from os import mkdir
import sys
import subprocess

from random import choice

from settings import *
from Module.BaseModule import *
from Manifest.Manifest import *
from Languages.setup import launch

class MinecraftLauncher:

    def __init__(self) -> None:
        self.MinecraftSettings = loadall_json('./UserSettings.json')

        self.speck = launch().speck
        self.downloadModule = AdditionalModifications()
        self.Jsonfile = FMcV(load_file_with_manifest())
        self.__mainloop = asyncio.get_event_loop()
        self.LastVersion = self.Jsonfile[0]

        self.UserName = self.MinecraftSettings["Info-User"]["Name-with-Game"]
        self.Memory = [self.MinecraftSettings["Info-User"]["Memory-Min"], self.MinecraftSettings["Info-User"]["Memory-Max"]]

        self.McPath = self.MinecraftSettings["Launcher-Settings"]["Minecraft-Path"]

        self.JSon_Version = None
        self.DownloadInformation = {
            'VersionMinecraft': None,
            'Download-AssetIndex': None,
            'Download-Url-AssetIndex-Json': None,
            'Download-Url-AssetIndex-Id': None,
            'Download-Url-AssetIndex-Sha1': None,
            'Download-Url-Core-url': None,
            'Download-Url-Core-Json': None,
            'Download-Url-Logging': None,
            'Download-Logging': None,
            'Download-Lbraries': None,            
            'InfoLbrariesData': [],
            'Type-Requrse': 0 
        }

        self.CompelatorVersion = '1.0'
        self.tasks = []

    def CJFArgg_SAdd(self, data) -> None:
        """
        Create Json File _ Arguments_System Add
        """ 
        url = f'{self.McPath}/assets/LaFiles/StartsArguments.json'

        if not misfile(url):
            filedata = {
                self.DownloadInformation['VersionMinecraft']: data
            }
            self.CJFile_Argg(filedata)
        else:
            JsonData = self.OJFile_Argg()
            JsonData[self.DownloadInformation['VersionMinecraft']] = data
            self.CJFile_Argg(JsonData)

    def CJFile_Argg(self,data) -> None:
        """
        Create Json File _ Arguments
        """
        url = f'{self.McPath}/assets/LaFiles/StartsArguments.json'
        input_json(url,data)

    def OJFile_Argg(self) -> dict:
        """
        Open Json File _ Arguments
        """
        url = f'{self.McPath}/assets/LaFiles/StartsArguments.json'
        if not misfile(url):
            open(url,'w').write('{}')
        
        return loadall_json(url)

    def DetectNowVersionLauncher(self) -> None:
        """
        Pretect laucher Version
        """
        ManiFestlick = 'https://raw.githubusercontent.com/777Chara777/MinecraftLauncher/main/ManiFest/VersionManiFest.json'
        DataInfo = date(ManiFestlick)
        if DataInfo['$latest'].get('id') != None:
            Launcherlick = f'https://raw.githubusercontent.com/777Chara777/MinecraftLauncher/main/Launcher/MinecraftLauncher-{DataInfo["$latest"]["id"]}.exe'
            if DataInfo['$latest']['id'] != LauncherSettings['Version']:
                print(self.speck['MenuMessage']['LauncherUpDate'].format(LauncherSettings['Caption'], LauncherSettings['Version'], DataInfo['$latest']['id']))
                while True:
                    num = input('Y/N: ')
                    if num == 'Y' or num == 'y':
                        mcls()
                        break
                    elif num == 'N' or num == 'n':
                        mcls()
                        return
                MDowloadFiles(Launcherlick,['.'])
                
    def Downloadlist(self) -> None:
        self.__mainloop.run_until_complete(asyncio.wait(self.tasks[self.DownloadInformation['Type-Requrse']][0]))
        self.DownloadInformation['Type-Requrse'] += 1
        self.tasks[self.DownloadInformation['Type-Requrse']-1][0] = f'{Time(4)} : Done'

    def SetUpFiles(self) -> None:
        if not mexists(f'{self.McPath}'):
            mcdir(f'{self.McPath}')

        if not mexists(f'{self.McPath}/versions'):
            mcdir(f'{self.McPath}/versions')
        
        if not mexists(f'{self.McPath}/libraries'):
            mcdir(f'{self.McPath}/libraries')

        if not mexists(f'{self.McPath}/assets'):
            mcdir(f'{self.McPath}/assets')
        
        if not mexists(f'{self.McPath}/assets/indexes'):
            mcdir(f'{self.McPath}/assets/indexes')
        
        if not mexists(f'{self.McPath}/assets/objects'):
            mcdir(f'{self.McPath}/assets/objects')
        
        if not mexists(f'{self.McPath}/assets/log_configs'):
            mcdir(f'{self.McPath}/assets/log_configs')
        
        if not mexists(f'{self.McPath}/assets/skins'):
            mcdir(f'{self.McPath}/assets/skins')
        
        if not mexists(f'{self.McPath}/assets/LaFiles'):
            mcdir(f'{self.McPath}/assets/LaFiles')
        
        if not mexists(f'{self.McPath}/versions/{self.DownloadInformation["VersionMinecraft"]}'):
            mcdir(f'{self.McPath}/versions/{self.DownloadInformation["VersionMinecraft"]}')
        
        if not mexists(f'{self.McPath}/versions/{self.DownloadInformation["VersionMinecraft"]}/natives'):
            mcdir(f'{self.McPath}/versions/{self.DownloadInformation["VersionMinecraft"]}/natives')

    def Minecraft_DVaJF(self) -> None:
        """
        Minecraft Download Version and Json File
        """

        BaseTasks = [
            self.__mainloop.create_task(self.downloadModule.DowloadFiles(self.DownloadInformation["Download-Url-Core-url"], [f"{self.McPath}/versions/{self.DownloadInformation['VersionMinecraft']}"]), name='Core-Minecraft'),
            self.__mainloop.create_task(self.downloadModule.DowloadFiles(self.DownloadInformation["Download-Url-Core-Json"], [f"{self.McPath}/versions/{self.DownloadInformation['VersionMinecraft']}"]), name='Core-Json'),
            self.__mainloop.create_task(self.downloadModule.DowloadFiles(self.DownloadInformation["Download-Url-AssetIndex-Json"], [f"{self.McPath}/assets/indexes"]), name='AssetIndex-Json')
        ]
        if self.DownloadInformation['Download-Logging'] != None:
            BaseTasks.append(self.__mainloop.create_task(self.downloadModule.DowloadFiles(self.DownloadInformation["Download-Url-Logging"], [f"{self.McPath}/assets/log_configs"]), name='ClientLogging'))
        self.tasks.append([BaseTasks,f'{sys._getframe().f_code.co_name}'])

    def MinecraftDA(self) -> None:
        """
        Minecraft Download Assets
        """

        MinecraftDataIndexes = loadall_json(f"{self.McPath}/assets/indexes/{self.DownloadInformation['Download-Url-AssetIndex-Id']}.json")

        HashsID = {} # 'db': ['HASHS']
        for objecthash in MinecraftDataIndexes['objects']:
            if MinecraftDataIndexes['objects'][objecthash]['hash'][:2] not in HashsID:
                HashsID[MinecraftDataIndexes['objects'][objecthash]['hash'][:2]] = [MinecraftDataIndexes['objects'][objecthash]['hash']]
            else:
                HashsID[MinecraftDataIndexes['objects'][objecthash]['hash'][:2]].append(MinecraftDataIndexes['objects'][objecthash]['hash'])
        
        for HashName in HashsID:
            if misdir(f'{self.McPath}/assets/objects/{HashName}/') != True:
                mcdir(f'{self.McPath}/assets/objects/{HashName}')

        FileHashs = []
        for num, HashName in enumerate(HashsID):
            FileHashs.append( self.__mainloop.create_task(self.downloadModule.DowloadAssets(HashName, HashsID[HashName]),name=f'MinecraftDA Task {num}') )

        self.tasks.append([[
            x for x in FileHashs
        ],f'{sys._getframe().f_code.co_name}'])

    def MinecraftDL(self) -> None:
        """
        Minecraft Download Labraries
        """
        
        PathToFileGen = lambda : f'{self.McPath}/libraries/'

        JavaLibrariesID = {}
        self.DownloadInformation['InfoLbrariesData'] = {
            'Lbraries': [],
            'JavaDoc': [],
            'OS': [],
            'Sources': []
        }

        for LbrariesInfo in self.DownloadInformation['Download-Lbraries']:
            LbrariesData = LbrariesInfo['downloads']
            
            if dict(LbrariesData).get('artifact') != None:
                self.DownloadInformation['InfoLbrariesData']['Lbraries'].append([str(LbrariesData['artifact']['path']).split('/')[:-1], LbrariesData['artifact']['url'], str(LbrariesData['artifact']['path']).split('/')[-1]])

            if dict(LbrariesData).get('classifiers') != None:
                if LbrariesData['classifiers'].get('javadoc') != None:
                    self.DownloadInformation['InfoLbrariesData']['JavaDoc'].append([str(LbrariesData['classifiers']['javadoc']['path']).split('/')[:-1],LbrariesData['classifiers']['javadoc']['url'],str(LbrariesData['classifiers']['javadoc']['path']).split('/')[-1]])
                if LbrariesData['classifiers'].get(mplatform_min()) != None:
                    self.DownloadInformation['InfoLbrariesData']['OS'].append([str(LbrariesData['classifiers'][mplatform_min()]['path']).split('/')[:-1],LbrariesData['classifiers'][mplatform_min()]['url'],str(LbrariesData['classifiers'][mplatform_min()]['path']).split('/')[-1]])
                if LbrariesData['classifiers'].get('sources') != None:
                    self.DownloadInformation['InfoLbrariesData']['Sources'].append([str(LbrariesData['classifiers']['sources']['path']).split('/')[:-1],LbrariesData['classifiers']['sources']['url'],str(LbrariesData['classifiers']['sources']['path']).split('/')[-1]])  

        for data in enumerate(self.DownloadInformation['InfoLbrariesData']):

            for info in self.DownloadInformation['InfoLbrariesData'][data[1]]:
                
                LbrariesPath = info[0]
                LbrariesUrl = info[1]
                LbrariesName = info[2]

                PathToFile = PathToFileGen()

                for path in LbrariesPath:
                    PathToFile+=f'{path}/'
                    PathToFileFull = f'{self.McPath}/libraries/{"/".join(LbrariesPath)}/'
                    FileFull = (LbrariesPath, PathToFileFull, LbrariesName, LbrariesUrl)

                    if not mexists(PathToFile):
                        mcdir(PathToFile)
                    
                    if LbrariesPath[0] not in JavaLibrariesID:
                        JavaLibrariesID[LbrariesPath[0]] = [FileFull]

                    if FileFull not in JavaLibrariesID[LbrariesPath[0]]:
                        JavaLibrariesID[LbrariesPath[0]].append(FileFull)

        CreateTackLbraries = []
        for num, InfoLbrariesName in enumerate(JavaLibrariesID):
            CreateTackLbraries.append(
                self.__mainloop.create_task(self.downloadModule.DownloadLabraries(JavaLibrariesID[InfoLbrariesName]),name=f'MinecraftDL Task {num}')
            )

        self.tasks.append([[
            x for x in CreateTackLbraries
        ],f'{sys._getframe().f_code.co_name}'])

    def MinecraftDNdll(self) -> None:
        """
        Minecraft Download Natives dll
        """
        LbrariesList = []
        for LbrariesInfo in self.DownloadInformation['Download-Lbraries']:
            LbrariesData = LbrariesInfo['downloads']

            if dict(LbrariesData).get('artifact') != None:
                LbrariesList.append(str(LbrariesData['artifact']['path']))
            
            if dict(LbrariesData).get('classifiers') != None:
                if LbrariesData['classifiers'].get('javadoc') != None:
                    LbrariesList.append(LbrariesData['classifiers']['javadoc']['path'])
                if LbrariesData['classifiers'].get(mplatform_min()) != None:
                    LbrariesList.append(LbrariesData['classifiers'][mplatform_min()]['path'])
                if LbrariesData['classifiers'].get('sources') != None:
                    LbrariesList.append(LbrariesData['classifiers']['sources']['path'])

        self.tasks.append(
            [[self.__mainloop.create_task(self.downloadModule.DowloadFilesDll(LbrariesList, self.DownloadInformation['VersionMinecraft']),name='MinecraftDNdll')],
            f'{sys._getframe().f_code.co_name}']
        )

    def MinecraftCSF(self) -> None:
        """
        Minecraft Create Start
        """

        IndexData = loadall_json(f'{self.McPath}/versions/{self.DownloadInformation["VersionMinecraft"]}/{self.DownloadInformation["VersionMinecraft"]}.json')
        Arguments = {'Minecraft': [], 'Dlog4j': ['-Dfml.ignorePatchDiscrepancies=true','-Dfml.ignoreInvalidMinecraftCertificates=true']}

        random_uuid = lambda : ''.join([choice('qwertyuiopasdfghjklzxcvbnm1234567890') for _ in range(32)])  
        if IndexData.get('logging') != None:
            Arguments['Dlog4j'].append(str(IndexData['logging']["client"]['argument']).replace('${path}', f'{self.McPath}/assets/log_configs/'+IndexData['logging']["client"]['file']['id']))
        Arguments['Minecraft'].append(IndexData['mainClass'])
        CteateClassPath = []

        for infowithlist in self.DownloadInformation['InfoLbrariesData']['Lbraries']:
            CteateClassPath.append(str(infowithlist[1]).replace('https://libraries.minecraft.net/', f'{self.McPath}/libraries/'))
        
        CteateClassPath = ';'.join(CteateClassPath)

        ArgumentsList = {
            '${auth_player_name}': f'"{self.UserName}"',
            # '${auth_player_name}': f'{self.UserName}',
            '${version_name}': f'"{self.DownloadInformation["VersionMinecraft"]}"',
            # '${version_name}': f'{self.DownloadInformation["VersionMinecraft"]}',
            '${game_directory}': f'"{self.McPath}/"',
            '${assets_root}': f'"{self.McPath}/assets"', '${game_assets}': f'"{self.McPath}/assets"',
            '${assets_index_name}': self.DownloadInformation['Download-Url-AssetIndex-Id'],
            '${auth_uuid}': random_uuid(),
            '${auth_access_token}': self.DownloadInformation['Download-Url-AssetIndex-Sha1'],
            "${clientid}": 'null',
            "${auth_xuid}": 'null', 
            '${user_type}': 'null',
            '${version_type}': f'"{LauncherSettings["Caption"]} V{LauncherSettings["Version"]}"',
            # '${version_type}': f'{LauncherSettings["Caption"]} V{LauncherSettings["Version"]}',
            '${user_properties}': f'{self.McPath}/assets/log_configs/'+self.DownloadInformation['Download-Logging']['client']['file']['id'] if self.DownloadInformation['Download-Logging'] != None else '{}',

            '${natives_directory}': f'{self.McPath}/versions/'+self.DownloadInformation['VersionMinecraft']+'/natives',
            '${launcher_name}': f'"{LauncherSettings["Caption"]}"',
            # '${launcher_name}': f'{LauncherSettings["Caption"]}',
            '${launcher_version}': f'"V{LauncherSettings["Version"]}"',
            # '${launcher_version}': f'V{LauncherSettings["Version"]}',
            '${classpath}': CteateClassPath
        }

        if IndexData.get('minecraftArguments') != None:
            VersionCompelator = f'1.13 => {self.DownloadInformation["VersionMinecraft"]}'
            Aurgs = str(IndexData['minecraftArguments']).split()
            for num, detectArgum in enumerate(Aurgs):
                if str(detectArgum) == '${user_properties}':
                    Aurgs[num] = '{}'
                elif ArgumentsList.get(detectArgum) != None:
                    Aurgs[num] = ArgumentsList[detectArgum]
                elif ArgumentsList.get(detectArgum) == None and detectArgum[0] == '$':
                    Aurgs[num] = 'null'

            Arguments['Dlog4j'].append(f'-Djava.library.path={ArgumentsList["${natives_directory}"]}')
            Arguments['Dlog4j'].append('-cp')
            Arguments['Dlog4j'].append(CteateClassPath)

            minecraftArguments = ' '.join(Aurgs)

        elif IndexData.get('arguments') != None:
            VersionCompelator = f'1.13 <= {self.DownloadInformation["VersionMinecraft"]}'
            Aurgs = []
            for gamearg in IndexData['arguments']['game']:
                if type(gamearg) != dict:
                    Aurgs.append(gamearg)
            
            
            for jvmarg in IndexData['arguments']['jvm']:
                if type(jvmarg) == dict:
                    if dict(jvmarg['rules'][0]['os']).get('name') != None and dict(jvmarg['rules'][0]['os']).get('version') == None:
                        if jvmarg['rules'][0]['os']['name'] == mplatform_min_v2():
                            Arguments['Dlog4j'].append(jvmarg['value'])
                elif type(jvmarg) == str:
                    if str(jvmarg).find('$') != -1:
                        Dlog = str(jvmarg).split('=')
                        if Dlog[-1] in ArgumentsList:
                            Arguments['Dlog4j'].append(str(jvmarg).replace(str(Dlog[-1]), str(ArgumentsList[Dlog[-1]])))
                    else:
                        Arguments['Dlog4j'].append(jvmarg)
                
            for num, detectArgum in enumerate(Aurgs):
                if ArgumentsList.get(detectArgum) != None:
                    Aurgs[num] = ArgumentsList[detectArgum]
                elif ArgumentsList.get(detectArgum) == None and detectArgum[0] == '$':
                    Aurgs[num] = 'null'

            minecraftArguments = ' '.join(Aurgs)
        
        Arguments['Minecraft'].append(minecraftArguments)

        mine =' '.join(Arguments['Minecraft'])
        
        # StartArgum = f"""@REM  Version Compelator {self.CompelatorVersion}: {VersionCompelator}\n@echo off\n@chcp 1251\ncls\n{self.MinecraftSettings['Info-User']['Java-Path']} -Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M {' '.join(Arguments['Dlog4j'])};^\nversions\{self.DownloadInformation['VersionMinecraft']}\client.jar^\n {mine}\npause"""
        # print(f"""{self.MinecraftSettings['Info-User']['Java-Path']} -Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M {' '.join(Arguments['Dlog4j'])};{self.McPath}\\versions\{self.DownloadInformation['VersionMinecraft']}\client.jar {mine}""")

        # self.CJMessageAdd({
        self.CJFArgg_SAdd({
            "Version Compelator": f"{self.CompelatorVersion}",
            "ifoldVersion": f"{VersionCompelator}",
            "Java": f"{self.MinecraftSettings['Info-User']['Java-Path']}",
            "Memory": f"-Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M",
            "Dlog4": f"{' '.join(Arguments['Dlog4j'])}",
            "Client": f"{self.McPath}\\versions\{self.DownloadInformation['VersionMinecraft']}\client.jar",
            "MinecraftArg": f"{mine}"
        })
        # if createfile == True:
            # open(f'{self.McPath}/Minecraft{self.DownloadInformation["VersionMinecraft"]}.bat', 'w').write(StartArgum)
        if mplatform() == 'win32':
            # subprocess.call(f"""{self.MinecraftSettings['Info-User']['Java-Path']} -Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M {' '.join(Arguments['Dlog4j'])};{self.McPath}\\versions\{self.DownloadInformation['VersionMinecraft']}\client.jar {mine}""")
            # msystem(f"""{self.MinecraftSettings['Info-User']['Java-Path']} -Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M {' '.join(Arguments['Dlog4j'])};{self.McPath}\\versions\{self.DownloadInformation['VersionMinecraft']}\client.jar {mine}""")
            open(f'Minecarft-{self.DownloadInformation["VersionMinecraft"]}-Start.bat','w').write(f"""@echo off\n{self.MinecraftSettings['Info-User']['Java-Path']} -Xms{self.Memory[0]}M -Xmx{self.Memory[1]}M {' '.join(Arguments['Dlog4j'])};{self.McPath}\\versions\{self.DownloadInformation['VersionMinecraft']}\client.jar {mine}""")
            # msystem(f'start Minecarft{self.DownloadInformation["VersionMinecraft"]}Start.bat')

    def StatusTasks(self, function) -> None:
        def StatusPrint():
            print(f'Download Minecraft Client: {self.DownloadInformation["VersionMinecraft"]}')
            for x in enumerate(self.tasks):
                print(f'[{x[0]} # {len(self.tasks)}/{self.DownloadInformation["Type-Requrse"]}: {x[1][1]}{" " * (18-len(x[1][1]))}]:  {x[1][0] if type(x[1][0]) != list else len(x[1][0])}')
            print()
            print(self.speck["LauncherMessgae"]['DownloadWait'])

        def __wrapper():
            mcls()
            StatusPrint()
            result = function()
            mcls()
            StatusPrint()
            return result

        return __wrapper()

    def RunLauncher(self) -> None:
        """
        Run Minecraft Launcher
        """

        if not self.Jsonfile:
            print(self.speck['MenuMessage']['ErrorNoWi-Fi'])
            msystem('pause')
            return

        # Приведственое Сообщение
        print(self.speck["WelcomeDownload"].format(self.MinecraftSettings["Info-User"]['Name-with-Game'], self.LastVersion['id'], int(self.MinecraftSettings["Launcher-Settings"]['Visible-Versions']) )) 
        print(self.speck['MenuMessage']['BrackMessage'].format('back'))
        # Вывод версий мвйкрафт

        inputversionname = []
        listversion = [[] for _ in range(int(self.MinecraftSettings["Launcher-Settings"]['Visible-Versions'] / 5))]
        for num, version in enumerate(self.Jsonfile):
            div = divmod(num, self.MinecraftSettings["Launcher-Settings"]['Visible-Versions']/len(listversion)+1)
            listversion[int(div[0])].append([
                f'{num}', version['id']
                ])
            inputversionname.append({
                'Id': version['id'],
                'Number': num
            })
        
        for i in listversion:
            for x in i:
                print(f'{x[0]}: {x[1]} ',end='\t')
            print()

        # Выбор Версии
        while True:
            try:
                versionnum = input('Version: ')
                if versionnum == 'back':
                    return
                for version in inputversionname:
                    if str(versionnum) == version['Id']:
                        versionnum = int(version['Number'])
                        break

                if int(versionnum) >= 0 and int(versionnum) < int(self.MinecraftSettings["Launcher-Settings"]['Visible-Versions']):
                    versionnum = int(versionnum)
                    break
            except ValueError:
                pass

        # ------------------------------------------
        # ----[Скачивание Майкрафт клиента]---------
        # ------------------------------------------
        
        self.DownloadInformation['Download-Url-Core-Json'] = self.Jsonfile[versionnum]['url']
        self.DownloadInformation['VersionMinecraft'] = self.Jsonfile[versionnum]['id']

        self.JSon_Version = date(self.DownloadInformation['Download-Url-Core-Json'])

        self.DownloadInformation['Download-Url-Core-url'] = self.JSon_Version["downloads"]["client"]["url"]
        self.DownloadInformation['Download-AssetIndex'] = self.JSon_Version['assets']
        self.DownloadInformation['Download-Url-AssetIndex-Json'] = self.JSon_Version['assetIndex']["url"]
        self.DownloadInformation['Download-Url-AssetIndex-Id'] = self.JSon_Version['assetIndex']["id"]
        self.DownloadInformation['Download-Url-AssetIndex-Sha1'] = self.JSon_Version['assetIndex']["sha1"]
        self.DownloadInformation['Download-Lbraries'] = self.JSon_Version['libraries']
        
        if self.JSon_Version.get('logging') != None:
            self.DownloadInformation['Download-Url-Logging'] = self.JSon_Version['logging']["client"]['file']['url']
            self.DownloadInformation['Download-Logging'] = self.JSon_Version['logging']

        self.SetUpFiles()
        self.Minecraft_DVaJF()

        self.StatusTasks(self.Downloadlist)
 
        self.MinecraftDA()
        self.MinecraftDL()

        for _ in range(len(self.tasks)-1):
            self.StatusTasks(self.Downloadlist)

        self.MinecraftDNdll()        
        self.StatusTasks(self.Downloadlist)

        self.MinecraftCSF()
        print(f'End Download Minecraft Client: {self.DownloadInformation["VersionMinecraft" ]}')

    def RunFileminecraft(self) -> None:
        """
        Run Minecraft Client
        """
        if misdir(f'{self.McPath}/versions') != True:
            print(self.speck['MenuMessage']['ErrorNoVersion'])
            msystem('pause')
            mcls()
        else:
            loadversion = mwhatinfile(f'{self.McPath}/versions')

            listversions = []

            for num, version in enumerate(loadversion):
                listversions.append({
                    'Id': version,
                    'Number': num
                })
            
            listversions.reverse()
            listversions2 = {}
            for x in listversions:
                listversions2[x["Number"]] = x['Id']
            print(self.speck['MenuMessage']['BrackMessage'].format('back'))
            print(', '.join([f"{x['Number']}: {x['Id']}" for x in listversions]))
            while True:
                try:
                    versionnum = input('Version: ')
                    if versionnum == 'back':
                        return
                    for version in listversions:
                        if str(versionnum) == version['Id']:
                            versionnum = int(version['Number'])
                            break

                    if int(versionnum) >= 0 and int(versionnum) < len(listversions):
                        versionnum = int(versionnum)
                        break
                    else:
                        print(self.speck['MenuMessage']['ErrorNoVersion2'].format(versionnum))
                except ValueError:
                    print(self.speck['MenuMessage']['ErrorNoVersion2'].format(versionnum))

            StartfileJson = self.OJFile_Argg()
            if listversions2[versionnum] not in StartfileJson:
                print(self.speck['MenuMessage']['ErrorStartFileCrash'].format(listversions2[versionnum]))
            else:
                StartFile = StartfileJson[listversions2[versionnum]]
                argum = str(StartFile['Dlog4']).split()
                try:
                    subprocess.call(f"{str(StartFile['Java'])}".replace("'", '"')+f" {StartFile['Memory']} {' '.join(argum)};{StartFile['Client']} {StartFile['MinecraftArg']}")
                except: pass
                # open(f'Minecarft-{listversions2[versionnum]}-Start.bat','w').write(f"@echo off\n{str(StartFile['Java'])}".replace("'", '"')+f" {StartFile['Memory']} {' '.join(argum)};{StartFile['Client']} {StartFile['MinecraftArg']}")
                # subprocess.call(f"Minecarft-{listversions2[versionnum]}-Start.bat")
            msystem('pause')
            

class TerminalMenu():
    def __init__(self) -> None:
        self.CaptionsMenus = []
        self.speck = launch().speck

        self.MaxSize = 1
        self.whileTrue = False 
    def Menu(self, Name, *, discription: str='') -> None:
        self.CaptionsMenus.append(
            {'ID': Name, 'Type': len(self.CaptionsMenus), "Discription": discription if (discription.strip() != '') else ''}
        )

    def run(self):
        for i in self.CaptionsMenus:
            if int(len(i['ID'])+len(i['Discription'])) > self.MaxSize:
                self.MaxSize = int(len(i['ID'])+len(i['Discription']))
        while not self.whileTrue:
            # print('[+]>-----'+'-'*self.MaxSize+'<[+]')
            print(self.speck["WelcomeLauncher"].format(LauncherSettings['Caption'], LauncherSettings['Version']))
            for pri in self.CaptionsMenus:
                if pri["Discription"] != "":
                    print(f'[{pri["Type"]}: {pri["Discription"]}] {pri["ID"]}')
                else:
                    print(f'{pri["Type"]}: {pri["ID"]}')
            # print('[+]>-----'+'-'*self.MaxSize+'<[+]')

            try:
                num = int(input(': '))
            except ValueError:
                mcls()
            except KeyboardInterrupt:
                exit()
            else:
                for x in self.CaptionsMenus:
                    if num == x['Type']:
                        self.whileTrue = True
                else:
                    mcls()
        self.whileTrue = False
        return num

def main():
    while True:
        mcls()
        if not mexists('./logs'):
            mkdir('./logs')
        if misfile("./UserSettings.json") == False:
            lan = input("Language: ")
            if lan.split() == "":
                lan = "en"
            file = {
                "Info-User": {
                    "Name-with-Game": input("Your Game in nick: "),
                    "Language": lan,
                    "Java-Path": input("Path to Java or write Java: "),
                    "Memory-Min": int(input("Min Memory in Megabytes: ")),
                    "Memory-Max": int(input("Max Memory in Megabytes: "))
                },
                "Launcher-Settings": {
                    "Minecraft-Path": '.minecraft',
                    "Visible-Versions": 20,
                    "Release-Versions": True,
                    "Snapshot-Version": False,
                    "Old-Versions": False
                }
            }   
            input_json("./UserSettings.json", file)
        else:
            speck = launch().speck
            MLauncher = MinecraftLauncher()
            MLauncher.DetectNowVersionLauncher()

            menu = TerminalMenu()
            menu.Menu(speck['MenuMessage']['DownloadVersion'])
            menu.Menu(speck['MenuMessage']['VersionList'])
            number = menu.run()

            if number == 0:
                mcls()
                MLauncher.RunLauncher()
            elif number == 1:
                mcls()
                MLauncher.RunFileminecraft()
    
if __name__ == "__main__":
    mcls()
    mtitle(f'{LauncherSettings["Caption"]} V{LauncherSettings["Version"]}')
    main()
