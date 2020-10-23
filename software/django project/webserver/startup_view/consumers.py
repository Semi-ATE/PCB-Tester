# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 15:01:53 2020

@author: test
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer
from channels.db import database_sync_to_async
from datetime import datetime
from asgiref.sync import async_to_sync
from pcbtesterinterface import viewinterface as interface

scriptgroup = "scriptgroup"


class ScriptConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def getUserid(self):
        return self.scope["session"]["customuserid"]
        
    async def connect(self):
        self.userid = await self.getUserid()
        self.groupname = scriptgroup
        
        #Join group
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            self.state = text_data_json['state']
            self.scriptname = text_data_json['scriptname']
            self.version = text_data_json['version']
        except:
            await self.displaycontent({
                'information': "Invalid data received"
            })
            return
        
        if not self.state == 'runplugin':
            await self.displaycontent({
                'information': "Invalid state received"
            })
            return
        
        # start script if not already another script running
        if not self.version in interface.getAvailableVersions():
            # no valid version
            await self.displaycontent({
                'information': "Invalid version selected"
            })
        elif self.version == interface.getCurrentVersion():
            # selected version is currentversion -> runscript
            if self.scriptname in interface.getAllDevicePluginNames():
                # runscript
                if interface.isScriptRunning():
                    # already running
                    await self.displaycontent({
                        'information': "A script is already running"
                    })
                else:
                    # run script
                    await self.channel_layer.send(
                        "scripthandler",
                        {
                            "type": "runScript",
                            "groupname": self.groupname,
                            "scriptname": self.scriptname,
                            "version": self.version,
                            "username": interface.getUsername(self.userid)
                        },
                    )
            else:
                # invalid scriptname
                await self.displaycontent({
                    'information': "Scriptname not found"
                })
        else:
            # download selected version
            if interface.isScriptRunning():
                # plugin is already running
                await self.displaycontent({
                    'information': "Unable to download. A script is running"
                })
            else:
                # downloading selected version
                await self.channel_layer.send(
                    "scripthandler",
                    {
                        "type": "downloadVersion",
                        "groupname": self.groupname,
                        "version": self.version
                    },
                )
    
    async def displaycontent(self, event):
        # Send message to WebSocket
        if not 'message' in event.keys():
            event['message'] = None
        if not 'information' in event.keys():
            event['information'] = None
        await self.send(text_data=json.dumps(
            event
            ))
    
    async def displaycontentall(self, event):
        event['type'] = 'displaycontent'
        await self.channel_layer.group_send(
            self.groupname,
            event
        )

class RunScript(SyncConsumer):
    
    # send to channels
    def writeToGroup(self, message="", time=False, spinner=False, type='displaycontent', additionaldata=None):
        if time:
            strtime = datetime.now().strftime("%b-%d-%Y;%H:%M:%S")
            message = f"{strtime}> " + message
        self.messagebuffer += message
        self.messagebuffer = make_carriagereturn(self.messagebuffer)
        event = {'type': type, 'message': self.messagebuffer, 'spinner': spinner}
        if additionaldata:
            event = {**additionaldata, **event}
        async_to_sync(self.channel_layer.group_send)(
            self.groupname, event
        )
    
    # receive from channels
    def downloadVersion(self, event):
        self.messagebuffer = ""
        try:
            self.version = event["version"]
            self.groupname = event["groupname"]
            if not self.version in interface.getAvailableVersions():
                # invalid version
                self.writeToGroup("Unable to download the selected version.\n"+
                                  "The version is not valid.\n")
                return
            if not interface.isScriptRunning():
                # download version
                interface.setScriptRunning(True)
                self.writeToGroup(f"Downloading version: {self.version}\n",True,
                                  spinner=True)
                result, message = interface.downloadPackage(
                    interface.getDetectedPlugin(), self.version)
                self.writeToGroup(spinner=False)
                if result:
                    interface.updateAllDevicePluginNames()
                    interface.reloadPLugins()
                    interface.setCurrentVersion(self.version)
                    # write succesmessage and update view with new version
                    # and new pluginnames
                    self.writeToGroup("{} with version {} successfully installed.\n"\
                        .format(interface.getDetectedPlugin(), self.version)
                        , True, additionaldata={
                            "currentversion": self.version,
                            "pluginlist": interface.getAllDevicePluginNames()
                        })
                        
                else:
                    # download failed
                    self.writeToGroup(message, True)
                interface.setScriptRunning(False)
            else:
                self.writeToGroup("Unable to download the selected version.\n"+
                                  "A script is currently running\n")
        except:
            self.writeToGroup("An error occured while downloading the package\n")
            interface.setScriptRunning(False)
        self.messagebuffer = ""
    
    # receive from channels
    def runScript(self, content):
        try:
            if not  interface.isScriptRunning():
                interface.setScriptRunning(True)
                self.groupname = content["groupname"]
                self.packagename = interface.getDetectedPlugin()
                self.scriptname = content["scriptname"]
                self.version = content["version"]
                self.username = content["username"]
                
                # setup messagebuffer
                self.messagebuffer = ""
                
                # reload plugin, because this class
                # can be executed in a different process
                interface.reloadPLugins()
                
                # run test
                self.starttime = datetime.now()
                self.resultstate, self.resultmessage = self.maketest(self.scriptname)
                self.endtime = datetime.now()
                
                # write test in database
                interface.addTestResults(
                    self.starttime,
                    self.endtime,
                    self.username,
                    self.packagename,
                    self.version,
                    self.scriptname,
                    self.messagebuffer,
                    self.resultstate,
                    self.resultmessage
                )
                # clear messagebuffer
                self.messagebuffer = ""
                interface.setScriptRunning(False)
        except Exception as e:
            interface.setScriptRunning(False)
            self.writeToGroup(f"\nAn Exception occured while trying to run the plugin:\n{e}", True)
    
    # select test and run test
    def maketest(self, scriptname):
        try:
            #callback for user output
            def printcallback(content="", time=False, spinner=False, lineending="\n"):
                self.writeToGroup(message=content+lineending, time=time,
                                  spinner=spinner)
            result, resultmessage = interface.runPlugin(scriptname, printcallback)
            if result:
                self.writeToGroup(f"PASS: {resultmessage}\n", True)
            else:
                self.writeToGroup(f"FAIL: {resultmessage}\n", True)
            return result, resultmessage
        except Exception as e:
            return False, "Excpetion in plugin: "+e

# compute carriage return
def make_carriagereturn(content):
    for i in range(len(content)-1, -1, -1):
        if(content[i] == '\r'):
            # remove substring
            endindex = i
            for a in range(endindex-1, -1, -1):
                # remove until line break
                if content[a] == '\n':
                    content = content[0:a+1] + content[endindex+1:len(content)]
                    break
            else:
                # remove everything
                content = content[endindex:len(content)]
                break
            break
    return content
