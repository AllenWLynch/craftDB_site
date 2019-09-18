'''

import craftDB.recipefinder as rf
rf.hitDB_or_wiki_for_item('Quarry','BuildCraft','Quarry')
'''
'''
import craftDB.wikiparser as wp
import craftDB.recipefinder as rf 
q = wp.PageParser('Wood Planks')

#print(wood.scrape_recipes())
#print(q.scrape_infobox())
#print('----')
#print(q.get_main_image())

#scraped = '\n\n'.join([str(num) + ': ' + str(x) for num, x in enumerate(q.scrape_recipes())])
#print(scraped)

output_item = rf.hitDB_or_wiki_for_item('Quarry', 'BuildCraft', 'Quarry')
log = []
rf.parse_recipe(log, 'Quarry', output_item, **q.scrape_recipes()[23])
'''

import craftDB.wikiparser as wp

root = wp.Log_Node('Yellow')
print(root.add_node('Hey There'))
root.add_node('Hello There')
grevnode = root.add_node('General Grevious')
grevnode.add_node('Robotic')
grevnode.add_node('Evil')

root2 = wp.Log_Node('Obi Wan Kenobi')
root2.add_node('Courageous')
root2.add_node('Witty')
root2.add_node('Senses a trap')

sub_node = root.connect_nodes(root2, 2)
print(sub_node)
print(root)

#print(root.render_string())

#print(root.render_html())

'''

import craftDB.wikiparser as wp
import craftDB.recipefinder as rf 
from craftDB.models import *

q = wp.PageParser('Mining Drill')

#recipe = q.scrape_recipes()[0]
output_item = Item.objects.all()[0]
parent = wp.Log_Node('Scraping Recipes for Mining Drill')
for recipe in q.scrape_recipes():
    test = rf.instantiate_recipe('Mining Drill', parent, output_item, **recipe)
    try:
        rf.parse_recipe(**test)
    except rf.ConstructRecipeException as err:
        parent.add_node(err.sub_error, 'max')


print(parent.render_string())


from craftDB.wikiparser import getIO_machining_recipe
parsethis = |Input=Redstone Ore (Minecraft)
|Output1=Redstone |OA1=8 |Output1-chance=100
|Output2=Redstone |Output2-chance=20
|Output3=Silicon (EnderIO) |Output3-chance=80
|Output4=Cobblestone |Output4-chance=15
|Energy=3000
getIO_machining_recipe(parsethis)
'''