import random
import os
import sys
import pickle
import character 
import combat 
import world 
from script import line2004, line000
from Settings import print_slow, play_sound_effect
from pathlib import Path
from copy import deepcopy
from playsound import playsound

directions_list = {
   'NORTH':['NORTH', 'N'], 
   'EAST':['EAST', 'E'], 
   'SOUTH':['SOUTH', 'S'], 
   'WEST':['WEST', 'W'], 
   'CLIMB':['CLIMB', 'C', 'UP']
}

actions_list = {
   "EXPLORE": ['EXPLORE', 'LOOK', 'SCOUT'],
    "EXAMINE": ['EXAMINE', 'SEARCH', 'INSPECT', 'INVESTIGATE', 'CHECK'], 
    "SPEAK": ['SPEAK', 'TALK', 'CHAT'],
    "HEAL": ['HEAL', 'RESTORE', 'MEND'], 
    "REST": ['REST', 'SLEEP'],
    "KINDLE": ['KINDLE', 'LIGHT FIRE', 'LIGHT FIREPLACE', 'KINDLING', 'LIGHT', 'BURN', 'FIRE', 'IGNITE'],
    "PRAY": ['PRAY'],
    "BUY": ['BUY','PURCHASE'], 
    "SELL": ['SELL', 'SALE'],
    "TRADE": ['TRADE', 'EXCHANGE', 'BARTER'],
    "UPGRADE": ['UPGRADE', 'ENHANCE'],
    "CRAFT": ['CRAFT'],
    "WARP": ['WARP', 'TELEPORT', 'FAST TRAVEL']
    }

special_list = {
   "JUMP": ['JUMP', 'LEAP', 'DIVE'],
   "SWIM": ['SWIM', 'DIVE', 'WADE'],
   "ATTACK": ["A", "ATK","ATTACK","HIT","SMASH","SMASHING","CRUSH","FIGHT"],
   "DRINK": ['DRINK'],
   "RIBBIT": ['RIBBIT', 'RIBBITING', 'CROAK','CROAKING', 'KERO', 'KEROKERO'],
   "PLAY": ['PLAY', ],
   "WAIT": ['WAIT', 'PAUSE', 'STOP'],
   "PICK": ['PICK', 'PICK UP', 'LIFT', 'GRAB', 'TAKE'],
   "SAIL": ['SAIL'],
   "READ": ['READ', 'STUDY', 'PERUSE'],
   "THROW WEAPON": ['THROW WEAPON', 'TOSS WEAPON', 'THROW', 'TOSS'],
   "TANNINIM": ['TANNINIM']
}

helper_list = {
    'HELP': ['HELP', 'ASSIST', 'COMMANDS'],
    'STATS': ['STATS', 'STATUS', 'CHARACTER'],
    'ITEMS': ['ITEM','ITEMS', 'INVENTORY', 'BAG'],
    'EQUIPMENT': ['EQUIPMENT', 'EQUIP', 'GEAR'],
    'MAP': ['MAP','LOCATION', 'WHERE AM I', 'WHERE'],
    'SETTINGS': ['SETTINGS'],
    'TYPE': ['TYPE', 'TYPING'],
    'SAVE': ['SAV', 'SAVE', 'SAVE GAME', 'SAVE FILE', 'SAVE PROGRESS', 'SAVE DATA'],
    'LOAD': ['LOA', 'LOAD', 'LOAD GAME', 'LOAD FILE', 'LOAD PROGRESS', 'LOAD DATA'],
    'PRINT': ['PRINT', 'DEBUG'],
    'QUIT': ['QUIT', 'QUIT GAME', 'EXIT GAME'],
    'VIEW': ['VIEW', 'KEYS']
}


def intro_load():
    global gameSetup
    while gameSetup == 2:
        print_slow(
            '\nWould you like to load saved data?\n\n\n"YES" to load\n\n"NO" to start new game\n', typingActive)
        playerInput = input().upper().strip()
        if playerInput == 'YES':
            load()
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            break
        elif playerInput == 'NO':
            gameSetup = 1
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            return gameSetup
        else:
            print('Please select a valid command.')


