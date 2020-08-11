# -*- coding: utf-8 -*-
import subprocess
try:
    from django.utils import simplejson as json
except ImportError:
    import json

PLUGINNAME = "Plugin1"
PLUGINCHANNEL = "marcom"

def downloadPackage(name):
    result = subprocess.run(["conda","install",name,"-c",PLUGINCHANNEL,"--json"], capture_output=True, shell=True)
    print(result)
    dic = json.loads(result.stdout)
    print(dic)
    return dic.success



if __name__ == '__main__':
    downloadPackage("plugin1")