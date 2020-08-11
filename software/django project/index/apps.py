from django.apps import AppConfig
from main import main

class IndexConfig(AppConfig):
    name = 'index'
    
    def ready(self):
        print("ready")
        main.run()
