
from django.core.management.base import BaseCommand, CommandError
import collect_library as collectLib
from craftDB.wikiparser import Log_Node
from craftDB.models import ModPack

class Command(BaseCommand):

    #help = 'Links mods with modpack, adds recipes for that modpack with user input'

    def add_arguments(self, parser):
        parser.add_argument('mod_name', type=str)
        parser.add_argument('modpack_name', type = str)

    def handle(self, *args, **options):
              
        mod_name = options['mod_name']
        modpack_name = options['modpack_name']

        ModPack.objects.get(name = modpack_name)
        
        root_log = Log_Node('Connecting to wiki for collection...')
        while True:
            save_log = input('Save Log? (Y/N)')
            if save_log == '' or save_log.lower() == 'y' or save_log.lower() == 'n':
                break

        if save_log.lower() == 'y':
            print('YEET')

        print(root_log)
        try:
            collectLib.collect_mod(mod_name, root_log, modpack_name)
        finally:
            #print(root_log)
            pass