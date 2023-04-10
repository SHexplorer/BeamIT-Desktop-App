import os
import platform
import subprocess
import json

if platform.system() == "Windows":
    configPath = os.path.expandvars(r'%APPDATA%/BeamIT')
else:
    configPath = os.path.expandvars(r'/home/$USER/.beamit')

"""
Method to read config out of config.json file
"""
def getConfig():
    try:
        with open(os.path.join(configPath, "config.json"), 'r') as f:
            config = json.load(f)
            return config
    except:
        return None

"""
Method to store a config in a config.json file
"""
def storeConfig(serverurl: str, username: str, devicename: str, devicetoken: str, filepath: str, autoOpen: bool):
    jsonConfig = json.loads('{"serverurl": "%s", "username": "%s", "devicename": "%s", "devicetoken": "%s", "filepath": "%s", "autoOpen": "%s"}' % (serverurl, username, devicename, devicetoken, filepath, autoOpen))
    try:
        if not os.path.exists(configPath):
            os.makedirs(configPath)
        with open(os.path.join(configPath, "config.json"), 'w') as f:
            json.dump(jsonConfig, f)
            return True
    except Exception as e:
        return False

"""
Method to remove the config.json file
"""
def removeConfig():
    try:
        if os.path.exists(os.path.join(configPath, "config.json")):
            os.remove(os.path.join(configPath, "config.json"))
            return True
    except Exception as e:
        return False

"""
Method to create a new folder at a given path
"""
def createFolder(path: str):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            return True
        except:
            return False

"""
Method to read a file at a given path
"""
def getFile(filepath: str):
    filepath = filepath.removeprefix("file:///")
    filename = os.path.basename(filepath)
    f = open(filepath, 'rb')
    return filename, f

"""
Method to store a file at a given path
"""
def storeFile(path: str, filename: str, content):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(e)
        return False
    
    destfile = os.path.join(path, filename)

    try:
        f = open(destfile, "wb")
        f.write(content)
        f.close
    except Exception as e:
        print(e)
        return False

"""
Method to launch a file with its default program
"""
def startfile(path: str, filename: str, args: str = ""):
    destfile = os.path.join(path, filename)
    try:
        if platform.system() == "Windows":
            os.startfile(destfile, args)
        else:
            subprocess.call(["open", destfile])
    except Exception as e:
        print(e)