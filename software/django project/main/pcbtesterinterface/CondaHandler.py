# -*- coding: utf-8 -*-
import os
import subprocess
import json

#PLUGINCHANNEL = "conda-forge"
PLUGINCHANNEL = "marcom"

def downloadPackage(name, version=None):
    '''Returns result, message'''
    if "CONDA_DEFAULT_ENV" in os.environ.keys():
        env = os.environ["CONDA_DEFAULT_ENV"]
        if version:
            command = "conda install {pn}={v} -q -n {n} -c {c} --json"\
                .format(pn = name, n = env, c = PLUGINCHANNEL, v=version)
            print(command)
        else:
            command = "conda install {pn} -q -n {n} -c {c} --json"\
                .format(pn = name, n = env, c = PLUGINCHANNEL)
            print(command)
        n = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        
        # map json output to a dictionary
        try:
            obj = json.loads(n.stdout)
        except:
            return False, "Unable to download the plugin: {}\n{}".format(name, n.stdout)
            
        if("success" in obj.keys() and obj["success"]):
            if version:
                return True, "{}={}".format(name,version)
            else:
                return True, "{}".format(name)
        else:
            if("message" in obj.keys()):
                return False ,obj["message"]
            return False, "Unable to install plugin: {}".format(name)
    return False, "no conda environment detected"

def getVersion_locally(name):
    '''Returns success, packet_installed, message'''
    if isCondaEnvironment():
        env = getCondaEnvironment()
        command = "conda list {pluginname} -n {env} --json"\
            .format(pluginname = name, env = env)
        n = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        
        # map json output to a dictionary
        try:
            obj = json.loads(n.stdout)
        except:
            return False, False, "Unable to find the plugin"
        for entry in obj:
            if type(entry)==dict and "name" in entry and entry["name"] == name:
                if "version" in entry.keys() and "build_number" in entry.keys():
                    # return version
                    return True, True, "{}={}".format(entry['version'], entry['build_number'])
        return True, False, "Package not found: {}"\
                    .format(name)
    return False, False, "no conda environment detected"

def getVersion_condas(name, majorversion):
    '''Returns result, message'''
    if "CONDA_DEFAULT_ENV" in os.environ.keys():
        # run search command
        command = "conda search {pluginname} -c {channel} --json"\
            .format(pluginname = name, channel = PLUGINCHANNEL)
        n = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        
        # map json output to a dictionary
        try:
            obj = json.loads(n.stdout)
        except:
           return False, "Unable to search for a new version"
        first = True
        newestversion = None
        
        # find the newest version
        # iterate over all available verions
        if name in obj.keys():
            for entry in obj[name]:
                if type(entry) == dict and "version" in entry.keys()\
                    and "build" in entry.keys():
                    currentversion = "{}={}".format(entry["version"], entry["build"])
                    if not isMajorversion(currentversion, majorversion):
                        continue
                    if first:
                        if version_to_intlist(currentversion):
                            newestversion = currentversion
                            first = False
                    else:
                        # compare version
                        success, result = is_Version2_greater_than_version1(newestversion, currentversion)
                        if success and result:
                            newestversion = currentversion
                        elif not success:
                            continue
            # return newest version if available
            if newestversion:
                return True, newestversion
            else:
                return False, "No version available for: {}"\
                    .format(name)
        else:
            return False, "Package not found: {}"\
                    .format(name)
    return False, "no conda environment detected"

def getAvailableVersions(name, majorversion):
    '''Returns result, list of versions'''
    if "CONDA_DEFAULT_ENV" in os.environ.keys():
        # run search command
        command = "conda search {pluginname} -c {channel} --json"\
            .format(pluginname = name, channel = PLUGINCHANNEL)
        n = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)
        
        # map json output to a dictionary
        try:
            obj = json.loads(n.stdout)
        except:
           return False, "Unable to search for a new version"
        
        result = []
        # find the newest version
        # iterate over all available verions
        if name in obj.keys():
            for entry in obj[name]:
                if type(entry) == dict and "version" in entry.keys()\
                    and "build" in entry.keys():
                    currentversion = "{}={}".format(entry["version"], entry["build"])
                    if not isMajorversion(currentversion, majorversion):
                        continue
                    version = version_to_intlist(currentversion)
                    if version:
                        result.append(currentversion)
            # return the list
            return True, result
        else:
            return False, "Package not found: {}"\
                    .format(name)
    return False, "no conda environment detected"

