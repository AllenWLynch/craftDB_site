import craftDB.wikiparser as wp
import craftDB.recipefinder as rf
from craftDB_site.settings import DOMAIN_NAME
import webbrowser
import requests
import json
from craftDB.models import ModPack, Mod


class UserSkippedException(Exception):
    
    def __init__(self, msg, incomplete_page_error, skip_item = False, skip_mod = False):
        self.msg = msg
        self.skip_item = skip_item
        self.skip_mod = skip_mod
        self.incomplete_page_error = incomplete_page_error

    def __str__(self):
        return str(self.msg)


def open_webpage(incomplete_page_error):
    webbrowser.open(DOMAIN_NAME + incomplete_page_error.create_item_url)
    user_input = input('Press [Enter] to continue, type "skip" to skip:')
    terms = [s.lower().strip() for s in user_input.split(' ')]
    if len(terms) > 0 and terms[0] == 'skip':
        if len(terms) >= 2:
            if terms[1] == 'item':
                raise UserSkippedException('Item skipped, did not add recipes to database.', incomplete_page_error, skip_item = True)
            elif terms[1] == 'mod':
                raise UserSkippedException('Item skipped, did not add recipes to database.', incomplete_page_error, skip_mod = True)
        else:
            raise UserSkippedException('Item skipped, did not add recipes to database.', incomplete_page_error)

def old_collect_mod(mod_name, root_lognode, modpack = 'all'):

    skip_items = set()
    skip_mods = set()
    
    mod_items_endpoint = 'https://ftbwiki.org/api.php?action=query&list=categorymembers&cmtitle=Category:{}&cmlimit=10000&format=json'

    r = requests.get(mod_items_endpoint.format(mod_name), True)

    mod_node = root_lognode.add_node('Collecting Mod: {}'.format(mod_name), 'max')
    print(mod_node)

    try:
        item_pages = json.loads(r.text)['query']['categorymembers']
    except KeyError:
        print(mod_node.add_node('Mod: {} contains no items'.format(mod_name)))
    
    for item_page_data in item_pages:
        page_title = item_page_data['title']
        item_node = mod_node.add_node('Collecting Item: {}'.format(page_title))
        print(item_node)
        display_name, mod = wp.parse_pagetitle(page_title)
        item = None
        try:
            try:
                while item == None:
                    try:
                        item = rf.hitDB_or_wiki_for_item(display_name, mod, page_title, item_node)
                    except wp.IncompletePageException as err:
                        print(item_node.add_node(str(err)))
                        open_webpage(err)
                    except wp.NoWikiTextException as err:
                        print(item_node.add_node(str(err)))
                        open_webpage(wp.IncompletePageException(page_title, {'display_name':display_name, 'mod':mod}))
            except wp.BadItemPageException as err:
                print(item_node.add_node(err))
                        
            if item: # continue writing here
                q = wp.PageParser(page_title)
                for recipe in q.scrape_recipes():
                    if not any(banned_item_page in recipe['recipe_terms'] for banned_item_page in skip_items):
                        while True:
                            try:    
                                prelim_recipe_data = rf.instantiate_recipe(page_title, item, **recipe)
                                #print('From mod:', prelim_recipe_data['new_recipe'].from_mod)
                                #print(modpack == 'all', prelim_recipe_data['new_recipe'].from_mod in ModPack.objects.get(name = modpack).mods.all(), not prelim_recipe_data['new_recipe'].from_mod.name in skip_mods)
                                if (modpack == 'all' or prelim_recipe_data['new_recipe'].from_mod in ModPack.objects.get(name = modpack).mods.all()) and not prelim_recipe_data['new_recipe'].from_mod.id in skip_mods: 
                                    try:
                                        sub_log = rf.parse_recipe(**prelim_recipe_data)
                                    except rf.ConstructRecipeException as err:
                                        print(item_node.add_node(str(prelim_recipe_data['parent_node'].value) + '-> ERROR: ' + str(err.sub_error)))
                                        try:
                                            raise err.sub_error
                                        except wp.IncompletePageException as err:
                                            # fix this here from opening prompts for mods that are skipped
                                            if not err.scraped_data['mod'] in skip_mods:
                                                open_webpage(err)
                                        except wp.BadItemPageException as err:
                                            incomplete_exception = wp.IncompletePageException(page_title, {'display_name':err.display_name, 'mod':err.mod})

                                            open_webpage(wp.IncompletePageException(page_title, {'display_name':err.display_name, 'mod':err.mod}))
                                        #except wp.BadItemPageException as err:   
                                    else:                                     
                                        item_node.connect_nodes(sub_log)
                                        print(sub_log)
                                        break
                                else:
                                   break
                            except rf.ConstructRecipeException as err:
                                print(item_node.add_node(err))
                            except UserSkippedException as err:
                                print(item_node.add_node(err))
                                if err.skip_item:
                                    skip_items.add(page_title)
                                if err.skip_mod and err.incomplete_page_error.scraped_data['mod']:
                                    skip_mods.add(err.incomplete_page_error.scraped_data['mod'])
                                break
                    else:
                        print(item_node.add_node('Template {} contains skipped item.'.format(recipe['header'])))

        except UserSkippedException as err:
            print(item_node.add_node(err))
            if err.skip_item:
                skip_items.add(page_title)
            if err.skip_mod and err.incomplete_page_error.scraped_data['mod']:
                skip_mods.add(err.incomplete_page_error.scraped_data['mod'])
                
