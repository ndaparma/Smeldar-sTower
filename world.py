from script import *
from character import *
#from combat import *
from Settings import *
from map import *
import random
import combat
import os
import sys
from pathlib import Path

affRes = ["YES","Y"] # affirmative responses
negRes = ["NO","N"] # negative responses
atkRes = ["A", "ATK","ATTACK","HIT","SMASH","SMASHING","CRUSH"] # attack responses
searchRes = ['EXAMINE', 'SEARCH', 'INSPECT', 'INVESTIGATE'] # search responses
backRes = ["BACK","B","LEAVE"] # back responses
openRes = ["OPEN","O","UNLOCK"] # open responses
forceRes = ["FORCE","FORCE OPEN","BREAK","BREAK OPEN","SMASH OPEN"] # force responses

song_term = ['RIBBIT', 'RIBBITING', 'CROAK', 'CROAKING', 'KERO', 'KEROKERO']

craftingitem_Terms = {
        'PLANT PARTS': ['PLANT PARTS', 'PLANT P.', 'PLANT', 'P PARTS', 'P P', 'PP', 'P'],
        'MONSTER PARTS': ['MONSTER PARTS', 'MONSTER P.', 'MONSTER', 'M PARTS', 'M P', 'MP', 'M'],
        'RARE MONSTER PARTS': ['RARE MONSTER PARTS', 'RARE MONSTER P.', 'RARE MONSTER', 'R PARTS', 'R P', 'RP', 'R'],
        'FAE DUST': ['FAE DUST', 'FAE D.', 'FAE', 'F D', 'FD', 'F'],
    }   


