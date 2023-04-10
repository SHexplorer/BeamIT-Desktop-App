import requests
from typing import List
import json
from time import sleep
from threading import Thread, Event
import webbrowser
import pyperclip

import util

"""
Class for receiving and handling shared data
"""
class beamit_receive():
    server_url = None
    username = None
    devicename = None
    devicetoken = None
    filePath = None
    autoOpen = None
    timeout = 5

    receivethread = None
    stopEvent = Event()

    """
    Method to initialize a receiver instance
    """
    def init(self, server_url: str, username: str, devicename: str, devicetoken: str, filePath: str, autoOpen: bool) -> None:
        self.server_url = server_url
        self.username = username
        self.devicename = devicename
        self.devicetoken = devicetoken
        self.filePath = filePath
        self.autoOpen = autoOpen
        self.receivethread = Thread(target=self.receive, args=(self.stopEvent, ))

    """
    Method to start the receiver thread
    """
    def start(self):
        self.receivethread.start()

    """
    Method to stop the receiver thread
    """
    def stop(self):
        self.stopEvent.set()
        self.receivethread.join()

    """
    Method to periodically check for new data and handle it accordingly
    """
    def receive(self, event: Event):
        while(1):
            try:
                if event.is_set():
                    break
                dataAvailable = self.beamitCheckAvailableData()
                if dataAvailable['successfull']:
                    for data in dataAvailable['message']:
                        if data[3] == "url":
                            self.beamitReceive(data[0])
                            webbrowser.open(data[4])
                        if data[3] == "text":
                            self.beamitReceive(data[0])
                            print(data[4])
                            pyperclip.copy(data[4])
                        if data[3] == "file":
                            filename, filecontent = self.beamitReceiveFile(data[0])
                            util.storeFile(path=self.filePath, filename=filename, content=filecontent)
                            if self.autoOpen:
                                util.startfile(path=self.filePath, filename=filename)
            except Exception as e:
                print(e)
            finally:
                pass
            sleep(1)

    """
    Method to check for available data on server
    """
    def beamitCheckAvailableData(self) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken}
        response = requests.post(self.server_url + "/beamit/checkAvailableData", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))
    
    """
    Method to receive text or url data
    """
    def beamitReceive(self, timestamp: str) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'timestamp' : timestamp}
        response = requests.post(self.server_url + "/beamit/receive", data=data, timeout=self.timeout)
        if response.headers['content-type'] == 'application/json':
            return json.loads(response.text.strip(']['))
    
    """
    Method to receive file data
    """
    def beamitReceiveFile(self, timestamp: str) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'timestamp' : timestamp}
        response = requests.post(self.server_url + "/beamit/receive", data=data, timeout=self.timeout)
        if response.headers['content-type'] == 'application/octet-stram':
            filename = response.headers['content-disposition'].removeprefix('attachment; filename="').removesuffix('"')
            return filename, response.content
    
"""
Class to send data to server
"""
class beamit_send():
    server_url = None
    username = None
    devicename = None
    devicetoken = None
    timeout = 5

    """
    Method to initialize a sender instance
    """
    def init(self, server_url: str, username: str, devicename: str, devicetoken: str) -> None:
        self.server_url = server_url
        self.username = username
        self.devicename = devicename
        self.devicetoken = devicetoken

    """
    Method to register a user on the server
    """
    def register(self, username: str, password: str) -> json:
        data = {'username' : username, 'password' : password}
        response = requests.post(self.server_url + "/user/register", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))

    """
    Method to unregister a user on the server
    """
    def unregister(self) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken}
        response = requests.post(self.server_url + "/user/unregister", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))

    """
    Method to add a device on the server
    """
    def login(self, url: str, username: str, password: str, devicename: str):
        data = {'username' : username, 'password' : password, 'devicename' : devicename}
        response = requests.post(url + "/user/login", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))
    
    """
    Method to remove a device on the server
    """
    def removeDevice(self, targetDevice: str) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'targetDevice': targetDevice}
        response = requests.post(self.server_url + "/device/remove", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))

    """
    Method to list all devices for a user on the server
    """
    def listDevices(self) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken}
        response = requests.post(self.server_url + "/device/list", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))
    
    """
    Method to rename the current device on the server
    """
    def renameDevices(self, devicenameNew) -> json:
        data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'devicenameNew' : devicenameNew}
        response = requests.post(self.server_url + "/device/rename", data=data, timeout=self.timeout)
        return json.loads(response.text.strip(']['))

    """
    Method to send data to other clients of user
    """
    def beamitShare(self, targetDevices: list, autoOpen: bool, encrypted: bool, datatype: str, senddata: str | tuple) -> json:
        response = None
        if datatype == "text":
            data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'targetDevices' : targetDevices, 'autoOpen' : autoOpen, 'encrypted' : encrypted, 'text' : senddata}
            response = requests.post(self.server_url + "/beamit/share", data=data, timeout=self.timeout)
            return json.loads(response.text.strip(']['))
            
        if datatype == "url":
            data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'targetDevices' : targetDevices, 'autoOpen' : autoOpen, 'encrypted' : encrypted, 'url' : senddata}
            response = requests.post(self.server_url + "/beamit/share", data=data, timeout=self.timeout)
            return json.loads(response.text.strip(']['))

        if datatype == "files":
            senddata = {'files': senddata}
            data = {'username' : self.username, 'devicename' : self.devicename, 'devicetoken' : self.devicetoken, 'targetDevices' : targetDevices, 'autoOpen' : autoOpen, 'encrypted' : encrypted}
            response = requests.post(self.server_url + "/beamit/share", data=data, files=senddata, timeout=self.timeout)
            return json.loads(response.text.strip(']['))