## work on this
def old_collect_mod(mod_name, root_lognode, modpack = 'all'):

    skip_items = set()
    skip_mods = set()
    
    mod_items_endpoint = 'https://ftbwiki.org/api.php?action=query&list=categorymembers&cmtitle=Category:{}&cmlimit=10000&format=json'

    r = requests.get(mod_items_endpoint.format(mod_name), True)

    mod_node = root_lognode.add_node('Collecting Mod: {}'.format(mod_name), 'max')
    print(mod_node)

    try:
        item_pages = json.loads(r.text)['query']['categorymembers']
    except KeyError:
        print(mod_node.add_node('Mod: {} contains no items'.format(mod_name)))
    
    for item_page_data in item_pages:
        page_title = item_page_data['title']
        item_node = mod_node.add_node('Collecting Item: {}'.format(page_title))
        print(item_node)
        display_name, mod = wp.parse_pagetitle(page_title)
        item = None
        try:
            try:
                while item == None:
                    try:
                        item = rf.hitDB_or_wiki_for_item(display_name, mod, page_title, item_node)
                    except wp.IncompletePageException as err:
                        print(item_node.add_node(str(err)))
                        open_webpage(err)
                    except wp.NoWikiTextException as err:
                        print(item_node.add_node(str(err)))
                        open_webpage(wp.IncompletePageException(page_title, {'display_name':display_name, 'mod':mod}))
            except wp.BadItemPageException as err:
                print(item_node.add_node(err))
                        
            if item: # continue writing here
                q = wp.PageParser(page_title)
                for recipe in q.scrape_recipes():
                    if not any(banned_item_page in recipe['recipe_terms'] for banned_item_page in skip_items):
                        while True:
                            try:    
                                prelim_recipe_data = rf.instantiate_recipe(page_title, item, **recipe)
                                #print('From mod:', prelim_recipe_data['new_recipe'].from_mod)
                                #print(modpack == 'all', prelim_recipe_data['new_recipe'].from_mod in ModPack.objects.get(name = modpack).mods.all(), not prelim_recipe_data['new_recipe'].from_mod.name in skip_mods)
                                if (modpack == 'all' or prelim_recipe_data['new_recipe'].from_mod in ModPack.objects.get(name = modpack).mods.all()) and not prelim_recipe_data['new_recipe'].from_mod.id in skip_mods: 
                                    try:
                                        sub_log = rf.parse_recipe(**prelim_recipe_data)
                                    except rf.ConstructRecipeException as err:
                                        print(item_node.add_node(str(prelim_recipe_data['parent_node'].value) + '-> ERROR: ' + str(err.sub_error)))
                                        try:
                                            raise err.sub_error
                                        except wp.IncompletePageException as err:
                                            # fix this here from opening prompts for mods that are skipped
                                            if not err.scraped_data['mod'] in skip_mods:
                                                open_webpage(err)
                                        except wp.BadItemPageException as err:
                                            incomplete_exception = wp.IncompletePageException(page_title, {'display_name':err.display_name, 'mod':err.mod})

                                            open_webpage(wp.IncompletePageException(page_title, {'display_name':err.display_name, 'mod':err.mod}))
                                        #except wp.BadItemPageException as err:   
                                    else:                                     
                                        item_node.connect_nodes(sub_log)
                                        print(sub_log)
                                        break
                                else:
                                   break
                            except rf.ConstructRecipeException as err:
                                print(item_node.add_node(err))
                            except UserSkippedException as err:
                                print(item_node.add_node(err))
                                if err.skip_item:
                                    skip_items.add(page_title)
                                if err.skip_mod and err.incomplete_page_error.scraped_data['mod']:
                                    skip_mods.add(err.incomplete_page_error.scraped_data['mod'])
                                break
                    else:
                        print(item_node.add_node('Template {} contains skipped item.'.format(recipe['header'])))

        except UserSkippedException as err:
            print(item_node.add_node(err))
            if err.skip_item:
                skip_items.add(page_title)
            if err.skip_mod and err.incomplete_page_error.scraped_data['mod']:
                skip_mods.add(err.incomplete_page_error.scraped_data['mod'])