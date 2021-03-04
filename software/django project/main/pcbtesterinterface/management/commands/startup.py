from django.core.management.base import BaseCommand, CommandError
import pcbtesterinterface.Database.databasemanager as databasemanager
import pcbtesterinterface.viewinterface as interface
import requests
from django.conf import settings
from markdown2 import Markdown
import os
from shutil import copyfile


class Command(BaseCommand):
    help = "Initiates the database and downloads the newest packages"
    
    def handle(self, *args, **options):
        try:
            # download readme main page semi-ate/pcbtester
            content = downloadReadme(settings.GITHUB_PCBTESTER_README_URL)
            if content:
                content = replace_urls(content, "/documentation/pictures/PCB-Tester.png")
                writetofile(convertToMarkup(content),
                        settings.GITHUB_PCBTESTER_README)
            else:
                writetofile("Unable to get readme file of github",
                        settings.GITHUB_PCBTESTER_README)
            
            # Database
            databasemanager.startup()
            # TODO
            """Do magic -> make users for database"""
            self.stdout.write(self.style.SUCCESS("Database startup finished"))
            
            # Viewinterface -> read eeprom, download version
            result, message = interface.startup()
            self.stdout.write(message)
            
            # download readme for home page provided by plugin
            try:
                interface.reloadPLugins()
                names = interface.getAllDevicePluginNames()
                if names:
                    result = interface.getHomePage(interface.getAllDevicePluginNames()[0])
                    if result:
                        content, image_urls,package_path, media_directory = result
                        content = makeContent(package_path, media_directory, content, image_urls)
                        writetofile(convertToMarkup(content), settings.GITHUB_HOME_README)
                    else:
                        writetofile("Unable to get the home page content of the plugin",
                                    settings.GITHUB_HOME_README)
                else:
                    writetofile("No plugins downloaded", settings.GITHUB_HOME_README)
            except:
                writetofile("No home page available", settings.GITHUB_HOME_README)

            self.stdout.write(self.style.SUCCESS("Startup finished"))
        except Exception as e:
            raise CommandError(f"Failure. Startup failed\n{e}")


def downloadReadme(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.content.decode('utf-8')
    except:
        return None

def saveMarkup(url: str, filepath: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            writetofile(convertToMarkup(r.content.decode('utf-8')),
                        filepath)
    except:
        writetofile("Unable to get readme file of github",
                        filepath)


def convertToMarkup(content: str):
    m = Markdown()
    return m.convert(content)


def writetofile(content: str, filepath: str):
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)


def replace_urls(content: str, url_from, url_to=None):
    if not url_to:
        url_to = (settings.MEDIA_URL+url_from).replace("//", "/")
    content = content.replace(f"<img src=\"{ url_from }\">",
                            f"<img src=\"{ url_to }\">")
    return content


def makeContent(package_path: str, media_directory: str, 
                content: str, image_urls: list):
    for image_url in image_urls:
        # set paths
        imagefilename = os.path.basename(image_url)
        imagefrom = os.path.normpath(package_path + os.sep + media_directory + os.sep + imagefilename)
        imageto = os.path.normpath(settings.MEDIA_ROOT + image_url)
        imagepathto = os.path.dirname(imageto)
        
        # make path in django
        if not os.path.exists(imagepathto):
            os.makedirs(imagepathto)
        
        # copy image
        copyfile(imagefrom, imageto)
        
        # replace ensure the path is valid
        content = replace_urls(content, image_url)
    return content