def is_Version2_greater_than_version1(version1, version2):
    '''Returns success, whether version2 is greater than version1'''
    if not version_to_intlist(version2):
        return True, False
    version1list = version_to_intlist(version1)
    version2list = version_to_intlist(version2)
    if not version2list:
        return False, False
    elif not version1list:
        return False, False
    # Determine length
    length = len(version1list)
    if len(version2list) > length:
        length = len(version2list)
    
    for i in range(length):
        if i == len(version2list):
            return True, False
        elif i == len(version1list):
            return True, True
        elif version2list[i] > version1list[i]:
            return True, True
    return True, False

def version_to_intlist(version):
    ''' Returns the version as a list of integers'''
    try:
        split = version.split("=")
        if split:
            build = version.split("=")[1]
            versionstr = version.split("=")[0]
            versionlist = [int(v) for v in versionstr.split(".")]
            versionlist.append(int(build))
        else:
            versionstr = version
            versionlist = [int(v) for v in versionstr.split(".")]
        return versionlist
    except:
        return None

def isMajorversion(version, majorversion):
    versionlist = version_to_intlist(version)
    if not versionlist:
        return False
    try:
        if versionlist[0] == int(majorversion):
            return True
        else:
            return False
    except:
        return False

def getNewestVersion(name, majorversion):
    '''Returns success, message'''
    try:
        # check online versions
        return getVersion_condas(name, majorversion)
    except Exception:
        return False, "Exception while looking for a new version for: {}"\
            .format(name)

def newVersion_available(name, majorversion):
    '''Returns success, result, message'''
    try:
        # check local version
        success, ispacketinstalled, message1 = getVersion_locally(name)
        if success:
            if not ispacketinstalled:
                return True, False, "Packet not installed: {}".format(name)
        else:
            return False, False, "Failure while getting the local package: {}"\
                .format(name)
        
        # check online versions
        result2, message2 = getVersion_condas(name, majorversion)
        if not result2:
            return False, False, message2
        
        # compare versions
        success2, result3 = is_Version2_greater_than_version1(message1, message2)
        if success2 and result3:    
            return True, True, message2
        elif success2 and not result3:
            return True, False, "No new version available"
        return False, False, "Exception while comparing the two versions {} and {}"\
            .format(message1, message2)
    except Exception:
        return False, False, "Exception while looking for a new version for: {}"\
            .format(name)

def install_newVersion(name, majorversion):
    '''Returns result, message'''
    # check for new version
    success, result, message = newVersion_available(name, majorversion)
    if success and result:
        try:
            # download the new version
            result, message = downloadPackage(name, version=message)
            if result:
                return True, "Installed new package {}".format(message)
            else:
                return False, "Unable to install package {}\nMessage: {}".format(name,message)
        except:
            return False, "Unable to download the package {}".format(name)
    elif success:
        return False, message
    else:
        return (
            False,
            "Failure while looking for the new version with messag.\n{}"
            .format(message)
            )


def isPackageInstalled(name, majorversion, version=None):
    '''Returns whether package is installed'''
    if isCondaEnvironment():
        env = getCondaEnvironment()
        command = f"conda list {name} -n {env} --json"
        n = subprocess.run(command, shell=True,
                           capture_output=True, universal_newlines=True)

        # map json output to a dictionary
        try:
            obj = json.loads(n.stdout)
        except:
            return False
        for entry in obj:
            if isinstance(entry, dict) and "name" in entry.keys()\
                    and entry["name"] == name:
                if "version" in entry.keys() and \
                    isMajorversion(entry["version"], majorversion):
                    if version:
                        if  version==entry["version"]:
                            return True
                        else:
                            return False
                    return True
                else:
                    return False
    return False

def isCondaEnvironment():
    return "CONDA_DEFAULT_ENV" in os.environ.keys()

def getCondaEnvironment():
    return os.environ["CONDA_DEFAULT_ENV"]

# example usage
# result, message = install_newVersion(name)
# print("Result: {}, Message: {}".format(result, message))
        
if __name__ == '__main__':
    print(is_Version2_greater_than_version1("0.0.2=1", "0.0.2=10"))