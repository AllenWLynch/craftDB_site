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

import craftDB.wikiparser as wp
root = wp.Log_Node('Yellow')
root.add_node('Hey There')
root.add_node('Hello There')
grevnode = root.add_node('General Grevious', 2)
grevnode.add_node('Robotic')
grevnode.add_node('Evil')

root2 = wp.Log_Node('Obi Wan Kenobi')
root2.add_node('Courageous')
root2.add_node('Witty')
root2.add_node('Senses a trap')

root.connect_nodes(root2, 1)

print(root.render_html())
'''

import craftDB.wikiparser as wp
import craftDB.recipefinder as rf 
q = wp.PageParser('Mining Drill')

for recipe in q.scrape_recipes:
    print(recipe)