def setup():
    global gameSetup
    global p1

    settingsMenu()
    while gameSetup == 1:
        print_slow("\nPlease enter your character's NAME:", typingActive)
        player_name = input().strip()
        soundFile = str(world.SFX_Library['Select'])
        play_sound_effect(soundFile, SoundsOn)
        gameSetup = 2
        while gameSetup == 2:
            print_slow("""\nPlease choose your CLASS: 
WARRIOR 
WIZARD 
THIEF 
SUMMONER 
Type INFO for class information. Type HELP for further assistance.
                       """, typingActive)
            player_job = input().upper().strip()
            print_slow('', typingActive)
            if player_job == "WARRIOR":
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              p1 = character.player(
                player_name, # Player's name
                player_job, # Player's class
                ['HARDEN',], # Player's skills
                ['RUSTY DAGGER'], # Player's inventory
                [], # Player's materials
                1, # Player's level
                100, #EXP to next level
                0, # Current EXP
                70, #Player's Max HP
                70, #Player's Current HP
                3, #Player's Max MP
                3, #Player's Current MP
                16, #Player's Strength
                70, #Player's Defense
                0, #Player's Gear Defense
                100, #Player's Temp Defense
                95, #Player's Accuracy
                1, #Player's Focus
                10, #Player's Speed 
                100, #Player's Gold
                5, #Player's Max Potions
                5, #Player's Current Potions
                5, #Player's Max Antidotes
                1, #Player's Current Antidotes
                5, #Player's Max Ethers
                0, #Player's Current Ethers
                5, #Player's Max Saline
                0, #Player's Current Saline
                5, #Player's Max Smoke Bombs
                3, #Player's Current Smoke Bombs
                3, #Player's Max Warp Crystals
                0, #Player's Current Warp Crystals
                5, #Player's Max Kindling
                1, #Player's Current Kindling
                0, #Player's Royal Jelly (healing bonus)
                1, #Player's Gold Ring (GP bonus)
                'RUSTY DAGGER', # Player's main hand weapon
                None, # Player's off hand weapon
                None, # Player's head gear
                None, # Player's body gear
                None, # Player's leg gear
                None, # Player's accessory1
                None, # Player's accessory2
                0, #Gear Level
                0, #Goblins Killed
                0, #Fae Killed
                0, #Plant Parts
                0, #Monster Parts
                0, #Rare Parts
                0, #Fae Parts
                0, #Dragon Parts
                0, #Poison Status
                0, #Blind Status
                0, #Rooms Moved
                0, #Enemies Killed
                0, #keys collected(Defunct)
                False, #Has Won Game
                ['Camp Site'] ) # Fast Travel Points Unlocked
              gameSetup = 3

            elif player_job in ['WIZARD', 'WITCH']:
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              p1 = character.player(
                player_name, # Player's name
                player_job, # Player's class
                ['FOCUS',], # Player's skills
                ['RUSTY DAGGER',], # Player's inventory
                [], # Player's materials
                1, # Player's level
                100, #EXP to next level
                0, # Current EXP
                45, #Player's Max HP
                45, #Player's Current HP
                8, #Player's Max MP
                8, #Player's Current MP
                22, #Player's Strength
                89, #Player's Defense
                0, #Player's Gear Defense
                100, #Player's Temp Defense
                95, #Player's Accuracy
                1, #Player's Focus
                10, #Player's Speed 
                100, #Player's Gold
                5, #Player's Max Potions
                3, #Player's Current Potions
                5, #Player's Max Antidotes
                1, #Player's Current Antidotes
                5, #Player's Max Ethers
                1, #Player's Current Ethers
                5, #Player's Max Saline
                0, #Player's Current Saline
                5, #Player's Max Smoke Bombs
                2, #Player's Current Smoke Bombs
                3, #Player's Max Warp Crystals
                0, #Player's Current Warp Crystals
                3, #Player's Max Kindling
                0, #Player's Current Kindling
                0, #Player's Royal Jelly (healing bonus)
                1, #Player's Gold Ring (GP bonus)
                'RUSTY DAGGER', # Player's main hand weapon
                None, # Player's off hand weapon
                None, # Player's head gear
                None, # Player's body gear
                None, # Player's leg gear
                None, # Player's accessory1
                None, # Player's accessory2
                0, #Gear Level
                0, #Goblins Killed
                0, #Fae Killed
                0, #Plant Parts
                0, #Monster Parts
                0, #Rare Parts
                0, #Fae Parts
                0, #Dragon Parts
                0, #Poison Status
                0, #Blind Status
                0, #Rooms Moved
                0, #Enemies Killed
                0, #keys collected(Defunct)
                False, #Has Won Game
                ['Camp Site'] ) # Fast Travel Points Unlocked
              gameSetup = 3
              
            elif player_job == "THIEF":
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              p1 = character.player(
                player_name, # Player's name
                player_job, # Player's class
                ['STEAL',], # Player's skills
                ['RUSTY DAGGER'], # Player's inventory
                [], # Player's materials
                1, # Player's level
                100, #EXP to next level
                0, # Current EXP
                55, #Player's Max HP
                55, #Player's Current HP
                5, #Player's Max MP
                5, #Player's Current MP
                19, #Player's Strength
                78, #Player's Defense
                0, #Player's Gear Defense
                100, #Player's Temp Defense
                95, #Player's Accuracy
                1, #Player's Focus
                15, #Player's Speed 
                200, #Player's Gold
                5, #Player's Max Potions
                3, #Player's Current Potions
                5, #Player's Max Antidotes
                2, #Player's Current Antidotes
                5, #Player's Max Ethers
                1, #Player's Current Ethers
                5, #Player's Max Saline
                3, #Player's Current Saline
                5, #Player's Max Smoke Bombs
                5, #Player's Current Smoke Bombs
                5, #Player's Max Warp Crystals
                1, #Player's Current Warp Crystals
                3, #Player's Max Kindling
                0, #Player's Current Kindling
                0, #Player's Royal Jelly (healing bonus)
                1, #Player's Gold Ring (GP bonus)
                'RUSTY DAGGER', # Player's main hand weapon
                None, # Player's off hand weapon
                None, # Player's head gear
                None, # Player's body gear
                None, # Player's leg gear
                None, # Player's accessory1
                None, # Player's accessory2
                0, #Gear Level
                0, #Goblins Killed
                0, #Fae Killed
                0, #Plant Parts
                0, #Monster Parts
                0, #Rare Parts
                0, #Fae Parts
                0, #Dragon Parts
                0, #Poison Status
                0, #Blind Status
                0, #Rooms Moved
                0, #Enemies Killed
                0, #keys collected(Defunct)
                False, #Has Won Game
                ['Camp Site'] ) # Fast Travel Points Unlocked
              gameSetup = 3

            elif player_job in ['SUMMONER']:
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              p1 = character.player(
                player_name, # Player's name
                player_job, # Player's class
                ['EMBER',], # Player's skills
                ['RUSTY DAGGER',], # Player's inventory
                [], # Player's materials
                1, # Player's level
                100, #EXP to next level
                0, # Current EXP
                35, #Player's Max HP
                35, #Player's Current HP
                12, #Player's Max MP
                12, #Player's Current MP
                10, #Player's Strength
                92, #Player's Defense
                0, #Player's Gear Defense
                100, #Player's Temp Defense
                95, #Player's Accuracy
                1, #Player's Focus
                10, #Player's Speed 
                100, #Player's Gold
                5, #Player's Max Potions
                3, #Player's Current Potions
                5, #Player's Max Antidotes
                1, #Player's Current Antidotes
                5, #Player's Max Ethers
                3, #Player's Current Ethers
                5, #Player's Max Saline
                0, #Player's Current Saline
                5, #Player's Max Smoke Bombs
                2, #Player's Current Smoke Bombs
                3, #Player's Max Warp Crystals
                0, #Player's Current Warp Crystals
                3, #Player's Max Kindling
                0, #Player's Current Kindling
                0, #Player's Royal Jelly (healing bonus)
                1, #Player's Gold Ring (GP bonus)
                'RUSTY DAGGER', # Player's main hand weapon
                None, # Player's off hand weapon
                None, # Player's head gear
                None, # Player's body gear
                None, # Player's leg gear
                None, # Player's accessory1
                None, # Player's accessory2
                0, #Gear Level
                0, #Goblins Killed
                0, #Fae Killed
                0, #Plant Parts
                0, #Monster Parts
                0, #Rare Parts
                0, #Fae Parts
                0, #Dragon Parts
                0, #Poison Status
                0, #Blind Status
                0, #Rooms Moved
                0, #Enemies Killed
                0, #keys collected(Defunct)
                False, #Has Won Game
                ['Camp Site'] ) # Fast Travel Points Unlocked
              gameSetup = 3

            elif player_job == "GOD":
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              p1 = character.player(
                player_name, # Player's name
                player_job, # Player's class
                ['HARDEN', 'STRIKE', 'BERSERK', 'FOCUS', 'BOLT', 'STORM', 'BLAST', 'STEAL', 'THROW', 'MUG', 'HASTE'], # Player's skills
                ['MAP', 'SHARP AXE', 'LANTERN', 'MESSER', 'ADAMANTITE SWORD', 'BUCKLER', 'MYTHRIL MAIL', 'BRIGANDINE', 'AETHON', 'FULGUR', 'MIDAS'], # Player's inventory
                [], # Player's materials
                1, # Player's level
                999999, #EXP to next level
                0, # Current EXP
                999, #Player's Max HP
                999, #Player's Current HP
                99, #Player's Max MP
                99, #Player's Current MP
                99, #Player's Strength
                30, #Player's Defense
                0, #Player's Gear Defense
                100, #Player's Temp Defense
                100, #Player's Accuracy
                1, #Player's Focus
                10, #Player's Speed 
                5000, #Player's Gold
                10, #Player's Max Potions
                10, #Player's Current Potions
                5, #Player's Max Antidotes
                5, #Player's Current Antidotes
                5, #Player's Max Ethers
                5, #Player's Current Ethers
                5, #Player's Max Saline
                5, #Player's Current Saline
                5, #Player's Max Smoke Bombs
                5, #Player's Current Smoke Bombs
                5, #Player's Max Warp Crystals
                5, #Player's Current Warp Crystals
                5, #Player's Max Kindling
                5, #Player's Current Kindling
                0, #Player's Royal Jelly (healing bonus)
                1, #Player's Gold Ring (GP bonus)
                None, # Player's main hand weapon
                None, # Player's off hand weapon
                None, # Player's head gear
                None, # Player's body gear
                None, # Player's leg gear
                None, # Player's accessory1
                None, # Player's accessory2
                0, #Gear Level
                0, #Goblins Killed
                0, #Fae Killed
                10, #Plant Parts
                10, #Monster Parts
                10, #Rare Parts
                10, #Fae Parts
                10, #Dragon Parts
                0, #Poison Status
                0, #Blind Status
                0, #Rooms Moved
                0, #Enemies Killed
                0, #keys collected(Defunct)
                False, #Has Won Game
                ['Camp Site'] ) # Fast Travel Points Unlocked
              gameSetup = 3
            
            elif player_job == "INFO":
                character.stat_check_menu(typingActive)

            elif player_job == 'HELP':
                print_slow(
                    'Type your CLASS selection to choose your CLASS. Type INFO for CLASS details.',
                    typingActive)
            else:
                print_slow('Please select a valid command or type HELP.',
                           typingActive)
            while gameSetup == 3:
                p1.stat_check(typingActive)
                gameSetup = 0