def camp_healing(p1, current_room, typingActive, SoundsOn):
    if rooms[current_room]['fire'] > 0:
        heal = random.randrange(p1.lvl, (p1.lvl*3)+1) + (p1.MaxHP // 2)
        p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
        rooms[current_room]['fire'] -= 1
        soundFile = str(SFX_Library['Camp'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(rooms[current_room]['fireTalk'], typingActive)
        print_slow(f'\n{p1.name} has rested and restored {heal}HP. {p1.name} now has {p1.HP}/{p1.MaxHP}HP.\n',typingActive)
        if rooms[current_room]['fire'] > 0:
            print_slow(f"{p1.name} may rest {rooms[current_room]['fire']} times before the tinder runs out.\n",typingActive)
        else:
            print_slow(f'The tinder has been used up and {p1.name} is unable to rest here.\n',typingActive)
    else:
        print_slow(f'The tinder has been used up and {p1.name} is unable to rest here.\n',typingActive)

def camp_rest(p1, current_room, typingActive, SoundsOn):
    camp_healing(p1, current_room, typingActive, SoundsOn)
    if rooms[current_room]['fire'] == 0:
        if rooms[current_room]['name'] == 'Camp Site':
            rooms['Camp Site']['intro'] = line102
            rooms['Camp Site']['EXPLORE'] = line104
            rooms['Camp Site']['map'] = camp_map2
        elif rooms[current_room]['name'] == 'Fae Woods - Camp':
            rooms['Fae Woods - Camp']['intro'] = line4002
            rooms['Fae Woods - Camp']['EXPLORE'] = line4004
            rooms['Fae Woods - Camp']['map'] = faecamp_map2
        elif rooms[current_room]['name'] == 'Misty Woods - Camp':
            rooms['Misty Woods - Camp']['EXPLORE'] = line5010
            rooms['Misty Woods - Camp']['map'] = mistcamp_map2
        elif rooms[current_room]['name'] == 'Smeldars Tower - Hidden Room':
            rooms['Smeldars Tower - Hidden Room']['EXPLORE'] = line5225b
            rooms['Smeldars Tower - Hidden Room']['map'] = smeldarstowerS_map2


def kindling_fire(p1, current_room, typingActive, SoundsOn):
    if p1.KDL >= 1:
        p1.KDL -= 1
        rooms[current_room]['fire'] = rooms[current_room]['Maxfire']
        soundFile = str(SFX_Library['Kindle'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"{p1.name} uses 1 KINDLING to rekindle the fire. The fire can now be used {rooms[current_room]['fire']} more times.\n", typingActive)
        if rooms[current_room]['name'] == 'Camp Site':
            rooms['Camp Site']['intro'] = line101
            rooms['Camp Site']['EXPLORE'] = line103
            rooms['Camp Site']['map'] = camp_map1
        elif rooms[current_room]['name'] == 'Fae Woods - Camp':
            rooms['Fae Woods - Camp']['intro'] = line4001
            rooms['Fae Woods - Camp']['EXPLORE'] = line4003
            rooms['Fae Woods - Camp']['map'] = faecamp_map1
        elif rooms[current_room]['name'] == 'Misty Woods - Camp':
            rooms['Misty Woods - Camp']['EXPLORE'] = line5009
            rooms['Misty Woods - Camp']['map'] = mistcamp_map1
        elif rooms[current_room]['name'] == 'Smeldars Tower - Hidden Room':
            rooms['Smeldars Tower - Hidden Room']['EXPLORE'] = line5225
            rooms['Smeldars Tower - Hidden Room']['map'] = smeldarstowerS_map1
    else:
        print_slow(f"{p1.name} does not have enough KINDLING to rekindle the fire.\n", typingActive)


def shrine_pray(p1, typingActive, SoundsOn):
    print_slow(f"{p1.name} approaches the altar and kneels to pray.\n", typingActive)
    print_slow("Do you wish to donate? (YES or NO)\n", typingActive)

    while True:
        playerInput = (input().upper()).strip()
        print("\n")
        if playerInput in affRes:
            if p1.GP >= 35:
                p1.MP = p1.MaxMP
                p1.GP -= 35
                soundFile = str(SFX_Library['Pray'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"{p1.name} drops 35 GP into an ornate donation box and kneels between the lanterns at the altar. The magic of the altar fills {p1.name} with renewed energy. {p1.name}'s MP is fully restored.\n", typingActive)
                break
            else:
                soundFile = str(SFX_Library['NoGP'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"{p1.name} is too poor to donate to charity.\n", typingActive)
                return
        elif playerInput in negRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f"{p1.name} decides not to donate at this time.\n", typingActive)
            return
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow("Invalid input. Please respond with YES or NO.\n", typingActive)
def merchant_death():
    enemy_spawn5.remove(p28)
    enemy_spawn9.remove(p28)
    enemy_spawn17.remove(p28)
    enemy_spawn22.remove(p28)


def shop_menu(p1, rooms, current_room, typingActive, SoundsOn):
    global shop_open
    global traveling_shop
    shop_open = 1
    traveling_shop = 0

    while shop_open == 1:
        if current_room == 'Capital City - Shop':
            print_slow(""""Well what will it be?"\n """, typingActive)
        elif current_room == 'Deep Woods - Forest Hut':
            print_slow(""""Many helpful things for other friend!"\n """, typingActive)
        elif current_room == 'Harbor Town - Shop':
            print_slow(""""Anything catch yer eye?"\n """, typingActive)
        elif current_room == "Dwarf's Workshop":
            print_slow(""""The finest weapons and armor in the realm!"\n """, typingActive)
        for k in rooms[current_room]['items']:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
        print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
        print_slow('\nType your selection or input BACK to leave the shopping window.\n', typingActive)
        sales_mechanic(p1, rooms, current_room, typingActive, SoundsOn)


def key_itemBought(p1, playerInput, typingActive, SoundsOn):
    try:
        print_slow(f"\n{p1.name} purchased a {playerInput}! " + key_items[playerInput]['purchased'] + f"\n{p1.GP}GP remaining.\n", typingActive)
        if playerInput == 'EXTRA POUCH':
            p1.MaxPOTS += 5
            p1.MaxANT += 5
            p1.MaxETR += 5
            p1.MaxSAL += 5
            p1.MaxSMB += 5
        if playerInput == 'DRAGON SCALE':
            p1.DragonP += 1
    except KeyError:
        print_slow(f"\n{p1.name} purchased a {playerInput}!\n{p1.GP}GP remaining.\n", typingActive)
    

def sales_mechanic(p1, rooms, current_room, typingActive, SoundsOn):
    global shop_open
    global traveling_shop
    global merchant_alive

    

    def consumable_display():
        if playerInput == 'POTION':
            print_slow(f"""{p1.name} has {p1.POTS}/{p1.MaxPOTS} POTIONS.\n""", typingActive)
        if playerInput == 'ANTIDOTE':
            print_slow(f"""{p1.name} has {p1.ANT}/{p1.MaxANT} ANTIDOTES.\n""", typingActive)
        if playerInput == 'ETHER':
            print_slow(f"""{p1.name} has {p1.ETR}/{p1.MaxETR} ETHERS.\n""", typingActive)
        if playerInput == 'SALINE':
            print_slow(f"""{p1.name} has {p1.SAL}/{p1.MaxSAL} SALINE.\n""", typingActive)
        if playerInput == 'SMOKE BOMB':
            print_slow(f"""{p1.name} has {p1.SMB}/{p1.MaxSMB} SMOKE BOMBS.\n""", typingActive)
        if playerInput == 'WARP CRYSTAL':
            print_slow(f"""{p1.name} has {p1.WCR}/{p1.MaxWCR} WARP CRYSTALS.\n""", typingActive)
        if playerInput == 'KINDLING':
            print_slow(f"""{p1.name} has {p1.KDL}/{p1.MaxKDL} KINDLING.\n""", typingActive)

    def consumable_normalizer():
        nonlocal playerInput
        for key, value in consumableTerms.items():
            if playerInput in value:
                playerInput = key
                break

    consumableTerms = {
        'POTION': ['POTION', 'POTIONS', 'POT', 'POTS'],
        'ANTIDOTE': ['ANTIDOTE', 'ANTIDOTES', 'ANT', 'ANTS'],
        'ETHER': ['ETHER', 'ETHERS', 'ETH', 'ETHS'],
        'SALINE': ['SALINE', 'SALINES', 'SAL', 'SALS', 'EYE DROP', 'EYE DROPS'],
        'SMOKE BOMB': ['SMOKE BOMB', 'SMOKE BOMBS', 'SMOKE', 'SMB', 'SB'],
        'WARP CRYSTAL': ['WARP CRYSTAL', 'WARP CRYSTALS', 'WARP', 'WCR', 'WC'],
        'KINDLING': ['KINDLE', 'KINDLING', 'KDLL', 'KDL']
    }

    sale = 0
    
    playerInput = (input().upper()).strip()
    print_slow("\n", typingActive)

    if (playerInput in atkRes) and traveling_shop == 1:
      foe = p28
      print_slow(f"{p1.name} assaults the Traveling Merchant! The Merchant narrowly avoids the attack before drawing his own weapon!\n",typingActive)
      combat.standard_battle(p1, foe, typingActive, SoundsOn)
      if p1.HP <= 0:
        return
      print_slow(f"{p1.name} slays the Merchant in cold blood. The gnome's body lays motionless on the ground. {p1.name} rummages through the Merchants wares for anything valuable that is still intact. {p1.name} finds some POTIONS, ANTIDOTES, and ETHERS. {p1.name} takes whatever they can carry; it's not like the Merchant will be needing them anymore.\n", typingActive)
      p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
      p1.ANT = min(p1.ANT + 2, p1.MaxANT)
      p1.ETR = min(p1.ETR + 2, p1.MaxETR)
      p1.SMB = min(p1.SMB + 2, p1.MaxSMB)
      p1.WCR = min(p1.WCR + 1, p1.MaxWCR)
      merchant_death()
      p1.stat_check(typingActive)
      shop_open = 0
      traveling_shop = 0
      merchant_alive = 0
      return
    
    consumable_normalizer()
    if playerInput in shop_items or playerInput in shop_keyitems:

        if p1.GP < key_items[playerInput]['price']:
            print_slow(f"""{p1.name} does not have enough GP.\n""", typingActive)   

        if p1.GP >= key_items[playerInput]['price']:

            if playerInput in shop_items:
                if playerInput in consumableTerms['POTION']:
                    if p1.POTS < p1.MaxPOTS:
                        p1.POTS += 1
                        sale = 2
                    else:
                        sale = 1
                if playerInput in consumableTerms['ANTIDOTE']:
                    if p1.ANT < p1.MaxANT:
                        p1.ANT += 1
                        sale = 2
                    else:
                        sale = 1
                if playerInput in consumableTerms['ETHER']:
                    if p1.ETR < p1.MaxETR:
                        p1.ETR += 1
                        sale = 2
                    else:
                        sale = 1
                if playerInput in consumableTerms['SMOKE BOMB']:
                    if p1.SMB < p1.MaxSMB:
                        p1.SMB += 1
                        sale = 2
                    else:
                        sale = 1
                if playerInput in consumableTerms['WARP CRYSTAL']:
                    if p1.WCR < p1.MaxWCR:
                        p1.WCR += 1
                        sale = 2
                    else:
                        sale = 1              
                if playerInput in consumableTerms['KINDLING']:
                    if p1.KDL < p1.MaxKDL:
                        p1.KDL += 1
                        sale = 2
                    else:
                        sale = 1                
            if playerInput in shop_keyitems:
                if traveling_shop == 1:
                    if playerInput in travelingMerchant_items:
                        sale = 5
                    else:
                        print_slow("""That item is unavailable!\n""", typingActive)
                        sale = 3
                else:
                    if playerInput in rooms[current_room]['items']:
                        sale = 5
                    else:
                        print_slow(f""""That item is unavailable!"\n""", typingActive)
                        sale = 3
                
                  

            if sale == 5: #traveling merchant checks
                if playerInput in p1.inventory:
                    print_slow(f"""{p1.name} already has one in their inventory and cannot carry another!\n""", typingActive)
                    sale = 3
                else:
                    if 'classes' in key_items[playerInput]:
                        if p1.job in key_items[playerInput]['classes']:
                            sale = 4
                        else:
                            print_slow( f"""{p1.name} is unable to purchase this. (Cannot be used by {p1.job}'s.)\n""", typingActive)
                            sale = 3               
                    else:
                        sale = 4
            if sale == 4: #sale completed
              if traveling_shop == 1:
                      p1.GP -= key_items[playerInput]['price']
                      p1.inventory.append(playerInput)
                      travelingMerchant_items.remove(playerInput)
                      key_itemBought(p1, playerInput, typingActive, SoundsOn)
              else:
                  if playerInput == 'DRAGON SCALE' and 'CRAFTING POUCH' not in p1.inventory:
                    print_slow(f""""You'll need a CRAFTING POUCH in order to carry this item!"\n""", typingActive)
                  else:
                      p1.inventory.append(playerInput)
                      rooms[current_room]['items'].remove(playerInput)
                      p1.GP -= key_items[playerInput]['price']
                      soundFile = str(SFX_Library['Buy'])
                      play_sound_effect(soundFile, SoundsOn)
                      key_itemBought(p1, playerInput, typingActive, SoundsOn)
            if sale == 3: #item unavailable
                soundFile = str(SFX_Library['NoItem'])
                play_sound_effect(soundFile, SoundsOn)
            if sale == 2: #consumable purchased
                p1.GP -= key_items[playerInput]['price']
                soundFile = str(SFX_Library['Buy'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"{p1.name} purchases a {playerInput}. {p1.name} has {p1.GP} GP.\n", typingActive)
                consumable_display()
            if sale == 1: #inventory full
                soundFile = str(SFX_Library['NoItem'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"""{p1.name} is unable to carry any more {playerInput}S. {p1.name}'s inventory is full!""", typingActive)

    elif playerInput in backRes:
        shop_open = 0
        traveling_shop = 0
        print_slow('\n"Come back soon!"\n', typingActive)
    else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('\nInvalid input. Try again.\n', typingActive)


def selling_to_Shopkeeper(p1, rooms, current_room, typingActive, SoundsOn):

    while True:
        salesList = [i for i in p1.inventory if i in sellable_items]

        if salesList != []:
            if rooms[current_room]['name'] == "Dwarf's Workshop":
                print_slow(""""Ye lokin' to sel sumtn', mukker? Aye! Wat d'ye 'av?"\n """, typingActive)
            elif rooms[current_room]['name'] == 'Deep Woods - Forest Hut':
                print_slow(""""Oh, other friend have good thing for me? I can takes a look and maybe give you shiny?"\n """, typingActive)
            else:
                print_slow('\nWhat would you like to sell? Let me see what you have.\n', typingActive)
            print_slow('Type item to sell or BACK to leave the selling window.\n', typingActive)
            print_slow("Items available to sell:\n", typingActive)
            for item in salesList:
                print_slow(f'{key_items[item]["name"]}: [{round(key_items[item]["price"]/2)} GP]\n', typingActive)
            while True:
                playerInput = (input().upper()).strip()
                print("\n")
                if playerInput in salesList:
                    p1.inventory.remove(playerInput)
                    p1.GP += round(key_items[playerInput]['price'] / 2)
                    soundFile = str(SFX_Library['Sell'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(f"{p1.name} sells the {playerInput} for {round(key_items[playerInput]['price']/2)} GP. {p1.name} now has {p1.GP} GP.\n", typingActive)
                    break
                elif playerInput in backRes:
                    if rooms[current_room]['name'] == "Dwarf's Workshop":
                        print_slow(""""Come back wi' more t' sell soon, mukker!'\n """, typingActive)
                    elif rooms[current_room]['name'] == 'Deep Woods - Forest Hut':
                        print_slow('\nCome back with more shinies to share!\n', typingActive)    
                    else:
                        print_slow('\nCome back with more items to sell soon!\n', typingActive)    
                    return
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(f"\n{p1.name} has nothing to sell.\n", typingActive)
            return


def alchemist_buy(p1, rooms, current_room, typingActive, SoundsOn):
    def boughtSound(SoundsOn):
        soundFile = str(SFX_Library['Buy'])
        play_sound_effect(soundFile, SoundsOn)
    def notEnoughGP(SoundsOn):
        soundFile = str(SFX_Library['NoGP'])
        play_sound_effect(soundFile, SoundsOn)

    while True:
        print_slow('"What are you looking to buy?"', typingActive)
        print_slow(f'PLANT PARTS [75GP]\nMONSTER PARTS [125GP]\nRARE MONSTER PARTS [250GP]\nFAE DUST [150]\nType the item you wish to purchase or BACK to exit the menu.\n', typingActive)
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in craftingitem_Terms['PLANT PARTS']:
            if p1.GP >= 75:
                p1.GP -= 75
                p1.PlantP += 1
                boughtSound(SoundsOn)
                print_slow(f"{p1.name} has purchased PLANT PARTS from the Alchemist! {p1.name} now has {p1.PlantP} PLANT PARTS.\n", typingActive)
            else:
                notEnoughGP(SoundsOn)
                print_slow(f"{p1.name} does not have enough GP to purchase PLANT PARTS. {p1.name} has {p1.GP}/75 GP required.\n", typingActive)

        elif playerInput in craftingitem_Terms['MONSTER PARTS']:
            if p1.GP >= 125:
                p1.GP -= 125
                p1.MonP += 1
                boughtSound(SoundsOn)
                print_slow(f"{p1.name} has purchased MONSTER PARTS from the Alchemist! {p1.name} now has {p1.MonP} MONSTER PARTS.\n", typingActive)
            else:
                notEnoughGP(SoundsOn)
                print_slow(f"{p1.name} does not have enough GP to purchase MONSTER PARTS. {p1.name} has {p1.GP}/125 GP required.\n", typingActive)

        elif playerInput in craftingitem_Terms['RARE MONSTER PARTS']:
            if p1.GP >= 250:    
                p1.GP -= 250
                p1.RareP += 1
                boughtSound(SoundsOn)
                print_slow(f"{p1.name} has purchased RARE MONSTER PARTS from the Alchemist! {p1.name} now has {p1.RareP} RARE MONSTER PARTS.\n", typingActive)
            else:
                notEnoughGP(SoundsOn)
                print_slow(f"{p1.name} does not have enough GP to purchase RARE MONSTER PARTS. {p1.name} has {p1.GP}/250 GP required.\n", typingActive)

        elif playerInput in craftingitem_Terms['FAE DUST']:
            if p1.GP >= 150:    
                p1.GP -= 150
                p1.FaeDust += 1
                boughtSound(SoundsOn)
                print_slow(f"{p1.name} has purchased FAE DUST from the Alchemist! {p1.name} now has {p1.FaeDust} FAE DUST.\n", typingActive)
            else:
                notEnoughGP(SoundsOn)
                print_slow(f"{p1.name} does not have enough GP to purchase FAE DUST. {p1.name} has {p1.GP}/150 GP required.\n", typingActive)

        elif playerInput in backRes:
            print_slow(""""Come back with more gold soon!"\n """, typingActive)
            break
            
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Please try again.\n',typingActive)


def alchemist_sell(p1, rooms, current_room, typingActive, SoundsOn):
    def soldSound(SoundsOn):
        soundFile = str(SFX_Library['Sell'])
        play_sound_effect(soundFile, SoundsOn)
    
    def noItemSound(SoundsOn):
        soundFile = str(SFX_Library['NoItem'])
        play_sound_effect(soundFile, SoundsOn)

    while True:

        print_slow('"What are you looking to sell?"', typingActive)
        print_slow(f'PLANT PARTS [25GP]\nMONSTER PARTS [50GP]\nRARE MONSTER PARTS [100GP]\nFAE DUST [75GP]\nType the item you wish to sell or BACK to exit the menu.\n', typingActive)
        playerInput = input().upper().strip()
        print('\n')

        if playerInput in craftingitem_Terms['PLANT PARTS']:
            if p1.PlantP >= 1 :
                p1.GP += 25
                p1.PlantP -= 1
                soldSound(SoundsOn)
                print_slow(f"{p1.name} has sold PLANT PARTS to the Alchemist! {p1.name} now has {p1.GP} GP in their wallet.\n", typingActive)
            else:
                noItemSound(SoundsOn)
                print_slow(f"{p1.name} does not have any PLANT PARTS to sell.\n", typingActive)

        elif playerInput in craftingitem_Terms['MONSTER PARTS']:
            if p1.MonP >= 1 :
                p1.GP += 50
                p1.MonP -= 1
                soldSound(SoundsOn)
                print_slow(f"{p1.name} has sold MONSTER PARTS to the Alchemist! {p1.name} now has {p1.GP} GP in their wallet.\n", typingActive)
            else:
                noItemSound(SoundsOn)
                print_slow(f"{p1.name} does not have any MONSTER PARTS to sell.\n", typingActive)

        elif playerInput in craftingitem_Terms['RARE MONSTER PARTS']:
            if p1.RareP >= 1 :
                p1.GP += 100
                p1.RareP -= 1
                soldSound(SoundsOn)
                print_slow(f"{p1.name} has sold RARE MONSTER PARTS to the Alchemist! {p1.name} now has {p1.GP} GP in their wallet.\n", typingActive)
            else:
                noItemSound(SoundsOn)
                print_slow(f"{p1.name} does not have any RARE MONSTER PARTS to sell.\n", typingActive)

        elif playerInput in craftingitem_Terms['FAE DUST']:
            if p1.FaeDust >= 1 :
                p1.GP += 75
                p1.FaeDust -= 1
                print_slow(f"{p1.name} has sold FAE DUST to the Alchemist! {p1.name} now has {p1.GP} GP in their wallet.\n", typingActive)
            else:
                noItemSound(SoundsOn)
                print_slow(f"{p1.name} does not have any FAE DUST to sell.\n", typingActive)

        elif playerInput in backRes:
            print_slow(""""Come back with more items to sell soon!"\n """, typingActive)
            break

        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Please try again.\n',typingActive)


def dwarf_trade(p1, rooms, current_room, typingActive, SoundsOn):
  global line4506
  while True:
    if rooms["Dwarf's Workshop"]['event2'] == 1:
      print_slow(""""Ah appreciate th' offer bit a've git plenty tae wirk wi' fur th' time bein', 'n' nothn' else tae trade wi' ye.  "\n """, typingActive)
      break
    elif rooms["Dwarf's Workshop"]['event2'] == 0:
      print_slow(""""If ye trade me 5 dragon scales ah wull gift ye yin o' mah greatest weapons. Whit dae ye say?"\n """, typingActive)
      playerInput = (input().upper()).strip()
      print_slow("\n", typingActive)
      if playerInput in affRes:
        if p1.DragonP >= 5:
          p1.DragonP -= 5
          if p1.job == "WARRIOR":
            p1.inventory.append('AETHON')
            ultimateweapon = 'AETHON'
          if p1.job in ["WIZARD", "WITCH"]:
            p1.inventory.append('FULGUR')
            ultimateweapon = 'FULGUR'
          if p1.job == "THIEF":   
            p1.inventory.append('MIDAS')
            ultimateweapon = 'MIDAS'
          if p1.job == "SUMMONER":
            p1.inventory.append('DELPHI')
            ultimateweapon = 'DELPHI'
          
          if p1.job == "GOD":
            p1.inventory.append('AETHON')
            p1.inventory.append('FULGUR')
            p1.inventory.append('MIDAS')
            p1.inventory.append('DELPHI')
            ultimateweapon = 'ULTIMATE WEAPONS'
          rooms["Dwarf's Workshop"]['event2'] = 1
          line4506 = line4506b
          print_slow(""""Ye'v made a wise choice mukker. As promised, yin o' mah greatest wirks. Tak' stoatin care wi' it, wull ye?"\n """, typingActive)
          time.sleep(0.5)
          soundFile = str(SFX_Library['GotLegendary'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{p1.name} receives the {ultimateweapon} from the DWARF! This weapon is of legendary quality, crafted from the greatest smith in all the realm.\n", typingActive)
          break
        if p1.DragonP < 5:
          soundFile = str(SFX_Library['NoItem'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(""""Dinnae wass mah time! Come back whin ye actually hae th' materials 'am needin'!"\n """, typingActive)
          break
      elif playerInput in negRes:
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(""""Bah! Then be gaen wi' ye!"\n """, typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('\nInvalid input. Input YES or NO.\n', typingActive)


def traveling_merchant(p1, foe, current_room, typingActive, SoundsOn):
    global shop_open
    global traveling_shop
    global merchant_alive
    shop_open = 1
    traveling_shop = 1
    merchant_alive = 1

    print_slow(line305, typingActive)
    while shop_open == 1:
        print_slow(""""Take a look!"\n""", typingActive)
        for k in travelingMerchant_items:
            item = k
            print_slow(f'{key_items[item]["name"]}: [{key_items[item]["price"]} GP]\n', typingActive)      
        print_slow(f"\n{p1.name}'s Wallet:[{p1.GP} GP]\n", typingActive)
        print_slow('\nType your selection or input BACK to leave the shopping window.\n', typingActive)
        sales_mechanic(p1, rooms, current_room, typingActive, SoundsOn)

        if shop_open == 0:
            if merchant_alive == 1:
                print_slow('You bid farewell to the merchant and continue on your way.\n', typingActive)
            break


def city_inn(p1, current_room, typingActive, SoundsOn): 
    inn_room = 40

    while True:
        print_slow(f'"A room for the night will be 40 GP. Would you like to stay? (YES or NO)"\n', typingActive)
        playerInput = (input().upper()).strip()
        print_slow("\n", typingActive)
        if playerInput in affRes:
            if p1.GP >= inn_room:
                p1.GP -= 40
                p1.HP = p1.MaxHP
                p1.POISON = 0
                p1.BLIND = 0
                soundFile = str(SFX_Library['Inn'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'The innkeeper shows {p1.name} to their room where they get a good night\'s rest.\n', typingActive)
                time.sleep(1.3)
                print_slow(f'\n{p1.name} took a well earned rest and restored HP. {p1.name} has {p1.HP}/{p1.MaxHP}HP, and {p1.GP}GP.\n',typingActive)
            else:
                soundFile = SFX_Library['NoGP']
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'{p1.name} does not have enough GP in their wallet. {p1.name} has {p1.GP}GP.\n',typingActive)
            break
        elif playerInput in negRes:
            soundFile = SFX_Library['Back']
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nMaybe next time then.\n', typingActive)
            break
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid input. Please type YES or NO.\n', typingActive)
            

def smithing_upgrade(p1, current_room, typingActive, SoundsOn):
    while True:
        s = set(mainHand_equipment)
        weapons = [x for x in p1.inventory if x in s]
        z = set(armor_equipment)
        armor = [x for x in p1.inventory if x in z]
        print_slow(f"""Input the weapon or armor piece you would like to UPGRADE, or type BACK to exit menu.\n""", typingActive)
        print_slow(f"""Weapons: {weapons}\n""", typingActive)
        print_slow(f"""Armor: {armor}\n""", typingActive)
        playerInput = (input().upper()).strip()
        print_slow("\n", typingActive)
        if playerInput in weapons:
            smithing_check(p1, playerInput, current_room, typingActive, SoundsOn)
        elif playerInput in armor:
            smithing_check(p1, playerInput, current_room, typingActive, SoundsOn)
        elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Aye, dun wass mae tim.\n', typingActive)
            break
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid command. Please select a weapon or armor from the lists, or type BACK to exit menu.\n', typingActive)


def smithing_check(p1, playerInput, current_room, typingActive, SoundsOn):
    if key_items[playerInput]['quality'] == 'POOR':
        if key_items[playerInput]['gear_level'] < 3:
            smithing_increase(p1, playerInput, current_room, typingActive, SoundsOn)
        else:
            print_slow(""""Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n" """, typingActive)
    elif key_items[playerInput]['quality'] == 'GOOD':
        if key_items[playerInput]['gear_level'] < 5:
            smithing_increase(p1, playerInput, current_room, typingActive, SoundsOn)
        else:
            print_slow(
                """"Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n """, typingActive,)
    elif key_items[playerInput]['quality'] == 'LEGENDARY':
        if current_room == "Smith's Workshop":
            print_slow(""""Wat an incredible piece... A'm feart a'd dae it na justice. If ye kin tak' it tae mah auld master oot WAST he kin be able tae hulp. He's a streenge jimmy, bit na finer smith ye'll fin'."\n """, typingActive)
        elif current_room == "Dwarf's Workshop":
            if key_items[playerInput]['gear_level'] < 7:
                smithing_increase(p1, playerInput, current_room, typingActive, SoundsOn)
            else:
                print_slow(""""Aye, it looks lik' a've dane everything ah kin fur ye 'n' yer equipment.\n" """, typingActive)


def smithing_increase(p1, playerInput, current_room, typingActive, SoundsOn):
    while True:
        print_slow(f""""So you'd like to upgrade your {playerInput} for {key_items[playerInput]['upgrade']} GP?" (YES or NO.)\n""", typingActive)
        print_slow(f"""{p1.name}'s Wallet': {p1.GP} GP\n""", typingActive)
        playerInput2 = (input().upper()).strip()
        print_slow("\n", typingActive)
        if playerInput2 in affRes and p1.GP >= key_items[playerInput]['upgrade']:
            p1.GP -= key_items[playerInput]['upgrade']
            key_items[playerInput]['upgrade'] *= 2
            key_items[playerInput]['gear_level'] += 1
            if playerInput in mainHand_equipment:
                if playerInput == p1.mainHand or playerInput == p1.offHand:
                    p1.ATK += 1
                key_items[playerInput]['ATK'] += 1
            elif playerInput in armor_equipment:
                if playerInput == p1.head or playerInput == p1.chest or playerInput == p1.legs or playerInput == p1.offHand:
                    p1.GDEF += .5
                key_items[playerInput]['DEF'] += .5
            soundFile = str(SFX_Library['Smith'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f"The Smith takes back {p1.name}'s equipment and begins making improvements. After a while he returns with your improved gear.\n",typingActive, SoundsOn)
            break
        elif playerInput2 in affRes and p1.GP < key_items[playerInput]['upgrade']:
            soundFile = str(SFX_Library['NoGP'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f""""Why don't you come back when you have enough GP for that..."\n\n{p1.name} only has {p1.GP} GP in their wallet.\n""",typingActive, SoundsOn)
            break
        elif playerInput2 in negRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Aye, dun wass mae tim.\n', typingActive)
            break
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid command. Please select YES or NO.\n', typingActive)


def witch_crafting(p1, typingActive, SoundsOn):
    
    tonic_Terms = {
        'HEALTH TONIC': ['HEALTH TONIC', 'HEALTH T.', 'HEALTH', 'H Tonic', 'H T', 'HT', 'HTONIC', 'H'],
        'MAGIC TONIC': ['MAGIC TONIC', 'MAGIC T.', 'MAGIC', 'M Tonic', 'M T', 'MT', 'MTONIC', 'M'],
        'SPEED TONIC': ['SPEED TONIC', 'SPEED T.', 'SPEED', 'S Tonic', 'S T', 'ST', 'STONIC', 'S'],
        'STRENGTH TONIC': ['STRENGTH TONIC', 'STR T.', 'STRENGTH', 'S Tonic', 'S T', 'ST', 'STONIC', 'S'],}
    
    def brew_SFX(SoundsOn):
        soundFile = str(SFX_Library['Brew'])
        play_sound_effect(soundFile, SoundsOn)

    def no_materials_SFX(SoundsOn):
        soundFile = str(SFX_Library['NoItem'])
        play_sound_effect(soundFile, SoundsOn)

    while True:
        print_slow(line2406, typingActive)

        if rooms["Witch's Cabin"]['event'] == 1:
            print_slow(f"""
TONIC:    REQUIRES:    INV:
HEALTH T. 0 PLANT P.   {p1.PlantP} PLANT P.
MAGIC T.  0 FAE D.    {p1.FaeP} FAE D.
SPEED T.  0 MON P.   {p1.MonP} MON P.
STR T.    0 RARE P.  {p1.RareP} RARE P.
""", typingActive)  
            
        else:
            print_slow(f"""
TONIC:    REQUIRES:    INV:
HEALTH T. 5 PLANT P.   {p1.PlantP} PLANT P.
MAGIC T.  5 FAE D.    {p1.FaeP} FAE D.
SPEED T.  5 MON P.   {p1.MonP} MON P.
STR T.    5 RARE P.  {p1.RareP} RARE P.
""", typingActive)  
            
        print_slow('Type the item you would like to craft or BACK to exit.\n', typingActive)
        playerInput = (input().upper()).strip()
        print_slow('\n', typingActive)

        if playerInput in tonic_Terms['HEALTH TONIC']:
            if rooms["Witch's Cabin"]['event'] == 1:
                p1.MaxHP += 100
                p1.HP += 100
                brew_SFX(SoundsOn)
                print_slow(""""Hehehe! One HEALTH TONIC coming right up.\n" """, typingActive)
                print_slow(f"{p1.name}'s HP has permanently increased! {p1.name}'s is now {p1.HP}/{p1.MaxHP}\n", typingActive)
                rooms["Witch's Cabin"]['event'] = 0
            else:
                if p1.PlantP >= 5:
                    p1.PlantP -= 5
                    p1.MaxHP += 100
                    p1.HP += 100
                    brew_SFX(SoundsOn)
                    print_slow(""""Hehehe! One HEALTH TONIC coming right up.\n" """, typingActive)
                    print_slow(f"{p1.name}'s HP has permanently increased! {p1.name}'s is now {p1.HP}/{p1.MaxHP}\n", typingActive)
                else:
                    no_materials_SFX(SoundsOn)
                    print_slow(f'{p1.name} does not have enough PLANT PARTS. {p1.name} only has {p1.PlantP}/5 PLANT PARTS required\n', typingActive)

        elif playerInput in tonic_Terms['MAGIC TONIC']:
            if rooms["Witch's Cabin"]['event'] == 1:
                p1.MaxMP += 5
                p1.MP += 5
                brew_SFX(SoundsOn)
                print_slow(""""Hehehe! One MAGIC TONIC coming right up.\n" """, typingActive)
                print_slow(f"{p1.name}'s MP has permanently increased! {p1.name}'s is now {p1.MP}/{p1.MaxMP}\n", typingActive)
                rooms["Witch's Cabin"]['event'] = 0
            else:
                if p1.FaeP >= 5:
                    p1.FaeP -= 5
                    p1.MaxMP += 5
                    p1.MP += 5
                    brew_SFX(SoundsOn)
                    print_slow(""""Hehehe! One MAGIC TONIC coming right up.\n" """, typingActive)
                    print_slow(f"{p1.name}'s MP has permanently increased! {p1.name}'s is now {p1.MP}/{p1.MaxMP}\n", typingActive)
                else:
                    no_materials_SFX(SoundsOn)
                    print_slow(f'{p1.name} does not have enough FAE DUST. {p1.name} only has {p1.FaeP}/5 FAE DUST required\n', typingActive)

        elif playerInput in tonic_Terms['SPEED TONIC']:
            if rooms["Witch's Cabin"]['event'] == 1:
                p1.SPD += 3
                brew_SFX(SoundsOn)
                print_slow(""""Hehehe! One SPEED TONIC coming right up.\n" """, typingActive)
                print_slow(f"{p1.name}'s SPEED has permanently increased! {p1.name}'s is now {p1.SPD}\n", typingActive)
                rooms["Witch's Cabin"]['event'] = 0
            else:
                if p1.MonP >= 5:
                    p1.MonP -= 5
                    p1.SPD += 3
                    brew_SFX(SoundsOn)
                    print_slow(""""Hehehe! One SPEED TONIC coming right up.\n" """, typingActive)
                    print_slow(f"{p1.name}'s SPEED has permanently increased! {p1.name}'s is now {p1.SPD}\n", typingActive)
                else:
                    no_materials_SFX(SoundsOn)
                    print_slow(f'{p1.name} does not have enough MONSTER PARTS. {p1.name} only has {p1.MonP}/5 MONSTER PARTS required\n', typingActive)

        elif playerInput in tonic_Terms['STRENGTH TONIC']:
            if rooms["Witch's Cabin"]['event'] == 1:
                p1.ATK += 2
                brew_SFX(SoundsOn)
                print_slow(""""Hehehe! One STRENGTH TONIC coming right up.\n" """, typingActive)
                print_slow(f"{p1.name}'s ATTACK has permanently increased! {p1.name}'s is now {p1.ATK}\n", typingActive)
                rooms["Witch's Cabin"]['event'] = 0
            else:
                if p1.RareP >= 5:
                    p1.RareP -= 5
                    p1.ATK += 2
                    brew_SFX(SoundsOn)
                    print_slow(""""Hehehe! One STRENGTH TONIC coming right up.\n" """, typingActive)
                    print_slow(f"{p1.name}'s ATTACK has permanently increased! {p1.name}'s is now {p1.ATK}\n", typingActive)
                else:
                    no_materials_SFX(SoundsOn)
                    print_slow(f'{p1.name} does not have enough RARE PARTS. {p1.name} only has {p1.RareP}/5 RARE PARTS required\n', typingActive)        
        elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(""""Come back anytime ye need more tonics! Hehehe!"\n """, typingActive)
            break
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Please try again.\n', typingActive)


def cliff_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Cliff Side']['chest'] == "CLOSED" and ('AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory):
            print_slow(line604, typingActive)
            break
        elif rooms['Cliff Side']['chest'] == "CLOSED" and ('AXE' in p1.inventory or 'SHARP AXE' in p1.inventory):
            print_slow(line605, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("\n", typingActive)
            if playerInput == "CUT":
                soundFile = str(SFX_Library['Chop'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line605b, typingActive)
                rooms['Cliff Side']['chest'] = "OPEN"
                p1.inventory.append('PENDANT')
                rooms['Cliff Side']['EXPLORE'] = line603
                rooms['Cliff Side']['map'] = cliff_map2
                break

            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line605c, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line605d, typingActive)
            break


def hill_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Rocky Hill']['SOUTH'] == 'LOCKED':
            if 'AXE' or 'SHARP AXE' not in p1.inventory:
                print_slow(line805, typingActive)
                break
            elif 'AXE' or 'SHARP AXE' in p1.inventory:
                print_slow(line805b, typingActive)
                playerInput = (input().upper()).strip()
                print_slow("\n", typingActive)
                if playerInput == 'CUT':
                    soundFile = str(SFX_Library['Chop'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line806, typingActive)
                    rooms['Rocky Hill']['SOUTH'] = 'Berry Patch'
                    rooms['Rocky Hill']['EXPLORE'] = line804
                    rooms['Rocky Hill']['map'] = hill_map2
                    break
                elif playerInput in backRes:
                    print_slow(line806b, typingActive)
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line811, typingActive)
            break


def waterfall_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Waterfall Pool']['chest'] == 'CLOSED':
            print_slow(line1302b, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("\n", typingActive)
            if playerInput == "TAKE":
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line1303, typingActive)
                p1.inventory.append('SALMON')
                rooms['Waterfall Pool']['chest'] = 'OPEN'
                break
            elif playerInput == "SAVE":
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line1304, typingActive)
                rooms['Waterfall Pool']['chest'] = 'OPEN'
                rooms['Waterfall Pool']['event'] = 1
                break
            elif playerInput == "LEAVE":
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line1305, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        elif rooms['Waterfall Pool']['chest'] == 'OPEN':
            if rooms['Waterfall Pool']['event'] == 1:
                print_slow(line1307, typingActive)
                p1.GP += 100
                rooms['Waterfall Pool']['event'] = 2
                print_slow(f'\n{p1.name} has {p1.GP}GP.\n', typingActive)
                break
            else:
                print_slow(line1308, typingActive)
                break


def waterfallcave2_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Waterfall Cave 2']['SOUTH'] == 'LOCKED':
            print_slow(line1316, typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput == 'WEST':
                print_slow(line1317, typingActive)
                rooms['Waterfall Cave 2']['SOUTH'] = 'Waterfall Cave 3'
                rooms['Waterfall Cave 2']['map'] = waterfallcave2_map2
                rooms['Waterfall Cave 2']['EXPLORE'] = line1315b
                break
            elif playerInput == 'EAST':
                print_slow(line1318, typingActive)
                p1.HP = max(p1.HP - 20, 0)
                if p1.HP <= 0:
                    combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
                    break
                print_slow(f'{p1.name} takes 20 damage from the fall. {p1.name} has {p1.HP}/{p1.MaxHP} HP.', typingActive)
                rooms['Waterfall Cave 2']['SOUTH'] = 'Waterfall Cave 3'
                rooms['Waterfall Cave 2']['map'] = waterfallcave2_map2
                rooms['Waterfall Cave 2']['secret_path'] = 1
                rooms['Waterfall Cave 2']['EXPLORE'] = line1315b
                break
            elif playerInput in backRes:
                print_slow(line1320, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        elif rooms['Waterfall Cave 2']['SOUTH'] != 'LOCKED':
            print_slow(line1316, typingActive)
            break


def waterfallcave3_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if 'River Serpent' in rooms['Waterfall Cave 3']['boss']:
            if 'LANTERN' not in p1.inventory:
                print_slow(line1327, typingActive)
                p1.ACC = 60
                foe = p51
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms['Waterfall Cave 3']['map'] = waterfallcave3_map2
                rooms['Waterfall Cave 3']['boss'].remove('River Serpent')
                rooms['Waterfall Cave 3']['EXPLORE'] = line1325
                p1.ACC = 95
                p1.inventory.append('SERPENTS EYE')
                p1.inventory.append('STRANGE GREASE')
                print_slow(line1328, typingActive)
                break
            elif 'LANTERN' in p1.inventory:
                print_slow(line1327a, typingActive)
                rooms['Waterfall Cave 3']['EXPLORE'] = line1324
                rooms['Waterfall Cave 3']['event'] = 1
                while True:
                    playerInput = input().upper().strip()
                    print('\n')
                    if playerInput in atkRes:
                        print_slow(line1327b, typingActive)
                        foe = p51
                        combat.standard_battle(p1, foe, typingActive, SoundsOn)
                        if p1.HP <= 0:
                            break
                        rooms['Waterfall Cave 3']['map'] = waterfallcave3_map2
                        rooms['Waterfall Cave 3']['boss'].remove('River Serpent')
                        rooms['Waterfall Cave 3']['EXPLORE'] = line1326
                        p1.inventory.append('SERPENTS EYE')
                        p1.inventory.append('STRANGE GREASE')
                        print_slow(line1328, typingActive)
                        break
                    elif playerInput in backRes:
                        print_slow(line1327c, typingActive)
                        break
                    else:
                        soundFile = str(SFX_Library['Error'])
                        play_sound_effect(soundFile, SoundsOn)
                        print_slow('\nInvalid input. Input ATTACK or BACK.\n', typingActive)
        elif 'River Serpent' not in rooms['Waterfall Cave 3']['boss']:
            if 'LANTERN' not in p1.inventory:
                print_slow(line1328a, typingActive)
                break
            elif 'LANTERN' in p1.inventory:
                if rooms['Waterfall Cave 3']['event'] == 0:
                    rooms['Waterfall Cave 3']['event'] = 1
                    rooms['Waterfall Cave 3']['EXPLORE'] = line1326
                    print_slow(line1328b, typingActive)
                    print_slow(line1328c, typingActive)
                    break
                elif rooms['Waterfall Cave 3']['event'] == 1:
                    print_slow(line1328c, typingActive)
                    break
        break


def lake_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Echobo Lake']['EAST'] == 'LOCKED':
            if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
                print_slow(line1404, typingActive)
                break
            elif 'AXE' in p1.inventory:
                print_slow(line1405, typingActive)
                playerInput = (input().upper()).strip()
                print_slow("\n", typingActive)
                if playerInput == 'CUT':
                    soundFile = str(SFX_Library['Chop'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line1409, typingActive)
                    break
                elif playerInput in backRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line1407, typingActive)
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)
            elif 'SHARP AXE' in p1.inventory:
                print_slow(line1405, typingActive)
                playerInput = (input().upper()).strip()
                print_slow("\n", typingActive)
                if playerInput == 'CUT':
                    soundFile = str(SFX_Library['Chop'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line1406, typingActive)
                    foe = rooms['Echobo Lake']['foe']
                    combat.standard_battle(p1, foe, typingActive, SoundsOn)
                    if p1.HP <= 0:
                        break
                    print_slow(line1408, typingActive)
                    rooms['Echobo Lake']['EAST'] = 'Mushroom Grove'
                    rooms['Echobo Lake']['EXPLORE'] = line1403
                    rooms['Echobo Lake']['map'] = lake_map2
                    p1.inventory.append('THORN BRACERS')
                    break
                elif playerInput in backRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line1407, typingActive)
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line1408, typingActive)
            break


def cave_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if 'Bear' in rooms['Bear Cave']['boss']:
            if 'SALMON' not in p1.inventory:
                print_slow(f'\n{line903}\n', typingActive)
            else:
                print_slow(f'\n{line904}\n', typingActive)
            playerInput = (input().upper()).strip()
            print_slow("\n", typingActive)
            if playerInput == "POKE":
                print_slow(line911, typingActive)
                foe = rooms['Bear Cave']['foe']
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms['Bear Cave']['boss'].remove('Bear')
                p1.inventory.append('AXE')
                rooms['Bear Cave']['intro'] = line902
                rooms['Bear Cave']['EXPLORE'] = line906b
                rooms['Bear Cave']['map'] = cave_map2
                print_slow(line912, typingActive)
                print_slow(f'{p1.name} obtains an AXE!\n', typingActive)
                break

            elif playerInput == "FEED" and 'SALMON' in p1.inventory:
                p1.inventory.remove('SALMON')
                rooms['Bear Cave']['boss'].remove('Bear')
                p1.inventory.append('AXE')
                soundFile = str(SFX_Library['Bite'])
                play_sound_effect(soundFile, SoundsOn)
                rooms['Bear Cave']['intro'] = line902
                rooms['Bear Cave']['EXPLORE'] = line906b
                rooms['Bear Cave']['map'] = cave_map2
                print_slow(line913, typingActive)
                print_slow(f'{p1.name} obtains an AXE!\n', typingActive)
                break
            elif playerInput in backRes:    
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line907, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line912b, typingActive)
            break


def cave2_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Rocky Cave 2']['chest'] == "CLOSED":
            print_slow(line925, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("", typingActive)
            if playerInput == "OPEN":
                print_slow(line926, typingActive)
                foe = p3b
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms['Rocky Cave 2']['chest'] = "OPEN"
                p1.inventory.append('IRON KEY')
                rooms['Rocky Cave 2']['EXPLORE'] = line924
                rooms['Rocky Cave 2']['map'] = cave2_map2
                print_slow(line927, typingActive)
                break
            elif playerInput in atkRes:
                soundFile = str(SFX_Library['Smash'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line929, typingActive)
                foe = p3b
                foe.HP -= 10
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms['Rocky Cave 2']['chest'] = "OPEN"
                p1.inventory.append('IRON KEY')
                rooms['Rocky Cave 2']['EXPLORE'] = line924
                rooms['Rocky Cave 2']['map'] = cave2_map2
                print_slow(line929, typingActive)
                break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line928, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line928b, typingActive)
            break


def cave4_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Rocky Cave 4']['EAST'] == 'LOCKED':
            if 'IRON KEY' not in p1.inventory:
                print_slow(f'\n{line940}', typingActive)
                break
            else:
                print_slow(f'\n{line940b}', typingActive)
                playerInput = (input().upper()).strip()
                print_slow("", typingActive)
                if playerInput == "OPEN":
                    print_slow(line941, typingActive)
                    rooms['Rocky Cave 4']['EAST'] = "Queen's Chamber"
                    rooms['Rocky Cave 4']['EXPLORE'] = line939
                    break
                elif playerInput == "BACK" or playerInput == "BACK OUT":
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line941b, typingActive)
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)


def berry_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Berry Patch']['chest'] == 'CLOSED':
            print_slow(line1002b, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("", typingActive)
            if playerInput == "PICK":
                print_slow(line1003, typingActive)
                foe = rooms['Berry Patch']['foe']
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                print_slow(line1004, typingActive)
                berriesPicked = random.randrange(2, 6)
                p1.POTS = min(p1.POTS + berriesPicked, p1.MaxPOTS)
                rooms['Berry Patch']['chest'] = "OPEN"
                rooms['Berry Patch']['EXPLORE'] = line1005
                print_slow(f'{p1.name} has made {berriesPicked} POTIONS. {p1.name} has {p1.POTS} POTS.\n', typingActive)
                break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line1002c, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
        else:
            print_slow(line1006, typingActive)
            break


def oak_examine(p1, rooms, typingActive, SoundsOn):
    print_slow(line2003, typingActive)


def hive_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Bee Hive']['chest'] == "CLOSED":
            print_slow(line2105b, typingActive)
            p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
            print_slow(f'\n{p1.name} gains 3 potions.\n', typingActive)
            rooms['Bee Hive']['EXPLORE'] = line2106
            rooms['Bee Hive']['chest'] = "OPEN"
            rooms['Bee Hive']['map'] = hive_map2
            break
        else:
            print_slow(line2106b, typingActive)
            break


def mushroom_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if p1.gobCount >= 20 and rooms['Mushroom Grove']['chest'] == 'CLOSED':
            print_slow(line1604, typingActive)
            soundFile = str(SFX_Library['GotLegendary'])
            play_sound_effect(soundFile, SoundsOn)
            time.sleep(0.5)
            p1.inventory.append('HEROS MEDAL')
            rooms['Mushroom Grove']['chest'] = 'OPEN'
            break
        elif p1.gobCount >= 20 and rooms['Mushroom Grove']['chest'] == 'OPEN':
            print_slow(line1604b, typingActive)
            break
        else:
            print_slow(line1603, typingActive)
            break


def fairy_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if p1.faeCount == 0:
            print_slow(line2905, typingActive)
            break
        elif p1.faeCount >= 1 and rooms['Fairy Circle']['speech'] == 0:
            print_slow(line2906, typingActive)
            rooms['Fairy Circle']['speech'] = 1
            rooms['Fairy Circle']['EXPLORE'] = line2903
            break
        elif "Dark Fairy Prince" in rooms['Fairy Circle']['boss'] and rooms['Fairy Circle']['speech'] == 1:
            print_slow(line2907, typingActive)
            break
        elif "Dark Fairy Prince" not in rooms['Fairy Circle']['boss']:
            print_slow(line2908, typingActive)
            break


def swamp4_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Rotten Swamp 4']['event'] == 0:
            print_slow(line2709, typingActive)
            playerInput = (input().upper()).strip()
            print("")
          
            if playerInput == 'LEFT':
              print_slow(line2712b, typingActive)
              while True:
                playerInput = (input().upper()).strip()
                print("")
                if playerInput == 'OPEN':
                  print_slow(line2713, typingActive)
                  p1.POISON += 3
                  foe = rooms['Rotten Swamp 4']['foe']
                  combat.standard_battle(p1, foe, typingActive, SoundsOn)
                  if p1.HP <= 0:
                    break
                  print_slow(line2714, typingActive)
                  rooms['Rotten Swamp 4']['map'] = swamp4_map2
                  rooms['Rotten Swamp 4']['event'] = 1
                  break
                elif playerInput in atkRes:
                  soundFile = str(SFX_Library['Smash'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow(line2713b, typingActive)
                  foe = rooms['Rotten Swamp 4']['foe']
                  combat.standard_battle(p1, foe, typingActive, SoundsOn)
                  if p1.HP <= 0:
                    break
                  print_slow(line2714, typingActive)
                  rooms['Rotten Swamp 4']['map'] = swamp4_map2
                  rooms['Rotten Swamp 4']['event'] = 1
                  break
                elif playerInput in backRes:
                  soundFile = str(SFX_Library['Back'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('You decide to leave the chests be for now.\n', typingActive)
                  break
                else:
                  soundFile = str(SFX_Library['Error'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('\nInvalid input. Try again.\n', typingActive)
              break
              
            elif playerInput == 'RIGHT':
              print_slow(line2712c, typingActive)
              while True:
                playerInput = (input().upper()).strip()
                print("")
                if playerInput == 'OPEN':
                  print_slow(line2715, typingActive)
                  p1.inventory.append('MOUTH-PIECE')
                  rooms['Rotten Swamp 4']['map'] = swamp4_map3
                  if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
                      p1.inventory.append('COMPLETE HORN')
                      p1.inventory.remove('MOUTH-PIECE')
                      p1.inventory.remove('BROKEN HORN')
                      rooms['Rotten Swamp 8']['EXPLORE'] = line2729
                      print_slow(line2716, typingActive)
                      rooms['Rotten Swamp 4']['event'] = 2
                  break
                elif playerInput in atkRes:
                  print_slow(line2715b, typingActive)
                  p1.inventory.append('MOUTH-PIECE')
                  rooms['Rotten Swamp 4']['map'] = swamp4_map3
                  if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
                      p1.inventory.append('COMPLETE HORN')
                      p1.inventory.remove('MOUTH-PIECE')
                      p1.inventory.remove('BROKEN HORN')
                      rooms['Rotten Swamp 8']['EXPLORE'] = line2729
                      print_slow(line2716, typingActive)
                      rooms['Rotten Swamp 4']['event'] = 2
                  break
                elif playerInput == 'BACK':
                  print_slow('You decide to leave the chest be for now.\n', typingActive)
                  break
                else:
                  soundFile = str(SFX_Library['Error'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('\nInvalid input. Try again.\n', typingActive)
              break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('You decide to leave the chests be for now.\n', typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)

        elif rooms['Rotten Swamp 4']['event'] == 1:
            print_slow(line2710, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("", typingActive)
            if playerInput == 'RIGHT':
              print_slow(line2712c, typingActive)
              while True:
                playerInput = (input().upper()).strip()
                print("")
                if playerInput == 'OPEN':
                  print_slow(line2715, typingActive)
                  p1.inventory.append('MOUTH-PIECE')
                  rooms['Rotten Swamp 4']['map'] = swamp4_map4
                  if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
                      p1.inventory.append('COMPLETE HORN')
                      p1.inventory.remove('MOUTH-PIECE')
                      p1.inventory.remove('BROKEN HORN')
                      print_slow(line2716, typingActive)
                      rooms['Rotten Swamp 4']['event'] = 3
                  break
                elif playerInput in atkRes:
                  soundFile = str(SFX_Library['Smash'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow(line2715b, typingActive)
                  p1.inventory.append('MOUTH-PIECE')
                  rooms['Rotten Swamp 4']['map'] = swamp4_map4
                  if ('MOUTH-PIECE' and 'BROKEN HORN') in p1.inventory:
                      p1.inventory.append('COMPLETE HORN')
                      p1.inventory.remove('MOUTH-PIECE')
                      p1.inventory.remove('BROKEN HORN')
                      print_slow(line2716, typingActive)
                      rooms['Rotten Swamp 4']['event'] = 3
                  break
                elif playerInput in backRes:
                  soundFile = str(SFX_Library['Back'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('You decide to leave the chests be for now.\n', typingActive)
                  break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Try again.\n', typingActive)
              break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('You decide to leave the chests be for now.\n', typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)

        elif rooms['Rotten Swamp 4']['event'] == 2:
            print_slow(line2711, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("", typingActive)
            if playerInput == 'LEFT':
              print_slow(line2712b, typingActive)
              while True:
                playerInput = (input().upper()).strip()
                print("")
                if playerInput == 'OPEN':
                  print_slow(line2713, typingActive)
                  p1.POISON = 3
                  foe = rooms['Rotten Swamp 4']['foe']
                  combat.standard_battle(p1, foe, typingActive, SoundsOn)
                  if p1.HP <= 0:
                    break
                  print_slow(line2714, typingActive)
                  rooms['Rotten Swamp 4']['map'] = swamp4_map4
                  rooms['Rotten Swamp 4']['event'] = 3
                  break
                elif playerInput in atkRes:
                  soundFile = str(SFX_Library['Smash'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow(line2713b, typingActive)
                  p1.POISON = 6
                  foe = rooms['Rotten Swamp 4']['foe']
                  combat.standard_battle(p1, foe, typingActive, SoundsOn)
                  if p1.HP <= 0:
                    break
                  print_slow(line2714, typingActive)
                  rooms['Rotten Swamp 4']['map'] = swamp4_map4
                  rooms['Rotten Swamp 4']['event'] = 3
                  break
                elif playerInput in backRes:
                  soundFile = str(SFX_Library['Back'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('You decide to leave the chests be for now.\n', typingActive)
                  break
                else:
                  soundFile = str(SFX_Library['Error'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('\nInvalid input. Try again.\n', typingActive)
              break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('You decide to leave the chests be for now.\n', typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)

        elif rooms['Rotten Swamp 4']['event'] == 3:
            print_slow(line2712, typingActive)
            break


def shipwreck_examine(p1, rooms, typingActive, SoundsOn):
    while True:
        if rooms['Shipwreck']['chest'] == 'OPEN':
            print_slow(line3309, typingActive)
            break
        elif rooms['Shipwreck']['chest'] == 'CLOSED':
            print_slow(line3304, typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes:
                print_slow(line3306, typingActive)
                roll = random.randrange(0, 10) + rooms['Shipwreck']['event']
                if roll >= 9:
                    print_slow(line3308, typingActive)
                    p1.GP += 300
                    p1.POTS = min(p1.POTS + 2, p1.MaxPOTS)
                    print_slow(f"{p1.name} has {p1.GP} GP and {p1.POTS}/{p1.MaxPOTS} POTIONS.\n", typingActive)
                    rooms['Shipwreck']['chest'] = 'OPEN'
                    soundFile = str(SFX_Library['Buy'])
                    play_sound_effect(soundFile, SoundsOn)
                    break
                elif roll < 9:
                    print_slow(line3307, typingActive)
                    foe = random.choice(rooms['Shipwreck']['enemy_spawn_set'])
                    combat.standard_battle(p1, foe, typingActive, SoundsOn)
                    if p1.HP <= 0:
                        break
                    rooms['Shipwreck']['event'] += 2
                    break
            elif playerInput in negRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line3305, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Input YES or NO.', typingActive)



def riverwest_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['River - West Bank']['event'] == 0:
        print_slow(line3805, typingActive)
        while True:
            playerInput = input().upper().strip()
            print('\n')
            if playerInput == 'PUSH':
                print_slow(line3806, typingActive)
                rooms['River - West Bank']['map'] = westriver_map2
                rooms['Serpent River']['map'] = river_map2
                rooms['River - West Bank']['secrets'].append('SAIL')
                rooms['Serpent River']['secrets'].append('SAIL')
                rooms['River - West Bank']['event'] = 1
                rooms['Serpent River']['EXPLORE'] = line1203
                rooms['River - West Bank']['EXPLORE'] = line3803
                break
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Input PUSH or LEAVE.\n', typingActive)
    elif rooms['River - West Bank']['event'] == 1:
        print_slow(line3807, typingActive)
    elif rooms['River - West Bank']['event'] == 2:
        print_slow(line3808, typingActive)


def deepwoodsfork_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Deep Woods - Fork']['EAST'] == 'LOCKED':
      if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
        print_slow(line4708, typingActive)
      elif 'AXE' in p1.inventory:
        print_slow(line4709, typingActive)
        while True:
          playerInput = input().upper().strip()
          print('\n')
          if playerInput == 'CUT':
            soundFile = str(SFX_Library['Chop'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4711, typingActive)
            break
          elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4711d, typingActive)
            break
          else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Input CUT or LEAVE.\n', typingActive)
      elif 'SHARP AXE' in p1.inventory:
        print_slow(line4709, typingActive)
        while True:
          playerInput = input().upper().strip()
          print('\n')
          if playerInput == 'CUT':
            soundFile = str(SFX_Library['Chop'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4710, typingActive)
            rooms['Deep Woods - Fork']['EAST'] = 'Deep Woods - EAST'
            rooms['Deep Woods - Fork']['map'] = deepwoodsfork_map2
            rooms['Deep Woods - Fork']['EXPLORE'] = line4707
            break
          elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4711d, typingActive)
            break
          else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Input CUT or LEAVE.\n', typingActive)
    else:
        print_slow(line4711c, typingActive)


def deepwoodswest_examine(p1, rooms, typingActive, SoundsOn):
  if rooms['Deep Woods - WEST']['NORTH'] == 'LOCKED':
      if 'AXE' not in p1.inventory and 'SHARP AXE' not in p1.inventory:
        print_slow(line4715, typingActive)
      elif 'AXE' in p1.inventory:
        print_slow(line4716, typingActive)
        while True:
          playerInput = input().upper().strip()
          print('\n')
          if playerInput == 'CUT':
            soundFile = str(SFX_Library['Chop'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4717, typingActive)
            break
          elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4719, typingActive)
            break
          else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Input CUT or LEAVE.\n', typingActive)
      elif 'SHARP AXE' in p1.inventory:
        print_slow(line4716, typingActive)
        while True:
          playerInput = input().upper().strip()
          print('\n')
          if playerInput == 'CUT':
            soundFile = str(SFX_Library['Chop'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4718, typingActive)
            rooms['Deep Woods - WEST']['NORTH'] = 'Deep Woods - Fallen Hive'
            rooms['Deep Woods - WEST']['map'] = deepwoodswest_map2
            rooms['Deep Woods - WEST']['EXPLORE'] = line4714
            break
          elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line4719, typingActive)
            break
          else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Input CUT or LEAVE.\n', typingActive)
  else:
      print_slow(line4718c, typingActive)
      

def tatteredhive_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Tattered Hive']['event'] == 0:
      print_slow(line4805, typingActive)
      foe = p74
      combat.standard_battle(p1, foe, typingActive, SoundsOn)
      if p1.HP <= 0:
        return
      print_slow(line4806, typingActive)
      foe = p75
      combat.standard_battle(p1, foe, typingActive, SoundsOn)
      if p1.HP <= 0:
        return
      print_slow(line4807, typingActive)
      p1.HP += round(p1.MaxHP // 2)
      p1.stat_check(typingActive, SoundsOn)
      rooms['Tattered Hive']['event'] = 1
      rooms['Tattered Hive']['EXPLORE'] = line4803
      rooms['Tattered Hive']['map'] = hive2_map2
    elif rooms['Tattered Hive']['event'] == 1:
      print_slow(line4808, typingActive)
      p1.inventory.append('STRANGE JELLY')
      p1.RJ += 20
      rooms['Tattered Hive']['EXPLORE'] = line4804
      rooms['Tattered Hive']['map'] = hive2_map3
    else:
      print_slow(line4809, typingActive)


def orc1_examine(p1, rooms, typingActive, SoundsOn):
  if rooms["Orc Fortress 1"]['event2'] == 0:
    if 'CRANK' not in p1.inventory:
      print_slow(line4907, typingActive)
    else:
      print_slow(line4910, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput == 'INSERT':
          soundFile = str(SFX_Library['Select'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4912, typingActive)
          rooms["Orc Fortress 1"]['event2'] = 1
          rooms["Orc Fortress 1"]['map'] = orcfort1_map2
          key_items['CRANK']['quantity'] -= 1
          if key_items['CRANK']['quantity'] == 0:
            p1.inventory.remove('CRANK')
          break
        elif playerInput in backRes:
          soundFile = str(SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4916, typingActive)
          break
        else:
          soundFile = str(SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Input INSERT or LEAVE.', typingActive)
          
  elif rooms["Orc Fortress 1"]['event2'] == 1:
    if 'CRANK' not in p1.inventory:
      print_slow(line4908, typingActive)
    else:
      print_slow(line4911, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput == 'INSERT':
          soundFile = str(SFX_Library['Select'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4913, typingActive)
          rooms["Orc Fortress 1"]['event2'] = 2
          rooms["Orc Fortress 1"]['map'] = orcfort1_map3
          rooms["Orc Fortress 1"]['NORTH'] = "Orc Keep"
          p1.inventory.remove('CRANK')
          break
        elif playerInput in backRes:
          soundFile = str(SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4916, typingActive)
          break
        else:
          soundFile = str(SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Input INSERT or LEAVE.', typingActive)
  else:
      print_slow(line4909, typingActive)
    

def orc2_examine(p1, rooms, typingActive, SoundsOn):  
  if rooms["Orc Fortress 2"]['chest'] == 0:
    if 'CHEST KEY' not in p1.inventory:
      print_slow(line4920, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in atkRes:
          soundFile = str(SFX_Library['Smash'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4921, typingActive)
          foe = random.choice(enemy_spawn28)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
            break
          print_slow(f"You deafeat the {foe.name} and search the chest for any spoils. Inside you find a CRANK. Looks like this was removed from a mechanism for some strange reason.\n", typingActive)
          if 'CRANK' not in p1.inventory:
            p1.inventory.append('CRANK')
          key_items['CRANK']['quantity'] += 1
          rooms["Orc Fortress 2"]['EXPLORE'] = line4919b
          rooms["Orc Fortress 2"]['chest'] = 1
          break
        elif playerInput == 'SEARCH':
          soundFile = str(SFX_Library['Select'])
          play_sound_effect(soundFile, SoundsOn)
          orc2_special(p1, playerInput, typingActive, SoundsOn)
          break
        elif playerInput in backRes:
          soundFile = str(SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4922, typingActive)
          break
        else:
          soundFile = str(SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Input SMASH or SEARCH, or LEAVE to exit.', typingActive)
          
    else:
      print_slow(line4923, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput == 'OPEN':
          print_slow(line4924, typingActive)
          if 'CRANK' not in p1.inventory:
            p1.inventory.append('CRANK')
            key_items['CRANK']['quantity'] += 1
          else:
            key_items['CRANK']['quantity'] += 1
          p1.inventory.remove('CHEST KEY')
          rooms["Orc Fortress 2"]['EXPLORE'] = line4919b
          rooms["Orc Fortress 2"]['chest'] = 1
          break
        if playerInput in atkRes:
          soundFile = str(SFX_Library['Smash'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4925, typingActive)
          foe = random.choice(enemy_spawn28)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
            break
          print_slow(f"You deafeat the {foe.name} and search the chest for any spoils. Inside you find a CRANK. Looks like this was removed from a mechanism for some strange reason.\n", typingActive)
          if 'CRANK' not in p1.inventory:
            p1.inventory.append('CRANK')
            key_items['CRANK']['quantity'] += 1
          else:
            key_items['CRANK']['quantity'] += 1
          p1.inventory.remove('CHEST KEY')
          rooms["Orc Fortress 2"]['EXPLORE'] = line4919b
          rooms["Orc Fortress 2"]['chest'] = 1
          break
        elif playerInput in backRes:
          soundFile = str(SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4926, typingActive)
          break
        else:
          soundFile = str(SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Input OPEN, SMASH, or LEAVE.', typingActive)
  else:
    print_slow(line4926b, typingActive)


def orc4_examine(p1, rooms, typingActive, SoundsOn):  
  if rooms["Orc Fortress 4"]['chest'] == 0:
    if rooms["Orc Fortress 4"]['event2'] == 0:
      print_slow(line4939, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput == 'SNEAK':
          if p1.job != 'THIEF':
            roll = random.randrange(0,4)
          else:
            roll = 3
          while True:
            if roll <= 1:
              print_slow(line4940, typingActive)
              foe = random.choice(enemy_spawn28)
              combat.standard_battle(p1, foe, typingActive, SoundsOn)
              if p1.HP <= 0:
                break
              orc4_examine2(line4942, p1, typingActive)
              break
            else:
              orc4_examine2(line4943, p1, typingActive)
              break
          break
        elif playerInput in backRes:
          soundFile = str(SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(line4950, typingActive)
          break
        else:
          soundFile = str(SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Input SNEAK or LEAVE.', typingActive)
    else:
      print_slow(line4941, typingActive)
      orc4_examine2(line4943, p1, typingActive)    
  else:
    print_slow("The chest near the war tent has been opened and its contents pillaged. It doesn't look like theres anything else around here worth checking out.", typingActive)

              
def orc4_examine2(inq, p1, typingActive, SoundsOn):
  mod = 0
  print_slow(inq, typingActive)
  while True:
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'PRY':
      print_slow(line4944, typingActive)
      roll =  random.randrange(0,5) + mod
      if roll >= 3:
        print_slow(line4948, typingActive)
        if 'CRANK' not in p1.inventory:
          p1.inventory.append('CRANK')
          key_items['CRANK']['quantity'] += 1
        else:
          key_items['CRANK']['quantity'] += 1
        rooms["Orc Fortress 4"]['EXPLORE'] = line4938
        rooms["Orc Fortress 4"]['chest'] = 1
        rooms["Orc Fortress 4"]['map'] = orcfort4_map2
        break
      if roll == 2:
        print_slow(line4946, typingActive)
        mod += 1
      else:
        print_slow(line4945, typingActive)
        foe = random.choice(enemy_spawn28)
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            break
        print_slow(line4947, typingActive)
        mod += 1
    elif playerInput in atkRes:
      soundFile = str(SFX_Library['Smash'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(line4949, typingActive)
      if 'CRANK' not in p1.inventory:
        p1.inventory.append('CRANK')
        key_items['CRANK']['quantity'] += 1
      else:
        key_items['CRANK']['quantity'] += 1
      rooms["Orc Fortress 4"]['EXPLORE'] = line4938
      rooms["Orc Fortress 4"]['chest'] = 1
      rooms["Orc Fortress 4"]['map'] = orcfort4_map2
      foe = p82
      combat.standard_battle(p1, foe, typingActive, SoundsOn)
      if p1.HP <= 0:
        break
      print_slow(line4949b, typingActive)
      break
    elif playerInput in backRes:
      soundFile = str(SFX_Library['Back'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(line4950, typingActive)
      break
    else:
      soundFile = str(SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid input. Input PRY, SMASH, or LEAVE.', typingActive)
      

def orc5_examine(p1, rooms, typingActive, SoundsOn):
  if rooms["Orc Fortress 5"]['chest'] == 0 and rooms["Orc Fortress 5"]['event2'] == 0:
    print_slow(line4956, typingActive)
    while True:
      playerInput = input().upper().strip()
      print('\n')
      if playerInput == "CHEST":
        orc5_examine_chest(p1, rooms, typingActive, SoundsOn)
        break
      elif playerInput == "WOOD":
        orc5_examine_wood(p1, rooms, typingActive, SoundsOn)
        break
      elif playerInput in backRes:
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line4969, typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input CHEST, WOOD, or BACK.', typingActive)
  elif rooms["Orc Fortress 5"]['chest'] == 0 and rooms["Orc Fortress 5"]['event2'] == 1:
    print_slow(line4957, typingActive)
    while True:
      playerInput = input().upper().strip()
      print('\n')
      if playerInput == "CHEST":
        orc5_examine_chest(p1, rooms, typingActive, SoundsOn)
        break
      elif playerInput in backRes:
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line4969, typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input CHEST or BACK.', typingActive)
  elif rooms["Orc Fortress 5"]['chest'] == 1 and rooms["Orc Fortress 5"]['event2'] == 0:
    print_slow(line4958, typingActive)
    while True:
      playerInput = input().upper().strip()
      print('\n')
      if playerInput == "WOOD":
        orc5_examine_wood(p1, rooms, typingActive, SoundsOn)
        break
      elif playerInput in backRes:
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line4969, typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input WOOD or BACK.', typingActive)
  else:
      print_slow(line4970, typingActive)


def orc5_examine_chest(p1, rooms, typingActive, SoundsOn):
  print_slow(line4959, typingActive)
  while True:
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'OPEN':
      print_slow(line4960, typingActive)
      p1.HP = max(p1.HP - 15, 0)
      print_slow(f"{p1.name} has lost 15 HP! {p1.name} has {p1.HP}/{p1.MaxHP}", typingActive)
      combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
      if p1.HP <= 0:
        return
      print_slow(line4960b, typingActive)
      p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
      print_slow(f"{p1.name} gathers the POTIONS into their inventory. {p1.name} now has {p1.POTS}/{p1.MaxPOTS}", typingActive)
      rooms["Orc Fortress 5"]['chest'] = 1
      orc5_examine_update1(rooms)
      break
    elif playerInput in atkRes:
      roll = random.randrange(0,5)
      if roll >= 3:
        print_slow(line4962, typingActive)
        p1.POTS = min(p1.POTS + 3, p1.MaxPOTS)
        print_slow(f"{p1.name} gathers the POTIONS into their inventory. {p1.name} now has {p1.POTS}/{p1.MaxPOTS}", typingActive)
        rooms["Orc Fortress 5"]['chest'] = 1
        orc5_examine_update1(rooms)
        break
      else:
        print_slow(line4961, typingActive)
        rooms["Orc Fortress 5"]['chest'] = 1
        orc5_examine_update1(rooms)
        break
    elif playerInput in backRes:
      soundFile = str(SFX_Library['Back'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(line4963, typingActive)
      break
    else:
      soundFile = str(SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid input. Input OPEN, SMASH, or BACK.', typingActive)


def orc5_examine_wood(p1, rooms, typingActive, SoundsOn):
  print_slow(line4964, typingActive)
  while True:
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'LIGHT':
      hit = random.randrange(0,6)
      if hit >= 2:
        print_slow(line4965, typingActive)
        rooms["Orc Fortress 5"]['event2'] = 1
        rooms["Orc Fortress 4"]['event2'] = 1
        rooms['Orc Fortress 5']['spawn_modifier'] = -1
        orc5_examine_update2(rooms)
        break
      else:
        print_slow(line4965, typingActive)
        rooms["Orc Fortress 5"]['event2'] = 1
        rooms['Orc Fortress 5']['spawn_modifier'] = 1
        orc5_examine_update2(rooms)
        break
    elif playerInput in backRes:
      soundFile = str(SFX_Library['Back'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(line4968, typingActive)
      break
    else:
      soundFile = str(SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid input. Input LIGHT or LEAVE.', typingActive)


def orc5_examine_update1(rooms):
  if rooms["Orc Fortress 5"]['event2'] == 0:
     rooms["Orc Fortress 5"]['map'] = orcfort5_map2
  else:
     rooms["Orc Fortress 5"]['map'] = orcfort5_map4
    

def orc5_examine_update2(rooms):
  if rooms["Orc Fortress 5"]['chest'] == 0:
     rooms["Orc Fortress 5"]['map'] = orcfort5_map3
  else:
     rooms["Orc Fortress 5"]['map'] = orcfort5_map4
    
  
def rotshrine_examine(p1, rooms, typingActive, SoundsOn):
  if rooms['Hidden Shrine']['event'] == 0:
    print_slow(line2611, typingActive)
    foe = p85
    combat.standard_battle(p1, foe, typingActive, SoundsOn)
    if p1.HP <= 0:
        return
    print_slow(line2612, typingActive)
    rooms['Hidden Shrine']['event'] = 1
    rooms['Hidden Shrine']['map'] = rot3_map2
    rooms['Hidden Shrine']['intro'] = line2608
    rooms['Hidden Shrine']['EXPLORE'] = line2610
    rooms['Rotting Woods - EAST']['EXPLORE'] = line2606
    key_items['LANTERN']['BF'] += 1 #Adds Blue flame to lantern
    key_items['LANTERN']['description'] = 'A lantern that attaches to a belt for hands free use. Allows travel through dark areas. Enhanced with the power of a DIVINE FLAME. This everlasting blue flame is capable of dispelling and warding off evil miasma.'
  else:
    print_slow(line2613, typingActive)


def vamp_3_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Forest Palace - 3']['event'] == 2:
        print_slow(line5108g, typingActive)
    elif rooms['Forest Palace - 3']['event'] == 1:
        print_slow(line5108c, typingActive)
        foe = rooms['Forest Palace - 3']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        p1.inventory.append('SAPPHIRE GEMSTONE')
        print_slow(line5108d, typingActive)
        print_slow(line5108e, typingActive)
        rooms['Forest Palace - 3']['event'] = 2
        rooms['Forest Palace - 3']['EXPLORE'] = line5108f
    else:
        print_slow('You are unable to do that here.\n', typingActive)    


def vamp_4_examine(p1, rooms, typingActive, SoundsOn):
  
  if rooms['Forest Palace - 4']['event'] == 0:
    print_slow(line5111, typingActive)
    while True:
      playerInput = input().upper().strip()
      print('\n')
      if playerInput in affRes :
        soundFile = str(SFX_Library['Select'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line5111b, typingActive)
        damage = random.randrange(10, 26)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        print_slow(f"{p1.name} has lost {damage} HP! {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining.\n", typingActive)
        combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
        if p1.HP <= 0:
            return
        foe = rooms['Forest Palace - 4']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            break
        vamp_queen_update(rooms)
        rooms['Forest Palace - 4']['event'] = 1
        rooms['Forest Palace - 4']['map'] = vcastle_4_map2
        if rooms["Forest Palace - 6"]['event'] == 2:
            print_slow(line5111e, typingActive)
        else:
           print_slow(line5111d, typingActive)
        break
      elif playerInput in negRes :
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line5111c, typingActive)
        foe = rooms['Forest Palace - 4']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            break
        vamp_queen_update(rooms)
        rooms['Forest Palace - 4']['event'] = 1
        rooms['Forest Palace - 4']['map'] = vcastle_4_map2
        if rooms["Forest Palace - 6"]['event'] == 2:
            print_slow(line5111e, typingActive)
        else:
           print_slow(line5111d, typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input YES or NO.', typingActive)
  else:
    print_slow("The lever has already been pulled. No use pulling it any further...", typingActive)


def vamp_5_examine(p1, rooms, typingActive, SoundsOn):
   if rooms['Forest Palace - 5']['event'] == 0:
        print_slow(line5114, typingActive)
   else:
       print_slow(line5114b, typingActive)


def vamp_6_examine(p1, rooms, typingActive, SoundsOn):
   if rooms['Forest Palace - 6']['event'] == 2:
        print_slow(line5116f, typingActive)
   elif rooms['Forest Palace - 6']['event'] == 1:
        print_slow(line5116e, typingActive)     
   else:
       print_slow(line5116d, typingActive)


def vamp_7_examine(p1, rooms, typingActive, SoundsOn):
  if rooms['Forest Palace - 7']['event'] == 0:
    print_slow(line5119, typingActive)
    if "MAGIC GREASE" in p1.inventory and rooms['Forest Palace - 7']['event2'] == 0: 
       print_slow(line5119b, typingActive)
       while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in affRes :
            soundFile = str(SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5119c, typingActive)
            rooms['Forest Palace - 7']['event2'] = 1
            break
        elif playerInput in negRes :
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5119d, typingActive)
            break
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid input. Input YES or NO.', typingActive)      

    while True:
      print_slow(line5119e, typingActive)
      playerInput = input().upper().strip()
      print('\n')       
      if playerInput in affRes :
        soundFile = str(SFX_Library['Select'])
        play_sound_effect(soundFile, SoundsOn)
        vamp_queen_update(rooms)
        rooms['Forest Palace - 7']['event'] = 1
        if rooms['Forest Palace - 7']['event2'] == 0:
            print_slow(line5120c, typingActive)
            damage = random.randrange(10, 26)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            print_slow(f"{p1.name} has lost {damage} HP! {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining.\n", typingActive)
            combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
            if p1.HP <= 0:
             return
            foe = rooms['Forest Palace - 7']['foe']
            combat.standard_battle(p1, foe, typingActive, SoundsOn)
            if p1.HP <= 0:
                break
            print_slow(line5120d, typingActive)
            rooms['Forest Palace - 7']['EXPLORE'] = line5118c
            rooms['Forest Palace - Dungeon']['EXPLORE'] = line5122b
            rooms['Forest Palace - 7']['map'] = vcastle_7_map2
            rooms['Forest Palace - Dungeon']['map'] = vcastle_dungeon_map2
        else:
            print_slow("\nThe lever moves without a sound!\n", typingActive)
            rooms['Forest Palace - 7']['EXPLORE'] = line5118b
            rooms['Forest Palace - 7']['map'] = vcastle_7_map3
        if rooms["Forest Palace - 6"]['event'] == 2:
            print_slow(line5120b, typingActive)
        else:
            print_slow(line5120, typingActive)
            break
        break        
      elif playerInput in negRes :
        soundFile = str(SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow("You ignore the lever and walk away.", typingActive)
        break
      else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input YES or NO.', typingActive)

  else:
    print_slow("The lever has already been pulled. No use pulling it any further...", typingActive)


def vamp_9_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Forest Palace - 9']['event'] == 1:
          print_slow(line5129d, typingActive)
    else:
         print_slow(line5129c, typingActive)


def vamp_10_examine(p1, rooms, typingActive, SoundsOn):
   if rooms['Forest Palace - 10']['chest'] == 'CLOSED':
      print_slow(line5132, typingActive)
      while True:
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in openRes and 'DININGHALL KEY' in p1.inventory:
            soundFile = str(SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5133d, typingActive)
            p1.inventory.remove('DININGHALL KEY')
            p1.inventory.append('SKELETON KEY')
            rooms['Forest Palace - 10']['chest'] = 'OPEN'
            if rooms['Forest Palace - 12']['event'] == 0:
                rooms['Forest Palace - 10']['map'] = vcastle_10_map2
                rooms['Forest Palace - 10']['EXPLORE'] = line5131b
            else:
                rooms['Forest Palace - 10']['map'] = vcastle_10_map4
                rooms['Forest Palace - 10']['EXPLORE'] = line5131d
            break   
        elif playerInput in backRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5132c, typingActive)
            break
        elif playerInput in openRes and 'DININGHALL KEY' not in p1.inventory:
            print_slow(line5132b, typingActive)
            break
        elif playerInput in atkRes:
            soundFile = str(SFX_Library['Smash'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5133e, typingActive)
            p1.HP = min(max(p1.HP - 1, 0), p1.MaxHP)
            print_slow(f"{p1.name} has lost 1 HP! {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining.\n", typingActive)
            combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
            if p1.HP <= 0:
                return
        else:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Input OPEN or BACK.', typingActive)


def vamp_11_examine(p1, rooms, typingActive, SoundsOn): 

    gem_List = ["EMERALD GEMSTONE", "RUBY GEMSTONE", "SAPPHIRE GEMSTONE"]

    def show_gem_list(i):
        gem_Inventory = []
        for item in p1.inventory:
            if item in gem_List:
                gem_Inventory.append(item)
        for i in gem_Inventory:
            gem_Inventory.index(i,0,3)
            print(str(gem_Inventory.index(i,0,3)+1) + ": " + i + "\n")

    
    if rooms['Forest Palace - 11']['event'] == 2:
        print_slow(line5137c, typingActive)
        return
    if rooms['Forest Palace - 11']['event'] == 0:
        print_slow(line5136, typingActive)
    
    if rooms['Forest Palace - 11']['event'] == 1 and any(item in p1.inventory for item in gem_List) == False:
        if rooms['Forest Palace - 11']['event2'] != 3:
            print_slow(line5136d, typingActive)
        return
    if any(item in p1.inventory for item in gem_List):
        i = p1.inventory
        print_slow(line5136b, typingActive)

        while True:
            if any(item in p1.inventory for item in gem_List) == False:
                if rooms['Forest Palace - 11']['event2'] != 3:
                    print_slow(line5136d, typingActive)
                break
            print_slow(f'There are {3 - rooms["Forest Palace - 11"]["event2"]} empty slots remaining.', typingActive)
            print_slow("\nYour current inventory of gems:\n", typingActive)
            show_gem_list(i)
            print_slow("\nWhich gem would you like to place into the pedestal? (Input the name of the gem you wish to place or BACK to cancel)\n", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in p1.inventory and playerInput in gem_List:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"You place the {playerInput} into the trident.\n", typingActive)
                p1.inventory.remove(playerInput)
                rooms['Forest Palace - 11']['event'] = 1
                rooms['Forest Palace - 11']['event2'] += 1
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5136c, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input the name of the gem you wish to place or BACK to cancel.\n', typingActive)

    if rooms['Forest Palace - 11']['event2'] == 3:
        print_slow(line5137, typingActive)
        foe = rooms['Forest Palace - 11']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        print_slow(line5137b, typingActive)
        rooms['Forest Palace - 14']['NORTH'] = "Forest Palace - 15"
        rooms['Forest Palace - 11']['event'] = 2
        rooms['Forest Palace - 14']['event'] = 2
        rooms['Forest Palace - 11']['EXPLORE'] = line5135b
        rooms['Forest Palace - 14']['EXPLORE'] = line5146b
        rooms['Forest Palace - 11']['map'] = vcastle_11_map2
        rooms['Forest Palace - 14']['map'] = vcastle_14_map2


def vamp_12_examine(p1, rooms, typingActive, SoundsOn): 
    if rooms['Forest Palace - 12']['event'] == 2:
        print_slow("The lever has been pulled already", typingActive)
        return
    if rooms['Forest Palace - 12']['event'] == 1:
        while True:
            print_slow(line5140b, typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes or playerInput == 'PULL' :
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5140c, typingActive) 
                rooms['Forest Palace - 10']['EAST'] = "Forest Palace - 16"
                rooms['Forest Palace - 12']['event'] = 2
                if rooms["Forest Palace - 10"]['chest'] == "CLOSED":
                    rooms['Forest Palace - 10']['map'] = vcastle_10_map3
                    rooms['Forest Palace - 10']['EXPLORE'] = line5131c 
                else:
                    rooms['Forest Palace - 10']['map'] = vcastle_10_map4
                    rooms['Forest Palace - 10']['EXPLORE'] = line5131d
                rooms['Forest Palace - 12']['map'] = vcastle_12_map3
                break
            elif playerInput in negRes or playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5140d, typingActive) 
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input PULL or LEAVE.', typingActive)

    else:
        print_slow(line5140, typingActive) 
        rooms['Forest Palace - 12']['event'] = 1
        rooms['Forest Palace - 12']['intro'] = line5138b
        rooms['Forest Palace - 12']['EXPLORE'] = line5139b
        rooms['Forest Palace - 12']['map'] = vcastle_12_map2

    
def vamp_13_examine(p1, rooms, typingActive, SoundsOn):
        def vamp_13_update(rooms):
            if rooms['Forest Palace - 13']['event'] == 0:
               rooms['Forest Palace - 13']['event'] = 1
            else:
               pass
        in_Event = 0
        print_slow(line5143, typingActive)
        while in_Event == 0:    
            print_slow("\nContinue reading? (YES or NO)\n", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                if rooms['Forest Palace - 13']['event2'] == 0:
                    print_slow(line5143b, typingActive)
                    rooms['Forest Palace - 13']['event2'] = 1
                    vamp_13_update(rooms)
                    continue
                if rooms['Forest Palace - 13']['event2'] == 1: 
                    print_slow(line5143c, typingActive)
                    rooms['Forest Palace - 13']['event2'] = 2
                    vamp_13_update(rooms)
                    continue
                if rooms['Forest Palace - 13']['event2'] == 2:
                    print_slow(line5143d, typingActive)
                    rooms['Forest Palace - 13']['event2'] = 0
                    vamp_13_update(rooms)
                    continue
            elif playerInput in negRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow("You decide not to continue reading.\n", typingActive)
                in_Event = 1
                continue
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input YES or NO.\n', typingActive)
        while in_Event == 1:
            if rooms['Forest Palace - 13']['event'] in [0, 2]:
               break
            elif rooms['Forest Palace - 13']['event'] == 1:
               print_slow(line5143e, typingActive)
               print_slow(line5143f, typingActive)
               p1.inventory.append('LIBRARY NOTE')
               rooms['Forest Palace - 13']['event'] = 2
               break


def vamp_14_examine(p1, rooms, typingActive, SoundsOn):
   if rooms['Forest Palace - 14']['event'] == 2:
        print_slow(line5147g, typingActive)
   elif rooms['Forest Palace - 14']['event'] == 1:
        print_slow(line5147f, typingActive)
        print_slow(line5147b, typingActive)
   else:
        print_slow(line5147, typingActive)
        print_slow(line5147b, typingActive)
        while True:
            print_slow(line5147c, typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes :
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5147d, typingActive)
                p1.inventory.append('EMERALD GEMSTONE')
                rooms['Forest Palace - 14']['event'] = 1
                break
            elif playerInput in negRes :
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5147e, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input YES or NO.', typingActive)
        

def vamp_15_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Forest Palace - 15']['event'] == 1:
          print_slow(line5150b, typingActive)
          return
    else:
          print_slow(line5150, typingActive)
          rooms['Forest Palace - 15']['event'] = 1
          rooms['Forest Palace - 15']['EXPLORE'] = line5149b
          rooms['Forest Palace - 15']['map'] = vcastle_15_map2
          p1.inventory.append("SMELDARS BANE")


def vamp_16_examine(p1, rooms, typingActive, SoundsOn):
    cRoom = 'Forest Palace - 16'
    vamp_statue_update(cRoom, rooms, typingActive, SoundsOn)


def vamp_17_examine(p1, rooms, typingActive, SoundsOn):
    cRoom = 'Forest Palace - 17'
    vamp_statue_update(cRoom, rooms, typingActive, SoundsOn)


def vamp_18_examine(p1, rooms, typingActive, SoundsOn):
    cRoom = 'Forest Palace - 18'
    vamp_statue_update(cRoom, rooms, typingActive, SoundsOn)


def vamp_19_examine(p1, rooms, typingActive, SoundsOn):
    cRoom = 'Forest Palace - 19'
    vamp_statue_update(cRoom, rooms, typingActive, SoundsOn)


def vamp_queen_examine(p1, rooms, typingActive, SoundsOn):
    if rooms["Forest Palace - Queen's Chamber"]['event'] == 0:
        print_slow(line5125, typingActive)
        while True:
            print_slow("Do you want to try opening it? (YES or NO)\n", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes :
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5125b, typingActive)
                foe = rooms["Queen's Chamber"]['foe']
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms["Forest Palace - Queen's Chamber"]['event'] = 1
                rooms["Forest Palace - Queen's Chamber"]['EXPLORE'] = line5124b
                rooms['Forest Palace - 5']['intro'] = line5112b
                rooms['Forest Palace - 5']['EXPLORE'] = line5113b
                rooms['Forest Palace - 5']['WEST'] = 'Forest Palace - 8'
                rooms['Forest Palace - 5']['map'] = vcastle_5_map2
                rooms['Forest Palace - 5']['event'] = 1
                print_slow(line5125c, typingActive)
                break
            elif playerInput in negRes :
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow("Feeling a suspicion of what may lie inside, you decide to back away from the coffin.\n", typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input YES or NO.', typingActive)
    else:
        print_slow("The Vampire Queen has already been defeated.", typingActive)


def vamp_lord_examine(p1, rooms, typingActive, SoundsOn):
    if rooms["Forest Palace - Lord's Chamber"]['event'] == 2:
        print_slow(line5165b, typingActive)
    else:
        p_Input = "EXAMINE"
        vamp_lord_update(p1, p_Input, typingActive, SoundsOn)


def thicket_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Dense Thicket']['event'] == 1:
        print_slow(line2507d, typingActive)
    elif rooms['Dense Thicket']['event'] == 0 and 'SHARP AXE' in p1.inventory:
        print_slow(line2507, typingActive)
        rooms['Dense Thicket']['event'] = 1
        rooms['Dense Thicket']['intro'] = line2502
        rooms['Dense Thicket']['EXPLORE'] = line2504
    elif rooms['Dense Thicket']['event'] == 0 and 'AXE' in p1.inventory:
        print_slow(line2507c, typingActive)
    else:
        print_slow(line2505, typingActive)
    
    
def tower1_examine(p1, rooms, typingActive, SoundsOn): 

    warlockKey_List = ["GOBLIN'S WARLOCK KEY","OGRE'S WARLOCK KEY", "ORC'S WARLOCK KEY", "VAMPIRE'S WARLOCK KEY"]

    def show_wKey_list(i):
        wKey_Inventory = []
        for item in p1.inventory:
            if item in warlockKey_List:
                wKey_Inventory.append(item)
        for i in wKey_Inventory:
            wKey_Inventory.index(i,0,3)
            print(str(wKey_Inventory.index(i,0,3)+1) + ": " + i + "\n")

    
    def tower1_update(rooms):
        if rooms['Smeldars Tower - 1']['event2'] == 1:
              rooms['Smeldars Tower - 1']['EXPLORE'] = line5204b
        if rooms['Smeldars Tower - 1']['event2'] == 2: 
              rooms['Smeldars Tower - 1']['EXPLORE'] = line5204c
        if rooms['Smeldars Tower - 1']['event2'] == 3:
                rooms['Smeldars Tower - 1']['EXPLORE'] = line5204d
        if rooms['Smeldars Tower - 1']['event2'] == 4:
              rooms['Smeldars Tower - 1']['EXPLORE'] = line5204e    
        else:
           pass

    if rooms['Smeldars Tower - 1']['event'] == 2:
        print_slow(line5206b, typingActive)
        return
    if rooms['Smeldars Tower - 1']['event'] == 0:
        print_slow(line5205, typingActive)

    if rooms['Smeldars Tower - 1']['event'] == 1 and any(item in p1.inventory for item in warlockKey_List) == False:
        if rooms['Smeldars Tower - 1']['event2'] != 3:
            print_slow(line5206d, typingActive)
        return
    if any(item in p1.inventory for item in warlockKey_List):
        i = p1.inventory
        print_slow(line5205b, typingActive)

        while True:
            if any(item in p1.inventory for item in warlockKey_List) == False:
                if rooms['Smeldars Tower - 1']['event2'] != 3:
                    print_slow(line5206d, typingActive)
                break
            print_slow(f'There are {4 - rooms["Smeldars Tower - 1"]["event2"]} empty slots remaining.', typingActive)
            print_slow("\nYour current inventory of warlock keys:\n", typingActive)
            show_wKey_list(i)
            print_slow("\nWhich warlock key would you like to place into the door? (Input the name of the warlock key you wish to place or BACK to cancel)\n", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in p1.inventory and playerInput in warlockKey_List:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"You place the {playerInput} into the keyhole.\n", typingActive)
                p1.inventory.remove(playerInput)
                rooms['Smeldars Tower - 1']['event'] = 1
                rooms['Smeldars Tower - 1']['event2'] += 1
            elif playerInput in backRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line5205c, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input the name of the key you wish to place or BACK to cancel.\n', typingActive)

    if rooms['Smeldars Tower - 1']['event2'] == 4:
        print_slow(line5206, typingActive)
        rooms['Smeldars Tower - 1']['NORTH'] = 'Smeldars Tower - 2'
        rooms['Smeldars Tower - 2']['event'] = 2
        rooms['Smeldars Tower - 2']['map'] = smeldarstower1_map2


def tower2_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 2']['event'] == 1:
        print_slow(line5209f, typingActive)
    else:
        print_slow(line5209, typingActive)


def tower3_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 3']['event'] == 1:
        print_slow(line5212f, typingActive)
    elif rooms['Smeldars Tower - 3']['event'] == 0 and (p1.job == 'WIZARD' or p1.job == 'WITCH'):
        print_slow(line5212b, typingActive)
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in affRes :
            soundFile = str(SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            roll = random.randrange(0,7)
            if roll >= 2:
                print_slow(line5212c, typingActive)
                rooms['Smeldars Tower - 3']['event'] = 1
            else:
                print_slow(line5212e, typingActive)
                soundFile = str(combat.battle_sounds['MagicBolt'])
                play_sound_effect(soundFile, SoundsOn)
                rooms['Smeldars Tower - 3']['event'] = 1
                damage = random.randrange(p1.lvl, p1.lvl*3)
                p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
                combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
                if p1.HP <= 0:
                    return
        elif playerInput in negRes:
            soundFile = str(SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line5212d, typingActive)
    else:
        print_slow(line5212, typingActive)


def tower4_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 4']['event'] == 1:
        print_slow(line5215b, typingActive)
    else:
        print_slow(line5215, typingActive)
def tower7_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 7']['event'] == 1:
        print_slow(line5215b, typingActive)
    else:
        print_slow(line5215, typingActive)
def tower8_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 8']['event'] == 1:
        print_slow(line5215b, typingActive)
    else:
        print_slow(line5215, typingActive)


def tower5_examine(p1, rooms, typingActive, SoundsOn):
    playerInput = ""
    tower5_lock(p1, playerInput, rooms, typingActive, SoundsOn)


def tower6_examine(p1, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 6']['event'] == 1:
        print_slow(line5223e, typingActive)
    else:
        if rooms['Smeldars Tower - 6']['event'] == 0 and (p1.job == "WARRIOR" or "HAMMER" in p1.inventory):
            print_slow(line5223b, typingActive)
            while True:
                playerInput = input().upper().strip()
                print('\n')
                if playerInput in affRes or playerInput in atkRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5223c, typingActive)
                    rooms['Smeldars Tower - 6']['event'] = 1
                    rooms['Smeldars Tower - 6']['EXPLORE'] = line5222b
                    rooms['Smeldars Tower - 6']['NORTH'] = 'Smeldars Tower - Hidden Room'
                    rooms['Smeldars Tower - 6']['map'] = smeldarstower6_map2
                elif playerInput in negRes or playerInput in backRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5223d, typingActive)
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('Invalid input. Input YES or NO.', typingActive)
        else:
            print_slow(line5223, typingActive)


def hill_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Rocky Hill']['SOUTH'] == 'LOCKED':
    print_slow(line812, typingActive)


def lake_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Echobo Lake']['EAST'] == 'LOCKED':
    print_slow(line1410, typingActive)


def cave_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if 'Bear' in rooms['Bear Cave']['boss']:
      print_slow(line914, typingActive)
      
  elif rooms['Bear Cave']['EAST'] == 'LOCKED' and "LANTERN" in p1.inventory:
      print_slow(line915, typingActive)
      rooms['Bear Cave']['EAST'] = 'Rocky Cave 1'
      
  elif rooms['Bear Cave']['EAST'] == 'LOCKED' and (p1.job == 'WIZARD' or p1.job == 'WITCH'):
      print_slow(line915b, typingActive)
      rooms['Bear Cave']['EAST'] = 'Rocky Cave 1'
      
  elif (playerInput == 'EAST' and rooms['Bear Cave']['EAST']
        == 'LOCKED') and "LANTERN" not in p1.inventory:
      print_slow(line909, typingActive)
            

def cave4_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Rocky Cave 4']['EAST'] == 'LOCKED':
      print_slow(line943, typingActive)


def waterfallcave2_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Waterfall Cave 2']['SOUTH'] == 'LOCKED':
      print_slow(line1319, typingActive)


def deepwoodsfork_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Deep Woods - Fork']['EAST'] == 'LOCKED':
      print_slow(line4711b, typingActive)
        

def deepwoodswest_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Deep Woods - WEST']['NORTH'] == 'LOCKED':
    print_slow(line4718b, typingActive)


def orc1_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Orc Fortress 1']['NORTH'] == 'LOCKED':
    print_slow(line4917, typingActive)


def mistywoodsCentral_lock(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms['Misty Woods - Central']['SOUTH'] == 'LOCKED':
    if key_items['LANTERN']['BF'] == 0 or 'LANTERN' not in p1.inventory:
      print_slow("You try to walk through the fog, but it is much too thick and you find that you quickly lose your barrings.\n", typingActive)
      hit = random.randrange(0,4)
      if hit == 0:
        foe = random.choice(rooms['Misty Woods - Central']['enemy_spawn_set'])
        print_slow(f"While trying to find your way back to the path you are assualted by a {foe.name}!\n", typingActive)
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        print_slow(f"You defeat the {foe.name} and find your way back to the main path.\n", typingActive)
      else:
        print_slow(f"You stumble through the woods and manage to find your way back to the main path.\n", typingActive)
    else:
      print_slow(f"You wave the DIVINE FLAME LANTERN in front of you. The light of the blue flames pierces the veil of fog, dissipating the mist and clearing the path to the SOUTH!\n", typingActive)
      rooms['Misty Woods - Central']['SOUTH'] = 'Misty Woods - SOUTH'
      rooms['Misty Woods - Central']['intro'] = line5005b
      rooms['Misty Woods - Central']['EXPLORE'] = line5007
  else:
    pass
        

def vamp_lock1(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms["Forest Palace - 6"]['NORTH'] == 'LOCKED':
    print_slow("The door to the NORTH is locked tight; it seems to be some complex mechanism.\n", typingActive)


def vamp_lock2(p1, playerInput, rooms, typingActive, SoundsOn):
    if rooms["Forest Palace - 5"]['WEST'] == 'LOCKED':
        print_slow("The way WEST is blocked; the iron gate is sealed tight.\n", typingActive)
    else:
        pass


def vamp_lock3(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms["Forest Palace - 9"]['NORTH'] == 'LOCKED':
    print_slow("The door NORTH is blocked; the door is sealed by some dark magic.\n", typingActive)
  else:
    pass


def vamp_lock4(p1, playerInput, rooms, typingActive, SoundsOn):
  if rooms["Forest Palace - 10"]['EAST'] == 'LOCKED':
    print_slow("You cannot go to the EAST. That wall looks rather unusual however...\n", typingActive)
  else:
    pass
  

def vamp_lock5(p1, playerInput, rooms, typingActive, SoundsOn):
  pass


def thicket_lock(p1, playerInput, rooms, typingActive, SoundsOn):
    if any(item in p1.inventory for item in ['AXE','SHARP AXE']):
        print_slow(line2509, typingActive)
    else:
        print_slow(line2508, typingActive)


def tower1_lock(p1, playerInput, rooms, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 1']['NORTH'] == 'LOCKED':
        print_slow(line5204f, typingActive)


def tower5_lock(p1, playerInput, rooms, typingActive, SoundsOn):

    if rooms['Smeldars Tower - 5']['event'] == 2:
        print_slow(line5219b, typingActive)

    if rooms['Smeldars Tower - 5']['EAST'] == "LOCKED":
        print_slow(line5219, typingActive)
        if p1.job == 'THIEF':
            while True:
                print_slow(line5219c, typingActive)
                playerInput = input().upper().strip()
                print('\n')
                if playerInput in affRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219d, typingActive)
                    rooms['Smeldars Tower - 5']['EAST'] = 'Smeldars Tower - 6'
                    rooms['Smeldars Tower - 5']['event'] = 2
                    break
                elif playerInput in negRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219e, typingActive)
                    break
                elif playerInput in openRes or playerInput in forceRes:
                    print_slow(line5219f, typingActive)
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('Invalid input. Input YES or NO.', typingActive)

        elif "SKELETON KEY" in p1.inventory:
            while True:
                print_slow(line5219g, typingActive)
                playerInput = input().upper().strip()
                print('\n')
                if playerInput in affRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219h, typingActive)
                    rooms['Smeldars Tower - 5']['EAST'] = 'Smeldars Tower - 6'
                    rooms['Smeldars Tower - 5']['event'] = 2
                    break
                elif playerInput in negRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219i, typingActive)
                    break
                elif playerInput in openRes or playerInput in forceRes:
                    print_slow(line5219f, typingActive)    
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('Invalid input. Input YES or NO.', typingActive)

        elif "TOWER KEY" in p1.inventory:
            while True:    
                print_slow(line5219j, typingActive)
                playerInput = input().upper().strip()
                print('\n')
                if playerInput in affRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219k, typingActive)
                    rooms['Smeldars Tower - 5']['EAST'] = 'Smeldars Tower - 6'
                    rooms['Smeldars Tower - 5']['event'] = 2
                    break
                elif playerInput in negRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line5219l, typingActive)
                    break
                elif playerInput in openRes or playerInput in forceRes:
                    print_slow(line5219f, typingActive)    
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('Invalid input. Input YES or NO.', typingActive)     

        else:
            print_slow(line5220, typingActive)
            flag = 1
            flag2 = 0
            while flag == 1:
                if flag2 == 0:
                    playerInput = input().upper().strip()
                    print('\n')
                elif flag2 == 1:
                    playerInput = "YES"
                if playerInput in affRes or playerInput in searchRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow("You start looking around the room...", typingActive)
                    roll = random.randrange(0,9)
                    if roll >= 6:
                        print_slow(line5220b, typingActive)
                        p1.inventory.append('TOWER KEY')
                        rooms['Smeldars Tower - 5']['event'] = 1
                        flag = 0
                        break
                    else:    
                        foe = random.choice(rooms['Smeldars Tower - 5']['enemy_spawn_set'])
                        print_slow(f"While searching you stumble upon a {foe.name}!", typingActive)
                        combat.standard_battle(p1, foe, typingActive, SoundsOn)
                        if p1.HP <= 0:
                            break
                        print_slow(line5220c, typingActive)
                        while True:
                            if playerInput in affRes:
                                soundFile = str(SFX_Library['Select'])
                                play_sound_effect(soundFile, SoundsOn)
                                flag2 = 1
                                break
                            elif playerInput in negRes:
                                soundFile = str(SFX_Library['Back'])
                                play_sound_effect(soundFile, SoundsOn)
                                flag = 0
                                print_slow(line5220d, typingActive)
                                break
                            else:
                                soundFile = str(SFX_Library['Error'])
                                play_sound_effect(soundFile, SoundsOn)
                                print_slow('Invalid input. Input YES or NO.', typingActive)

                elif playerInput in negRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    flag = 0
                    print_slow(line5220d, typingActive) 
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('Invalid input. Input YES or NO.', typingActive)     


def tower4_lock(p1, playerInput, rooms, typingActive, SoundsOn):
    
    if playerInput == 'NORTH':
        if rooms['Smeldars Tower - 4']['event'] == 0:
            print_slow(line5216c, typingActive)
            rooms['Smeldars Tower - 4']['NORTH'] = 'Smeldars Tower - 5'
            rooms['Smeldars Tower - 4']['event'] = 1
            rooms['Smeldars Tower - 4']['map'] = smeldarstower4_map2
            rooms['Smeldars Tower - 4']['EXPLORE'] = line5214b
        else:
            print("ERROR: This door should already be unlocked.")
    
    if playerInput == 'EAST' and rooms['Smeldars Tower - 4']['event2'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 4']['event2'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'EAST' and rooms['Smeldars Tower - 4']['event2'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)

    elif playerInput == 'WEST' and rooms['Smeldars Tower - 4']['event3'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 4']['event3'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'WEST' and rooms['Smeldars Tower - 4']['event3'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)
           

def tower7_lock(p1, playerInput, rooms, typingActive, SoundsOn):
    
    if playerInput == 'NORTH':
        if rooms['Smeldars Tower - 7']['event'] == 0:
            print_slow(line5216c, typingActive)
            rooms['Smeldars Tower - 7']['EAST'] = 'Smeldars Tower - 8'
            rooms['Smeldars Tower - 7']['event'] = 1
            rooms['Smeldars Tower - 7']['map'] = smeldarstower7_map2
            rooms['Smeldars Tower - 7']['EXPLORE'] = line5214b
        else:
            print("ERROR: This door should already be unlocked.")

    if playerInput == 'EAST' and rooms['Smeldars Tower - 7']['event2'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 7']['event2'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'NORTH' and rooms['Smeldars Tower - 7']['event2'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)

    elif playerInput == 'WEST' and rooms['Smeldars Tower - 7']['event3'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 7']['event3'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'WEST' and rooms['Smeldars Tower - 7']['event3'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)
  

def tower8_lock(p1, playerInput, rooms, typingActive, SoundsOn):
    
    if playerInput == 'NORTH':
        if rooms['Smeldars Tower - 8']['event'] == 0:
            print_slow(line5216c, typingActive)
            rooms['Smeldars Tower - 8']['NORTH'] = 'Smeldars Tower - 9'
            rooms['Smeldars Tower - 8']['event'] = 1
            rooms['Smeldars Tower - 8']['map'] = smeldarstower8_map2
            rooms['Smeldars Tower - 8']['EXPLORE'] = line5214b
        else:
            print("ERROR: This door should already be unlocked.")

    elif playerInput == 'EAST' and rooms['Smeldars Tower - 8']['event2'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 8']['event2'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'EAST' and rooms['Smeldars Tower - 8']['event2'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)

    elif playerInput == 'SOUTH' and rooms['Smeldars Tower - 8']['event3'] == 0:
        print_slow(line5216, typingActive)
        foe = p95
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower - 8']['event3'] = 1
        print_slow(line5216b, typingActive)
    elif playerInput == 'SOUTH' and rooms['Smeldars Tower - 8']['event3'] == 1:
        print_slow(f"You check on the {playerInput} wall again. Still no passageway. Better check a different direction.", typingActive)
  

def cave4_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    if 'Hobgoblin Gang' in rooms['Rocky Cave 4']['boss']:
        print_slow(line935, typingActive)
        foe = rooms['Rocky Cave 4']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        p1.inventory.append('GOBLIN CHOPPER')
        rooms['Rocky Cave 4']['boss'].remove('Hobgoblin Gang')
        rooms['Rocky Cave 4']['spawn_rate'] = 8
        print_slow(line936, typingActive)


def cave5_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    if 'Goblin Queen' in rooms["Queen's Chamber"]['boss']:
        print_slow(line947, typingActive)
        foe = rooms["Queen's Chamber"]['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms["Queen's Chamber"]['boss'].remove('Goblin Queen')
        rooms['Pinerift Forest - EAST']['event'] = 1
        rooms['Royal Castle']['event2'].append('A')
        p1.inventory.append("GOBLIN'S WARLOCK KEY")
        time.sleep(0.5)
        soundFile = str(SFX_Library['GotLegendary'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line949, typingActive)
        p1.keys += 1
        rot_update(p1)
        if rooms["Smith's Workshop"]['event'] == 1:
          p1.inventory.append('GOBLIN FINGER')
          print_slow(line951, typingActive)


def foresteast_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    if rooms['Pinerift Forest - EAST']['event'] == 1:
        ambush = random.randrange(0, 10)
        if ambush >= 7:
            foe = p67
            print_slow(line707, typingActive)
            combat.standard_battle(p1, foe, typingActive, SoundsOn)
            if p1.HP <= 0:
                return
            print_slow(line708, typingActive)
            rooms['Pinerift Forest - EAST']['event'] = 2
            rooms['Pinerift Forest - EAST']['EXPLORE'] = line706
            rooms['Pinerift Forest']['EXPLORE'] = line703


def hive_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    global enemy_spawn3
    global enemy_spawn9
    if 'Giant Bee Queen' in rooms['Bee Hive']['boss']:
        print_slow(line2101, typingActive)
        foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        print_slow(line2101b, typingActive)
        foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        print_slow(line2101b, typingActive)
        foe = random.choice(rooms['Bee Hive']['enemy_spawn_set'])
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        print_slow(line2102, typingActive)
        foe = rooms['Bee Hive']['foe']
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Bee Hive']['boss'].remove('Giant Bee Queen')
        rooms['Bee Hive']['spawn_rate'] = 0
        p1.inventory.append('ROYAL JELLY')
        enemy_spawn3.remove(p14)
        enemy_spawn9.remove(p14)
        enemy_spawn3.append(p25)
        enemy_spawn9.append(p25)
        p1.RJ += 10
        print_slow(line2103, typingActive)


def faeeast_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    global stolen_gp

    if 'Rogue Gang' in rooms['Fae Woods - EAST']['boss']:
        print_slow(line3903, typingActive)
        while True:
            playerInput = input().upper().strip()
            print('\n')
            if playerInput == "FIGHT" or playerInput in atkRes:
                print_slow(line3905, typingActive)
                foe = p52
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                rooms['Fae Woods - EAST']['boss'].remove('Rogue Gang')
                rooms['Fae Woods - Camp']['boss'].remove('Rogue Gang')
                p1.GP += 250
                print_slow(line3906, typingActive)
                print_slow(f'{p1.name} adds the 250 GP to their wallet. {p1.name} has {p1.GP} GP.\n', typingActive)
                break
            elif playerInput == "GIVE":
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line3904, typingActive)
                rooms['Fae Woods - EAST']['boss'].remove('Rogue Gang')
                stolen_gp = p1.GP
                p1.GP -= p1.GP
                print_slow(f'{p1.name} gives up all their gold. {p1.name} has {p1.GP} GP.', typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Input GIVE or FIGHT.\n', typingActive)

def faecamp_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    global stolen_gp

    if 'Rogue Gang' in rooms['Fae Woods - Camp']['boss']:
        print_slow(line4005, typingActive)
        foe = p52
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Fae Woods - Camp']['boss'].remove('Rogue Gang')
        p1.GP += stolen_gp
        print_slow(line4006, typingActive)
        print_slow(f'{p1.name} adds their GP back to their wallet. {p1.name} has {p1.GP} GP.\n', typingActive)


def dragon_boss_ambush(p1, playerInput, typingActive, SoundsOn):
  if "Dragon King, Tanninim" in rooms['Drake Mountains Summit']['boss']:
      print_slow(line4615, typingActive)
      foe = p73
      combat.standard_battle(p1, foe, typingActive, SoundsOn)
      if p1.HP <= 0:
        return
      rooms['Drake Mountains Summit']['boss'].remove("Dragon King, Tanninim")
      rooms['Drake Mountains Summit']['intro'] = line4613
      rooms['Drake Mountains 3']['EXPLORE'] = line4607b
      p1.inventory.append('DRAGON HEART')
      print_slow(line4616, typingActive)
      print_slow(f'{p1.name} adds the DRAGON HEART to their inventory!\n', typingActive)
  else:
      print_slow("You speak the Dragon Lords name, but nothing happens.", typingActive)


def mistnorth_boss_ambush(p1, playerInput, typingActive, SoundsOn):
      ambush = random.randrange(0, 10)
      if ambush >= 7:
          foe = p67
          print_slow(line707, typingActive)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
            return
          print_slow(line708, typingActive)
          rooms['Pinerift Forest - EAST']['event'] = 2
          rooms['Pinerift Forest - EAST']['EXPLORE'] = line706
          rooms['Pinerift Forest']['EXPLORE'] = line703


def orckeep_boss_ambush(p1, playerInput, typingActive, SoundsOn):
    if "Orc King, Kargath" in rooms['Orc Keep']['boss']:
        print_slow(line4974, typingActive)
        foe = p84
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Orc Keep']['boss'].remove("Orc King, Kargath")
        rooms['Royal Castle']['event2'].append('C')
        p1.inventory.append("ORC'S WARLOCK KEY")
        print_slow(line4975, typingActive)
        time.sleep(0.5)
        soundFile = str(SFX_Library['GotLegendary'])
        play_sound_effect(soundFile, SoundsOn)  
        print_slow(f"{p1.name} adds the ORC'S WARLOCK KEY to their inventory!\n", typingActive)
        p1.keys += 1
        rot_update(p1)


def tower_boss0_ambush(p1, playerInput, typingActive, SoundsOn):
    if 'Dragon' in rooms['Smeldars Tower']['boss']:
        print_slow(line5201, typingActive)
        foe = p72b
        combat.standard_battle(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
            return
        rooms['Smeldars Tower']['boss'].remove('Dragon')
        print_slow(line5202, typingActive)
    else:
        pass    


def tower_boss1_ambush(p1, playerInput, typingActive, SoundsOn):
   print_slow(line5229, typingActive)
   print_slow(line5230, typingActive)
   print_slow(line5231, typingActive)
   while True:
       playerInput = input().upper().strip()
       if playerInput in affRes:
           print_slow(line5233, typingActive)
           p1.HP = 0
           combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
           return
       else:
           print_slow(line5232, typingActive)
           foe = p666
           combat.standard_battle(p1, foe, typingActive, SoundsOn)
           if p1.HP <= 0:
               break
           if foe.HP <= 0:
               p1.win = True
               print_slow(line5234 + f'{p1.name}' + line5234b, typingActive)
               print_slow(line5235, typingActive)
               time.sleep(3)
               print_slow(line001, typingActive)
               time.sleep(2)
               print_slow(line5236, typingActive)
               time.sleep(2)
               print_slow(line5237, typingActive)
               print_slow(f'\nName: {p1.name}\nClass: {p1.job}\nLevel: {p1.lvl}\nMovements: {p1.roomMoves}\nEnemies Defeated: {p1.enemiesKilled}', typingActive)
               time.sleep(2)
               print_slow(line5238, typingActive)
               time.sleep(5)
               return


def orc1_ambush(p1, playerInput, current_room, typingActive, SoundsOn): #modify text for this function to make more sense if player flees from fight. Maybe change so player cant sneak after?
   
   def orc1_ambush_update(current_room, foe):
    fortress_groupA = ['Outer Fortress', 'Orc Fortress 1', 'Orc Fortress 3']
    fortress_groupB = ['Orc Fortress 2', 'Orc Fortress 4', 'Orc Fortress 5']
    if foe.HP <= 0:
        rooms[current_room]['event'] = 1
        rooms[current_room]['ambush_pass'] = 1
        if current_room in fortress_groupA:
            rooms[current_room]['enemy_spawn_set'] = enemy_spawn28
        elif current_room in fortress_groupB:
            rooms[current_room]['enemy_spawn_set'] = enemy_spawn29
   
   
    if rooms[current_room]['event'] == 0:
        rooms[current_room]['ambush_pass'] = 0
        while True:
            print_slow("You've not yet been discovered by the patroling Orcs in this area... You could try to SNEAK by, or ATTACK the Orcs pre-emptively?", typingActive)
            playerInput2 = input().upper().strip()
            print('\n')
            if playerInput2 == 'SNEAK':
                if p1.job == 'THIEF':
                    hit = 5
                else:
                    hit = random.randrange(1,6)
                while True:
                    if hit >= 3 :
                        print_slow(f"You successfully sneak past the Orcs and make your way {playerInput}!\n", typingActive)
                        rooms[current_room]['ambush_pass'] = 1
                        break
                    else:
                        print_slow(f"You attempt to sneak sneak past the Orcs and make your way {playerInput}, but are caught by an Orc Guard! \n", typingActive)
                        foe = p78
                        combat.standard_battle(p1, foe, typingActive, SoundsOn)
                        if p1.HP <= 0:
                            break
                        hit = random.randrange(1,5)
                        if hit >= 2:
                            print_slow(f"You defeat the Orc Guard, but not before he was able to signal that there is an intruder. Now the Orcs in this area will be on high alert for you... \n", typingActive)
                            rooms[current_room]['spawn_rate'] += 5 + rooms['Orc Fortress 5']['spawn_modifier']
                            orc1_ambush_update(current_room, foe)
                            break
                        else:
                            print_slow(f"You defeat the Orc Guard, but another quickly rushes to stop you!\n", typingActive)
                            foe = p78
                            combat.standard_battle(p1, foe, typingActive, SoundsOn)
                            if p1.HP <= 0:
                                break
                            print_slow(f"The Orc Guards have been defeated, but your presence has been signaled to the other Orcs. Now the Orcs in this area will be on high alert for you... \n", typingActive)
                            rooms[current_room]['spawn_rate'] += 5 + rooms['Orc Fortress 5']['spawn_modifier']
                            orc1_ambush_update(current_room, foe)
                            break
                break
            elif playerInput2 in atkRes:
                hit = random.randrange(1,6)
                if hit >= 2:
                    print_slow(f"You attack a patroling Orc Guard and get the jump on him!\n", typingActive)
                    foe = p78
                    if hit >= 4:
                        dam = random.randrange((p1.ATK // 4), p1.ATK) 
                        damage = min(max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)),0), 20)
                        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
                        print_slow(f"The {foe.name} really didnt see that coming! {p1.name} manages to get a pre-emptive strike for {damage}!\n", typingActive)
                    combat.standard_battle(p1, foe, typingActive, SoundsOn)
                    if p1.HP <= 0:
                        break
                    print_slow(f"You defeat the {foe.name}, but your presence will soon be known to the other Orcs. Sneaking certainly won't be possible here, and the Orcs may be on alert... \n", typingActive)
                    rooms[current_room]['spawn_rate'] += 3 + rooms['Orc Fortress 5']['spawn_modifier']
                    orc1_ambush_update(current_room, foe)
                    break
                else:
                    print_slow(f"You try to attack a patroling {foe.name} but fail and they are alerted to your presence!\n", typingActive)
                    foe = p78
                    combat.standard_battle(p1, foe, typingActive, SoundsOn)
                    if p1.HP <= 0:
                        break
                    print_slow(f"You defeat the {foe.name}, but not before he was able to signal that there is an intruder. Now the Orcs in this area will be on high alert for you... \n", typingActive)
                    rooms[current_room]['spawn_rate'] += 4 + rooms['Orc Fortress 5']['spawn_modifier']
                    orc1_ambush_update(current_room, foe)
                    break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid input. Input SNEAK or ATTACK.', typingActive)
    else:
        pass


def tower3_ambush(p1, playerInput, current_room, typingActive, SoundsOn):
    if rooms['Smeldars Tower - 3']['event'] == 1 or "CRYSTAL NECKLACE" in p1.accs1 or "CRYSTAL NECKLACE" in p1.accs2:
        pass
    else:
        roll = random.randrange(0, 10)
        if roll >= 7:
            print_slow(line5212h, typingActive)
        else:
            print_slow(line5212g, typingActive)
            damage = random.randrange(p1.lvl, p1.lvl*3)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            print_slow(f'{p1.name} takes {damage} damage from the magical blast!\n', typingActive)
            combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
            if p1.HP <= 0:
                return


def cityshop_speak(p1, rooms, current_room, typingActive, SoundsOn):
    #default lines for shopkeep
    if rooms['Capital City - Shop']['speech'] == 0:
        print_slow(line306, typingActive)
        rooms['Capital City - Shop']['speech'] = 1

    elif rooms['Capital City - Shop']['speech'] == 1:  
        #shop quest completed
        if rooms['Capital City - Shop']['event'] == 3:
            print_slow(line306c, typingActive)
            rooms['Capital City - Shop']['speech'] = 0

        #shop quest completion
        if rooms['Capital City - Shop']['event'] == 2 and p1.MonP >= 5:
            print_slow(""""I can tell you've got those MONSTER GUTS! Quick, pass them here before anyone else walks in!"\nThe Shop Keep frantically grabs the MONSTER GUTS and slips them into a jar tucked away under the counter.\n"Now I suppose I should hold up my end of the deal. I'll discount that SPECIAL FEED just for you." """, typingActive)
            p1.MonP -= 5
            rooms['Capital City - Shop']['event'] = 3
            key_items['SPECIAL FEED']['price'] = key_items['SPECIAL FEED']['price'] // 2
            print_slow(f'The price of SPECIAL FEED has been reduced to [{key_items["SPECIAL FEED"]["price"]}GP]!\n', typingActive)
            rooms['Farm House']['speech'] = 0
        #shop quest + farm incomplete
        if rooms['Capital City - Shop']['event'] == 2 and p1.MonP < 5:
            print_slow(f"""\n"You don't have those MONSTER GUTS yet, do you? Well if you change your mind about finding them, you know where to find me..."\n""", typingActive)
        #farmer quest active, shop quest start
        if 'SPECIAL FEED' in rooms['Capital City - Shop']['items'] and rooms['Capital City - Shop']['event'] == 1:
            print_slow(f"""\n"Hmm? Looking for SPECIAL FEED? We have some for sale, sure. I'll tell you what, you look like a pretty capable adventurer. Let's make a deal; If you can find me those 5 MONSTER GUTS I will give you a big discount on that SPECIAL FEED. Just be sure not to tell anyone I want them...What do I need them for? Shh, don\'t ask."\n""", typingActive)
            rooms['Capital City - Shop']['event'] = 2
            if 'CRAFTING POUCH' not in p1.inventory:
                print_slow(f"""\n"Oh, before you go, take this CRAFTING POUCH. You'll need it to store those MONSTER GUTS. On the house!"\n""", typingActive)
                rooms['Capital City - Shop']['items'].remove('CRAFTING POUCH')
                p1.inventory.append('CRAFTING POUCH')
                print_slow(f'{p1.name} received a CRAFTING POUCH! This will help you carry crafting materials you find on your adventures.\n', typingActive)
        #Farmer quest not active
        else:
            print_slow(line306b, typingActive)
            rooms['Capital City - Shop']['speech'] = 0


def castle_speak(p1, rooms, current_room, typingActive, SoundsOn):

    lineA = line508
    lineB = line509
    lineC = line510
    lineD = line511




    def castle_speak_update():
        nonlocal lineA
        nonlocal lineB
        nonlocal lineC
        nonlocal lineD


        if 'A' in rooms['Royal Castle']['event2']:
            lineA = line508b
        if 'B' in rooms['Royal Castle']['event2']:
            lineB = line509b
        if 'C' in rooms['Royal Castle']['event2']:
            lineC = line510b
        if 'D' in rooms['Royal Castle']['event2']:
            lineD = line511b
        if all(item in smeldar_keys for item in p1.inventory):
            rooms['Royal Castle']['speech'] = 5


    castle_speak_update()
    if rooms['Royal Castle']['event'] == 0:
        print_slow(line505, typingActive)
        print_slow(line506, typingActive)
        rooms['Royal Castle']['event2'] += 1
        return
    
    if rooms['Royal Castle']['speech'] == 0:
        print_slow(line507, typingActive)
        rooms['Royal Castle']['speech'] += 1
        return
    elif rooms['Royal Castle']['speech'] == 1:
        print_slow(lineA, typingActive)
        rooms['Royal Castle']['speech'] += 1
        return
    elif rooms['Royal Castle']['speech'] == 2:
        print_slow(lineB, typingActive)
        rooms['Royal Castle']['speech'] += 1
        return
    elif rooms['Royal Castle']['speech'] == 3:
        print_slow(lineC, typingActive)
        rooms['Royal Castle']['speech'] += 1
        return
    elif rooms['Royal Castle']['speech'] == 4:
        print_slow(lineD, typingActive)
        rooms['Royal Castle']['speech'] = 0
        return
    elif rooms['Royal Castle']['speech'] == 5:
        print_slow(line512, typingActive)
        return  


def cityinn_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Capital City - Inn']['speech'] == 0:
        print_slow(line405, typingActive)
        rooms['Capital City - Inn']['speech'] = 1
    elif rooms['Capital City - Inn']['speech'] == 1:
        print_slow(line406, typingActive)
        rooms['Capital City - Inn']['speech'] = 0


def boat_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        if rooms['Boat House']['speech'] == 0:
            print_slow(line1504, typingActive)
            rooms['Boat House']['speech'] = 1
            break
        elif rooms['Boat House']['speech'] == 1 and 'SALMON' in p1.inventory:
            print_slow(line1506, typingActive)
            playerInput = (input().upper()).strip()
            print_slow("\n", typingActive)
            if playerInput == "GIVE":
                print_slow(line1508, typingActive)
                print_slow(f'{p1.name} was given a BUCKLER! This sturdy steel shield should help block damage.\n', typingActive)
                rooms['Boat House']['speech'] = 2
                rooms['Boat House']['EXPLORE'] = line1503
                p1.inventory.remove('SALMON')
                p1.inventory.append('BUCKLER')
                p1.stat_check(typingActive, SoundsOn)
                break
            elif playerInput == "KEEP":
                print_slow(line1507, typingActive)
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n')
        elif rooms['Boat House']['speech'] == 1 and 'SALMON' not in p1.inventory:
            print_slow(line1510, typingActive)
            break
        else:
            print_slow(line1509, typingActive)
            break


def shrine_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Mystic Shrine']['speech'] == 0:
        print_slow(line1105, typingActive)
        print_slow(line1106, typingActive)
        rooms['Mystic Shrine']['speech'] = 1
        rooms['Mystic Shrine']['EXPLORE'] = line1103
    elif rooms['Mystic Shrine'][
            'speech'] == 1 and 'PENDANT' in p1.inventory:
        print_slow(line1108, typingActive)
        print_slow(line1109, typingActive)
        print_slow(f"{p1.name} is given the Friar's MESSER. This sword is much better than the old RUSTY DAGGER you found in the trash before you started adventuring...\n", typingActive)
        rooms['Mystic Shrine']['EXPLORE'] = line1104
        p1.inventory.remove('PENDANT')
        p1.inventory.append('MESSER')
        p1.stat_check(typingActive, SoundsOn)
    elif rooms['Mystic Shrine']['speech'] == 1:
        print_slow(line1107, typingActive)


def villageinn_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Village Inn']['speech'] == 0:
        print_slow(line405b, typingActive)
        rooms['Village Inn']['speech'] = 1
    elif rooms['Village Inn']['speech'] == 1:
        print_slow(line406b, typingActive)
        rooms['Village Inn']['speech'] = 0


def smith_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if 'AXE' in p1.inventory and rooms["Smith's Workshop"]['event'] == 0:
      print_slow(line1906, typingActive)
      rooms["Smith's Workshop"]['event'] = 1
      if 'Goblin Queen' not in rooms["Queen's Chamber"]['boss']:
        print_slow(line1907b, typingActive)
        rooms["Smith's Workshop"]['event'] = 2
        p1.inventory.remove('AXE')
        p1.inventory.append('SHARP AXE')
    elif 'GOBLIN FINGER' not in p1.inventory and rooms["Smith's Workshop"]['event'] == 1:
      print_slow(line1906b, typingActive)
    elif 'GOBLIN FINGER' in p1.inventory and rooms["Smith's Workshop"]['event'] == 1:
      print_slow(line1907, typingActive)
      rooms["Smith's Workshop"]['event'] = 2
      p1.inventory.remove('GOBLIN FINGER')
      p1.inventory.remove('AXE')
      p1.inventory.append('SHARP AXE')
    elif 'STRANGE GREASE' in p1.inventory:
        print_slow(line1905, typingActive)
    else:
        print_slow(line1904, typingActive)


def farm_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        #quest start
        if rooms['Farm House']['speech'] == 0:
            print_slow(line2203, typingActive)
            rooms['Farm House']['speech'] = 1
        if rooms['Farm House']['speech'] == 1:
            playerInput = (input().upper()).strip()
            print("\n")
            #quest accepted
            if playerInput in affRes:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line2205, typingActive)
                print_slow(f'{p1.name} was given a 100GP. The Farmer expects you to use his money to buy his pig some special feed from the City\n', typingActive)
                p1.GP += 100
                rooms['Capital City - Shop']['event'] = 1
                rooms['Capital City - Shop']['items'].append('SPECIAL FEED')
                rooms['Farm House']['speech'] = 3
                break
            #quest rejected
            elif playerInput in negRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line2204, typingActive)
                rooms['Farm House']['speech'] = 2
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again. Please select YES or NO\n', typingActive)
        #2nd time requesting help
        if rooms['Farm House']['speech'] == 2:
            print_slow(line2204b, typingActive)
            rooms['Farm House']['speech'] = 1
        #quest completing
        if rooms['Farm House']['speech'] == 3:
            if 'SPECIAL FEED' in p1.inventory:
                p1.inventory.remove('SPECIAL FEED')
                p1.inventory.append('HAMMER')
                rooms['Farm House']['speech'] = 4
                rooms['Capital City - Shop']['event'] = 3
                print_slow(line2206, typingActive)
                print_slow(f'{p1.name} receives a HAMMER!\n', typingActive)
                break
            #quest in progress
            else:
                print_slow(line2207, typingActive)
                break
            #quest completed
        elif rooms['Farm House']['speech'] == 4:
            print_slow(line2208, typingActive)
            break


def witch_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        #introduction
        if rooms["Witch's Cabin"]['speech'] == 0:
            print_slow(line2403, typingActive)
            rooms["Witch's Cabin"]['speech'] = 1
            break
        #insufficient materials
        if rooms["Witch's Cabin"]['speech'] == 1 and (p1.PlantP <5 or p1.MonP <5 or p1.RareP <5 or p1.FaeDust <5):
            print_slow(line2404, typingActive)
            break
        #Crafting unlocked
        if rooms["Witch's Cabin"]['speech'] == 1 and p1.PlantP >=5 and p1.MonP >=5 and p1.RareP >=5 and p1.FaeDust >=5:
            print_slow(line2405, typingActive)
            p1.PlantP -= 5
            p1.MonP -= 5
            p1.RareP -= 5
            p1.FaeDust -= 5
            rooms["Witch's Cabin"]['speech'] = 2
            rooms["Witch's Cabin"]['crafting'] = 'ACTIVE'
            print_slow(line2410, typingActive)
            rooms["Witch's Cabin"]['event'] = 1
            witch_crafting(p1, typingActive)
            break
        #Crafting already active
        if rooms["Witch's Cabin"]['speech'] == 2:
            print_slow(line2409, typingActive)
            break


def fairy_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        if rooms['Fairy Circle']['speech'] == 0:
            soundFile = str(SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('\nInvalid input. Try again.', typingActive)
            break
        elif rooms['Fairy Circle']['speech'] == 1:
            if p1.faeCount < rooms['Fairy Circle']['fairy_reward']:
                print_slow(f""""Hello, thank you for returning. I appreciate all of your assistance. If you can return after defeating {rooms['Fairy Circle']['fairy_reward'] - p1.faeCount} more Dark Fae I should regain enough strength to reward you."\n """,typingActive)
                break
            elif p1.faeCount >= rooms['Fairy Circle']['fairy_reward']:
                if rooms['Fairy Circle']['fairy_reward'] == 5:
                    print_slow(line2909, typingActive)
                    p1.GP += 100
                    print_slow(f'{p1.name} is given 100 GP! {p1.name} has {p1.GP} GP in their wallet.', typingActive)
                    rooms['Fairy Circle']['fairy_reward'] = 10
                    break
                if rooms['Fairy Circle']['fairy_reward'] == 10:
                    print_slow(line2910, typingActive)
                    p1.ETR = min(p1.ETR + 3, p1.MaxETR)
                    print_slow(f'{p1.name} is given 3 ETHERS! {p1.name} has {p1.ETR}/{p1.MaxETR} ETHERS in their bag.', typingActive)
                    rooms['Fairy Circle']['fairy_reward'] = 20
                    break
                if rooms['Fairy Circle']['fairy_reward'] == 20:
                    print_slow(line2911, typingActive)
                    foe = rooms['Fairy Circle']['foe']
                    combat.standard_battle(p1, foe, typingActive, SoundsOn)
                    if p1.HP <= 0:
                        break
                    print_slow(line2912, typingActive)
                    p1.inventory.append('CRYSTAL NECKLACE')
                    p1.MP = p1.MaxMP
                    rooms['Fairy Circle']['boss'].remove('Dark Fairy Prince')
                    rooms['Fairy Circle']['speech'] = 2
                    rooms['Fairy Circle']['EXPLORE'] = line2904
                    rooms['Fairy Circle']['map'] = fairy_map2
                    break
        elif rooms['Fairy Circle']['speech'] == 2:
            print_slow('You try talking to the Dark Fairy Prince, but remember you killed him. Oh well. He was kind of a jerk.', typingActive)
            break


def marsh_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        if rooms["Frog Marsh"]['speech'] == 0:
            print_slow(line2803, typingActive)
            rooms["Frog Marsh"]['speech'] = 1
            p1.inventory.append('BROKEN HORN')
            if 'MOUTH-PIECE' in p1.inventory and 'BROKEN HORN' in p1.inventory:
                p1.inventory.append('COMPLETE HORN')
                p1.inventory.remove('MOUTH-PIECE')
                p1.inventory.remove('BROKEN HORN')
                rooms['Rotten Swamp 8']['EXPLORE'] = line2729
                print_slow(line2716, typingActive)
            break

        elif rooms["Frog Marsh"]['speech'] == 1:
            print_slow(line2804, typingActive)
            rooms["Frog Marsh"]['speech'] += 1
            break

        elif rooms["Frog Marsh"]['speech'] == 2:
            print_slow(line2805, typingActive)
            rooms["Frog Marsh"]['speech'] += 1
            break

        elif rooms["Frog Marsh"]['speech'] == 3:
            print_slow(line2806, typingActive)
            rooms["Frog Marsh"]['speech'] = 1
            break


def harborinn_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Harbor Inn']['speech'] == 0:
        print_slow(line405c, typingActive)
        rooms['Harbor Inn']['speech'] = 1
    elif rooms['Harbor Inn']['speech'] == 1:
        print_slow(line406c, typingActive)
        rooms['Harbor Inn']['speech'] = 0


def alchemist_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms["Alchemist Shop"]['speech'] == 0:
        print_slow(line3604, typingActive)
        rooms["Alchemist Shop"]['speech'] += 1      
    elif rooms["Alchemist Shop"]['speech'] == 1:
        print_slow(line3603, typingActive)
        rooms["Alchemist Shop"]['speech'] += 1
    elif rooms["Alchemist Shop"]['speech'] == 2:
        print_slow(line3605, typingActive)
        rooms["Alchemist Shop"]['speech'] = 0
        

def harbortemple_speak(p1, rooms, current_room, typingActive, SoundsOn):
  if rooms['Harbor Temple']['speech'] == 0:
    print_slow(line3405, typingActive)
    rooms['Harbor Temple']['speech'] = 1
  elif rooms['Harbor Temple']['speech'] == 1:
    print_slow(line3406, typingActive)
    rooms['Harbor Temple']['speech'] = 2
  elif rooms['Harbor Temple']['speech'] == 2:
    print_slow(line3407, typingActive)
    

def harborshop_speak(p1, rooms, current_room, typingActive, SoundsOn):
    print_slow(line307, typingActive)


def ship_speak(p1, rooms, current_room, typingActive, SoundsOn):
    while True:
        if rooms['Docked Ship']['speech'] == 0:
            if rooms['Docked Ship']['event'] == 0:
                print_slow(line3503, typingActive)
            elif rooms['Docked Ship']['event'] == 1:
                print_slow(line3503b, typingActive)
            choice = 1
            while choice == 1:
                playerInput = input().upper().strip()
                print('\n')
                if playerInput in affRes:
                    soundFile = str(SFX_Library['Select'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line3504, typingActive)
                    rooms['Docked Ship']['speech'] = 1
                    rooms['Waterfall Pool']['SOUTH'] = 'Waterfall Cave 1'
                    rooms['Waterfall Pool']['map'] = waterfall_map2
                    choice = 0
                    break
                elif playerInput in negRes:
                    soundFile = str(SFX_Library['Back'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(line3505, typingActive)
                    rooms['Docked Ship']['event'] = 1
                    choice = 0
                    break
                else:
                    soundFile = str(SFX_Library['Error'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow('\nInvalid input. Input YES or NO.\n', typingActive)
            rooms['Docked Ship']['intro'] = line3501b
            break
        elif rooms['Docked Ship'][
                'speech'] == 1 and 'SERPENTS EYE' not in p1.inventory:
            print_slow(line3506, typingActive)
            break
        elif rooms['Docked Ship'][
                'speech'] == 1 and 'SERPENTS EYE' in p1.inventory:
            print_slow(line3507, typingActive)
            p1.inventory.remove('SERPENTS EYE')
            p1.GP += 500
            print_slow(f"{p1.name} received a small treasure chest filled with gold coins worth 500 GP! {p1.name} has {p1.GP} GP in their wallet.", typingActive)
            rooms['Docked Ship']['speech'] = 2
            break
        elif rooms['Docked Ship']['speech'] == 2:
            print_slow(line3508, typingActive)
            break


def dwarf_speak(p1, rooms, current_room, typingActive, SoundsOn):
    global line4506
  
    if rooms["Dwarf's Workshop"]['speech'] == 0:
        print_slow(line4505, typingActive)
        rooms["Dwarf's Workshop"]['intro'] = line4502
        rooms["Dwarf's Workshop"]['EXPLORE'] = line4504
        rooms["Dwarf's Workshop"]['UPGRADE'] = smithing_upgrade
        rooms["Dwarf's Workshop"]['BUY'] = shop_menu
        rooms["Dwarf's Workshop"]['SELL'] = selling_to_Shopkeeper,
        rooms["Dwarf's Workshop"]['TRADE'] = dwarf_trade
        rooms["Dwarf's Workshop"]['speech'] = 1
    elif rooms["Dwarf's Workshop"]['event'] == 1:
        print_slow(line4510, typingActive)
        while True:
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4508, typingActive)
                p1.inventory.append('MAGIC CIRCLET')
                key_items['MAGIC GREASE']['ATK'] -= 3
                print_slow(f'{p1.name} gave some of the extra MAGIC GREASE to the Dwarf and added the MAGIC CIRCLET to their inventory.', typingActive)
                break
            elif playerInput in negRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4509, typingActive)
                rooms["Dwarf's Workshop"]['event'] = 1
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid command. Type YES or NO.\n', typingActive)
    elif rooms["Dwarf's Workshop"][
            'speech'] == 1 and 'STRANGE GREASE' not in p1.inventory:
        print_slow(line4506, typingActive)
    elif rooms["Dwarf's Workshop"][
            'speech'] == 1 and 'STRANGE GREASE' in p1.inventory:
        print_slow(line4507, typingActive)
        p1.inventory.remove('STRANGE GREASE')
        p1.inventory.append('MAGIC GREASE')
        while True:
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes:
                soundFile = str(SFX_Library['Select'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4508, typingActive)
                p1.inventory.append('MAGIC CIRCLET')
                print_slow(f'{p1.name} shared some of the MAGIC GREASE to the Dwarf and added the MAGIC CIRCLET to their inventory.', typingActive)
                break
            elif playerInput in negRes:
                soundFile = str(SFX_Library['Back'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4509, typingActive)
                rooms["Dwarf's Workshop"]['event'] = 1
                break
            else:
                soundFile = str(SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid command. Type YES or NO.\n', typingActive)


def dwarfvillage_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Dwarf Village']['speech'] == 0:
        print_slow(line5413, typingActive)
        rooms['Dwarf Village']['speech'] = 1
    elif rooms['Dwarf Village']['speech'] == 1:
        print_slow(line5414, typingActive)
        rooms['Dwarf Village']['speech'] = 0


def dwarfinn_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Dwarf Village - Inn']['speech'] == 0:
        print_slow(line405d, typingActive)
        rooms['Dwarf Village - Inn']['speech'] = 1
    elif rooms['Dwarf Village - Inn']['speech'] == 1:
        print_slow(line406d, typingActive)
        rooms['Dwarf Village - Inn']['speech'] = 0


def kobold_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms['Deep Woods - Forest Hut']['speech'] == 0:
        print_slow(line4728, typingActive)
        rooms['Deep Woods - Forest Hut']['speech'] = 1
    elif rooms['Deep Woods - Forest Hut']['speech'] == 1:
        print_slow(line4729, typingActive)
        rooms['Deep Woods - Forest Hut']['speech'] = 2
    elif rooms['Deep Woods - Forest Hut']['speech'] == 2:
        print_slow(line4730, typingActive)
        rooms['Deep Woods - Forest Hut']['intro'] = line4723
        rooms['Deep Woods - Forest Hut']['EXPLORE'] = line4726
        rooms['Deep Woods - Forest Hut']['speech'] = 3
        rooms['Deep Woods - Forest Hut']['EXAMINE'] = kobold_special
        rooms['Deep Woods - Forest Hut']['event'] = 1
    elif rooms['Deep Woods - Forest Hut']['speech'] == 3 and 'PAINTED SNAIL' in p1.inventory:
        print_slow(line4733, typingActive)
        p1.inventory.remove("PAINTED SNAIL")
        if "SLEEPY SQUIRELL" in p1.inventory:
            p1.inventory.remove("SLEEPY SQUIRELL")
        if "WET TOAD" in p1.inventory:
            p1.inventory.remove("WET TOAD")
        rooms['Deep Woods - Forest Hut']['intro'] = line4724
        rooms['Deep Woods - Forest Hut']['EXPLORE'] = line4727
        rooms['Deep Woods - Forest Hut']['BUY'] = shop_menu
        rooms['Deep Woods - Forest Hut']['SELL'] = selling_to_Shopkeeper
        rooms['Deep Woods - Forest Hut']['speech'] = 4
        rooms['Deep Woods - Forest Hut']['event'] = 2
    elif rooms['Deep Woods - Forest Hut']['speech'] == 3 and ("WET TOAD" or "SLEEPY SQUIRELL") in p1.inventory:
        print_slow(line4732, typingActive)
        while True:
            if "SLEEPY SQUIRELL" in p1.inventory:
                p1.inventory.remove("SLEEPY SQUIRELL")
                break
            elif "WET TOAD" in p1.inventory:
                p1.inventory.remove("WET TOAD")
                break
    elif rooms['Deep Woods - Forest Hut']['speech'] == 3 and any(x in rooms['Deep Woods - Forest Hut']['items2'] for x in p1.inventory) == False:
        print_slow(line4731, typingActive)
    elif rooms['Deep Woods - Forest Hut']['speech'] == 4:
        print_slow(line4734, typingActive)
        

def vampLord_speak(p1, rooms, current_room, typingActive, SoundsOn):
    if rooms["Forest Palace - Lord's Chamber"]['event'] == 2:
        print_slow(line5166, typingActive)
    else:
        p_Input = "SPEAK"
        vamp_lord_update(p1, p_Input, typingActive, SoundsOn)


def cliff_special(p1, playerInput, typingActive, SoundsOn):
    soundFile = str(SFX_Library['Jump'])
    play_sound_effect(soundFile, SoundsOn)
    print_slow(line610, typingActive)
    damage = 69
    p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
    if p1.HP > 0:
        rooms['Cliff Side']['secret_path'] = 1
        print_slow(line611, typingActive)
        print_slow(f"{p1.name} has {p1.HP} HP", typingActive)
    combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
    return


def cave4_special(p1, playerInput, typingActive, SoundsOn):
    soundFile = str(SFX_Library['Jump'])
    play_sound_effect(soundFile, SoundsOn)
    print_slow(line946, typingActive)
    p1.HP = 0
    combat.player_death(p1, typingActive, SoundsOn,  foe = p2)
    return


def berry_special(p1, playerInput, typingActive, SoundsOn):
    if rooms['Berry Patch']['chest'] == "OPEN":
        if playerInput == 'WAIT':
            print_slow(f"{p1.name} waits for the REZZBERRIES to regrow. In the year it takes, Smeldars forces have conquered the kingdom. What do you think was going to happen?", typingActive)
            p1.HP = 0
            combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
            return
        if playerInput == 'PICK':
            soundFile = str(SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line1006, typingActive)
    else:
        soundFile = str(SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('\nInvalid input. Try again.', typingActive)
    return


def river_special(p1, playerInput, typingActive, SoundsOn):
    if playerInput != 'SAIL':
        soundFile = str(SFX_Library['Jump'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line1207, typingActive)
        p1.HP = 0
        combat.player_death(p1, typingActive, SoundsOn,  foe = p2)
        return
    elif playerInput == 'SAIL':
        if rooms['Serpent River']['event'] == 1:
            rooms['River - West Bank']['map'] = westriver_map2
            rooms['River - West Bank']['event'] = 1
            rooms['River - West Bank']['EXPLORE'] = line3803
            rooms['Serpent River']['map'] = river_map2
            rooms['Serpent River']['secret_path'] = 1
            rooms['Serpent River']['event'] = 2
            rooms['Serpent River']['EXPLORE'] = line1203
            print_slow(f'{p1.name} hops on the raft and begins sailing across the river!\n',typingActive)
        elif rooms['Serpent River']['event'] == 2:
            print_slow(f'{p1.name} is unable to SAIL across - the raft is on the wrong side of the river for that.\n', typingActive)


def lake_special(p1, playerInput, typingActive, SoundsOn):
    soundFile = str(SFX_Library['Jump'])
    play_sound_effect(soundFile, SoundsOn)
    print_slow(line1414, typingActive)
    p1.HP = 0
    combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
    return


def swamp_special(p1, playerInput, typingActive, SoundsOn):
    if playerInput == 'DRINK':
        print_slow(line2721, typingActive)
        p1.POISON += 3
        p1.HP -= 5
        if p1.HP <= 0:
            combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
            return
        else:
            print_slow(f'{p1.name} takes 5 damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
    elif playerInput in ['SWIM', 'WADE', 'DIVE']:
        soundFile = SFX_Library['Jump']
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line2722, typingActive)
        p1.HP = 0
        combat.player_death(p1, typingActive, SoundsOn,  foe=p2)
        return


def swamp7_special(p1, playerInput, typingActive, SoundsOn):
    if playerInput in song_term and rooms['Rotten Swamp 7']['event'] == 1:
        print_slow(line2726, typingActive)
    elif playerInput in song_term and rooms['Rotten Swamp 7']['event'] == 0:
        print_slow(line2725, typingActive)
        p1.inventory.append('GOLD RING')
        print_slow(f'{p1.name} recieved a GOLD RING! {p1.name} feels their fortune improving with the ring in hand.\n', typingActive)
        rooms['Rotten Swamp 7']['event'] = 1
    else:
        swamp_special(p1, playerInput, typingActive, SoundsOn)


def swamp8_special(p1, playerInput, typingActive, SoundsOn):
    if playerInput == 'PLAY' and rooms['Rotten Swamp 8']['event'] == 1:
        print_slow(line2737, typingActive)
    elif playerInput == 'PLAY' and rooms['Rotten Swamp 8']['event'] == 0:
        print_slow(line2731, typingActive)
        if 'WAFFLE' in p1.inventory:
            print_slow(line2733, typingActive)
            playerInput = (input().upper()).strip()
            print_slow('\n', typingActive)
            if playerInput == 'GIVE':
                time.sleep(0.5)
                soundFile = SFX_Library['GotLegendary']
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line2735, typingActive)
                p1.inventory.remove('WAFFLE')
                p1.inventory.append("OGRE'S WARLOCK KEY")
                rooms['Rotten Swamp 8']['event'] = 1
                rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
                rooms['Rotten Swamp 8']['map'] = swamp8_map2
                p1.keys += 1
                rot_update(p1)
            if playerInput == 'KEEP':
                print_slow(line2736, typingActive)
                foe = rooms['Rotten Swamp 8']['foe']
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    return
                time.sleep(0.5)
                soundFile = SFX_Library['GotLegendary']
                play_sound_effect(soundFile, SoundsOn)
                p1.inventory.append("OGRE'S WARLOCK KEY")
                rooms['Royal Castle']['event2'].append('B')
                rooms['Rotten Swamp 8']['event'] = 1
                rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
                rooms['Rotten Swamp 8']['map'] = swamp8_map2
                print_slow(line2738, typingActive)
                p1.keys += 1
                rot_update(p1)
            else:
                soundFile = SFX_Library['Error']
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.', typingActive)
        elif 'WAFFLE' not in p1.inventory:
            print_slow(line2732, typingActive)
            foe = rooms['Rotten Swamp 8']['foe']
            combat.standard_battle(p1, foe, typingActive, SoundsOn)
            if p1.HP <= 0:
                return
            p1.inventory.append("OGRE'S WARLOCK KEY")
            rooms['Royal Castle']['event2'].append('B')
            rooms['Rotten Swamp 8']['event'] = 1
            rooms['Rotten Swamp 8']['EAST'] = 'Western Lake'
            rooms['Rotten Swamp 8']['map'] = swamp8_map2
            time.sleep(0.5)
            soundFile = SFX_Library['GotLegendary']
            play_sound_effect(soundFile, SoundsOn)
            print_slow(line2738, typingActive)
            p1.keys += 1
            rot_update(p1)
    else:
        swamp_special(p1, playerInput, typingActive, SoundsOn)


def riverwest_special(p1, playerInput, typingActive, SoundsOn):
    if rooms['River - West Bank']['event'] == 1:
        rooms['River - West Bank']['map'] = westriver_map3
        rooms['River - West Bank']['secret_path'] = 1
        rooms['River - West Bank']['event'] = 2
        rooms['River - West Bank']['EXPLORE'] = line3804
        rooms['Serpent River']['map'] = river_map3
        rooms['Serpent River']['event'] = 1
        rooms['Serpent River']['EXPLORE'] = line1204
        print_slow(f'{p1.name} hops on the raft and begins sailing across the river\n', typingActive)
    elif rooms['River - West Bank']['event'] == 2:
        print_slow(f'{p1.name} is unable to SAIL across - the raft is on the wrong side of the river for that.\n', typingActive)


def crescent_special(p1, playerInput, typingActive, SoundsOn):
    if 'Naga' in rooms['Crescent Pond']['boss']:
        print_slow(f"""You take your {p1.mainHand} and throw it into the pool. The water begins to foam and a women clad in flowing white robes raises from the depths of the pond. In her hands she holds a blade of pure silver\n\n"Hello dear traveler. It seems you may have lost something in the waters... I have retreived it for you. This is your SILVER BLADE, correct?\n" """, typingActive)
        previous_gear = p1.mainHand
        p1.mainHand = 'EMPTY'
        playerInput = 'EMPTY'
        p1.equip_stat_update(playerInput, previous_gear, key_items)
        while True:
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes:
                soundFile = SFX_Library['Select']
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4106, typingActive)
                foe = p53
                combat.standard_battle(p1, foe, typingActive, SoundsOn)
                if p1.HP <= 0:
                    break
                print_slow(f"""The defeated Naga writhes in agony on the ground before its gut burst open, the {p1.mainHand} falling to the ground. You wipe off the Naga's innards from the {p1.mainHand} and notice that it seems more polished than before.""", typingActive)
                rooms['Crescent Pond']['EXPLORE'] = line4104
                rooms['Crescent Pond']['boss'].remove('Naga')
                key_items[previous_gear]['ATK'] += 3
                p1.mainHand = previous_gear 
                previous_gear = 'EMPTY'
                playerInput = 'EMPTY'
                p1.equip_stat_update(playerInput, previous_gear, key_items)
                p1.stat_check(typingActive, SoundsOn)
                break
            elif playerInput in negRes:
                soundFile = SFX_Library['Back']
                play_sound_effect(soundFile, SoundsOn)
                print_slow(line4107, typingActive)
                while True:
                    playerInput = input().upper().strip()
                    print('\n')
                    if playerInput in affRes:
                        soundFile = SFX_Library['Select']
                        play_sound_effect(soundFile, SoundsOn)
                        print_slow(line4106, typingActive)
                        foe = p53
                        combat.standard_battle(p1, foe, typingActive, SoundsOn)
                        if p1.HP <= 0:
                            break
                        print_slow(f"""The defeated Naga writhes in agony on the ground before its gut burst open, the {p1.mainHand} falling to the ground. You wipe off the Naga's innards from the {p1.mainHand} and notice that it seems more polished than before.""", typingActive)
                        rooms['Crescent Pond']['EXPLORE'] = line4104
                        rooms['Crescent Pond']['boss'].remove('Naga')
                        key_items[previous_gear]['ATK'] += 5
                        p1.stat_check(typingActive, SoundsOn)
                        break
                    elif playerInput in negRes:
                        soundFile = SFX_Library['Back']
                        play_sound_effect(soundFile, SoundsOn)
                        print_slow(f"""The women submerges herself in the pond once more this time pulling out the {p1.mainHand} you threw into the water.\n\n"This must be your weapon then. It does not befit one as noble as you though. I will take this from you and in exchange I will grant you the ADAMANTITE SWORD. No blade is sharper or more durable. May it serve you well..."\n\n The woman pulls the ADAMANTITE SWORD from her robes and places the blade at your feet. You draw your new weapon and admire its immaculate craftsmanship before returning it to its scabbard. When you look back up the woman is already gone...\n """, typingActive)
                        rooms['Crescent Pond']['EXPLORE'] = line4103
                        rooms['Crescent Pond']['boss'].remove('Naga')
                        p1.inventory.remove(previous_gear)
                        p1.inventory.append('ADAMANTITE SWORD')
                        previous_gear = p1.mainHand
                        p1.mainHand = 'ADAMANTITE SWORD'
                        playerInput = 'ADAMANTITE SWORD'
                        p1.equip_stat_update(playerInput, previous_gear, key_items)
                        p1.stat_check(typingActive, SoundsOn)
                        break
                    else:
                        soundFile = SFX_Library['Error']
                        play_sound_effect(soundFile, SoundsOn)
                        print_slow('\nInvalid input. Input YES or NO.\n',typingActive)
                break
            else:
                soundFile = SFX_Library['Error']
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Input YES or NO.\n', typingActive)
    else:
        soundFile = SFX_Library['Error']
        play_sound_effect(soundFile, SoundsOn)
        print_slow('\nInvalid input. Try again.\n', typingActive)


def drake_special(p1, playerInput, typingActive, SoundsOn):
  if rooms['Drake Mountains 3']['event'] == 0:
    soundFile = combat.battle_sounds['Roar4']
    play_sound_effect(soundFile, SoundsOn)
    rooms['Drake Mountains 3']['SOUTH'] = 'Drake Mountains Summit'
    rooms['Drake Mountains 3']['EXPLORE'] = line4607
    rooms['Drake Mountains 3']['event'] = 1
    print_slow(line4607c, typingActive)
  else: 
    print_slow('You speak the name "TANNINIM" once more, but nothing else seems to happen...', typingActive)


def kobold_special(p1, rooms, typingActive, SoundsOn):
    if rooms['Deep Woods - Forest Hut']['event'] == 1:
        hit = random.randrange(0,11)
        investigate = rooms['Deep Woods - Forest Hut']['event2'] + hit
        if investigate >=7:
            if bool(rooms['Deep Woods - Forest Hut']['items2']):
              friend = random.choice(rooms['Deep Woods - Forest Hut']['items2'])
              if friend == "PAINTED SNAIL":
                  p1.inventory.append("PAINTED SNAIL")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("PAINTED SNAIL")
                  print_slow(line4735, typingActive)
              if friend == "SLEEPY SQUIRELL":
                  p1.inventory.append("SLEEPY SQUIRELL")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("SLEEPY SQUIRELL")
                  print_slow(line4736, typingActive)
              if friend == "WET TOAD":
                  p1.inventory.append("WET TOAD")
                  rooms['Deep Woods - Forest Hut']['items2'].remove("WET TOAD")
                  print_slow(line4737, typingActive)
              print_slow(f"{p1.name} picks up the {friend} and carefully places it in their bag.\n", typingActive)
            else:
              print_slow(f"You search around the area, but turn up nothing.\n", typingActive)
        if 2 < investigate < 7:
          foe = random.choice(enemy_spawn26)
          print_slow(f"You search around the area, and soon hear a rustling come from the woods. Suddenly a {foe.name} rushes to attack you! You draw your weapon and defend yourself against the ambush!\n", typingActive)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
            return
          rooms['Deep Woods - Forest Hut']['event2'] += 1
        if investigate <= 2:
          foe = random.choice(enemy_spawn27)
          print_slow(f"You search around the area, and soon hear crashing come from the woods. Suddenly a {foe.name} emerges and sets its sights on you! You draw your weapon and defend yourself against the ambush!\n", typingActive)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
                return
          rooms['Deep Woods - Forest Hut']['event2'] += 2
    if rooms['Deep Woods - Forest Hut']['event'] == 2:
        print_slow(line4738, typingActive)
            

def orc2_special(p1, playerInput, typingActive, SoundsOn):
  if rooms["Orc Fortress 2"]['chest'] == 0 and rooms["Orc Fortress 2"]['event'] == 0:
    print_slow(line4927, typingActive)
    while True:
      playerInput = input().upper().strip()
      print('\n')
      if playerInput == 'STEAL':
        soundFile = combat.battle_sounds['Steal']
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line4928, typingActive)
        hit = random.randrange(0,5)
        if hit > 0:
          print_slow(line4929, typingActive)
          print_slow(f'{p1.name} adds the CHEST KEY to their inventory!\n', typingActive)   
        else:
          print_slow(line4930, typingActive)
          foe = random.choice(enemy_spawn28)
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if p1.HP <= 0:
            break
          print_slow(f"You succsessfully defeat the {foe.name} and claim the CHEST KEY. Seems like you're more cut out for murder than burglary.\n", typingActive)
        p1.inventory.append('CHEST KEY')
        rooms["Orc Fortress 2"]['event'] = 1
        break
      elif playerInput in backRes:
        soundFile = SFX_Library['Back']
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line4931, typingActive)
        break
      else:
        soundFile = SFX_Library['Error']
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Input STEAL or LEAVE.\n', typingActive)
  elif rooms["Orc Fortress 2"]['chest'] == 1:
    print_slow("You've already opened the chest here; no need to keep searching for the key.\n", typingActive)
  elif rooms["Orc Fortress 2"]['event'] == 1:
    print_slow("You've already found the CHEST KEY; no need to keep searching\n", typingActive)


def vamp13_special(p1, playerInput, typingActive, SoundsOn):
   print_slow(line5144, typingActive)


def vampLord_Special(p1, playerInput, typingActive, SoundsOn):
    if rooms["Forest Palace - Lord's Chamber"]['event'] == 2:
        print_slow(line5166b, typingActive)
    else:
        p_Input = "ATTACK"
        vamp_lord_update(p1, p_Input, typingActive, SoundsOn)


def tower2_special(p1, playerInput, typingActive, SoundsOn):
    if playerInput in atkRes:
        soundFile = combat.battle_sounds['Cut']
        play_sound_effect(soundFile, SoundsOn)
        if rooms['Smeldars Tower - 2']['event'] == 1:
            print_slow(line5209d, typingActive)
        else:
            print_slow(line5209b, typingActive)
            rooms['Smeldars Tower - 2']['event'] = 1
            rooms['Smeldars Tower - 2']['EXPLORE'] = line5208b
            p1.inventory.append('TOWER KEY')
            p1.inventory.append('TORN NOTE')
    elif playerInput == 'JUMP':
        if rooms['Smeldars Tower - 2']['event'] == 1:
            print_slow(line5209e, typingActive)
        else:    
            print_slow(line5209c, typingActive)
            rooms['Smeldars Tower - 2']['event'] = 1
            rooms['Smeldars Tower - 2']['EXPLORE'] = line5208b
            p1.inventory.append('TOWER KEY')
            p1.inventory.append('TORN NOTE')


def rot_update(p1):
  if p1.keys >= 2:
    rooms['Rotting Woods']['EAST'] = 'Rotting Woods - EAST'
    rooms['Rotting Woods']['map'] = rot_map2
    rooms['Rotting Woods']['EXPLORE'] = line2603


def vamp_queen_update(rooms):
   rooms['Forest Palace - 6']['event'] += 1
   if rooms["Forest Palace - 6"]['event'] == 2:
      rooms['Forest Palace - 6']['map'] = vcastle_6_map2
      rooms['Forest Palace - 6']['NORTH'] = "Forest Palace - Queen's Chamber"
      rooms['Forest Palace - 6']['EXPLORE'] = line5116c
   else:
      rooms['Forest Palace - 6']['EXPLORE'] = line5116b


def vamp_statue_update(cRoom, rooms, typingActive, SoundsOn):
    def statue_rotation():
        if rooms[cRoom]['event2'] == 0:
            statueFace = "NORTH"
        elif rooms[cRoom]['event2'] == 1:
            statueFace = "NORTH-EAST"
        elif rooms[cRoom]['event2'] == 2:
            statueFace = "EAST"
        elif rooms[cRoom]['event2'] == 3:
            statueFace = "SOUTH-EAST"
        elif rooms[cRoom]['event2'] == 4:
            statueFace = "SOUTH"
        elif rooms[cRoom]['event2'] == 5:
            statueFace = "SOUTH-WEST"
        elif rooms[cRoom]['event2'] == 6:
            statueFace = "WEST"
        elif rooms[cRoom]['event2'] == 7:
            statueFace = "NORTH-WEST"
        return statueFace
    
    def statue_rooms_update(rooms):
       if rooms["Forest Palace - 16"]['event2'] == 1 and rooms["Forest Palace - 17"]['event2'] == 3 and rooms["Forest Palace - 18"]['event2'] == 6 and rooms["Forest Palace - 19"]['event2'] == 6:
           rooms["Forest Palace - 16"]['event'] = 1
           rooms["Forest Palace - 17"]['event'] = 1
           rooms["Forest Palace - 18"]['event'] = 1
           rooms["Forest Palace - 19"]['event'] = 1
           rooms["Forest Palace - 16"]['EXPLORE'] = line5152b
           rooms["Forest Palace - 17"]['EXPLORE'] = line5155b
           rooms["Forest Palace - 18"]['EXPLORE'] = line5157b
           rooms["Forest Palace - 19"]['EXPLORE'] = line5159b
           rooms["Forest Palace - 9"]['map'] = vcastle_9_map2
           rooms["Forest Palace - 9"]['NORTH'] = "Forest Palace - Lord's Chamber"
           rooms["Forest Palace - 9"]['EXPLORE'] = line5129b
           rooms["Forest Palace - 9"]['event'] = 1
           print_slow(line5160, typingActive)

    def statue_map_update(cRoom, rooms):
        if cRoom == "Forest Palace - 16":
            if rooms[cRoom]['event2'] == 0:
                rooms[cRoom]['map'] = vcastle_16_map4
            elif rooms[cRoom]['event2'] == 1:
                rooms[cRoom]['map'] = vcastle_16_map5
            elif rooms[cRoom]['event2'] == 2:
                rooms[cRoom]['map'] = vcastle_16_map6
            elif rooms[cRoom]['event2'] == 3:
                rooms[cRoom]['map'] = vcastle_16_map7
            elif rooms[cRoom]['event2'] == 4:
                rooms[cRoom]['map'] = vcastle_16_map8
            elif rooms[cRoom]['event2'] == 5:
                rooms[cRoom]['map'] = vcastle_16_map1
            elif rooms[cRoom]['event2'] == 6:
                rooms[cRoom]['map'] = vcastle_16_map2
            elif rooms[cRoom]['event2'] == 7:
                rooms[cRoom]['map'] = vcastle_16_map3   
        
        elif cRoom == "Forest Palace - 17":
            if rooms[cRoom]['event2'] == 0:
                rooms[cRoom]['map'] = vcastle_17_map1
            elif rooms[cRoom]['event2'] == 1:
                rooms[cRoom]['map'] = vcastle_17_map2
            elif rooms[cRoom]['event2'] == 2:
                rooms[cRoom]['map'] = vcastle_17_map3
            elif rooms[cRoom]['event2'] == 3:
                rooms[cRoom]['map'] = vcastle_17_map4
            elif rooms[cRoom]['event2'] == 4:
                rooms[cRoom]['map'] = vcastle_17_map5
            elif rooms[cRoom]['event2'] == 5:
                rooms[cRoom]['map'] = vcastle_17_map6
            elif rooms[cRoom]['event2'] == 6:
                rooms[cRoom]['map'] = vcastle_17_map7
            elif rooms[cRoom]['event2'] == 7:
                rooms[cRoom]['map'] = vcastle_17_map8

        elif cRoom == "Forest Palace - 18":
            if rooms[cRoom]['event2'] == 0:
                rooms[cRoom]['map'] = vcastle_18_map2
            elif rooms[cRoom]['event2'] == 1:
                rooms[cRoom]['map'] = vcastle_18_map3
            elif rooms[cRoom]['event2'] == 2:
                rooms[cRoom]['map'] = vcastle_18_map4
            elif rooms[cRoom]['event2'] == 3:
                rooms[cRoom]['map'] = vcastle_18_map5
            elif rooms[cRoom]['event2'] == 4:
                rooms[cRoom]['map'] = vcastle_18_map6
            elif rooms[cRoom]['event2'] == 5:
                rooms[cRoom]['map'] = vcastle_18_map7
            elif rooms[cRoom]['event2'] == 6:
                rooms[cRoom]['map'] = vcastle_18_map8
            elif rooms[cRoom]['event2'] == 7:
                rooms[cRoom]['map'] = vcastle_18_map1

        elif cRoom == "Forest Palace - 19":
            if rooms[cRoom]['event2'] == 0:
                rooms[cRoom]['map'] = vcastle_19_map6
            elif rooms[cRoom]['event2'] == 1:
                rooms[cRoom]['map'] = vcastle_19_map7
            elif rooms[cRoom]['event2'] == 2:
                rooms[cRoom]['map'] = vcastle_19_map8
            elif rooms[cRoom]['event2'] == 3:
                rooms[cRoom]['map'] = vcastle_19_map1
            elif rooms[cRoom]['event2'] == 4:
                rooms[cRoom]['map'] = vcastle_19_map2
            elif rooms[cRoom]['event2'] == 5:
                rooms[cRoom]['map'] = vcastle_19_map3
            elif rooms[cRoom]['event2'] == 6:
                rooms[cRoom]['map'] = vcastle_19_map4
            elif rooms[cRoom]['event2'] == 7:
                rooms[cRoom]['map'] = vcastle_19_map5

    if rooms[cRoom]['event'] == 1:
        print_slow(line5161, typingActive)
    
    else:
        statueFace = statue_rotation()
        print_slow(line5153, typingActive)
        print_slow(f"The statue is currently facing {statueFace}.\n", typingActive)
        while True:
            print_slow("\nWould you like to try rotating the statue? (YES or NO)\n", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in affRes :
                rooms[cRoom]['event2'] += 1
                if rooms[cRoom]['event2'] == 8:
                    rooms[cRoom]['event2'] = 0
                statueFace = statue_rotation()
                soundFile = SFX_Library['Rotate']
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f"You rotate the statue to face {statueFace}.\n", typingActive)
                statue_map_update(cRoom, rooms)
                statue_rooms_update(rooms)
                if rooms[cRoom]['event'] == 1:
                    break
            elif playerInput in negRes :
                soundFile = SFX_Library['Back']
                play_sound_effect(soundFile, SoundsOn)
                print_slow("You decide not to rotate the statue any further.\n", typingActive)
                break


def vamp_lord_update(p1, p_Input, typingActive, SoundsOn):
    def vampBoss_Start(p92):
       foe = p92
       combat.standard_battle(p1, foe, typingActive, SoundsOn)
       if p1.HP <= 0:
        return

    if rooms["Forest Palace - Lord's Chamber"]['event'] == 1:
       print_slow(line5165, typingActive)
       p1.inventory.append("RUBY GEMSTONE")
       gp = random.randrange(250,500)
       p1.GP += gp
       print_slow(f'{p1.name} searches the chamber and finds a RUBY GEMSTONE and {gp} GP!\n', typingActive)
       rooms["Forest Palace - Lord's Chamber"]['event'] = 2
       rooms["Forest Palace - Lord's Chamber"]['EXPLORE'] = line5163c

    elif rooms["Forest Palace - Lord's Chamber"]['event'] == 0:
        if p_Input == "SPEAK":
            print_slow(line5164, typingActive)
            p92.DEF -= 5
            print_slow("Your courage has caught the Vampire Lord's attention! The Vampire Lord's defenses have been weakened!\n", typingActive)
            vampBoss_Start(p92)
        elif p_Input == "ATTACK":
            print_slow(line5164b, typingActive)
            hit = random.randrange(25,40)
            p92.HP -= hit
            print_slow(f"The Vampire Lord reels back from your attack, narrowly escaping the full impact! The Vampire Lord takes {hit} damage!\n", typingActive)
            vampBoss_Start(p92)
        elif p_Input == "EXAMINE":
            print_slow(line5164c, typingActive)
            vampBoss_Start(p92)
        time.sleep(0.5)
        soundFile = SFX_Library['GotLegendary']
        play_sound_effect(soundFile, SoundsOn)
        print_slow(line5164d, typingActive)
        p1.inventory.append("VAMPIRE'S WARLOCK KEY")
        rooms["Forest Palace - Lord's Chamber"]['event'] = 1
        rooms["Forest Palace - Lord's Chamber"]['intro'] = line5162b
        rooms["Forest Palace - Lord's Chamber"]['EXPLORE'] = line5163b
        rooms["Forest Palace - 3"]["event"] = 1
        rooms["Forest Palace - 3"]["intro"] = line5107b
        rooms["Forest Palace - 3"]["EXPLORE"] = line5108b
        rooms['Royal Castle']['event2'].append('D')


rooms = {
    '': {
        'name': '',
        'intro': None,
        'map': None,
        'discovered': [],
        'NORTH': None,
        'EAST': None,
        'SOUTH': None,
        'WEST': None,
        'SECRET_ROUTE': None,
        'EXPLORE': None,
        'EXAMINE': None,
        'SPEAK': None,
        'REST': None,
        'PRAY': 'pray',
        'BUY': "BUY",
        'CRAFT': 'craft',
        'speech': None,
        'crafting': None,
        'secrets': [],
        'secret_path': 0,
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': [],
        'boss_ambush': None,
        'ambush': None,
        'items': [],
        'foe': None,
        'LOCK': None,
        'chest': None,
        'event': None,
        'floor': None,
    },
    'Testing Ground': {
        'name': 'Testing Ground',
        'intro': "How'd you end up here?",
        'map': vcastle_15_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - Outer Gate',
        'EAST': 'Smeldars Throne',
        'SOUTH': 'Deep Woods - Forest Hut',
        'WEST': 'Camp Site',
        'CLIMB': 'Forest Palace - 13',
        'EXPLORE': 'Nothing to see here...',
        # 'EXAMINE' : None,
        #'SPEAK' : None,
        #'REST' : None,
        #'PRAY' : 'pray',
        #'BUY' : "BUY",
        #'CRAFT' : 'craft',
        #'speech' : None,
        #'crafting' : None,
        'secrets' : ['WAIT'],
        #'secret_path' : 0,
        #'special': test_special,
        'spawn_rate': 10,
        'enemy_spawn_set': enemy_spawnT,
        #'boss' : [],
        #'boss_ambush' : None,
        #'ambush' : test_ambush,
        #'ambush_pass' : 0,
        'fire': 0,
        #'foe' : None,
        #'LOCK' : None,
        #'chest' : None,
        #'event' : None,
        'floor': 'GRASS',
    },
    'Camp Site': {
        'name': 'Camp Site',
        'intro': line101,
        'map': camp_map1,
        'discovered': [],
        'NORTH': 'Pinerift Forest',
        #'EAST': 'Testing Ground',
        'SOUTH': 'Capital City',
        'WEST': 'Cliff Side',
        'EXPLORE': line103,
        'REST': camp_rest,
        'fire': 3,
        'Maxfire': 3,
        'fireTalk': line105,
        'spawn_rate': 0,
        'floor': 'GRASS',
    },
    'Cliff Side': {
        'name': 'Cliff Side',
        'intro': line601,
        'map': cliff_map1,
        'discovered': [],
        'EAST': 'Camp Site',
        'SECRET_ROUTE': 'Waterfall Pool',
        'EXPLORE': line602,
        'EXAMINE': cliff_examine,
        'secrets': ['JUMP', 'FLY', 'DIVE'],
        'secret_path': 0,
        'special': cliff_special,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn0,
        'chest': 'CLOSED',
        'floor': 'GRASS',
    },
  
    #Town start
    'Capital City': {
        'name': 'Capital City',
        'intro': line201,
        'map': town_map1,
        'discovered': [],
        'NORTH': 'Camp Site',
        'EAST': 'Capital City - Shop',
        'SOUTH': 'Royal Castle',
        'WEST': 'Capital City - Main Street',
        'EXPLORE': line202,
        'spawn_rate': 0,
        'floor': 'GRAVEL',
    },
    'Capital City - Shop': {
        'name': 'Capital City - Shop',
        'intro': line301,
        'map': shop_map1,
        'discovered': [],
        'WEST': 'Capital City',
        'EXIT': 'Capital City',
        'EXPLORE': line304,
        'SPEAK': cityshop_speak,
        'BUY': shop_menu,
        'SELL': selling_to_Shopkeeper,
        'spawn_rate': 0,
        'event': 0,
        'speech': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'SALINE', 'WARP CRYSTAL', 'KINDLING', 'MAP', 'LANTERN','CRAFTING POUCH', 'MACE', 'GAMBESON', 'LEATHER BOOTS', 'LEATHER CAP'],
        'floor': 'STONE',
    },
    'Capital City - Main Street': {
        'name': 'Capital City - Main Street',
        'intro': line203,
        'map': town2_map1,
        'discovered': [],
        'NORTH': 'Capital City - Church',
        'EAST': 'Capital City',
        'WEST': 'Capital City - Inn',
        'EXPLORE': line204,
        'spawn_rate': 0,
        'floor': 'GRAVEL',
        
    },
    'Capital City - Inn': {
        'name': 'Capital City - Inn',
        'intro': line401,
        'map': inn_map1,
        'discovered': [],
        'EAST': 'Capital City - Main Street',
        'EXPLORE': line404,
        'SPEAK': cityinn_speak,
        'REST': city_inn,
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'STONE',
    },
    'Capital City - Church': {
        'name': 'Capital City - Church',
        'intro': line205,
        'map': cityshrine_map1,
        'discovered': [],
        'SOUTH': 'Capital City - Main Street',
        'EXPLORE': line206,
        #'SPEAK': city_inn,
        'PRAY': shrine_pray,
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'STONE',
    },
    'Royal Castle': {
        'name': 'Royal Castle',
        'intro': line501,
        'map': castle_map1,
        'discovered': [],
        'NORTH': 'Capital City',
        'EXIT': 'Capital City',
        'EXPLORE': line502,
        'spawn_rate': 0,
        'SPEAK': castle_speak,
        'speech': 0,
        'event': 0,
        'event2': [],
        'speech': 0,
        'floor': 'STONE',
    },  
    #Town end
  
    'Pinerift Forest': {
        'name': 'Pinerift Forest',
        'intro': line701,
        'map': forest_map1,
        'discovered': [],
        'NORTH' : 'Dense Thicket',
        'EAST': 'Pinerift Forest - EAST',
        'SOUTH': 'Camp Site',
        'WEST': 'Pinerift Forest - WEST',
        'EXPLORE': line702,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn1,
        'floor': 'FOLIAGE',
    },
    'Pinerift Forest - EAST': {
        'name': 'Pinerift Forest - EAST',
        'intro': line704,
        'map': foresteast_map1,
        'discovered': [],
        'EAST': 'Rocky Hill',
        'WEST': 'Pinerift Forest',
        'EXPLORE': line705,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn1,
        'boss_ambush': foresteast_boss_ambush,
        'event': 0,
        'floor': 'FOLIAGE',
    },
    'Pinerift Forest - WEST': {
        'name': 'Pinerift Forest - WEST',
        'intro': line709,
        'map': forestwest_map1,
        'discovered': [],
        'EAST': 'Pinerift Forest',
        'WEST': 'Serpent River',
        'EXPLORE': line710,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn1,
        'floor': 'FOLIAGE',
    },
    'Rocky Hill': {
        'name': 'Rocky Hill',
        'intro': line801,
        'map': hill_map1,
        'discovered': [],
        'NORTH': 'Mystic Shrine',
        'EAST': 'Bear Cave',
        'SOUTH': 'LOCKED',
        'WEST': 'Pinerift Forest - EAST',
        'EXPLORE': line802,
        'EXAMINE': hill_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn6,
        'LOCK': hill_lock,
        'floor': 'GRAVEL',
    },
    'Mystic Shrine': {
        'name': 'Mystic Shrine',
        'intro': line1101,
        'map': shrine_map1,
        'discovered': [],
        'EAST': 'Deep Woods - Entrance',
        'SOUTH': 'Rocky Hill',
        'EXPLORE': line1102,
        'SPEAK': shrine_speak,
        'PRAY': shrine_pray,
        'speech': 0,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn4,
        'floor': 'GRASS',
    },
  
    #Dungeon 1 start
    'Bear Cave': {
        'name': 'Bear Cave',
        'intro': line901,
        'map': cave_map1,
        'discovered': [],
        'WEST': 'Rocky Hill',
        'EAST': 'LOCKED',
        'EXPLORE': line906,
        'EXAMINE': cave_examine,
        'spawn_rate': 0,
        'boss': ['Bear'],
        'foe': p12,
        'LOCK': cave_lock,
        'floor': 'GRAVEL',
    },
    'Rocky Cave 1': {
        'name': 'Rocky Cave 1',
        'intro': line916,
        'map': cave1_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 2',
        'SOUTH': 'Rocky Cave 3',
        'WEST': 'Bear Cave',
        'EXPLORE': line917,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn8,
        'floor': 'GRAVEL',
    },
    'Rocky Cave 2': {
        'name': 'Rocky Cave 2',
        'intro': line922,
        'map': cave2_map1,
        'discovered': [],
        'SOUTH': 'Rocky Cave 1',
        'EXPLORE': line923,
        'EXAMINE': cave2_examine,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn8,
        'chest': 'CLOSED',
        'floor': 'GRAVEL',
    },
    'Rocky Cave 3': {
        'name': 'Rocky Cave 3',
        'intro': line931,
        'map': cave3_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 1',
        'SOUTH': 'Rocky Cave 4',
        'EXPLORE': line932a,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn8,
        'floor': 'GRAVEL',
    },
    'Rocky Cave 4': {
        'name': 'Rocky Cave 4',
        'intro': line937,
        'map': cave4_map1,
        'discovered': [],
        'NORTH': 'Rocky Cave 3',
        'EAST': 'LOCKED',
        'EXPLORE': line938,
        'EXAMINE': cave4_examine,
        'secrets': ['JUMP', 'FLY', 'DIVE'],
        'special': cave4_special,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn8,
        'boss': ['Hobgoblin Gang'],
        'boss_ambush': cave4_boss_ambush,
        'foe': p22b,
        'LOCK': cave4_lock,
        'floor': 'GRAVEL',
    },
    "Queen's Chamber": {
        'name': "Queen's Chamber",
        'intro': line948,
        'map': cave5_map1,
        'discovered': [],
        'WEST': 'Rocky Cave 4',
        'EXPLORE': line950,
        'spawn_rate': 0,
        'boss': ['Goblin Queen'],
        'boss_ambush': cave5_boss_ambush,
        'foe': p23,
        'floor': 'GRAVEL',
    },  
    #Dungeon 1 end
  
    #Waterfall start
    'Serpent River': {
        'name': 'Serpent River',
        'intro': line1201,
        'map': river_map1,
        'discovered': [],
        'NORTH': 'Echobo Lake',
        'EAST': 'Pinerift Forest - WEST',
        'SOUTH': 'Waterfall Pool',
        'SECRET_ROUTE': 'River - West Bank',
        'EXPLORE': line1202,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'special': river_special,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn5,
        'event': 0,
        'floor': 'GRASS',
    },
    'Waterfall Pool': {
        'name': 'Waterfall Pool',
        'intro': line1301,
        'map': waterfall_map1,
        'discovered': [],
        'NORTH': 'Serpent River',
        'EXPLORE': line1302,
        'EXAMINE': waterfall_examine,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'special': river_special,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn5,
        'chest': 'CLOSED',
        'event': 0,
        'floor': 'GRASS',
    },
    'Waterfall Cave 1': {
        'name': 'Waterfall Cave 1',
        'intro': line1312,
        'map': waterfallcave1_map1,
        'discovered': [],
        'NORTH': 'Waterfall Pool',
        'SOUTH': 'Waterfall Cave 2',
        'WEST': 'Waterfall Cave 4',
        'EXPLORE': line1313,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn23,
        'floor': 'GRAVEL',
    },
    'Waterfall Cave 2': {
        'name': 'Waterfall Cave 2',
        'intro': line1314,
        'map': waterfallcave2_map1,
        'discovered': [],
        'NORTH': 'Waterfall Cave 1',
        'SOUTH': 'LOCKED',
        'SECRET_ROUTE': 'Waterfall Cave 4',
        'EXPLORE': line1315,
        'EXAMINE': waterfallcave2_examine,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn23,
        'LOCK': waterfallcave2_lock,
        'event': 0,
        'floor': 'GRAVEL',
    },
    'Waterfall Cave 3': {
        'name': 'Waterfall Cave 3',
        'intro': line1322,
        'map': waterfallcave3_map1,
        'discovered': [],
        'NORTH': 'Waterfall Cave 2',
        'EXPLORE': line1323,
        'EXAMINE': waterfallcave3_examine,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn23,
        'boss': ['River Serpent'],
        'event': 0,
        'floor': 'GRAVEL',
    },
    'Waterfall Cave 4': {
        'name': 'Waterfall Cave 4',
        'intro': line1329,
        'map': waterfallcave4_map1,
        'discovered': [],
        'EAST': 'Waterfall Cave 1',
        'EXPLORE': line1330,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 0,
        'floor': 'GRAVEL',
    },
    #Waterfall end
    
    'Echobo Lake': {
        'name': 'Echobo Lake',
        'intro': line1401,
        'map': lake_map1,
        'discovered': [],
        'NORTH': 'Boat House',
        'EAST': 'LOCKED',
        'SOUTH': 'Serpent River',
        'EXPLORE': line1402,
        'EXAMINE': lake_examine,
        'secrets': ['JUMP', 'SWIM', 'DIVE'],
        'special': lake_special,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn5,
        'foe': p16,
        "LOCK": lake_lock,
        'floor': 'GRASS',
    },
    'Boat House': {
        'name': 'Boat House',
        'intro': line1501,
        'map': boat_map1,
        'discovered': [],
        'SOUTH': 'Echobo Lake',
        'EXPLORE': line1502,
        'SPEAK': boat_speak,
        'speech': 0,
        'spawn_rate': 0,
        'floor': 'GRASS',
    },
  
    'Berry Patch': {
        'name': 'Berry Patch',
        'intro': line1001,
        'map': berry_map1,
        'discovered': [],
        'NORTH': 'Rocky Hill',
        'EAST': 'Flower Meadow',
        'EXPLORE': line1002,
        'EXAMINE': berry_examine,
        'secrets': ['WAIT', 'PICK'],
        'special': berry_special,
        'secret_path': 0,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn3,
        'foe': p15b,
        'chest': 'CLOSED',
        'floor': 'GRASS',
    },
    'Flower Meadow': {
        'name': 'Flower Meadow',
        'intro': line1701,
        'map': meadow_map1,
        'discovered': [],
        'NORTH': "Witch's Cabin",
        'EAST': 'Great Oak',
        'SOUTH': 'Quiet Village',
        'WEST': 'Berry Patch',
        'EXPLORE': line1702,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn9,
        'foe': None,
        'chest': None,
        'event': None,
        'floor': 'GRASS',
    },
    "Witch's Cabin": {
        'name': "Witch's Cabin",
        'intro': line2401,
        'map': witch_map1,
        'discovered': [],
        'SOUTH': 'Flower Meadow',
        'EXPLORE': line2402,
        'SPEAK': witch_speak,
        'CRAFT': witch_crafting,
        'speech': 0,
        'crafting': 'INACTIVE',
        'spawn_rate': 0,
        'event': 0,
        'floor': 'FOLIAGE',
    },
    #Quite Village start
    'Quiet Village': {
        'name': 'Quiet Village',
        'intro': line1801,
        'map': village_map1,
        'discovered': [],
        'NORTH': 'Flower Meadow',
        'EAST': 'Farm House',
        'SOUTH': 'Tavern & Inn',
        'WEST': "Smith's Workshop",
        'EXPLORE': line1802,
        'spawn_rate': 0,
        'floor': 'GRASS',
    },
    'Tavern & Inn': {
        'name': 'Tavern & Inn',
        'intro': line401b,
        'map': tavern_map1,
        'discovered': [],
        'NORTH': 'Quiet Village',
        'EXPLORE': line404b,
        'SPEAK': villageinn_speak,
        'REST': city_inn,
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'STONE',
    },
    "Smith's Workshop": {
        'name': "Smith's Workshop",
        'intro': line1901,
        'map': smith_map1,
        'discovered': [],
        'EAST': 'Quiet Village',
        'EXIT': 'Quiet Village',
        'EXPLORE': line1902,
        'SPEAK': smith_speak,
        'UPGRADE': smithing_upgrade,
        'speech' : 0,
        'upgrade_cost': 75,
        'spawn_rate': 0,
        'event': 0,
        'floor': 'STONE',
    },
    'Farm House': {
        'name': 'Farm House',
        'intro': line2201,
        'map': farm_map1,
        'discovered': [],
        'WEST': 'Quiet Village',
        'EXPLORE': line2202,
        'SPEAK': farm_speak,
        'speech': 0,
        'spawn_rate': 0,
        'floor': 'GRASS',
    },
    #Quite Village end
  
    'Great Oak': {
        'name': 'Great Oak',
        'intro': line2001,
        'map': oak_map1,
        'discovered': [],
        'WEST': 'Flower Meadow',
        'CLIMB': 'Bee Hive',
        'EXPLORE': line2002,
        'EXAMINE': oak_examine,
        'spawn_rate': 0,
        'floor': 'GRASS',
    },
    'Bee Hive': {
        'name': 'Bee Hive',
        'intro': line2104,
        'map': hive_map1,
        'discovered': [],
        'EXIT': 'Great Oak',
        'CLIMB': 'Great Oak',
        'EXPLORE': line2105,
        'EXAMINE': hive_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn10,
        'boss': ['Giant Bee Queen'],
        'boss_ambush': hive_boss_ambush,
        'foe': p24,
        'chest': "CLOSED",
        'floor': 'STONE',
    },
  
    'Mushroom Grove': {
        'name': 'Mushroom Grove',
        'intro': line1601,
        'map': mushroom_map1,
        'discovered': [],
        'NORTH': 'Rotting Woods',
        'SOUTH': 'Fairy Circle',
        'WEST': 'Echobo Lake',
        'EXPLORE': line1602,
        'EXAMINE': mushroom_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn7,
        #'LOCK' : None,
        'chest': "CLOSED",
        #'event' : None,
        'floor': 'FOLIAGE',
    },    
    'Fairy Circle': {
        'name': 'Fairy Circle',
        'intro': line2901,
        'map': fairy_map1,
        'discovered': [],
        'NORTH': 'Mushroom Grove',
        'EXPLORE': line2902,
        'EXAMINE': fairy_examine,
        'SPEAK': fairy_speak,
        'speech': 0,
        'spawn_rate': 0,
        'boss': ["Dark Fairy Prince"],
        'foe': p40,
        'fairy_reward': 5,
        'floor': 'FOLIAGE',
    },
    'Rotting Woods': {
        'name': 'Rotting Woods',
        'intro': line2601,
        'map': rot_map1,
        'discovered': [],
        'NORTH': 'Frog Marsh',
        'SOUTH': 'Mushroom Grove',
        'WEST': 'Rotten Swamp 1',
        'EXPLORE': line2602,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn11,
        'floor': 'FOLIAGE',
    },
    'Rotting Woods - EAST': {
        'name': 'Rotting Woods - EAST',
        'intro': line2604,
        'map': rot2_map1,
        'discovered': [],
        'NORTH': 'Hidden Shrine',
        'WEST': 'Rotting Woods',
        'EXPLORE': line2605,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn11,
        'floor': 'FOLIAGE',
    },
    'Hidden Shrine': {
        'name': 'Hidden Shrine',
        'intro': line2607,
        'map': rot3_map1,
        'discovered': [],
        'SOUTH': 'Rotting Woods - EAST',
        'EXPLORE': line2609,
        'EXAMINE': rotshrine_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn11,
        'event' : 0,
        'floor': 'FOLIAGE',
    },

    #Ogre Dungeon start
    'Rotten Swamp 1': {
        'name': 'Rotten Swamp 1',
        'intro': line2701,
        'map': swamp1_map1,
        'discovered': [],
        'EAST': 'Rotting Woods',
        'WEST': 'Rotten Swamp 2',
        'EXPLORE': line2702,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn12,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 2': {
        'name': 'Rotten Swamp 2',
        'intro': line2703,
        'map': swamp2_map1,
        'discovered': [],
        'EAST': 'Rotten Swamp 1',
        'SOUTH': 'Rotten Swamp 6',
        'WEST': 'Rotten Swamp 3',
        'EXPLORE': line2704,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn13,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 3': {
        'name': 'Rotten Swamp 3',
        'intro': line2705,
        'map': swamp3_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 4',
        'EAST': 'Rotten Swamp 2',
        'SOUTH': 'Rotten Swamp 5',
        'EXPLORE': line2706,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn13,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 4': {
        'name': 'Rotten Swamp 4',
        'intro': line2707,
        'map': swamp4_map1,
        'discovered': [],
        'SOUTH': 'Rotten Swamp 3',
        'EXPLORE': line2708,
        'EXAMINE': swamp4_examine,
        'event': 0,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn12,
        'foe': p29b,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 5': {
        'name': 'Rotten Swamp 5',
        'intro': line2717,
        'map': swamp5_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 3',
        'EAST': 'Rotten Swamp 6',
        'SOUTH': 'Rotten Swamp 8',
        'WEST': 'Rotten Swamp 7',
        'EXPLORE': line2718,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn13,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 6': {
        'name': 'Rotten Swamp 6',
        'intro': line2719,
        'map': swamp6_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 2',
        'WEST': 'Rotten Swamp 5',
        'EXPLORE': line2720,
        'special': swamp_special,
        'secrets': ['DRINK', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn14,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 7': {
        'name': 'Rotten Swamp 7',
        'intro': line2723,
        'map': swamp7_map1,
        'discovered': [],
        'EAST': 'Rotten Swamp 5',
        'EXPLORE': line2724,
        'special': swamp7_special,
        'secrets': [ 'DRINK', 'SWIM', 'DIVE', 'RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO'],
        'secret_path': 0,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn12,
        'event': 0,
        'floor': 'FOLIAGE',
    },
    'Rotten Swamp 8': {
        'name': 'Rotten Swamp 8',
        'intro': line2727,
        'map': swamp8_map1,
        'discovered': [],
        'NORTH': 'Rotten Swamp 5',
        'EXPLORE': line2728,
        'special': swamp8_special,
        'secrets': ['PLAY', 'DRINK', 'SWIM', 'DIVE'],
        'secret_path': 0,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn13,
        'foe': p35,
        'event': 0,
        'floor': 'FOLIAGE',
    },
    #Ogre Dungeon End
  
    'Frog Marsh': {
        'name': 'Frog Marsh',
        'intro': line2801,
        'map': marsh_map1,
        'discovered': [],
        'EAST': 'Grassy Plains',
        'SOUTH': 'Rotting Woods',
        'EXPLORE': line2802,
        'SPEAK': marsh_speak,
        'speech': 0,
        'spawn_rate': 0,
        'floor': 'STONE',
    },
    'Grassy Plains': {
        'name': 'Grassy Plains',
        'intro': line3001,
        'map': plains_map1,
        'discovered': [],
        'NORTH': 'Northern Coast',
        'EAST': 'Foot Hills',
        'WEST': 'Frog Marsh',
        'EXPLORE': line3002,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn17,
        'floor': 'GRASS',
    },
    'Foot Hills': {
        'name': 'Foot Hills',
        'intro': line3101,
        'map': foothills_map1,
        'discovered': [],
        'NORTH': 'Shipwreck',
        'WEST': 'Grassy Plains',
        'EXPLORE': line3102,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn18,
        'floor': 'GRASS',
    },
    'Northern Coast': {
        'name': 'Northern Coast',
        'intro': line3201,
        'map': coast_map1,
        'discovered': [],
        'EAST': 'Shipwreck',
        'SOUTH': 'Grassy Plains',
        'WEST': 'Harbor Town',
        'EXPLORE': line3202,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn16,
        'floor': 'GRAVEL',
    },
    'Shipwreck': {
        'name': 'Shipwreck',
        'intro': line3301,
        'map': shipwreck_map1,
        'discovered': [],
        'SOUTH': 'Foot Hills',
        'WEST': 'Northern Coast',
        'EXPLORE': line3302,
        'EXAMINE': shipwreck_examine,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn16,
        'chest': 'CLOSED',
        'event': 0,
        'floor': 'GRAVEL',
    },
  
    #Harbor Town Start
    'Harbor Town': {
        'name': 'Harbor Town',
        'intro': line3401,
        'map': harbor1_map1,
        'discovered': [],
        'NORTH': 'Harbor Markets',
        'EAST': 'Northern Coast',
        'WEST': 'Harbor Inn',
        'EXPLORE': line3402,
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'GRAVEL',
    },
    'Harbor Inn': {
        'name': 'Harbor Inn',
        'intro': line401c,
        'map': harborinn_map1,
        'discovered': [],
        'EAST': 'Harbor Town',
        'EXIT': 'Harbor Town',
        'EXPLORE': line404c,
        'REST': city_inn,
        'spawn_rate': 0,
        'floor': 'STONE',
        'speech': 0,
    },
    'Harbor Markets': {
        'name': 'Harbor Markets',
        'intro': line302,
        'map': harbormarket_map1,
        'discovered': [],
        'EAST': 'Harbor Temple',
        'SOUTH': 'Harbor Town',
        'WEST': 'Docked Ship',
        'EXPLORE': line303,
        'SPEAK': harborshop_speak,
        'BUY': shop_menu,
        'SELL': selling_to_Shopkeeper,
        'spawn_rate': 0,
        'speech': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'SALINE', 'WARP CRYSTAL', 'KINDLING', 'MAP','CRAFTING POUCH','DRAGON SCALE','EXTRA POUCH','ARMING SWORD', 'PARMA', 'BASCINET', 'BRIGANDINE', 'OLD CUIRASS', 'GREAVES', 'GORGET',],
        'floor': 'GRAVEL',   
    },
    'Docked Ship': {
        'name': 'Docked Ship',
        'intro': line3501,
        'map': harborship_map1,
        'discovered': [],
        'EAST': 'Harbor Markets',
        'EXPLORE': line3502,
        'SPEAK': ship_speak,
        'speech': 0,
        'spawn_rate': 0,
        'event': 0,
        'floor': 'GRAVEL',
    },
    'Alchemist Shop': {
        'name': 'Alchemist Shop',
        'intro': line3601,
        'map': alchemist_map1,
        'discovered': [],
        'NORTH': 'Harbor Town',
        'EXPLORE': line3602,
        'SPEAK': alchemist_speak,
        'BUY': alchemist_buy,
        'SELL': alchemist_sell,
        'speech': 0,
        'crafting': 'INACTIVE',
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 0,
        'floor': 'STONE',
    },
    'Harbor Temple': {
        'name': 'Harbor Temple',
        'intro': line3403,
        'map': harborshrine_map1,
        'discovered': [],
        'WEST': 'Harbor Markets',
        'EXPLORE': line3404,
        'SPEAK': harbortemple_speak,
        'PRAY': shrine_pray,
        'speech': 0,
        'spawn_rate': 0,
        'floor': 'STONE',
    },
    #Harbor Town end
  
    'Western Lake': {
        'name': 'Western Lake',
        'intro': line3701,
        'map': westlake_map1,
        'discovered': [],
        'WEST': 'Rotten Swamp 8',
        'SOUTH': 'River - West Bank',
        'EXPLORE': line3702,
        'secrets': [],
        'secret_path': 0,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn19,
        'floor': 'GRASS',
    },
    'River - West Bank': {
        'name': 'River - West Bank',
        'intro': line3801,
        'map': westriver_map1,
        'discovered': [],
        'NORTH': 'Western Lake',
        'SOUTH': 'Fae Woods - EAST',
        'SECRET_ROUTE': 'Serpent River',
        'EXPLORE': line3802,
        'EXAMINE': riverwest_examine,
        'secrets': [],
        'secret_path': 0,
        'special': riverwest_special,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn20,
        'event': 0,
        'floor': 'GRASS',
    },
  
    #Fae Woods start 
    'Fae Woods - EAST': {
        'name': 'Fae Woods - EAST',
        'intro': line3901,
        'map': faeeast_map1,
        'discovered': [],
        'NORTH': 'River - West Bank',
        'WEST': 'Fae Woods - Camp',
        'EXPLORE': line3902,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn21,
        'boss': ['Rogue Gang'],
        'boss_ambush': faeeast_boss_ambush,
        'floor': 'FOLIAGE',
    },
    'Fae Woods - Camp': {
        'name': 'Fae Woods - Camp',
        'intro': line4001,
        'map': faecamp_map1,
        'discovered': [],
        'NORTH': 'Crescent Pond',
        'EAST': 'Fae Woods - EAST',
        'WEST': 'Fae Woods - WEST',
        'EXPLORE': line4003,
        'REST': camp_rest,
        'spawn_rate': 0,
        'boss': ['Rogue Gang'],
        'boss_ambush': faecamp_boss_ambush,
        'fire': 3,
        'Maxfire': 3,
        'fireTalk': line105,
        'floor': 'FOLIAGE',
    },
    'Crescent Pond': {
        'name': 'Crescent Pond',
        'intro': line4101,
        'map': crescentlake_map1,
        'discovered': [],
        'SOUTH': 'Fae Woods - Camp',
        'EXPLORE': line4102,
        'secrets': ['THROW WEAPON'],
        'special': crescent_special,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn21,
        'boss': ['Naga'],
        'event': None,
        'floor': 'FOLIAGE',
    },
    'Fae Woods - WEST': {
        'name': 'Fae Woods - WEST',
        'intro': line4201,
        'map': faewest_map1,
        'discovered': [],
        'EAST': 'Fae Woods - Camp',
        'SOUTH': 'Fae Woods - SOUTH',
        'EXPLORE': line4202,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn22,
        'floor': 'FOLIAGE',
    },
    'Fae Woods - SOUTH': {
        'name': 'Fae Woods - SOUTH',
        'intro': line4301,
        'map': faesouth_map1,
        'discovered': [],
        'NORTH': 'Fae Woods - WEST',
        'SOUTH': 'Mountain Pass',
        'EXPLORE': line4302,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn21,
        'floor': 'FOLIAGE',
    },
    #Fae Woods end
  
    'Mountain Pass': {
        'name': 'Mountain Pass',
        'intro': line4401,
        'map': mountainpass_map1,
        'discovered': [],
        'NORTH': 'Fae Woods - SOUTH',
        'EAST': "Dwarf's Workshop",
        'SOUTH': 'Drake Mountains 1',
        'EXPLORE': line4402,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn24,
        'floor': 'GRAVEL',
    },
    "Dwarf's Workshop": {
        'name': "Dwarf's Workshop",
        'intro': line4501,
        'map': dwarf_map1,
        'discovered': [],
        'EAST': 'Dwarf Village',
        'WEST': 'Mountain Pass',
        'EXPLORE': line4503,
        'SPEAK': dwarf_speak,
        'speech': 0,
        'secrets': [],
        'spawn_rate': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'SALINE', 'BROAD SWORD', 'SIDE SWORD', 'HANGER', 'SALLET', 'CUISSES', 'ORICHALCUM BRIGANDINE'],
        'event': 0,
        'event2' : 0,
        'floor': 'GRAVEL',
    },
    'Dwarf Village': {
        'name': 'Dwarf Village',
        'intro': line4511, 
        'map': dwarfvillage_map1, 
        'discovered': [],
        'NORTH': 'Dwarf Village - Inn',
        'WEST':  "Dwarf's Workshop",
        'EXPLORE': line5412,
        'SPEAK': dwarfvillage_speak, 
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'GRASS',
    },
    'Dwarf Village - Inn': {
        'name': 'Dwarf Village - Inn',
        'intro': line401d, 
        'map': dwarfinn_map1, 
        'discovered': [],
        'SOUTH': 'Dwarf Village',
        'EXPLORE': line404d,  
        'SPEAK': dwarfinn_speak, 
        'REST': city_inn,
        'spawn_rate': 0,
        'speech': 0,
        'floor': 'STONE',
    },

    #Drake Mountain Dungeon start
    'Drake Mountains 1': {
        'name': 'Drake Mountains 1',
        'intro': line4601,
        'map': drake1_map1,
        'discovered': [],
        'NORTH': 'Mountain Pass',
        'SOUTH': 'Drake Mountains 2',
        'EXPLORE': line4602,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn25,
        'floor': 'GRAVEL',
    },
    'Drake Mountains 2': {
        'name': 'Drake Mountains 2',
        'intro': line4603,
        'map': drake2_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 1',
        'EAST': 'Drake Mountains 3',
        'EXPLORE': line4604,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn25,
        'floor': 'GRAVEL',
    },
    'Drake Mountains 3': {
        'name': 'Drake Mountains 3',
        'intro': line4605,
        'map': drake3_map1,
        'discovered': [],
        'EAST': 'Drake Mountains 4',
        'WEST': 'Drake Mountains 2',
        'SECRET_ROUTE': None,
        'EXPLORE': line4606,
        'secrets': ['TANNINIM'],
        'special': drake_special,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn25,
        'event': 0,
        'floor': 'GRAVEL',
    },
    'Drake Mountains 4': {
        'name': 'Drake Mountains 4',
        'intro': line4608,
        'map': drake4_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 5',
        'WEST': 'Drake Mountains 3',
        'EXPLORE': line4609,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn25,
        'floor': 'GRAVEL',
    },
    'Drake Mountains 5': {
        'name': 'Drake Mountains 5',
        'intro': line4610,
        'map': drake5_map1,
        'discovered': [],
        'SOUTH': 'Drake Mountains 4',
        'EXPLORE': line4611,
        'spawn_rate': 9,
        'enemy_spawn_set': enemy_spawn25,
        'floor': 'GRAVEL',
    },
    'Drake Mountains Summit': {
        'name': 'Drake Mountains Summit',
        'intro': line4612,
        'map': drake6_map1,
        'discovered': [],
        'NORTH': 'Drake Mountains 3',
        'EXPLORE': line4614,
        'secrets': ['TANNINIM'],
        'secret_path': 0,
        'special': dragon_boss_ambush,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': ["Dragon King, Tanninim"],
        'foe': None,
        'event': None,
        'floor': 'GRAVEL',
    },
    #Drake Mountain Dungeon end

    #Deep Woods start
    'Deep Woods - Entrance': {
        'name': 'Deep Woods - Entrance',
        'intro': line4701,
        'map': deepwoodsentrance_map1,
        'discovered': [],
        'NORTH' : 'Deep Woods - SOUTH',
        'WEST': 'Mystic Shrine',
        'EXPLORE': line4702,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn15,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - SOUTH': {
        'name': 'Deep Woods - SOUTH',
        'intro': line4703,
        'map': deepwoodssouth_map1,
        'discovered': [],
        'NORTH' : 'Deep Woods - Fork',
        'SOUTH': 'Deep Woods - Entrance',
        'EXPLORE': line4704,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn15,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - Fork': {
        'name': 'Deep Woods - Fork',
        'intro': line4705,
        'map': deepwoodsfork_map1,
        'discovered': [],
        'EAST' : 'LOCKED',
        'SOUTH': 'Deep Woods - SOUTH',
        'WEST': 'Deep Woods - WEST',
        'EXPLORE': line4706,
        'EXAMINE' : deepwoodsfork_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn15,
        'LOCK': deepwoodsfork_lock,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - WEST': {
        'name': 'Deep Woods - WEST',
        'intro': line4712,
        'map': deepwoodswest_map1,
        'discovered': [],
        'NORTH' : 'LOCKED',
        'EAST': 'Deep Woods - Fork',
        'SOUTH': 'Deep Woods - Forest Hut',
        'EXPLORE': line4713,
        'EXAMINE' : deepwoodswest_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn15,
        'LOCK': deepwoodswest_lock,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - Forest Hut': {
        'name': 'Deep Woods - Forest Hut',
        'intro': line4722,
        'map': deepwoodshut_map1,
        'discovered': [],
        'NORTH': 'Deep Woods - WEST',
        'EXPLORE': line4725,
        'SPEAK': kobold_speak,
        'speech': 0,
        'secrets': [],
        'special': kobold_special,
        'spawn_rate': 0,
        'items': ['POTION', 'ANTIDOTE', 'ETHER', 'SMOKE BOMB', 'SALINE', 'WARP CRYSTAL', 'KINDLING', 'MAP', 'LANTERN', 'MAIN GAUCHE', 'STEEL MAIL', 'FEATHER CAP', 'GORGET', ],
        'items2': ['PAINTED SNAIL', 'SLEEPY SQUIRELL', 'WET TOAD'],
        'event': 0,
        'event2': 0,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - Fallen Hive': {
        'name': 'Deep Woods - Fallen Hive',
        'intro': 'place holder txt',
        'map': deepwoodshive_map1,
        'discovered': [],
        'NORTH': 'Tattered Hive',
        'SOUTH': 'Deep Woods - WEST',
        'EXPLORE': 'place holder txt',
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn15,
        'floor': 'FOLIAGE',
    },
    'Tattered Hive': {
        'name': 'Tattered Hive',
        'intro': line4801,
        'map': hive2_map1,
        'discovered': [],
        'SOUTH': 'Deep Woods - Fallen Hive',
        'EXPLORE': line4802,
        'EXAMINE': tatteredhive_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn15,
        'event': 0,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - EAST': {
        'name': 'Deep Woods - EAST',
        'intro': line4739,
        'map': deepwoodseast_map1,
        'discovered': [],
        'NORTH': 'Deep Woods - NORTH',
        'EAST' : 'Misty Woods - NORTH',
        'WEST': 'Deep Woods - Fork',
        'EXPLORE': line4740,
        'spawn_rate': 2,
        'enemy_spawn_set': enemy_spawn15,
        'floor': 'FOLIAGE',
    },
    'Deep Woods - NORTH': {
        'name': 'Deep Woods - NORTH',
        'intro': line4741,
        'map': deepwoodsnorth_map1,
        'discovered': [],
        'NORTH' : 'Outer Fortress',
        'SOUTH': 'Deep Woods - EAST',
        'EXPLORE': line4742,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn15,
        'floor': 'FOLIAGE',
    },
    #Deep Woods end

    #Orc Fortress Start
    'Outer Fortress': {
        'name': 'Outer Fortress',
        'intro': line4901,
        'map': outerfortress_map1,
        'discovered': [],
        'NORTH' : 'Orc Fortress 1',
        'SOUTH': 'Deep Woods - NORTH',
        'EXPLORE': line4902,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'floor': 'GRAVEL',
    },
    'Orc Fortress 1': {
        'name': 'Orc Fortress 1',
        'intro': line4903,
        'map': orcfort1_map1,
        'discovered': [],
        'NORTH' : 'LOCKED',
        'EAST' : 'Orc Fortress 2',
        'SOUTH': 'Outer Fortress',
        'EXPLORE': line4904,
        'EXAMINE' : orc1_examine,  
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'LOCK': orc1_lock,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'event2' : 0,
        'floor': 'GRAVEL',
    },
    'Orc Fortress 2': {
        'name': 'Orc Fortress 2',
        'intro': line4918,
        'map': orcfort2_map1,
        'discovered': [],
        'NORTH' : 'Orc Fortress 5',
        'EAST': 'Orc Fortress 3',
        'WEST' : 'Orc Fortress 1',
        'EXPLORE': line4919,
        'EXAMINE': orc2_examine,
        'special': orc2_special,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        #'boss_ambush': None,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'chest': 0,
        'floor': 'GRAVEL',
    },
    'Orc Fortress 3': {
        'name': 'Orc Fortress 3',
        'intro': line4932,
        'map': orcfort3_map1,
        'discovered': [],
        'NORTH' : 'Orc Fortress 4',
        'WEST' : 'Orc Fortress 2',
        'EXPLORE': line4933,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'floor': 'GRAVEL',
    },
    'Orc Fortress 4': {
        'name': 'Orc Fortress 4',
        'intro': line4935,
        'map': orcfort4_map1,
        'discovered': [],
        'SOUTH': 'Orc Fortress 3',
        'WEST' : 'Orc Fortress 5',
        'EXPLORE': line4936,
        'EXAMINE' : orc4_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'event2' : 0,
        'chest': 0,
        'floor': 'GRAVEL',
    },
    'Orc Fortress 5': {
        'name': 'Orc Fortress 5',
        'intro': line4951,
        'map': orcfort5_map1,
        'discovered': [],
        'EAST' : 'Orc Fortress 4',
        'SOUTH': 'Orc Fortress 2',
        'EXPLORE': line4952,
        'EXAMINE': orc5_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'ambush': orc1_ambush,
        'ambush_pass': 0,
        'event' : 0,
        'event2' : 0,
        'chest': 0,
        'spawn_modifier': 0,
        'floor': 'GRAVEL',
    },
    'Orc Keep': {
        'name': 'Orc Keep',
        'intro': line4971,
        'map': orcfort6_map1,
        'discovered': [],
        'SOUTH': 'Orc Fortress 1',
        'EXPLORE': line4972,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss_ambush': orckeep_boss_ambush,
        'boss': ["Orc King, Kargath"],
        'event' : 0,
        'floor': 'STONE',
    },
    #Orc Fortress End

    #Misty Woods Start
    'Misty Woods - NORTH': {
        'name': 'Misty Woods - NORTH',
        'intro': line5001,
        'map': mistnorth_map1,
        'discovered': [],
        'SOUTH': 'Misty Woods - Central',
        'WEST': 'Deep Woods - EAST',
        'EXPLORE': line5002,
        #'EXAMINE': None,
        #'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': [],
        #'boss_ambush': None,
        #'ambush': None,
        #'items': [],
        #'foe': None,
        #'LOCK': None,
        #'chest': None,
        #'event': None,
        'floor': 'FOLIAGE',
    },
    'Misty Woods - Central': {
        'name': 'Misty Woods - Central',
        'intro': line5005,
        'map': mistcentral_map1,
        'discovered': [],
        'NORTH': 'Misty Woods - NORTH',
        'SOUTH': 'LOCKED',
        'WEST': 'Misty Woods - Camp',
        'EXPLORE': line5006,
        'LOCK' : mistywoodsCentral_lock,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn30,
        'floor': 'FOLIAGE',
    },
    'Misty Woods - Camp': {
        'name': 'Misty Woods - Camp',
        'intro': line5008,
        'map': mistcamp_map1,
        'discovered': [],
        'EAST': 'Misty Woods - Central',
        'EXPLORE': line5009,
        'REST': camp_rest,
        'fire': 3,
        'Maxfire': 3,
        'fireTalk': line105,
        'spawn_rate': 0,
        'floor': 'FOLIAGE',
    },
    'Misty Woods - SOUTH': {
        'name': 'Misty Woods - SOUTH',
        'intro': line5011,
        'map': mistsouth_map1,
        'discovered': [],
        'NORTH': 'Misty Woods - Central',
        'EAST': 'Misty Woods - EAST',
        'EXPLORE': line5012,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn30,
        'floor': 'FOLIAGE',
    },
    'Misty Woods - EAST': {
        'name': 'Misty Woods - EAST',
        'intro': line5013,
        'map': misteast_map1,
        'discovered': [],
        'EAST': 'Forest Palace - Outer Gate',
        'WEST': 'Misty Woods - SOUTH',
        'EXPLORE': line5014,
        'spawn_rate': 0,
        'enemy_spawn_set': enemy_spawn30b,
        'floor': 'FOLIAGE',
    },
    #Misty Woods End

    #Vampire Castle Start
    'Forest Palace - Outer Gate': {
        'name': 'Forest Palace - Outer Gate',
        'intro': line5101,
        'map': vcastle_outer_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 1',
        'WEST': 'Misty Woods - EAST',
        'EXPLORE': line5102,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'foe': None,
        'floor': 'GRAVEL',
    },
    'Forest Palace - 1': {
        'name': 'Forest Palace - 1',
        'intro': line5103,
        'map': vcastle_1_map1,
        'discovered': [],
        'EAST': 'Forest Palace - 2',
        'SOUTH': 'Forest Palace - Outer Gate',
        'WEST': 'Forest Palace - 3',
        'EXPLORE': line5104,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn31,
        'boss': ["Shadow Snatcher"],
        #'boss_ambush': None,
        #'ambush': None,
        'floor': 'STONE',
    },
    'Forest Palace - 2': {
        'name': 'Forest Palace - 2',
        'intro': line5105,
        'map': vcastle_2_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 5',
        'EAST': 'Forest Palace - 6',
        'SOUTH': 'Forest Palace - Dungeon',
        'WEST': 'Forest Palace - 1',
        'EXPLORE': line5106,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn31,
        'floor': 'STONE',
    },
    'Forest Palace - 3': {
        'name': 'Forest Palace - 3',
        'intro': line5107,
        'map': vcastle_3_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 4',
        'EAST': 'Forest Palace - 1',
        'EXPLORE': line5108,
        'EXAMINE': vamp_3_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn31,
        'foe': p94,
        'event': 0, 
        #'ambush': vamp_ambush,
        'floor': 'STONE',
    },
    'Forest Palace - 4': {
        'name': 'Forest Palace - 4',
        'intro': line5109,
        'map': vcastle_4_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 3',
        'EXPLORE': line5110,
        'EXAMINE': vamp_4_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn31,
        'boss': [],
        #'boss_ambush': None,
        #'ambush': None,
        'foe': p87b,
        'LOCK': None,
        'chest': None,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 5': {
        'name': 'Forest Palace - 5',
        'intro': line5112,
        'map': vcastle_5_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 2',
        'WEST': 'LOCKED', #'Forest Palace - 8'
        'EXPLORE': line5113,
        'EXAMINE': vamp_5_examine,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn32,
        'LOCK': vamp_lock2,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - Dungeon': {
        'name': 'Forest Palace - Dungeon',
        'intro': line5121,
        'map': vcastle_dungeon_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 2',
        'EXPLORE': line5122,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn33,
        'foe': None,
        'floor': 'STONE',
    },
    'Forest Palace - 6': {
        'name': 'Forest Palace - 6',
        'intro': line5115,
        'map': vcastle_6_map1,
        'discovered': [],
        'NORTH': 'LOCKED', #Queen's Chamber
        'SOUTH': 'Forest Palace - 7',
        'WEST': 'Forest Palace - 2',
        'EXPLORE': line5116,
        'EXAMINE': vamp_6_examine,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn32,
        'foe': None,
        'LOCK': vamp_lock1,
        'chest': None,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 7': {
        'name': 'Forest Palace - 7',
        'intro': line5117,
        'map': vcastle_7_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 6',
        'EXPLORE': line5118,
        'EXAMINE': vamp_7_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn33,
        'foe': p88,
        'event': 0,
        'event2': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 8': {
        'name': 'Forest Palace - 8',
        'intro': line5126,
        'map': vcastle_8_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 9',
        'EAST': 'Forest Palace - 5',
        'EXPLORE': line5127,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn34,
        #'ambush': vamp_ambush,
        'floor': 'STONE',

    },
    'Forest Palace - 9': {
        'name': 'Forest Palace - 9',
        'intro': line5128,
        'map': vcastle_9_map1,
        'discovered': [],
        'NORTH': "LOCKED", #"Forest Palace - Lord's Chamber"
        'EAST': 'Forest Palace - 10',
        'SOUTH': 'Forest Palace - 8',
        'WEST': 'Forest Palace - 11',
        'EXPLORE': line5129,
        'EXAMINE': vamp_9_examine,
        'spawn_rate': 4,
        'enemy_spawn_set': enemy_spawn33,
        'LOCK': vamp_lock3,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 10': {
        'name': 'Forest Palace - 10',
        'intro': line5130,
        'map': vcastle_10_map1,
        'discovered': [],
        'WEST': 'Forest Palace - 9',
        'EAST': 'LOCKED',
        'EXPLORE': line5131,
        'EXAMINE': vamp_10_examine,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn34,
        'boss': [],
        #'ambush': vamp_ambush,
        'foe': None,
        'LOCK': vamp_lock2,
        'chest': "CLOSED",
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 11': {
        'name': 'Forest Palace - 11',
        'intro': line5134,
        'map': vcastle_11_map1,
        'discovered': [],
        'EAST': 'Forest Palace - 9',
        'WEST': 'Forest Palace - 12',
        'EXPLORE': line5135,
        'EXAMINE': vamp_11_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn34,
        'boss': [],
        #'boss_ambush': None,
        #'ambush': None,
        'foe': p93,
        'LOCK': None,
        'chest': None,
        'event': 0,
        'event2': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 12': {
        'name': 'Forest Palace - 12',
        'intro': line5138,
        'map': vcastle_12_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 14',
        'EAST': 'Forest Palace - 11',
        'SOUTH': 'Forest Palace - 13',
        'EXPLORE': line5139,
        'EXAMINE': vamp_12_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': enemy_spawn33,
        'boss': [],
        #'ambush': vamp_ambush,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 13': {
        'name': 'Forest Palace - 13',
        'intro': line5141,
        'map': vcastle_13_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 12',
        'EXPLORE': line5142,
        'EXAMINE': vamp_13_examine,
        'secrets': ['READ'],
        'special': vamp13_special,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn35,
        'event': 0,
        'event2': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 14': {
        'name': 'Forest Palace - 14',
        'intro': line5145,
        'map': vcastle_14_map1,
        'discovered': [],
        'NORTH': 'LOCKED',
        'SOUTH': 'Forest Palace - 12',
        'EXPLORE': line5146,
        'EXAMINE': vamp_14_examine,
        'spawn_rate': 6,
        'enemy_spawn_set': None,
        'LOCK' : vamp_lock5,
        'event': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 15': {
        'name': 'Forest Palace - 15',
        'intro': line5148,
        'map': vcastle_15_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 14',
        'EXPLORE': line5149,
        'EXAMINE': vamp_15_examine,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'event': None,
        'floor': 'STONE',
    },
    'Forest Palace - 16': {
        'name': 'Forest Palace - 16',
        'intro': line5151,
        'map': vcastle_16_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 17',
        'EAST': 'Forest Palace - 18',
        'WEST': 'Forest Palace - 10',
        'EXPLORE': line5152,
        'EXAMINE': vamp_16_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn34,
        'event': 0,
        'event2': 5,
        'floor': 'STONE',
    },
    'Forest Palace - 17': {
        'name': 'Forest Palace - 17',
        'intro': line5154,
        'map': vcastle_17_map1,
        'discovered': [],
        'EAST': 'Forest Palace - 19',
        'SOUTH': 'Forest Palace - 16',
        'EXPLORE': line5155,
        'EXAMINE': vamp_17_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn34,
        'event': 0,
        'event2': 0,
        'floor': 'STONE',
    },
    'Forest Palace - 18': {
        'name': 'Forest Palace - 18',
        'intro': line5156,
        'map': vcastle_18_map1,
        'discovered': [],
        'NORTH': 'Forest Palace - 19',
        'WEST': 'Forest Palace - 16',
        'EXPLORE': line5157,
        'EXAMINE': vamp_18_examine,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn34,
        'event': 0,
        'event2': 7,
        'floor': 'STONE',
    },
    'Forest Palace - 19': {
        'name': 'Forest Palace - 19',
        'intro': line5158,
        'map': vcastle_19_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 18',
        'WEST': 'Forest Palace - 17',
        'EXPLORE': line5159,
        'EXAMINE': vamp_19_examine,
        'special': None,
        'spawn_rate': 5,
        'enemy_spawn_set': enemy_spawn34,
        'event': 0,
        'event2': 3,
        'floor': 'STONE',
    },
    "Forest Palace - Queen's Chamber": {
        'name': "Forest Palace - Queen's Chamber",
        'intro': line5123,
        'map': vcastle_queen_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 6',
        'EXPLORE': line5124,
        'EXAMINE': vamp_queen_examine,
        'spawn_rate': 0,
        'boss': ['Vampire Queen'],
        'foe': p91,
        'event': 0,
        'floor': 'STONE',
    },
    "Forest Palace - Lord's Chamber": {
        'name': "Forest Palace - Lord's Chamber",
        'intro': line5162,
        'map': vcastle_lord_map1,
        'discovered': [],
        'SOUTH': 'Forest Palace - 9',
        'EXPLORE': line5163,
        'EXAMINE': vamp_lord_examine,
        'SPEAK': vampLord_speak,
        'secrets': ['ATTACK'],
        'special': vampLord_Special,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'foe': p92,
        'event': 0,
        'floor': 'STONE',
    },
    #Vampire Castle End

#Smeldars Tower Start
    'Dense Thicket': {
        'name': 'Dense Thicket',
        'intro': line2501,
        'map': thicket_map1,
        'discovered': [],
        'NORTH': 'LOCKED',
        'SOUTH': 'Pinerift Forest',
        'EXPLORE': line2503,
        'EXAMINE': "PLACE HOLDER TEXT",
        'secrets': [],
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'items': [],
        'foe': None,
        'LOCK':  thicket_lock,
        'event': None,
        'floor': 'FOLIAGE',
    },
    "Smeldars Tower - 1": {
        'name': "Smeldars Tower - 1",
        'intro': line5203,
        'map': smeldarstower1_map1,
        'discovered': [],
        'NORTH': "LOCKED",
        'SOUTH': 'Forest Thicket',
        'EXPLORE': line5204,
        'EXAMINE': tower1_examine,
        'secrets': [],
        'secret_path': 0,
        'special': None,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss': ['Dragon'],
        'boss_ambush': tower_boss0_ambush,
        'LOCK': tower1_lock,
        'event': 0,
        'event2': 0,
        'floor': 'GRAVEL',
    },
    "Smeldars Tower - 2": {
        'name': "Smeldars Tower - 2",
        'intro': line5207,
        'map': smeldarstower2_map1,
        'discovered': [],
        'SOUTH': "Smeldars Tower - 1",
        'WEST': "Smeldars Tower - 3",
        'EXPLORE': line5208,
        'EXAMINE': tower2_examine,
        'secrets': ['ATTACK', 'JUMP'],
        'special': tower2_special,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn36,
        'event': None,
        'floor': 'STONE',
    },
    "Smeldars Tower - 3": {
        'name': "Smeldars Tower - 3",
        'intro': line5210,
        'map': smeldarstower3_map1,
        'discovered': [],
        'NORTH': "Smeldars Tower - 4",
        'EAST': "Smeldars Tower - 2",
        'EXPLORE': line5211,
        'EXAMINE': tower3_examine,
        'spawn_rate': 9,
        'enemy_spawn_set': enemy_spawn36,
        'ambush': tower3_ambush,
        'event': 0,
        'floor': 'STONE',
    },
    "Smeldars Tower - 4": {
        'name': "Smeldars Tower - 4",
        'intro': line5213,
        'map': smeldarstower4_map1,
        'discovered': [],
        'NORTH': "LOCKED",
        'EAST': "LOCKED",
        'SOUTH': "Smeldars Tower - 3",
        'WEST': "LOCKED",
        'SECRET_ROUTE': None,
        'EXPLORE': line5214,
        'EXAMINE': tower4_examine,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn36,
        'LOCK': tower4_lock,
        'event': 0,
        'event2': 0,
        'event3': 0,
        'floor': 'STONE',
    },
    "Smeldars Tower - 5": {
        'name': "Smeldars Tower - 5",
        'intro': line5217,
        'map': smeldarstower5_map1,
        'discovered': [],
        'EAST': "LOCKED",
        'SOUTH': "Smeldars Tower - 4",
        'EXPLORE': line5218,
        'EXAMINE': tower5_examine,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn37,
        'LOCK': tower5_lock,
        'event': 0,
        'floor': 'STONE',
    },
    "Smeldars Tower - 6": {
        'name': "Smeldars Tower - 6",
        'intro': line5221,
        'map': smeldarstower6_map1,
        'discovered': [],
        'SOUTH': "Smeldars Tower - 7",
        'WEST': "Smeldars Tower - 5",
        'EXPLORE': line5222,
        'EXAMINE': tower6_examine,
        'spawn_rate': 9,
        'enemy_spawn_set': enemy_spawn37,
        'floor': 'STONE',
        
    },
    "Smeldars Tower - Hidden Room": {
        'name': 'Smeldars Tower - Hidden Room',
        'intro': line5224,
        'map': smeldarstowerS_map1,
        'discovered': [],
        'SOUTH': 'Smeldars Tower - 6',
        'EXPLORE': line5225,
        'REST': camp_rest,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'event': None,
        'fire': 5,
        'Maxfire': 5,
        'fireTalk': line5226,
        'floor': 'STONE',
    },
    "Smeldars Tower - 7": {
        'name': "Smeldars Tower - 7",
        'intro': line5213b,
        'map': smeldarstower7_map1,
        'discovered': [],
        'NORTH': "Smeldars Tower - 6",
        'EAST': "LOCKED",
        'SOUTH': "LOCKED",
        'WEST': "LOCKED",
        'EXPLORE': line5214,
        'EXAMINE': tower7_examine,
        'spawn_rate': 8,
        'enemy_spawn_set': enemy_spawn38,
        'LOCK': tower7_lock,
        'event': 0,
        'event2': 0,
        'event3': 0,
        'floor': 'STONE',
    },
    "Smeldars Tower - 8": {
        'name': "Smeldars Tower - 8",
        'intro': line5213c,
        'map': smeldarstower8_map1,
        'discovered': [],
        'NORTH': "LOCKED",
        'EAST': "LOCKED",
        'SOUTH': "LOCKED",
        'WEST': "Smeldars Tower - 7",
        'EXPLORE': line5214,
        'EXAMINE': tower8_examine,
        'spawn_rate': 7,
        'enemy_spawn_set': enemy_spawn38,
        'LOCK': tower8_lock,
        'event': 0,
        'event2': 0,
        'event3': 0,
        'floor': 'STONE',
    },
    "Smeldars Tower - 9": {
        'name': "Smeldars Tower - 9",
        'intro': line5227,
        'map': smeldarstower9_map1,
        'discovered': [],
        'NORTH': "Smeldars Throne",
        'SOUTH': "Smeldars Tower - 8",
        'EXPLORE': line5228,
        'spawn_rate': 3,
        'enemy_spawn_set': enemy_spawn38,
        'floor': 'STONE',
    },
    "Smeldars Throne": {
        'name': "Smeldars Throne",
        'intro': placeholderText,
        'map': smeldarstower10_map1,
        'discovered': [],
        'SOUTH': "Smeldars Tower - 9",
        'EXPLORE': placeholderText,
        'spawn_rate': 0,
        'enemy_spawn_set': None,
        'boss_ambush': tower_boss1_ambush,
        'floor': 'STONE',
    },
#Smeldars Tower End 
}


#define player key items
key_items = {
    '': {
        'name': '',
        'description': '',
    },
    'POTION': {
        'name': 'POTION',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 35,
    },
    'ANTIDOTE': {
        'name': 'ANTIDOTE',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 25,
    },
    'ETHER': {
        'name': 'ETHER',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 40,
    },
    'SALINE': {
        'name': 'SALINE',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 50,
    },
    'SMOKE BOMB': {
        'name': 'SMOKE BOMB',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 30,
    },
    'WARP CRYSTAL': {
        'name': 'WARP CRYSTAL',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 100,
    },
    'KINDLING': {
        'name': 'KINDLING',
        'description': None,
        'shop': ['REGULAR', 'TRAVEL'],
        'price': 80,
    },
    'DRAGON SCALE': {
        'name': 'DRAGON SCALE',
        'description': None,
        'purchased': "A genuine dragon scale, taken from a dragon! Or so you've been told...",
        'shop': 'REGULAR',
        'price': 350
    },


  
    'EMPTY': {
        'name': 'blank',
        'description': 'nothing.',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': None,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'RUSTY DAGGER': {
        'name': 'RUSTY DAGGER',
        'description': 'A simple quillon dagger with a dull edge and rusty blade. An awful weapon, but better than nothing... probably.',
        'slot': 'MAIN HAND',
        'ATK': 1,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A basic dagger. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 25,
        'shop': ['SALE'],
        'price': 40,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'MESSER': {
        'name': 'MESSER',
        'description': 'A long single edged sword with a knife like construction. The Friar kept it well maintained over the years.',
        'slot': 'MAIN HAND',
        'ATK': 5,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A well made, single edge sword. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'shop': ['SALE'],
        'price': 75,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'MACE': {
        'name': 'MACE',
        'description': 'A flanged mace with a strudy, full metal construction. The extra heaft adds to its power, but the weapon offers no defensive capabilities.',
        'purchased': 'A sturdy blunt weapon perfect for smashing and bashing.',
        'slot': 'MAIN HAND',
        'ATK': 8,
        'DEF': -3,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 90,
        'FOC': 0,
        'description2': 'A sturdy, flanged mace. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'shop': ['KEY', 'SALE'],
        'price': 100,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'GOBLIN CHOPPER': {
        'name': 'GOBLIN CHOPPER',
        'description': 'A brutish chopping weapon used by Goblins. Comfort was not a thought when crafting this weapon; sharp edges dig into your hand while holding it. The thick construction does make it a durable and powerful weapon, albiet slow to wield.',
        'slot': 'MAIN HAND',
        'ATK': 11,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 90,
        'FOC': 0,
        'description2':
        'A basic, single edge chopping blade. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['SALE'],
        'price': 100,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'OBSIDIAN DAGGER': {
        'name': 'OBSIDIAN DAGGER',
        'description': 'A dagger crafted from obsidian. Not particularly durable, but has a razor sharp edge. ',
        'purchased': 'A most unusual dagger made from volcanic glass. Traded from a far off land.',
        'slot': 'MAIN HAND',
        'ATK': 10,
        'DEF': -2,
        'HP': 0,
        'MP': 3,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2':
        'A fragile, razor sharp obsidian dagger. Usable by any class.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY','TRAVEL', 'SALE'],
        'price': 250,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'KATANA': {
        'name': 'KATANA',
        'description': 'A single edged, curved sword. Normally wielded with two hands, this one is a bit shorter and easily usable in one. Delivers deep cuts, but not very defensive.',
        'purchased': 'A finely crafted katana, perfect for swift and precise strikes. Can\'t slice through time and space though unfortunately.',
        'slot': 'MAIN HAND',
        'ATK': 13,
        'DEF': -2,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A curved, single edge sword. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 75,
        'shop': ['KEY', 'SALE'],
        'price': 275,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'ARMING SWORD': {
        'name': 'ARMING SWORD',
        'description': 'A typical arming sword. Not a fancy weapon by any means, but well crafted and reliable.',
        'purchased': "A common sword. Couldn't get more basic than this.",
        'slot': 'MAIN HAND',
        'ATK': 9,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A quality, arming sword. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 300,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'SILVER BLADE': {
        'name': 'SILVER BLADE',
        'description': 'A finely crafted sword made of silver. Effective against undead creatures.',
        'purchased': 'A sleek silver sword, gleaming with a sharp edge. Perfect for vanquishing undead foes.',
        'slot': 'MAIN HAND',
        'ATK': 12,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A quality, silver blade. Usable by any class.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY','TRAVEL', 'SALE'],
        'price': 500,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'BROAD SWORD': {
        'name': 'BROAD SWORD',
        'description': 'A broad sword with a basket hilt lined with a soft velvet. An elegant, and highly protective blade. The basket hilt does make wielding a little trickier, however.',
        'purchased': 'A protective, double edged sword with a basket hilt. Perfect for protecting those delicate hands.',
        'slot': 'MAIN HAND',
        'ATK': 17,
        'DEF': 8,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A protective, double edge sword. Usable by WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 500,
        'classes': ['GOD','WARRIOR',],
    },
    'SIDE SWORD': {
        'name': 'SIDE SWORD',
        'description': 'An exquisite double edge sword with finger rings on the hilt. Capable of delivering devestating cuts and thrusts.',
        'purchased': "A beautifully crafted, double edged sword with finger rings on the hilt. Look who's fancy now!",
        'slot': 'MAIN HAND',
        'ATK': 19,
        'DEF': 0,
        'HP': 0,
        'MP': 3,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'An exquisite, double edge sword. Usable by WIZARDS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 500,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'HANGER': {
        'name': 'HANGER',
        'description':'A robust single edge blade with a simple knuckle guard. A favorite among sea faring folk as the are great for close quarters combat on ships. You feel extra lucky wielding this sword.',
        'purchased': "A simple naval sword, but sturdy and well made. Makes you feel like a pirate swinging it around!",
        'slot': 'MAIN HAND',
        'ATK': 18,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A fine, single edge sword. Increases GP earned from combat. Usable by THIEVES.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 500,
        'classes': ['GOD', 'THIEF'],
    },
    'MORNING STAR': {
        'name': 'MORNING STAR',
        'description':'A spiked ball mace that is equally intimidating as it is deadly. Perfect against squishy and armored foes alike.',
        'purchased': "A fearsome mace with a spiked ball head. Perfect for crushing your enemies!",
        'slot': 'MAIN HAND',
        'ATK': 21,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 90,
        'FOC': 0,
        'description2': 'A deadly spiked mace. Usable by WARRIORS and WIZARDS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 520,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH',],
    },
    'RAPIER': {
        'name': 'RAPIER',
        'description':'A slender, sharply pointed sword ideal for thrusting attacks. Quick and precise, it excels in the hands of a skilled duelist.',
        'purchased': "A finely crafted rapier, perfect for those who prefer speed and finesse over brute strength.",
        'slot': 'MAIN HAND',
        'ATK': 20,
        'DEF': 5,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A well tempered rapier. Usable by WARRIORS and THIEVES.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 560,
        'classes': ['GOD', 'WARRIOR', 'THIEF',],
    },
    'SERPENT KNIFE': {
        'name': 'SERPENT KNIFE',
        'description':'A curved dagger with a serpent motif. Quick and deadly, it strikes with the precision of a snake.',
        'purchased': "A beautifully crafted dagger, perfect for assassins.",
        'slot': 'MAIN HAND',
        'ATK': 17,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A poisoned dagger. Usable by THIEVES.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 580,
        'classes': ['GOD', 'THIEF'],
    },
    'WAR PICK': {
        'name': 'WAR PICK',
        'description':'A strong pick designed for piercing through armor and shields. A favorite among front line fighters.',
        'purchased': "A sturdy war pick, perfect for shattering enemy defenses.",
        'slot': 'MAIN HAND',
        'ATK': 24,
        'DEF': 0,
        'HP': 0,
        'MP': -6,
        'GR': 0,
        'ACC': 90,
        'FOC': 0,
        'description2': 'A deadly war pick. Usable by WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 520,
        'classes': ['GOD', 'WARRIOR'],
    },
    
    'AETHON': {
        'name': 'AETHON',
        'description': "A falchion crafted from steel sourced from a fallen star. As the wielder's life force wanes, the blade's power surges.",
        'slot': 'MAIN HAND',
        'ATK': 41,
        'DEF': 4,
        'HP': 0,
        'MP': -10,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A mighty falchion of legendary quality. Bonus ATK the lower your HP, reduces max MP. Unlocks skill: BATTLECRY. Usable by WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','WARRIOR',],
    },
    'FULGUR': {
        'name': 'FULGUR',
        'description': 'An arming sword crafted from pure mythril. Embued with powerful magic, this blade gets its name from the way energy surges through the wielders body like lightning.',
        'slot': 'MAIN HAND',
        'ATK': 50,
        'DEF': -10,
        'HP': 0,
        'MP': 10,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A magic arming sword of legendary quality. Increases MP and skill power at the cost of DEF. Unlocks skill: SHOCK. Usable by WIZARDS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','WIZARD','WITCH',],
    },
    'MIDAS': {
        'name': 'MIDAS',
        'description': 'A xiphos crafted from the legendary Dwarven alloy, orichalcum. As ones wealth grows, so too does the strength of this blade. If one were so unfortunate as to lose all their riches however, this sword would just as quickly sap the users power...',
        'slot': 'MAIN HAND',
        'ATK': 44,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'ACC': 95,
        'FOC': 0,
        'description2':
        'A nimble xiphos of legendary quality. Bonus ATK the more GP in wallet, damage penalty for low GP. Unlocks skill: $TOSS. Usable by THEIVES.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','THIEF',],
    },
     'DELPHI': {
        'name': 'DELPHI',
        'description': "A short sword crafted from pure crystal. Enhances one's connection to the Astral Plane, but at a cost...",
        'slot': 'MAIN HAND',
        'ATK': 39,
        'DEF': 4,
        'HP': 0,
        'MP': -15,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A nimble short sword of legendary quality. Bonus ATK to Summons, reduces max MP. Unlocks skill: AETHER. Usable by SUMMONERS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD','SUMMONER',],
    },
    'ADAMANTITE SWORD': {
        'name': 'ADAMANTITE SWORD',
        'description':'A hand and a half sword made from the mythical metal adamantite. Legend states the metal is harvested off the shells of World Tortoise and is said to be stronger and tougher than any other metal. Few weapons can match this blades quality.',
        'slot': 'MAIN HAND',
        'ATK': 40,
        'DEF': 10,
        'HP': 500,
        'MP': 0,
        'GR': 0,
        'ACC': 95,
        'FOC': 0,
        'description2': 'A sword of legendary quality. Usable by any class.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },  
    "SMELDARS BANE": {
        'name': "SMELDARS BANE",
        'description':'A legendary longsword said to have been used to defeat the evil warlock SMELDARS. It was lost many ages ago, when the original forest of the Fae was overcome by darkness. The blade is imbued with powerful magic.',
        'slot': 'MAIN HAND',
        'ATK': 45,
        'DEF': 0,
        'HP': 0,
        'MP': 8,
        'GR': 0,
        'ACC': 95,
        'FOC': 0.5,
        'description2': 'A sword of legendary quality. Usable by any class.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },

  
    'BUCKLER': {
        'name': 'BUCKLER',
        'description':'A small center-grip shield made of hardened steel. Looks like its been a little neglected over the years.',
        'slot': 'OFF HAND',
        'ATK': 0,
        'DEF': 6,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Small shield that improves defenses for all classes',
        'shop': ['SALE'],
        'price': 60,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'PARMA': {
        'name': 'PARMA',
        'description':'A large center-grip shield made of wood and reinforced with a steel rim. The large size offers amazing protection, but at the cost of attack power and stamina.',
        'slot': 'OFF HAND',
        'ATK': -2,
        'DEF': 12,
        'HP': -25,
        'MP': 0,
        'GR': 0,
        'description2': 'Large shield that improves defenses for all classes. Reduces ATK and HP.',
        'shop': ['KEY', 'SALE'],
        'price': 127,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'HEATER SHIELD': {
        'name': 'HEATER SHIELD',
        'description':'A thick shield covered in a layer of steel. Heafty and durable, it provides excellent protection at the cost of some speed.',
        'slot': 'OFF HAND',
        'ATK': -1,
        'DEF': 14,
        'HP': 0,
        'MP': 0,
        'SPD': -3,
        'GR': 0,
        'description2': 'Large shield that improves defenses for all classes. Minor reduction to ATK and SPD.',
        'shop': ['KEY', 'SALE'],
        'price': 127,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'TOWER SHIELD': {
        'name': 'TOWER SHIELD',
        'description':'A massive shield that provides excellent protection, but is heavy and cumbersome.',
        'slot': 'OFF HAND',
        'ATK': -4,
        'DEF': 18,
        'HP': 0,
        'MP': 0,
        'SPD': -5,
        'GR': 0,
        'description2': 'Large shield that improves defenses for WARRIORS. Reduces ATK and SPD.',
        'shop': ['KEY', 'SALE'],
        'price': 127,
        'classes': ['GOD', 'WARRIOR',],
    },
    'STAFF': {
        'name': 'STAFF',
        'description': 'A staff carved from white oak. White oak is known for its magical properties and is prized by mages everywhere.',
        'slot': 'OFF HAND',
        'ATK' : 6,
        'DEF' : 0,
        'HP' : 0,
        'MP' : 6,
        'GR' : 0,
        'FOC' : .5,
        'description2': 'A white oak staff. Enhances ATK and magic abilities, increases MP. Usable by WIZARDS.',
        'shop': 'KEY',
        'price': 600,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'WAND': {
        'name': 'WAND',
        'description': 'A slender wand made from the wood of the white oak. White oak is known for its magical properties and is prized by mages everywhere.',
        'slot': 'OFF HAND',
        'ATK' : 4,
        'DEF' : 0,
        'HP' : 0,
        'MP' : 14,
        'GR' : 0,
        'FOC' : 0,
        'description2': 'A white oak wand. Enhances ATK and magic abilities, increases MP. Usable by WIZARDS and SUMMONERS.',
        'shop': 'KEY',
        'price': 600,
        'classes': ['GOD', 'WIZARD', 'WITCH', 'SUMMONER'],
    },
    'CLOAK': {
        'name': 'CLOAK',
        'description': 'A dark cloak useful for defending and concealing attacks. While not as defensive as a shield, foes would be wise not to underestimate its usefulness in combat...',
        'slot': 'OFF HAND',
        'ATK': 2,
        'DEF': 3,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Offers small increase in protection and power. Causes enemies to miss more frequently. Usable by THIEVES.',
        'shop': 'KEY',
        'price': 600,
        'classes': ['GOD', 'THIEF'],
    },
    'STILETTO': {
        'name': 'STILETTO',
        'description': 'A small, lightweight dagger designed for quick strikes and agility.',
        'slot': 'OFF HAND',
        'ATK': 10,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'SPD': 5,
        'description2': 'Offers small increase in protection and power. Causes enemies to miss more frequently. Usable by THIEVES.',
        'shop': 'KEY',
        'price': 600,
        'classes': ['GOD', 'THIEF'],
    },
    'BATTLE AXE': {
        'name': 'BATTLE AXE',
        'description': 'An single handed axe with a specialized head for combat. A devestating off-hand weapon used by WARRIORS seeking to cast aside extra protection for raw power.',
        'slot': 'OFF HAND',
        'ATK': 14,
        'DEF': -6,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases ATK, reduces DEF. Usable by WARRIORS.',
        'shop': 'KEY',
        'price': 600,
        'classes': ['GOD', 'WARRIOR'],
    },
    'MAIN GAUCHE': {
        'name': 'MAIN GAUCHE',
        'description': 'A specialized dagger made for parrying; the upswept quillons and side-ring are purposefully built for catching opponents blades.',
        'slot': 'OFF HAND',
        'ATK': 4,
        'DEF': 2,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases ATK, chance to parry enemy attack.',
        'shop': ['KEY', 'SALE'],
        'price': 430,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },


    'POINTED HAT': {
        'name': 'POINTED HAT',
        'description': 'A pointed hat with a wide brim. A common piece of fashion among magic users. Some say that the hat acts as a conduit for magical power.',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 2,
        'HP': 0,
        'MP': 8,
        'GR': 0,
        'description2':'Light armor for WIZARDS and SUMMONERS. Boosts MP, but offers little defense',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 130,
        'classes': ['GOD', 'WIZARD', 'WITCH', 'SUMMONER'],
    },
    'COWL': {
        'name': 'COWL',
        'description':'A large, loose hood often used by thieves to conceal their identity. Offers modest protection.',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 4,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Light armor for THIEVES. Boosts GP earned.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 140,
        'classes': ['GOD', 'THIEF'],
    },
    'LEATHER CAP': {
        'name': 'LEATHER CAP',
        'description':'A plain leather cap, commonly worn by travelers. Offers a very modest amount of protection, but is certainly better than nothing!',
        'purchased': 'It might help protect your head from the sun at least?..',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 1.5,
        'HP': 5,
        'MP': 0,
        'GR': 0,
        'description2': 'Light armor for for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 35,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'BASCINET': {
        'name': 'BASCINET',
        'description':'A full face helmet that offers good protection. The pointed visor may look a little silly, but it very well may save your life!',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 9,
        'HP': 175,
        'MP': 0,
        'GR': 0,
        'description2': 'Medium armor by WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 150,
        'classes': ['GOD', 'WARRIOR', ],
    },
    'SALLET': {
        'name': 'SALLET',
        'description': 'A hardened steel helmet with a movable visor. The craftsmanship of this helm is impeccable',
        'purchased': 'This helmet has got a hinged visor to protect your face in battle. Neat, huh?',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 7,
        'HP': 75,
        'MP': 0,
        'GR': 0,
        'description2': 'Medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 350,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'FEATHER CAP': {
        'name': 'FEATHER CAP',
        'description':'A fashionable cap with a feather. Offers nearly no protection, but its brightly coloured feather is said to bring luck and boost the spirits.',
        'purchased': 'A stylish cap that might just bring you some good fortune.',
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 1,
        'HP': 0,
        'MP': 1,
        'GR': .5,
        'description2': 'Light armor for for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 75,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'BARBUTE': {
        'name': 'BARBUTE',
        'description':'A full face helmet that offers good protection. A little hard to see out of the eye slit at times, but highly effective at protecting your nogging.',
        'purchased': "A sturdy helmet that covers your entire head. Don't forget to lift the visor to see!",
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 6,
        'HP': 125,
        'MP': 0,
        'GR': 0,
        'description2': 'Medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 150,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'ARMET': {
        'name': 'ARMET',
        'description':'A full face helmet that offers incredible protection. Made from thick steel plates, this helm is sure to keep your head safe in even the most dire of battles.',
        'purchased': "A formidable helmet that provides excellent protection. Wear it with pride!",
        'slot': 'HEAD',
        'ATK': 0,
        'DEF': 10,
        'HP': 225,
        'MP': 0,
        'GR': 0,
        'description2': 'Heavy armor for WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 800,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'MAGUS HAT': {
        'name': 'MAGUS HAT',
        'description': 'A tall, pointed hat adorned with mystical symbols. Worn by powerful magic users, this hat is said to enhance magical abilities.',
        'purchased': 'A mystical hat that amplifies your magical powers. A little smelly though...',
        'slot': 'HEAD',
        'ATK': 6,
        'DEF': 4,
        'HP': 0,
        'MP': 14,
        'GR': 0,
        'description2':'Light armor for WIZARDS. Boosts MP, but offers little defense',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 800,
        'classes': ['GOD', 'WIZARD', 'WITCH'],
    },
    'BLACK COWL': {
        'name': 'BLACK COWL',
        'description': 'A dark, hooded cloak that shrouds the wearer in shadows. It is said to enhance stealth and luck.',
        'purchased': 'A cloak that helps you blend into the shadows. Perfect for sneaky types.',
        'slot': 'HEAD',
        'ATK': 2,
        'DEF': 6,
        'HP': 0,
        'MP': 2,
        'GR': 1,
        'SPD': 5,
        'description2':'Light armor for THIEVES. Boosts GP gains and SPD.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 800,
        'classes': ['GOD', 'THIEF'],
    },
  
    'MAGIC ROBE': {
        'name': 'MAGIC ROBE',
        'description': 'A flowing blue robe made with gold and silver thread weaved through. Amplifies magical energy when worn.',
        'purchased': 'A mystical robe that enhances your magical abilities.',
        'slot': 'BODY',
        'ATK': 5,
        'DEF': 6,
        'HP': 0,
        'MP': 12,
        'GR': 0,
        'description2': 'Light armor for WIZARDS. Boosts power, but offers little defense',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 850,
        'classes': ['GOD', 'WIZARD', 'WITCH'],
    },
    'GAMBESON': {
        'name': 'GAMBESON',
        'description':'A padded jacket that is easy to repair and move around in. While not as protective as metal, it still offers a fair bit of defense.',
        'purchased': "Don't underestimate this armor just because it looks like a winter jacket!",
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 8,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Light armor for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 75,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'STEEL MAIL': {
        'name': 'STEEL MAIL',
        'description': 'A surprisingly bulky set of armor made from hardened steel rings. Offers a good deal of protection and mobility.',
        'purchased': 'A sturdy steel mail that provides reliable protection.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 10,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Average quality medium armor for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 650,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'BRIGANDINE': {
        'name': 'BRIGANDINE',
        'description':'Armor made from overlapping plates of steel. Offers excellent levels of protection without compromising too much on mobility.',
        'purchased': 'A well crafted brigandine that balances protection and mobility.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 13,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'High quality, medium armor for WARRIORS and THIEVES',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 750,
        'classes': ['GOD', 'WARRIOR', 'THIEF'],
    },
    'OLD CUIRASS': {
        'name': 'OLD CUIRASS',
        'description':'A cuirass with spots of rust and signs of battle damage. This previously used armor is heavy and poorly fitted, but the thick plate offers tremendous protection.',
        'purchased': 'A heavy cuirass that has seen better days, but still offers solid protection.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 16,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'SPD': -3,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 850,
        'classes': ['GOD', 'WARRIOR'],
    },
    'MAGUS ROBES': {
        'name': 'MAGUS ROBES',
        'description':'A flowing blue robe made with gold and silver thread weaved through. Amplifies magical energy when worn.',
        'purchased': 'A mystical robe that enhances your magical abilities.',
        'slot': 'BODY',
        'ATK': 9,
        'DEF': 6,
        'HP': 0,
        'MP': 12,
        'GR': 0,
        'description2': 'legendary quality, light armor for WIZARDS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'shop': ['KEY',],
        'price': 1100,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'ROGUES VEST': {
        'name': 'ROGUES VEST',
        'description':'A exquisetly crafted leather vest, designed for agility and stealth. Favored by thieves for its light weight and flexibility.',
        'purchased': 'A finely made vest that enhances your stealth and agility.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 13,
        'HP': 0,
        'MP': 0,
        'GR': .5,
        'SPD': 8,
        'description2': 'legendary quality, light armor for THIEVES.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'shop': ['KEY',],
        'price': 1100,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'MYTHRIL MAIL': {
        'name': 'MYTHRIL MAIL',
        'description':'A shirt made with rings of pure mythril. This legendary metal is stronger and tougher than steel, yet weighs as much as silk. Even a king would be jealous of such a fine piece of armor.',
        'purchased': 'A legendary shirt made of mythril rings, offering exceptional protection and lightness.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 20,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'SPD': 2,
        'description2': 'legendary quality, light armor for all classes.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'shop': ['KEY',],
        'price': 1100,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'ORICHALCUM BRIGANDINE': {
        'name': 'ORICHALCUM BRIGANDINE',
        'description':'Made from overlapping plates of the orichalcum. This legendary alloy invented by the Dwarfs never tarnishes and causes blows to glance off like oil repells water.',
        'purchased': "A legendary type of armor made from the mythical Dwarven metal, orichalcum. It's said to be nearly indestructible!",
        'slot': 'BODY',
        'ATK': 5,
        'DEF': 22,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2':
        'legendary quality, medium armor for WARRIORS and THIEVES',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 200,
        'shop': ['KEY',],
        'price': 1500,
        'classes': ['GOD', 'WARRIOR', 'THIEF'],
    },
    'ADAMANTITE CUIRASS': {
        'name': 'ADAMANTITE CUIRASS',
        'description':'A cuirass with a deep emerald hue, made of plates of adamantite. No other metal matches the quality of this legendary material. Offers incredible protection',
        'purchased': 'A heavy cuirass that has seen better days, but still offers solid protection.',
        'slot': 'BODY',
        'ATK': 0,
        'DEF': 25,
        'HP': 200,
        'MP': 0,
        'GR': 0,
        'SPD': -5,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 2000,
        'shop': 'KEY',
        'price': 0,
        'classes': ['GOD', 'WARRIOR'],
    },

  
    'VELVET SLIPPERS': {
        'name': 'VELVET SLIPPERS',
        'description':'Slippers crafted from a soft velvet. These light shoes are a favorite among thieves as they mute footsteps without affecting mobility.',
        'purchased': "These fancy shoes are light as a feather and fashionable to boot!",
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 1,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'SPD': 2,
        'description2':
        'Soft, light slippers for THIEVES. Increases GP earned.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 125,
        'shop': ['KEY', 'SALE'],
        'price': 400,
        'classes': ['GOD', 'THIEF'],
    },
    'CUISSES': {
        'name': 'CUISSES',
        'description': 'Plate metal leg coverings that fully encapsulate the thighs. Offers incredible protection against all kinds of strikes.',
        'purchased': "A solid choice for any warrior looking to protect their legs.",
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 5,
        'HP': 35,
        'MP': 0,
        'GR': 0,
        'SPD': -5,
        'description2': 'High quality, heavy armor for WARRIORS.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 125,
        'shop': ['KEY', 'SALE'],
        'price': 575,
        'classes': ['GOD', 'WARRIOR',],
    },
    'LEATHER BOOTS': {
        'name': 'LEATHER BOOTS',
        'description':'Simple leather boots with a nice thick soul. Offers little protection in combat, but may still come in handy.',
        'purchased': "Keeps your feet safe from rough terrain and stubbed toes",
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 1.5,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Basic light boots for all classes.',
        'quality': 'POOR',
        'gear_level': 0,
        'upgrade': 50,
        'shop': ['KEY', 'SALE'],
        'price': 25,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'CHAUSSES': {
        'name': 'CHAUSSES',
        'description':'Full mail leg coverings made from hardened steel rings. Highly effective against cuts and slashes, but lacks cushioning against blunt strikes.',
        'purchased': 'A sturdy pair of chausses that offer reliable protection for your legs.',
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 8,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'SPD': -4,
        'description2': 'Average quality, heavy armor for WARRIORS.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 275,
        'classes': ['GOD', 'WARRIOR',],
    },
    'OPEN GREAVES': {
        'name': 'OPEN GREAVES',
        'description':'Metal leg coverings that protect the full front of the shin. Offers great protection from frontal attacks, but leaves the back of the leg vulnerable',
        'purchased': 'A sturdy pair of open greaves that provide solid protection for your shins.',
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 6,
        'HP': -25,
        'MP': 0,
        'GR': 0,
        'description2': 'Average quality, medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 325,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'SABATONS': {
        'name': 'SABATONS',
        'description':'Metal foot coverings that protect the toes and feet. Offers great protection but a little on the heavy side...',
        'purchased': 'A sturdy pair of sabatons that provide solid protection for your feet.',
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 6,
        'HP': -25,
        'MP': 0,
        'GR': 0,
        'SPD': -2,
        'description2': 'Average quality, medium armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 325,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'TEMPERED GREAVES': {
        'name': 'TEMPERED GREAVES',
        'description':'Metal leg coverings that protect the full lower leg. Offers great protection from all angles, but is a bit heavy and cumbersome.',
        'purchased': 'A sturdy pair of tempered greaves that provide excellent protection for your lower legs.',
        'slot': 'LEGS',
        'ATK': 0,
        'DEF': 8,
        'HP': -80,
        'MP': 0,
        'GR': 0,
        'SPD': -5,
        'description2': 'Average quality, heavy armor for all classes.',
        'quality': 'GOOD',
        'gear_level': 0,
        'upgrade': 100,
        'shop': ['KEY', 'SALE'],
        'price': 325,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'MAGUS SHOES': {
        'name': 'MAGUS SHOES',
        'description':'Lightweight shoes designed for mages. Offers minimal protection but enhances magical abilities.',
        'purchased': 'A mystical pair of shoes that enhance your magical prowess.',
        'slot': 'LEGS',
        'ATK': 4,
        'DEF': 3,
        'HP': 0,
        'MP': 4,
        'GR': 0,
        'SPD': 2,
        'description2': 'Legendary quality, lightweight armor for WIZARDS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 725,
        'classes': ['GOD','WIZARD', 'WITCH',],
    },
    'ROGUE SLIPPERS': {
        'name': 'ROGUE SLIPPERS',
        'description':'Lightweight shoes designed for rogues. Offers minimal protection but enhances agility and stealth.',
        'purchased': 'A finely made pair of slippers that boost your agility and stealth.',
        'slot': 'LEGS',
        'ATK': 2,
        'DEF': 3,
        'HP': 0,
        'MP': 0,
        'GR': .25,
        'SPD': 8,
        'description2': 'Legendary quality, lightweight armor for THIEVES.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 725,
        'classes': ['GOD', 'THIEF'],
    },
    'ADAMANTITE BOOTS': {
        'name': 'ADAMANTITE BOOTS',
        'description':'Heavy boots made from adamantite. Offers unparalleled protection but is quite heavy.',
        'purchased': 'A pair of heavy boots made from the legendary metal adamantite. They offer exceptional protection.',
        'slot': 'LEGS',
        'ATK': 1,
        'DEF': 7,
        'HP': 120,
        'MP': 0,
        'GR': 0,
        'SPD': -5,
        'description2': 'Legendary quality, heavy armor for WARRIORS.',
        'quality': 'LEGENDARY',
        'gear_level': 0,
        'upgrade': 150,
        'shop': ['KEY', 'SALE'],
        'price': 725,
        'classes': ['GOD','WARRIOR'],
    },
  
    'GORGET': {
        'name': 'GORGET',
        'description':'A collar of metal plates covered in leather. Offers additional protection against blows to the throat; an essential piece of armor by all accounts.',
        'purchased': "Not particularly comfortable, but it might save your neck one day!",
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 5,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Offers additional DEF.',
        'shop': ['KEY','TRAVEL', 'SALE'],
        'price': 300,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'VAMBRACE': {
        'name': 'VAMBRACE',
        'description':'Metal forearm protection. A useful piece of armor, but makes moving the arms more tiring.',
        'purchased': "Protects your forearms from blows, but can be a bit tiring to wear for long periods.",
        'slot': 'ACCS',
        'ATK': -2,
        'DEF': 7,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Offers additional DEF at the cost of ATK.',
        'shop': ['KEY', 'SALE'],
        'price': 350,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'HEROS MEDAL': {
        'name': 'HEROS MEDAL',
        'description':'A gold medal found on a corpse covered in mushrooms. The name "Jeremy The Goblin-Slayer" is engraved on the front. What an unfitting end for such a valiant hero.',
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 0,
        'HP': 150,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases max HP by +150.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'GOLD RING': {
        'name': 'GOLD RING',
        'description':'A perfectly polished gold ring. Given to you by one of the Frog-Sirens of the swamp. You feel luckier holding this, like your wealth is about to grow.',
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Increases GP earned from combat.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'CRYSTAL NECKLACE': {
        'name': 'CRYSTAL NECKLACE',
        'description':'A necklace made from an unusual crystal. A faint warmth can be felt emanating from it. Wearing it fills you with magical energy.  May protect against certain magical traps...',
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 5,
        'GR': 0,
        'FOC': .25,
        'description2': 'Enhances skills and magic abilities, increases MP by +5.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER'],
    },
    'THORN BRACERS': {
        'name': 'THORN BRACERS',
        'description':'Bracers made from dried thorns. Surprisingly durable, the sharp thorns are as much a threat to the wearer as their foes.',
        'slot': 'ACCS',
        'ATK': 8,
        'DEF': -3,
        'HP': -85,
        'MP': 0,
        'GR': 0,
        'description2': 'Increases ATK, reduces DEF and HP.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER']
    },
    'WOLF FANG': {
        'name': 'WOLF FANG',
        'description': "A fang broken off a Dire Wolf. Wearing this around your neck gives you some of the wolf's strength.",
        'slot': 'ACCS',
        'ATK': 4,
        'DEF': 0,
        'HP': 35,
        'MP': 0,
        'GR': 0,
        'description2': 'Enhances ATK and HP. Usable by WARRIORS',
        'price': 0,
        'classes': ['GOD', 'WARRIOR'],
    },
    'CRYSTAL RING': {
        'name': 'CRYSTAL RING',
        'description': 'A ring carved from an unusual crystal. The crystal glows faintly in dim light. Wearing it fills you with magical energy.',
        'slot': 'ACCS',
        'ATK': 5,
        'DEF': 0,
        'HP': 0,
        'MP': 7,
        'GR': 0,
        'FOC': .25,
        'description2': 'Enhances ATK and magic abilities, increases MP +7. Usable by WIZARDS',
        'price': 0,
        'classes': ['GOD', 'WIZARD', 'WITCH',],
    },
    'GOLD HAIRPIN': {
        'name': 'GOLD HAIRPIN',
        'description': 'A glistening hairpin made of pure gold. Often worn for luck; the GOLD HAIRPIN is a symbol of wealth.',
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 1.5,
        'description2': 'Increases GP earned from combat. Usable by THIEVES',
        'price': 0,
        'classes': ['GOD', 'THIEF'],
    },
    'MAGIC CIRCLET': {
        'name': 'MAGIC CIRCLET',
        'description': 'A magically enhanced circlet crafted with secret dwarven smithing techniques from an orichalcum ingot. Confers several boons to the wearer.',
        'slot': 'ACCS',
        'ATK': 0,
        'DEF': 0,
        'HP': 55,
        'MP': 5,
        'GR': .5,
        'description2': 'Increases HP, MP, and GP earned.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER']
    },
    'MAGIC GREASE': {
        'name':'MAGIC GREASE',
        'description': 'A strange grease found in the Waterfall Cave after defeating the River Serpent. Blades coated in it never seem to rust and retain their edge indefinitely.',
        'slot': 'ACCS',
        'ATK': 12,
        'DEF': 0,
        'HP': 0,
        'MP': 0,
        'GR': 0,
        'description2': 'Significantly increases ATK.',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER']
    },
    'DRAGON HEART': {
        'name': 'DRAGON HEART',
        'description': 'A crimson gem created from the heart of an ancient and powerful dragon after its death. This gem holds incredible power, but using it comes at a steep price.',
        'slot': 'ACCS',
        'ATK': 20,
        'DEF': 0,
        'HP': -475,
        'MP': 8,
        'GR': 0,
        'description2': 'Greatly increases ATK and MP, greatly reduces HP',
        'price': 0,
        'classes': ['GOD', 'WARRIOR', 'WIZARD', 'WITCH', 'THIEF', 'SUMMONER']
    },

  
    'MAP': {
        'name': 'MAP',
        'description': 'A map coated in magical ink. The ink reacts to your surroundings and changes depending on your location. (Type MAP or LOCATION outside item menu to view current area.)',
        'purchased': 'Now you can stop getting lost all the time! (Type MAP to view current area and paths)',
        'shop': 'KEY',
        'price': 50,
    },
    'CRAFTING POUCH': {
        'name': 'CRAFTING POUCH',
        'description':"A special pouch in your pack for storing crafting materials. You're not sure how it can hold so much, but you're not about to question it either.",
        'purchased': 'You can store all sorts of weird things now!',
        'shop': 'KEY',
        'price': 100,
    },
    'LANTERN': {
        'name': 'LANTERN',
        'description': 'A lantern that attaches to a belt for hands free use. Allows travel through dark areas.',
        'purchased': 'You can now explore dark areas without being so scared and stumbling around blindly!',
        'shop': ['KEY','TRAVEL'],
        'price': 200,
        'BF': 0,
    },
    'EXTRA POUCH': {
        'name': 'EXTRA POUCH',
        'description': 'Increases consumable item inventory',
         'purchased': 'You can now carry more consumable items! (You can now store an additional 5 of each consumable item)',
        'shop': 'KEY',
        'price': 500,
    },
    'SPECIAL FEED': {
        'name': 'SPECIAL FEED',
        'description': 'A medicated feed for pigs. Quite pricey; the Farmer better have the GP to cover the costs...',
        'purchased': 'Hopefully the Farmers pig is still doing fine. It was a lot of GP to spend on that stuff!',
        'shop': 'KEY',
        'price': 500,
    },
    'AXE': {
        'name':'AXE',
        'description': 'An axe made for chopping wood. Covered in rust and in need of some serious maintenance. Not sure what a bear was doing with this in the first place...',
    },
    'SHARP AXE': {
        'name':'SHARP AXE',
        'description': 'An axe made for chopping wood. Freshly sharpened by the Village Smith. Should have no trouble chopping through trees now!',
    },
    'HAMMER': {
        'name':'HAMMER',
        'description': 'A sturdy hammer with a large iron head. Not well suited for combat, but could be useful for other tasks.',
    },
    'PENDANT': {
        'name': 'PENDANT',
        'description': 'A round silver pendant with the words "for my love" engraved on the back. Found stuck in an olive tree burl. Who knows how many years it has been there?',
    },
    'SALMON': {
        'name':'SALMON',
        'description':'A not so lucky fish found at the Waterfall. Could make for a tasty meal.',
    },
    'GOBLIN FINGER': {
        'name':'GOBLIN FINGER',
        'description': 'A finger procured from the Goblin Queen as evidence to the Village Smith of her demise... Really nasty that you just have this loose in your bag, you know.',
    },
    'IRON KEY': {
        'name': 'IRON KEY',
        'description':'A small key made of iron. Dropped from a pesky Hobgoblin.',
    },
    "GOBLIN'S WARLOCK KEY": {
        'name': "GOBLIN'S WARLOCK KEY",
        'description':'A key made of dragon bone by the evil WARLOCK Smeldar to seal his wicked tower... This one was taken from the Goblin Queen.',
    },
    "OGRE'S WARLOCK KEY": {
        'name': "OGRE'S WARLOCK KEY",
        'description': 'A key made of dragon bone by the evil WARLOCK Smeldar to seal his wicked tower... This one was taken from the Ogre Chief.',
    },
    "ORC'S WARLOCK KEY": {
        'name': "ORC'S WARLOCK KEY",
        'description': 'A key made of dragon bone by the evil WARLOCK Smeldar to seal his wicked tower... This one was taken from the Orc Commander.',
    },
    "VAMPIRE'S WARLOCK KEY": {
        'name': "VAMPIRE'S WARLOCK KEY",
        'description': 'A key made of dragon bone by the evil WARLOCK Smeldar to seal his wicked tower... This one was taken from the Vampire Lord.',
    },
    'ROYAL JELLY': {
        'name': 'ROYAL JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. Just a tiny bit mixed in will greatly increase the potancy.',
    },
    'STRANGE JELLY': {
        'name': 'STRANGE JELLY',
        'description':'A jar of Giant Bee Royal Jelly. This substance is capable of enhancing the healing properties of potions. This jelly has an unusually vibrant red colouring.',
    },
    'MOUTH-PIECE': {
        'name':'MOUTH-PIECE',
        'description': 'A mouth piece belonging to a musical horn. Not much use on its own, but it could be attached to the right instrument...',
    },
    'BROKEN HORN': {
        'name': 'BROKEN HORN',
        'description': 'A musical horn that is missing its mouth piece. The Frog-Man claims you will need this to seek an audience with the Ogre Chief. but it cant be played without the missing part.',
    },
    'COMPLETE HORN': {
        'name': 'COMPLETE HORN',
        'description': 'A complete musical horn. Made by combining the BROKEN HORN and the MOUTH PIECE. Can be played in the deepest part of the swamp to seak an audience with the Ogre Chief.',
    },
    'WAFFLE': {
        'name': 'WAFFLE',
        'description': 'A large, perfectly made breakfast waffle dropped by a donkey in the swamp. Probably not safe to eat, but maybe you will find some use for it?..',
    },
    'STRANGE GREASE': {
        'name':'STRANGE GREASE',
        'description':'A strange grease found in the Waterfall Cave after defeating the River Serpent. Perhaps you should ask a SMITH about it...',
    },
    'SERPENTS EYE': {
        'name':'SERPENTS EYE',
        'description':'An eye plucked from the River Serpent. This trophy was requested by the old Captain as retribution for his lost eye from many years ago. Hopefully it was worth the trouble to get this nasty thing.',
    },
    'PAINTED SAIL': {
        'name':'PAINTED SAIL',
        'description':"A snail found chomping on leaves right around the Kobold's home. This little guy's got a crude face painted on its shell. Maybe this is the Kobold's friend?",
    },
    'SLEEPY SQUIRREL': {
        'name':'SLEEPY SQUIRREL',
        'description':"A chunky squirrel found sleeping in a tree near the Kobold's home. This lazy critter just went right back to sleep after you grabbed him. Maybe this is the Kobold's friend?",
    },
    'WET TOAD': {
        'name':'WET TOAD',
        'description':"A slimy toad found hopping around the Kobold's home. Kind of cute if you look past all the warts and mucus. Maybe this is the Kobold's friend?",
    },
    'CRANK': {
        'name':'CRANK',
        'description':"A solid iron crank found in the Orc Fortress. Looks like it was removed from some mechanism some time ago.",
        'quantity': 0,
    },
    'CHEST KEY': {
        'name':'CHEST KEY',
        'description':"A brass key made for a chest lock. Taken from a sleeping Orc. You need it more than he did. Probably.",
    },
    'DININGHALL KEY': {
        'name':'DININGHALL KEY',
        'description':"A small gold key found in the Forest Palace's Dining hall. Probably opens the chest in the same room.",
        },
    'SKELETON KEY': {
        'name':'SKELETON KEY',
        'description':"A strange key literally in the shape of a skeleton. Definitely opens something important, but be who could say what that may be?",
    },
    'TOWER KEY': {
        'name':'TOWER KEY',
        'description':"A strange key literally in the shape of a skeleton. Man, even this guy's keys are evil looking!",
    },
    'LIBRARY NOTE': {
        'name':'LIBRARY NOTE',
        'description':'"The boy looks forward to his future, with ambition in his heart.\nThe soldier looks for glory on the battlefield, but only sees death.\nThe old man looks back on his youth, facing the setting sun.\nThe reaper looks on patiently, for none escape their fate.\n"',
    },
    'EMERALD GEMSTONE': {
        'name':'EMERALD GEMSTONE',
        'description':'A flawless emerald gemstone. Shimmers with a mysterious light. Grabbed from the Demon Statue in the Forest Palace\'s art gallery.'
    },
    'RUBY GEMSTONE': {
        'name':'RUBY GEMSTONE',
        'description':'A flawless ruby gemstone. Glows with a deep, blood red light. Found in the Vampire Lord\'s chamber.'
    },
    'SAPPHIRE GEMSTONE': {
        'name':'SAPPHIRE GEMSTONE',
        'description':'A flawless sapphire gemstone. Radiates a cool blue light. Taken from the Werewolf\'s maw.'
    },
    'TORN NOTE': {
        'name':'Torn Note',
        'description': note_Map1
    },

}

mainHand_equipment = []
offHand_equipment = []
body_equipment = []
head_equipment = []
legs_equipment = []
accs_equipment = []

shop_items = []
shop_keyitems = []
travelingMerchant_items = []
sellable_items = []


for s in key_items:
    try:
        if 'REGULAR' in key_items[s]['shop']:
           shop_items.append(key_items[s]['name'])
        if 'KEY' in key_items[s]['shop']:
           shop_keyitems.append(key_items[s]['name'])
        if 'TRAVEL' in key_items[s]['shop']:
           travelingMerchant_items.append(key_items[s]['name'])
        if 'SALE' in key_items[s]['shop']:
           sellable_items.append(key_items[s]['name'])
    except:
         pass
   
for s in key_items:
   try:
        if key_items[s]['slot'] == 'MAIN HAND':
           mainHand_equipment.append(key_items[s]['name'])
        if key_items[s]['slot'] == 'OFF HAND':
           offHand_equipment.append(key_items[s]['name'])
        if key_items[s]['slot'] == 'HEAD':
           head_equipment.append(key_items[s]['name'])
        if key_items[s]['slot'] == 'BODY':
           body_equipment.append(key_items[s]['name'])
        if key_items[s]['slot'] == 'LEGS':
           legs_equipment.append(key_items[s]['name'])
        if key_items[s]['slot'] == 'ACCS':
           accs_equipment.append(key_items[s]['name'])       
   except:
       pass
    


armor_equipment = head_equipment + body_equipment + legs_equipment
all_equipment = mainHand_equipment + offHand_equipment + head_equipment + body_equipment + legs_equipment + armor_equipment + accs_equipment

smeldar_keys = ["GOBLIN'S WARLOCK KEY", "OGRE'S WARLOCK KEY", "ORC'S WARLOCK KEY", "VAMPIRE'S WARLOCK KEY"]
crafting_items = {
    '': {
        'name': '',
        'description': '',
    },
    'PLANT PARTS': {
        'name': 'PLANT PARTS',
        'description': 'Various parts of magical plants. Commonly harvested from plant type enemies.',
    },
    'MONSTER GUTS': {
        'name': 'MONSTER GUTS',
        'description': 'A mix of different monster organs and body parts. Really weird that you just carry this stuff with you.',
    },
    'RARE MONSTER PARTS': {
        'name': 'RARE MONSTER PARTS',
        'description': "These uncommon monster parts are highly prized. Still weird that you're carring them with you.",
    },
    'FAE DUST': {
        'name': 'FAE DUST',
        'description': 'A glistening powder found on creatures of the fae like Fairies and Pixies. A common source of magical energy.',
    },
    'DRAGON SCALES': {
        'name': 'DRAGON SCALES',
        'description': "The scales of Dragons are incredibly hard to come by. Prying one off a dragon, live or dead, is nearly impossible before they're already loose, and these are rarely shed. The inner surface is a beautiful shifting rainbow.",
    },
}


SFX_Library = {
    'Camp': Path(sys.argv[0]).parent / 'sounds' / 'CampRest.wav',
    'Inn': Path(sys.argv[0]).parent / 'sounds' / 'InnRest.wav',
    'Pray': Path(sys.argv[0]).parent / 'sounds' / 'Pray.wav',
    'Kindle': Path(sys.argv[0]).parent / 'sounds' / 'Kindle.wav',
    'Buy': Path(sys.argv[0]).parent / 'sounds' / 'Buy.wav',
    'Sell': Path(sys.argv[0]).parent / 'sounds' / 'Sell.wav',
    'NoGP': Path(sys.argv[0]).parent / 'sounds' / 'NoGP.wav',
    'NoItem': Path(sys.argv[0]).parent / 'sounds' / 'NoItem.wav',
    'GotLegendary': Path(sys.argv[0]).parent / 'sounds' / 'GotLegendary.wav',
    'Equip': Path(sys.argv[0]).parent / 'sounds' / 'Equip.wav',
    'Unequip': Path(sys.argv[0]).parent / 'sounds' / 'Unequip.wav',
    'Save': Path(sys.argv[0]).parent / 'sounds' / 'Save.wav',
    'Load': Path(sys.argv[0]).parent / 'sounds' / 'Load.wav',
    'Map': Path(sys.argv[0]).parent / 'sounds' / 'Map.wav',
    'Select': Path(sys.argv[0]).parent / 'sounds' / 'Select.wav',
    'Back': Path(sys.argv[0]).parent / 'sounds' / 'Back.wav',
    'Warp': Path(sys.argv[0]).parent / 'sounds' / 'Warp.wav',
    'Error': Path(sys.argv[0]).parent / 'sounds' / 'Error.wav',

    'Brew': Path(sys.argv[0]).parent / 'sounds' / 'Brew.wav',
    'Chop': Path(sys.argv[0]).parent / 'sounds' / 'Axe_Chop.wav',
    'Smash': Path(sys.argv[0]).parent / 'sounds' / 'Smash.wav',
    'Bite': Path(sys.argv[0]).parent / 'sounds' / 'Bite.wav',
    'Jump': Path(sys.argv[0]).parent / 'sounds' / 'Jump.wav',
    'Rotate': Path(sys.argv[0]).parent / 'sounds' / 'StatueRotate.wav',
}
