from craftDB.wikiparser import getIO_machining_recipe
parsethis = '''|Input=Redstone Ore (Minecraft)
|Output1=Redstone |OA1=8 |Output1-chance=100
|Output2=Redstone |Output2-chance=20
|Output3=Silicon (EnderIO) |Output3-chance=80
|Output4=Cobblestone |Output4-chance=15
|Energy=3000'''
getIO_machining_recipe(parsethis, 'Redstone')