def encounter_initiation(typingActive, SoundsOn, inRoom):
    global current_room

    def foe_updates():
        if foe == character.p34 and character.p34.HP == 0: #donkey
          character.enemy_spawn14.remove(character.p34)
        if foe == character.p86 and character.p86.HP == 0: #Shadow Snatcher
          character.enemy_spawn30b.remove(character.p86)
          character.enemy_spawn31.remove(character.p86)
          character.enemy_spawn32.remove(character.p86)
          print_slow(f"You defeat the Shadow Snatcher! You may now proceed without fear of capture!\n", typingActive)
        if foe == character.p111 and character.p111.HP == 0: #Fat goblin
          character.enemy_spawn34.remove(character.p111)
          p1.inventory.append('DININGHALL KEY')
          print_slow(f"After defeating the Fat Goblin, you search its belongings and find a key in it's possession. You have obtained the DININGHALL KEY!\n", typingActive)
          

    encounter = random.randrange(1,11)
    if inRoom == True:
        encounter *= 2
    if encounter <= world.rooms[current_room]['spawn_rate']:
        foe = random.choice(world.rooms[current_room]['enemy_spawn_set'])
        if foe == character.p28: #traveling merchant
          world.traveling_merchant(p1, foe, current_room, typingActive, SoundsOn)
        else:
          combat.standard_battle(p1, foe, typingActive, SoundsOn)
          if combat.captured == 1:
            current_room = 'Forest Palace - Dungeon'
          foe_updates()


def move_rooms(p1):
    global current_room
    global previous_room
    global player_choice

    def moveSounds():
        if 'floor' in world.rooms[current_room]:
            if world.rooms[current_room]['floor'] == 'GRASS':
              soundFile = str(Path(sys.argv[0]).parent / 'sounds' / "Walk-Grass.wav")
              play_sound_effect(soundFile, SoundsOn)
            if world.rooms[current_room]['floor'] == 'GRAVEL':
              soundFile = str(Path(sys.argv[0]).parent / 'sounds' / "Walk-Gravel.wav")
              play_sound_effect(soundFile, SoundsOn)
            if world.rooms[current_room]['floor'] == 'FOLIAGE':
              soundFile = str(Path(sys.argv[0]).parent / 'sounds' / "Walk-Foliage.wav")
              play_sound_effect(soundFile, SoundsOn)
            if world.rooms[current_room]['floor'] == 'STONE':
              soundFile = str(Path(sys.argv[0]).parent / 'sounds' / "Walk-Stone.wav")
              play_sound_effect(soundFile, SoundsOn)


    while True:
        #"""This section checks to see if a room has a secret path, then checks to see if the secret path has been 'opened' during the rooms special actions. If the path was 'opened' in the special, the player is moved to the secret route. """
        if 'secret_path' in world.rooms[current_room]:
          if world.rooms[current_room]['secret_path'] == 1:
            previous_room = current_room
            current_room = world.rooms[current_room]['SECRET_ROUTE']
            world.rooms[previous_room]['secret_path']  = 0
            player_choice = 1
            p1.roomMoves += 1
            break
            
        #"""This section checks if a chosen direction in a room is locked. If locked, the rooms special 'lock' function will play. (Also confirms that playerInput is valid directional choice for room)"""
        if (playerInput in world.rooms[current_room] and playerInput in directions_list) and world.rooms[current_room][
                playerInput] == 'LOCKED':
            world.rooms[current_room]['LOCK'](p1, playerInput, world.rooms, typingActive, SoundsOn)

        #"""This section checks if a chosen direction in a room is not locked. If not locked, the player is moved to the selected room (Also confirms that playerInput is valid directional choice for room)..."""
        if (playerInput in world.rooms[current_room] and playerInput in directions_list) and world.rooms[current_room][playerInput] != 'LOCKED':
            
            #"""This section checks to see if there is an 'ambush event' in the room active, and if the ambush prevents movement to the next room (ambush_pass == 0 to block)."""
            if 'ambush' in world.rooms[current_room]:
              world.rooms[current_room]['ambush'](p1, playerInput, current_room, typingActive)
              if world.rooms[current_room]['ambush_pass'] == 0:
                break
          
            #"""...This section checks if the room the player is moving into has been previously entered from the 'current room'. If it has not yet been entered from the 'current room', it is added to the current rooms list of 'discovered' directions_list. Discovered directions_list are added to the map..."""
            if world.rooms[current_room][playerInput] not in world.rooms[current_room][
                    'discovered']:
                world.rooms[current_room]['discovered'].append(
                    world.rooms[current_room][playerInput])

            #"""...Next the 'current room' is switched to being the 'previous room' and the new 'current room' is updated. Then the 'previous room' is checked to be in the new 'current rooms' discovered list. If it is not, it will be added (for the map)..."""
            previous_room = current_room
            current_room = world.rooms[current_room][playerInput]
            if previous_room not in world.rooms[current_room]['discovered']:
                world.rooms[current_room]['discovered'].append(previous_room)
            if playerInput in directions_list and playerInput != "CLIMB":
                print_slow(f'You move to the {playerInput}.', typingActive)
            if playerInput == "CLIMB":
                print_slow("You begin climbing...", typingActive)
            #"""...This section checks to see if the player is poisoned. If they are, poison damage is calculated and applied, and poison duration is decreased by 1 turn..."""
            if p1.POISON > 0:
                damage = p1.MaxHP // 12.5
                p1.HP = p1.HP - damage
                p1.POISON = max(p1.POISON - 1, 0)
                print_slow(f"{p1.name} is suffering from the effects of poison! {p1.name} takes {damage} poison damage. {p1.name} has {p1.HP}/{p1.MaxHP}HP\n", typingActive)
            encounter_initiation(typingActive, SoundsOn, inRoom = False)
            player_choice = 1
            p1.roomMoves += 1
            if p1.HP <= 0:
              break
            moveSounds()

            #"""...This section checks if the new room contains a fire (rest point). If it does, it checks to see if the room name is already in the players fast travel list. If not, it adds the room name to the fast travel list..."""
            if 'fire' in world.rooms[current_room]:
              if world.rooms[current_room]['name'] not in p1.FT:
                  p1.FT.append(world.rooms[current_room]['name'])

            #"""...Finally, if a room that has been entered contains a boss ambush event, the event will play out here once the player 'enters' the next room."""
            if 'boss_ambush' in world.rooms[current_room]:
                world.rooms[current_room]['boss_ambush'](p1, playerInput, typingActive, SoundsOn)
                break 
            break

        #If playerInput is not a valid choice for room, but is a valid direction, provides this error. 
        elif playerInput in directions_list and (playerInput != "CLIMB" or playerInput != "EXIT"):
            print_slow(f"You cannot go to the {playerInput.upper()}.", typingActive)
            break
        else:
          break


