import craftDB.wikiparser as wp
import craftDB.recipefinder as rf
from craftDB_site.settings import DOMAIN_NAME
import webbrowser
import requests
import json

def open_webpage(url):
            webbrowser.open(DOMAIN_NAME + url)
            if input('Press [Enter] to continue, type "skip" to skip:') =='skip':
                raise wp.BadItemPageException('Item skipped, did not add recipes to database.')


def collect_mod(mod_name):
    
    mod_items_endpoint = 'https://ftbwiki.org/api.php?action=query&list=categorymembers&cmtitle=Category:{}&cmlimit=10000&format=json'

    r = requests.get(mod_items_endpoint.format(mod_name))

    try:
        item_pages = json.loads(r.text)['query']['categorymembers']

        print(mod_name)
        for item_page_data in item_pages:
            print(' * ', item_page_data['title'])
            page_title = item_page_data['title']
            display_name, mod = wp.parse_pagetitle(page_title)
            item = None
            try:
                while item == None:
                    try:
                        item = rf.hitDB_or_wiki_for_item(display_name, mod, page_title)
                    except wp.NoWikiTextException as err:
                        print('Error: ', str(err))
                        compiled_error = wp.IncompletePageException(page_title, {'display_name':display_name, 'mod':mod})
                        open_webpage(compiled_error.create_item_url)
                    except wp.IncompletePageException as err:
                        print('Error: ', page_title, ' contains incomplete information')
                        open_webpage(err.create_item_url)
                
                if item: # continue writing here
                    print('Found item: {}'.format(page_title))
                    print('**Now work on recipes!!')

            except wp.NoInfoboxException as err:
                print('Error: {} is not landing page for item'.format(page_title))
            except wp.BadItemPageException as err:
                print('Error: ', str(err))

    except KeyError:
        print('Mod: {} contains no items'.format(mod_name))