def special_actions(playerInput_Syn):
    global current_room
    while True:
      if 'secrets' in world.rooms[current_room]:
        if playerInput_Syn in world.rooms[current_room]['secrets']:
          world.rooms[current_room]['special'](p1, playerInput, typingActive, SoundsOn)
          move_rooms(p1)
          if p1.HP <= 0:
            quit_gameDead()
          break
        else:
            print_slow('You are unable to do that here.', typingActive)
      else:
          soundFile = str(world.SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid selection. Try again.', typingActive)
      break
        
  
def take_actions():
    global current_room
    global player_choice
    while True:

        if playerInput in actions_list['EXPLORE']:
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow(world.rooms[current_room]['EXPLORE'], typingActive)
              break
        elif playerInput in actions_list['EXAMINE'] and 'EXAMINE' in world.rooms[current_room]:
              soundFile = str(world.SFX_Library['Select'])
              play_sound_effect(soundFile, SoundsOn)
              world.rooms[current_room]['EXAMINE'](p1, world.rooms, typingActive, SoundsOn)
              move_rooms(p1)
              if p1.HP <= 0:
                quit_gameDead()
              break
        elif playerInput in actions_list['SPEAK'] and 'SPEAK' in world.rooms[current_room]:
              world.rooms[current_room]['SPEAK'](p1, world.rooms, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['BUY'] and 'BUY' in world.rooms[current_room]:
              player_choice = 1
              world.rooms[current_room]['BUY'](p1, world.rooms, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['SELL'] and 'SELL' in world.rooms[current_room]:
              player_choice = 1
              world.rooms[current_room]['SELL'](p1, world.rooms, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['TRADE'] and 'TRADE' in world.rooms[current_room]:
              player_choice = 1
              world.rooms[current_room]['TRADE'](p1, world.rooms, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['REST'] and 'REST' in world.rooms[current_room]:
              world.rooms[current_room]['REST'](p1, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['KINDLE'] and 'fire' in world.rooms[current_room]:
              world.kindling_fire(p1, current_room, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['PRAY'] and 'PRAY' in world.rooms[current_room]:
              world.rooms[current_room]['PRAY'](p1, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['UPGRADE'] and 'UPGRADE' in world.rooms[current_room]:
              world.rooms[current_room]['UPGRADE'](p1, current_room, typingActive, SoundsOn)
              break
        elif (playerInput in actions_list['CRAFT'] and 'CRAFT' in world.rooms[current_room]
              ) and world.rooms[current_room]['crafting'] == 'ACTIVE':
              world.rooms[current_room]['CRAFT'](p1, typingActive, SoundsOn)
              break
        elif playerInput in actions_list['WARP']:
              warp_menu(SoundsOn)
              break
        else:
              print_slow('You are unable to do that here.\n', typingActive)
              break


def helper_actions():
    global current_room
    global player_choice

    while True:
        if playerInput in helper_list['HELP']:
            world_menu(typingActive)
            break
        elif playerInput in helper_list['STATS']:
            p1.stat_check(typingActive)
            break
        elif playerInput in helper_list['ITEMS']:
            item_check(p1, typingActive)
            break
        elif playerInput in helper_list['EQUIPMENT']: 
            equipment_check(p1, typingActive, SoundsOn)
            break
        elif playerInput in helper_list['MAP']:
            soundFile = str(world.SFX_Library['Map'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(
                    f"\n**********[ {world.rooms[current_room]['name']} ]**********\n",
                    typingActive)
            if 'MAP' in p1.inventory and p1.BLIND == 0:
                print(world.rooms[current_room]['map'])
                if 'NORTH' in world.rooms[current_room]:
                    if world.rooms[current_room]['NORTH'] in world.rooms[current_room][
                            'discovered']:
                        print(f"N. {world.rooms[current_room]['NORTH']}")
                    else:
                        print('N. ???')
                if 'EAST' in world.rooms[current_room]:
                    if world.rooms[current_room]['EAST'] in world.rooms[current_room][
                            'discovered']:
                        print(f"E. {world.rooms[current_room]['EAST']}")
                    else:
                        print('E. ???')
                if 'SOUTH' in world.rooms[current_room]:
                    if world.rooms[current_room]['SOUTH'] in world.rooms[current_room][
                            'discovered']:
                        print(f"S. {world.rooms[current_room]['SOUTH']}")
                    else:
                        print('S. ???')
                if 'WEST' in world.rooms[current_room]:
                    if world.rooms[current_room]['WEST'] in world.rooms[current_room][
                            'discovered']:
                        print(f"W. {world.rooms[current_room]['WEST']}")
                    else:
                        print('W. ???')
                if 'CLIMB' in world.rooms[current_room]:
                    if world.rooms[current_room]['CLIMB'] in world.rooms[current_room][
                            'discovered']:
                        print(f"C. {world.rooms[current_room]['CLIMB']}")
                    else:
                        print('C. ???')
            break
        elif playerInput in helper_list['SETTINGS']:
            settingsMenu()
            break
        elif playerInput in helper_list['SAVE']:
            save()
            break
        elif playerInput in helper_list['LOAD']:
            load()
            break
        elif playerInput in helper_list['QUIT']:
            quit_game()
            break
        elif playerInput in helper_list['PRINT']:
            print(world.rooms[current_room])
            break
        elif playerInput == "VIEW":
            print(p1.keys)
            break


def item_check(p1, typingActive):
    while True:
        s = set(world.all_equipment)
        z = set(world.key_items).difference(world.all_equipment)
        equipment = [x for x in p1.inventory if x in s]       
        keyItems_list = [x for x in p1.inventory if x in z]
        print_slow(f'*****[Item Menu]*****', typingActive)
        print_slow(
            f'POTIONS: {p1.POTS}/{p1.MaxPOTS}\nANTIDOTES: {p1.ANT}/{p1.MaxANT}\nETHERS: {p1.ETR}/{p1.MaxETR}\nSMOKE BOMBS: {p1.SMB}/{p1.MaxSMB}\nWARP CRYSTALS: {p1.WCR}/{p1.MaxWCR}\nKINDLING: {p1.KDL}/{p1.MaxKDL}\n',
            typingActive)
        print_slow(f'\nKey Items: {keyItems_list}\n', typingActive)
        print_slow(f'Equipment: {equipment}', typingActive)
        print_slow('\nUSE: Open consumable item menu\n[ITEM NAME]: Type item name for more info\nBACK: Exit menu.',
                   typingActive)
        playerInput = input().upper().strip()
        print('\n')
        if playerInput in p1.inventory:
            print_slow(f"*****{world.key_items[playerInput]['name']}*****", typingActive)
            print_slow(f"\n{world.key_items[playerInput]['description']}", typingActive)
            if 'description2' in world.key_items[playerInput]:
              print_slow(f"{world.key_items[playerInput]['description2']}", typingActive)
            if 'ATK' in world.key_items[playerInput]:
              print_slow(f"ATK: {world.key_items[playerInput]['ATK']}", typingActive)
            if 'DEF' in world.key_items[playerInput]:
              print_slow(f"DEF: {world.key_items[playerInput]['DEF']}", typingActive)
            if 'HP' in world.key_items[playerInput]:
              print_slow(f"HP: {world.key_items[playerInput]['HP']}", typingActive)
            if 'MP' in world.key_items[playerInput]:
              print_slow(f"MP: {world.key_items[playerInput]['MP']}", typingActive)
            print_slow(f"*********************", typingActive)
            if playerInput == 'CRAFTING POUCH':
                while True:
                    p1.materials_list()
                    print_slow(f"\nCrafting Items:\n", typingActive)
                    p1.material_print(typingActive)
                    print_slow(
                        '\nType crafting material name for more info or BACK to return to previous menu.\n',
                        typingActive)
                    playerInput = input().upper().strip()
                    if playerInput in world.backRes:
                        soundFile = str(world.SFX_Library['Back'])
                        play_sound_effect(soundFile, SoundsOn)
                        break
                    elif playerInput in p1.materials:
                        print_slow("test", typingActive)
                        print_slow(f"\n{world.crafting_items[playerInput]['description']}",
                                   typingActive)
                    else:
                        soundFile = str(world.SFX_Library['Error'])
                        play_sound_effect(soundFile, SoundsOn)
                        print_slow('\nInvalid selection. Try again.',
                                   typingActive)
        elif playerInput == 'USE':
            combat.use_item(p1, typingActive, SoundsOn)
            break
        elif playerInput in world.backRes:
            soundFile = str(world.SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            break
        else:
            soundFile = str(world.SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid selection. Try again.', typingActive)


def equipment_check(p1, typingActive, SoundsOn):
  def equip_SFX():
      soundFile = str(world.SFX_Library['EQUIP'])
      play_sound_effect(soundFile, SoundsOn)
  
  def unequip_SFX():
      soundFile = str(world.SFX_Library['UNEQUIP'])
      play_sound_effect(soundFile, SoundsOn)
  
  def cant_equip_SFX():
      soundFile = str(world.SFX_Library['NoItem'])
      play_sound_effect(soundFile, SoundsOn)

  while True:
      print_slow(f"**********[{p1.name}'s Equipment]**********\n", typingActive)
      print_slow(f"[0]MAIN HAND: {p1.mainHand}", typingActive)
      print_slow(f"[1]OFF HAND: {p1.offHand}", typingActive)
      print_slow(f"[2]HEAD: {p1.head}", typingActive)
      print_slow(f"[3]BODY: {p1.body}", typingActive)
      print_slow(f"[4]LEGS: {p1.legs}", typingActive) 
      print_slow(f"[5]ACCS1: {p1.accs1}", typingActive)
      print_slow(f"[6]ACCS2: {p1.accs2}", typingActive)
      print_slow(f"\nType the name or number slot you wish to change, CHECK to view full equipment inventory, or BACK to exit menu.", typingActive)
      playerInput = input().upper().strip()
      print('\n')
      if playerInput == 'MAIN HAND' or playerInput == '0':
        playerInput = 'MAIN HAND'
        change_gear = 1
        while change_gear == 1:
          s = set(world.mainHand_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[MAIN HAND]*****',typingActive)
          if p1.mainHand == None or p1.mainHand == 'EMPTY':
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          elif p1.mainHand != None and p1.mainHand != 'EMPTY':
            print_slow(f'Equipped: {p1.mainHand}\nATK: {world.key_items[p1.mainHand]["ATK"]}\nDEF: {world.key_items[p1.mainHand]["DEF"]}%\nLVL: {world.key_items[p1.mainHand]["gear_level"]}\n"{world.key_items[p1.mainHand]["description2"]}"\n', typingActive)
          print_slow(f'Inventory: {equipment}',typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.mainHand
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX() 
                  p1.mainHand = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'OFF HAND' or playerInput == '1':
        playerInput = 'OFF HAND'
        change_gear = 1
        while change_gear == 1:
          s = set(world.offHand_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[OFF HAND]*****',typingActive)
          if p1.offHand == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.offHand != None:
            print_slow(f'Equipped: {p1.offHand}\nATK: {world.key_items[p1.offHand]["ATK"]}\nDEF: {world.key_items[p1.offHand]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.offHand]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.offHand
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.offHand = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'HEAD' or playerInput == '2':
        playerInput = 'HEAD'
        change_gear = 1
        while change_gear == 1:
          s = set(world.head_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[HEAD]*****',typingActive)
          if p1.head == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.head != None:
            print_slow(f'Equipped: {p1.head}\nATK: {world.key_items[p1.head]["ATK"]}\nDEF: {world.key_items[p1.head]["DEF"]}%\nLVL: {world.key_items[p1.head]["gear_level"]}\n"{world.key_items[p1.head]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.head
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.head = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'BODY' or playerInput == '3':
        playerInput = 'BODY'
        change_gear = 1
        while change_gear == 1:
          s = set(world.body_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[BODY]*****',typingActive)
          if p1.body == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.body != None:
            print_slow(f'Equipped: {p1.body}\nATK: {world.key_items[p1.body]["ATK"]}\nDEF: {world.key_items[p1.body]["DEF"]}%\nLVL: {world.key_items[p1.body]["gear_level"]}\n"{world.key_items[p1.body]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.body
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.body = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'LEGS' or playerInput == '4':
        playerInput = 'LEGS'
        change_gear = 1
        while change_gear == 1:
          s = set(world.legs_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[LEGS]*****',typingActive)
          if p1.legs == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.legs != None:
            print_slow(f'Equipped: {p1.legs}\nATK: {world.key_items[p1.legs]["ATK"]}\nDEF: {world.key_items[p1.legs]["DEF"]}%\nLVL: {world.key_items[p1.legs]["gear_level"]}\n"{world.key_items[p1.legs]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.legs
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.legs = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'ACCS1' or playerInput == '5':
        playerInput = 'ACCS1'
        change_gear = 1
        while change_gear == 1:
          s = set(world.accs_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[ACCS1]*****',typingActive)
          if p1.accs1 == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.accs1 != None:
            print_slow(f'Equipped: {p1.accs1}\nATK: {world.key_items[p1.accs1]["ATK"]}\nDEF: {world.key_items[p1.accs1]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.accs1]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment and playerInput != p1.accs2:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.accs1
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.accs1 = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput in equipment and playerInput == p1.accs2:
              cant_equip_SFX()
              print_slow('\nThat item is equipped in another slot. Try another item.', typingActive)
            elif playerInput == 'BACK':
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)

      elif playerInput == 'ACCS2' or playerInput == '6':
        playerInput = 'ACCS2'
        change_gear = 1
        while change_gear == 1:
          s = set(world.accs_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'*****[ACCS2]*****',typingActive)
          if p1.accs2 == None:
            print_slow(f'Equipped: None\nATK: 0\nDEF: 0\n"Nothing equipped."\n', typingActive)
          if p1.accs2 != None:
            print_slow(f'Equipped: {p1.accs2}\nATK: {world.key_items[p1.accs2]["ATK"]}\nDEF: {world.key_items[p1.accs2]["DEF"]}%\nLVL: N/A\n"{world.key_items[p1.accs2]["description2"]}"\n', typingActive)
          print_slow(f"Inventory: {equipment}", typingActive)
          while True:
            print_slow(f"\nType the item you wish to equip, or BACK to return to previous menu.", typingActive)
            playerInput = input().upper().strip()
            print('\n')
            if playerInput in equipment and playerInput != p1.accs1:
              if p1.job in world.key_items[playerInput]['classes']:
                if (p1.MaxHP + world.key_items[playerInput]['HP']) <= 0:
                  cant_equip_SFX()
                  print_slow(f"Unable to equip this item; {p1.name}'s HP will be reduced to 0.", typingActive)
                else:
                  previous_gear = p1.accs2
                  if playerInput == previous_gear:
                     playerInput = 'EMPTY'
                     unequip_SFX()
                  else:
                    equip_SFX()
                  p1.accs2 = playerInput
                  p1.equip_stat_update(playerInput, previous_gear, world.key_items)
                  break
              else:
                cant_equip_SFX()
                print_slow('\nThis piece of equipment cannot be used by your class. Please select a different item.', typingActive)
            elif playerInput in equipment and playerInput == p1.accs1:
              cant_equip_SFX()
              print_slow('That item is equipped in another slot. Try another item.', typingActive)
            elif playerInput in world.backRes:
              soundFile = str(world.SFX_Library['Back'])
              play_sound_effect(soundFile, SoundsOn)
              change_gear = 0
              break
            else:
              soundFile = str(world.SFX_Library['Error'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow('Invalid selection. Try again.', typingActive)
  
      elif playerInput == 'CHECK':
        while True:
          print_slow(f"\n**********[{p1.name}'s Equipment Inventory]**********\n", typingActive)
          s = set(world.mainHand_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'MAIN HAND: {equipment}',typingActive)

          s = set(world.offHand_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'OFF HAND: {equipment}',typingActive)

          s = set(world.head_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'HEAD: {equipment}',typingActive)  

          s = set(world.body_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'BODY: {equipment}',typingActive)  

          s = set(world.legs_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'LEGS: {equipment}',typingActive)  

          s = set(world.accs_equipment)
          equipment = [x for x in p1.inventory if x in s]
          print_slow(f'ACCS: {equipment}',typingActive)      

          print_slow(f"\nType item name for more information/stats, or BACK to return to previous menu.", typingActive)
          playerInput = input().upper().strip()
          print('\n')
          if playerInput in p1.inventory and world.all_equipment:
              print_slow(f"\n*****[{world.key_items[playerInput]['name']}]*****", typingActive)
              print_slow(f"{world.key_items[playerInput]['description']}", typingActive)
              print_slow(f"{world.key_items[playerInput]['description2']}", typingActive)
              print_slow(f"ATK: {world.key_items[playerInput]['ATK']}", typingActive)
              print_slow(f"DEF: {world.key_items[playerInput]['DEF']}", typingActive)
              print_slow(f"HP: {world.key_items[playerInput]['HP']}", typingActive)
              print_slow(f"MP: {world.key_items[playerInput]['MP']}", typingActive)
              print_slow(f'********************',typingActive)
          elif playerInput in world.backRes:
            soundFile = str(world.SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            break
          else:
            soundFile = str(world.SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid selection. Try again.', typingActive)
      else:
        soundFile = str(world.SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid selection. Try again.', typingActive)


def warp_menu(SoundsOn):
    global current_room
    global player_choice


    def input_normalizer(playerInp):
       if playerInp == 'CAMP SITE':
         return 'Camp Site'
       if playerInp == 'FAE WOODS - CAMP':
          return 'Fae Woods - Camp'
       if playerInp == 'MISTY WOODS - CAMP':
          return 'Misty Woods - Camp'
       if playerInp == 'SMELDARS TOWER - HIDDEN ROOM':
          return 'Smeldars Tower - Hidden Room'
       if playerInp in world.backRes:
          return 'BACK'

    if p1.WCR > 0:
      print_slow("********[Warp List]*********\n", typingActive)
      for w in p1.FT:
        print_slow(f'- {w}', typingActive)

      print_slow("Type the location you wish to warp to or BACK to exit the menu:\n", typingActive)
      while True:
        playerInp = input().upper().strip()
        playerInp = input_normalizer(playerInp)
        if playerInp in p1.FT:
          soundFile = str(world.SFX_Library['Warp'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"You use the Warp Crystal to teleport to {playerInp}. The crystal breaks in your hand as you arrive.\n", typingActive)
          current_room = playerInp
          player_choice = 1
          p1.roomMoves += 1
          p1.WCR -= 1
          break
        elif playerInp in world.backRes:  
          soundFile = str(world.SFX_Library['Back'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow("You decide not to use the Warp Crystal at this time.\n", typingActive)
          break
        else:
          soundFile = str(world.SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow("Invalid input. Please try again.\n", typingActive) 
          
    else:
      print_slow("You do not have a Warp Crystal to use at this time.\n", typingActive)
      return


def settingsMenu():
    global typingActive
    global SoundsOn

    def typeSettings():
      global typingActive
      while True:
        print_slow('Would you like to keep the typing effect on?\n\n"YES": ON\n"NO": OFF\n',typingActive)
        playerInput = input().upper().strip()
        if playerInput in world.affRes or playerInput== "ON":
            typingActive = "ON"
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            break
        elif playerInput in world.negRes or playerInput== "OFF":
            typingActive = "OFF"
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            break
        else:
            soundFile = str(world.SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid input. Input YES or NO.\n', typingActive)


    def soundSettings():
      global SoundsOn
      while True:
        print_slow('Would you like to keep the sound effects on?\n\n"YES": ON\n"NO": OFF\n',typingActive)
        playerInput = input().upper().strip()
        if playerInput in world.affRes or playerInput== "ON":
            SoundsOn = "ON"
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            break
        elif playerInput in world.negRes or playerInput== "OFF":
            SoundsOn = "OFF"
            soundFile = str(world.SFX_Library['Select'])
            play_sound_effect(soundFile, SoundsOn)
            break
        else:
            soundFile = str(world.SFX_Library['Error'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow('Invalid input. Input YES or NO.\n', typingActive)


    menu_option_Terms = {
       'TYPING': ["1", 'TYPE', 'TYPING', 'TEXT', 'TEXT EFFECT', 'PRINT', 'PRINTING', 'TYPING EFFECT'],
       'SOUND': ["2", 'SOUND', 'SOUNDS', 'SOUND EFFECT', 'SOUND EFFECTS', 'AUDIO']
    }
    

    while True:
      print_slow('Settings Menu - Choose the settings you wish to change, or BACK to leave the menu.\n',typingActive)
      print_slow(f'[1] Typing Effect: ({typingActive})\n[2] Sound Effects: ({SoundsOn})', typingActive)
      playerInput = input().upper().strip()
      if playerInput in menu_option_Terms['TYPING']:
        typeSettings()
      elif playerInput in menu_option_Terms['SOUND']:
        soundSettings()
      elif playerInput in world.backRes or playerInput in world.negRes or playerInput == 'OFF':
        soundFile = str(world.SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        break
      else:
        soundFile = str(world.SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Please choose a valid option or type BACK to exit.\n', typingActive)


def save():
    global p1
    global current_room
    global typingActive
    global SoundsOn
    
    saveMenu = "OPEN"
    invChar = ['/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.', ' '] #invalid characters for save file names
    while saveMenu == "OPEN":
      print_slow('\nWould you like to save? YES or NO:\n', typingActive)
      playerInput = input().upper().strip()
      if playerInput == 'YES':
        soundFile = str(world.SFX_Library['Select'])
        play_sound_effect(soundFile, SoundsOn)
        saveMenu = "SAVING"
        #"""This section checks to see if the save name entered by the player contains any invalid characters. If it does, it prompts the player to enter a valid name. If not, it creates the save file."""
        while saveMenu == "SAVING":
          print_slow('\nType name for your save:\n', typingActive)
          savefile1 = input().lower().strip()
          if savefile1 == "show":
              print_slow('Please enter a valid save name or BACK to return.', typingActive)
          elif savefile1 == "back":
               saveMenu = "OPEN"
          else:
              if any(char in savefile1 for char in invChar) or savefile1 == '':
                print_slow('Please enter a valid save name or BACK to return.', typingActive)               
              else:   
                savePath = Path(sys.argv[0]).parent / Path(f'saves/{savefile1}')
                os.makedirs(os.path.dirname(savePath), exist_ok=True)
                saveState = (p1, world.rooms, current_room, typingActive, SoundsOn)
                pickleFile = open(f'{savePath}', 'wb')
                pickle.dump(saveState, pickleFile)
                pickleFile.close()
                soundFile = str(world.SFX_Library['Save'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\n*****[Save Complete]*****', typingActive)
                saveMenu = "CLOSED"
                break             
      elif playerInput == 'NO':
        soundFile = str(world.SFX_Library['Back'])
        play_sound_effect(soundFile, SoundsOn)
        saveMenu = "CLOSED"
        break
      else:
        soundFile = str(world.SFX_Library['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow('Invalid input. Try again.', typingActive)


def load():
  #"""sys.argv[0] is used to """
    global p1
    global current_room
    global gameSetup
    global player_choice
    global typingActive
    global SoundsOn
    loadMenu = 1
    showPath = Path(sys.argv[0]).parent / Path(f'saves/')
    files = [file.stem for file in showPath.rglob('*') if file.is_file()]

    while loadMenu == 1:
        print_slow('\nType the name for the save file you wish to load or BACK to exit menu:', typingActive)
        print(sorted(files))
        playerInput = input().lower().strip()     
        print('\n')          
        if playerInput == 'back':
            soundFile = str(world.SFX_Library['Back'])
            play_sound_effect(soundFile, SoundsOn)
            loadMenu = 2
            break
        else:
            loadPath = Path(sys.argv[0]).parent / Path(f'saves/{playerInput}')
            if loadPath.is_file():
                try:
                  with open(loadPath, 'rb') as pickleFile:
                      loadState = pickle.load(pickleFile)
                      p1 = loadState[0]
                      world.rooms = loadState[1]
                      current_room = loadState[2]
                      typingActive = loadState[3]
                      SoundsOn = loadState[4]
                  loadMenu = 2
                  gameSetup = 0
                  player_choice = 1
                  soundFile = str(world.SFX_Library['Load'])
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow('\n*****[Load Complete]*****', typingActive)
                  break
                except Exception as e:
                  print_slow(f'Error loading file: {e}', typingActive)
            else:
                soundFile = str(world.SFX_Library['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('Invalid selection. Try again.', typingActive)


def quit_game():
  
  while True:
    print_slow('\nDo you really want to quit?\n\nRETURN: Save and return to the Start Menu.\nQUIT: Exit the game.\nCANCEL: Cancel and return to the game.', typingActive)
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'QUIT':
      save()
      sys.exit()
    elif playerInput == 'RETURN':
      save()
      global gameSetup
      global player_choice
      global current_room
      global previous_room
      player_choice = 1
      gameSetup = 3
      current_room = 'Camp Site' #Starting room
      previous_room = ''
      world.rooms = initial_rooms.copy()
      break  
    elif playerInput =='CANCEL':
      soundFile = str(world.SFX_Library['Back'])
      play_sound_effect(soundFile, SoundsOn)
      break
    else:
      soundFile = str(world.SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid selection. Try again.', typingActive)

def quit_gameDead():
  
  while True:
    print_slow('\nRETURN: Return to the Start Menu.\nQUIT: Exit the game.\n', typingActive)
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'QUIT':
      sys.exit()
    elif playerInput == 'RETURN':
      global gameSetup
      global player_choice
      global current_room
      global previous_room
      player_choice = 1
      gameSetup = 3
      current_room = 'Camp Site' #Starting room
      previous_room = ''
      world.rooms = initial_rooms.copy()
      break  
    else:
      soundFile = str(world.SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid selection. Try again.', typingActive)

def quit_gameVictory(p1):

  def ng_plus(p1):
    essential_items = ['MAP', 'CRAFTING POUCH', 'LANTERN', 'EXTRA POUCH', 'SPECIAL FEED', 'AXE', 'SHARP AXE', 'PENDANT', 'SALMON', 'GOBLIN FINGER', 'IRON KEY', "GOBLIN'S WARLOCK KEY",  "OGRE'S WARLOCK KEY", "ORC'S WARLOCK KEY", "VAMPIRE'S WARLOCK KEY", 'ROYAL JELLY', 'STRANGE JELLY', 'MOUTH-PIECE','BROKEN HORN','COMPLETE HORN','WAFFLE', 'STRANGE GREASE', 'SERPENTS EYE', 'PAINTED SAIL', 'SLEEPY SQUIRREL', 'WET TOAD','CRANK','CHEST KEY', 'DININGHALL KEY' , 'SKELETON KEY', 'LIBRARY NOTE', 'EMERALD GEMSTONE', 'RUBY GEMSTONE', 'SAPPHIRE GEMSTONE', 'TORN NOTE']
    p1.HP = p1.MaxHP
    p1.MP = p1.MaxMP
    p1.gobCount = 0
    p1.faeCount = 0
    p1.enemiesKilled = 0
    p1.roomMoves = 0
    p1.win = False
    for item in p1.inventory:
       if item in p1.inventory and item in essential_items:
         p1.inventory.remove(item)

    enemy_resets = [character.p666, character.p34, character.p86] #Smeldar, Donkey, Shadow Snatcher
    for enemy in enemy_resets:
      enemy.HP = enemy.MaxHP
      enemy.MP = enemy.MaxMP

    character.enemy_spawn14.append(character.p34) #donkey
    character.enemy_spawn30.append(character.p86) #Shadow Snatcher

  while True:
    print_slow('\nRETURN: Save for NG+ and return to the Start Menu.\nQUIT: Exit the game.\n', typingActive)
    playerInput = input().upper().strip()
    print('\n')
    if playerInput == 'QUIT':
      sys.exit()
    elif playerInput == 'RETURN':
      global gameSetup
      global player_choice
      global current_room
      global previous_room
      ng_plus(p1)
      player_choice = 1
      gameSetup = 3
      current_room = 'Camp Site' #Starting room
      previous_room = ''
      world.rooms = initial_rooms.copy()
      save()
      break  
    else:
      soundFile = str(world.SFX_Library['Error'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow('Invalid selection. Try again.', typingActive)      



def world_menu(typingActive):
    print_slow(
        '\nWorld commands:\nNORTH: Move NORTH.\nEAST: Move EAST.\nSOUTH: Move SOUTH.\nWEST: Move WEST.\nLOOK: Check your surroundings.\nSEARCH: Investigate area of interest.\nSPEAK: Talk to NPCs.\nSTATS: View your current level and stats.\nITEMS: Check current inventory.\nEQUIPMENT: View equipment.\nMAP: Display current area.\nWARP: Use WARP CRYSTAL\nSETTINGS: Open settings menu.\nSAVE: Create save file.\nLOAD: Load a save file.\nQUIT: Exit the game.\nAdditional commands may be presented to you or hidden. Try Experimenting\n',
        typingActive)




current_room = 'Camp Site' #Starting room
previous_room = ''


typingActive = "OFF"
SoundsOn = "ON"
gameSetup = 3
initial_rooms = deepcopy(world.rooms)
def run_game():
  global typingActive, gameSetup, playerInput, p1, current_room, player_choice, SoundsOn
  # existing main loop moved into a callable so importing main.py is safe

  def synonym_input(input):
    # map synonyms from actions_list and helper_list to their canonical keys
    for key, synonyms in actions_list.items():
      if input in synonyms:
        return key
    for key, synonyms in helper_list.items():
      if input in synonyms:
        return key
    for key, synonyms in special_list.items():
      if input in synonyms:
        return key
    for key, synonyms in directions_list.items():
      if input in synonyms:
        return key
    return input

  
  while True:
    while gameSetup == 0:
      try:
        if p1.HP <= 0:
          quit_gameDead()
          break
        if p1.win == True:
          quit_gameVictory(p1)
          break
      except:
          pass
      print_slow(f"\n**********[ {world.rooms[current_room]['name']} ]**********\n", typingActive)
      print_slow(world.rooms[current_room]['intro'], typingActive)
      player_choice = 0
      while player_choice == 0:
        print_slow('\n>', typingActive)
        playerInput = input().upper().strip()
        print('\n')
        # canonicalize synonyms to dict keys where appropriate
        playerInput_Syn = synonym_input(playerInput)

        if playerInput_Syn in directions_list:
          playerInput = playerInput_Syn
          move_rooms(p1)

        elif playerInput_Syn in special_list:
          special_actions(playerInput_Syn)

        elif playerInput_Syn in actions_list:
          take_actions()        

        elif playerInput_Syn in helper_list:
          helper_actions()

        elif p1.job == "GOD" and playerInput == 'ADD':
          print_slow('Enter item to add to inventory (cheater):', typingActive)
          playerInput = input().upper().strip()
          if playerInput in world.key_items:
            p1.inventory.append(playerInput)
            print_slow(f'{playerInput} added.', typingActive)
            break
          elif playerInput == "NONE":
            break
          else:
            print_slow('Enter a valid item dummy:', typingActive)
                        
        elif p1.job == "GOD" and playerInput == 'TRASH':
          print_slow('Enter item to remove from inventory (cheater?):', typingActive)
          playerInput = input().upper().strip()
          if playerInput in p1.inventory:
            p1.inventory.remove(playerInput)
            print_slow(f'{playerInput} removed.', typingActive)
            break
          elif playerInput == "NONE":
            break
          else:
            print_slow('Enter a valid item dummy:', typingActive)
                    
        else:
          soundFile = str(world.SFX_Library['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid input. Try again.', typingActive)
    while gameSetup == 1:
        setup()        
    while gameSetup == 2:
        intro_load()
    while gameSetup == 3:
        print(line000) #"Title screen"
        gameSetup = 2
        
    


if __name__ == '__main__':
  run_game()
