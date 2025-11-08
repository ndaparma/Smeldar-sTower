import random
import os
import sys
import time
from Settings import *
from pathlib import Path
player_special = None
captured = 0


def standard_battle(p1, foe, typingActive, SoundsOn):   
      global battle
      global turn_count  
      global player_turn
      global enemy_turn
      global player_wait
      global foe_wait
      global focus_turns
      global command
      global haste
      global cDEF
      global foe_powerdebuff_turns
      global foe_defensedebuff_turns
      global playerDefault_ATK
      global playerDefault_DEF
      global playerDefault_TDEF
      global playerDefaultACC
      global playerDefaultFOC
      global enemyDefault_ATK
      global enemyDefault_DEF
      global enemyDefault_TDEF
      global enemyDefaultACC
      global captured 
      global summon_active
      global sumMon

      #Initial stat backups
      playerDefault_ATK = p1.ATK
      playerDefault_DEF = p1.DEF
      playerDefault_TDEF = p1.TDEF
      playerDefaultACC = p1.ACC
      playerDefaultFOC = p1.FOC

      enemyDefault_ATK = foe.ATK
      enemyDefault_DEF = foe.DEF
      enemyDefault_TDEF = foe.TDEF
      enemyDefaultACC = foe.ACC
      
      
      cDEF = max(p1.DEF - p1.GDEF, 25) # cDEF == Character DEF with equipment modifiers applied, maximum of 75% protection from damage

      captured = 0 #Used for Shadow Snatcher capture mechanic
      foe_powerdebuff_turns = 0 #Turns enemy attack debuff is active
      foe_defensedebuff_turns = 0 #Turns enemy defense debuff is active
      haste = 0 #Status effect that grants extra player actions per turn (>0) or removes player APT (<0)
      focus_turns = 0 #Turns player buffs/debuffs are active
      turn_count = 1 #Turn counter
      player_wait = 0 # 0 == pass, 1 == Player has a multiturn skill active
      foe_wait = 0 #Turns an enemy has to use skill
      wait_skill = 0 #Skill used by the enemy that requires a wait time


      #Following declarations are for function scope
      damage = 0
      enemy_turn = 0
      turnOrder = 0
      summon_active = 0
      sumMon = None

      def turn_OrderDecision(p1, foe, turnOrder):
        if (p1.SPD + random.randrange(0, 11)) >= (foe.SPD + random.randrange(0, 21)):
          turnOrder = 0
        elif (p1.SPD + random.randrange(0, 11)) <= (foe.SPD + random.randrange(0, 21)):
          turnOrder = 1
        return turnOrder

      turnOrder = turn_OrderDecision(p1, foe, turnOrder)
      play_sound_effect(battle_sounds['Encounter'], SoundsOn)
      print_slow("\n**********COMBAT START**********\n", typingActive)
      print_slow(f"\nYou encounter a {foe.name}!\n", typingActive)  
      time.sleep(.5)
      if turnOrder == 0:
        print_slow(f"{p1.name} is faster and will act first this battle.\n", typingActive)
      elif turnOrder == 1:
        print_slow(f"The enemy {foe.name} is faster and will act first this battle.\n", typingActive)
      p1.stat_sCheck(typingActive)
      foe.stat_check(typingActive)
      print_slow("\nType battle command or type HELP for command list:\n", typingActive) 

      battle = 'ACTIVE'
      while battle == 'ACTIVE':
        print_slow(f"\n********** Turn[{turn_count}] **********\n", typingActive)
        print_slow(f"{p1.name}: [{p1.HP}/{p1.MaxHP}HP]  [{p1.MP}/{p1.MaxMP}MP]\n{foe.name}: [{foe.HP}/{foe.MaxHP}HP]\n", typingActive)
        print_slow("------------------------------", typingActive)


        #Focus turns determine number of turns damage augment lasts. Focus == 1 is normal, >1 is powered up, <1 is weakened
        if focus_turns > 0:
          focus_turns -= 1
          if focus_turns == 0:
              p1.FOC = playerDefaultFOC
              print_slow(f'{p1.name} damage has returned to normal.\n',typingActive)
          if p1.FOC > playerDefaultFOC:
            print_slow(f'\n{p1.name} is powered up for {focus_turns} more turns.\n',typingActive)
          if p1.FOC < playerDefaultFOC:
            print_slow(f'\n{p1.name} is weakend for {focus_turns} more turns.\n',typingActive)
          
        #Power debuff turns determine number of turns enemy attack debuff lasts
        if foe_powerdebuff_turns > 0:
            foe_powerdebuff_turns -= 1
            if foe_powerdebuff_turns == 0:
              print_slow(f'\nThe enemy {foe.name} is back to full strength!\n',typingActive)
              foe.ATK = enemyDefault_ATK
            else:
              print_slow(f'\nThe enemy {foe.name} is weakened for {foe_powerdebuff_turns} more turns.\n',typingActive)
       

        equipment_augments(p1, foe, sumMon,typingActive, SoundsOn)
        poison_effect(p1, foe, typingActive, SoundsOn)
        if p1.HP <= 0:
          player_death(p1, typingActive, SoundsOn, foe)
          break
        blind_effect(p1, foe, typingActive, SoundsOn)

        #Player goes first
        if turnOrder == 0:

          stop_effect(p1, typingActive, SoundsOn)
          player_Turn(p1, foe, player_turn, player_wait, typingActive, SoundsOn)
          equipment_augments(p1, foe, sumMon, typingActive, SoundsOn)
          command =  player_Turn
          time.sleep(1)
          enemy_death(p1, foe, command, damage, typingActive, SoundsOn) 
          turn_update(p1, foe, typingActive, SoundsOn)
          if battle != 'ACTIVE':
            break
          if summon_active == 1:
            summon_turn(p1, sumMon, foe, player_turn, player_wait, typingActive, SoundsOn)
            time.sleep(1)
            enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
            if battle != 'ACTIVE':
              break
          enemy_Turn(p1, foe, enemy_turn, foe_wait, typingActive, SoundsOn)
          turn_count += 1
          print_slow("______________________________", typingActive)
          time.sleep(1)
          if p1.HP <= 0:
            player_death(p1, typingActive, SoundsOn, foe)
            break
        #Enemy goes first
        if turnOrder == 1:

          turn_update(p1, foe, typingActive, SoundsOn)
          enemy_Turn(p1, foe, enemy_turn, foe_wait, typingActive, SoundsOn)
          time.sleep(1)
          if p1.HP <= 0:
            player_death(p1, typingActive, SoundsOn, foe)
            break
          #Start of player turn
          stop_effect(p1, typingActive, SoundsOn)
          time.sleep(1)
          if p1.HP <= 0 or battle != 'ACTIVE':
            break
          player_Turn(p1, foe, player_turn, player_wait, typingActive, SoundsOn)
          equipment_augments(p1, foe, sumMon, typingActive, SoundsOn)
          command =  player_Turn
          time.sleep(1)
          enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
          if battle != 'ACTIVE':
              break
          if summon_active == 1:
            summon_turn(p1, sumMon, foe, player_turn, player_wait, typingActive, SoundsOn)
            time.sleep(1)
            enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
            if battle != 'ACTIVE':
              break
          turn_count += 1
          print_slow("______________________________", typingActive)
            

def player_Turn(p1, foe, player_turn, player_wait, typingActive, SoundsOn):
  global item_used
  command = ""
  while player_turn == 1:       
          if player_wait == 0:
            
            command = (input().upper())
            
            #Attack command
            if command in attack_Terms:
                player_attack(p1, foe, typingActive, SoundsOn)
                break
                
              
            #Use item command
            elif command in item_Terms:
                use_item(p1, typingActive, SoundsOn)
                if item_used == True:
                  break
    
            #DEF Command
            elif command in defense_Terms:
                player_defend(p1, foe, typingActive, SoundsOn)
                break
    
            #Flee Command
            elif command in flee_Terms:
                player_flee(p1, foe, typingActive, SoundsOn)
                break
    
            #Player skills commands
            elif command in p1.skills:
                if p1.MP >= combat_skills[command]['MP']:
                  if p1.job != 'SUMMONER':
                    combat_skills[command]['s_Funk'](p1, foe, typingActive, SoundsOn)
                    break         
                  else:
                    if summon_active == 0:
                      combat_skills[command]['s_Funk'](p1, foe, typingActive, SoundsOn)
                      break
                    else:
                      print_slow(f'{p1.name} already has a summon active and cannot summon another at this time. \n', typingActive)
            #Out of MP for skill
                else:
                  print_slow(f'{p1.name} does not have enough MP and is unable to use {command} \n', typingActive)
              
            #Player needs help
            elif command in stat_Terms:
                p1.stat_check(typingActive)
                foe.stat_check(typingActive)
            elif command in help_Terms:
                combat_menu(p1, typingActive)
            else:
                soundFile = str(battle_sounds['Error'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow('\nInvalid input. Try again.\n', typingActive)
              
          elif player_wait >= 1:
            player_special(p1, foe, typingActive)
            break
  return command


def summon_turn(p1, sumMon, foe, player_turn, player_wait, typingActive, SoundsOn):
    global summon_active
    global foe_defensedebuff_turns

    def summon_attack(p1, sumMon, foe, typingActive):
      roll = random.randrange(1, 101)
      if roll <= sumMon.ACC:
          dam = random.randrange(sumMon.ATK // 2, sumMon.ATK * 1.5)
          damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
          foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
          print_slow(f'The summon {sumMon.name} ATTACKS.\n', typingActive)
          print_slow(
              f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP. \n', typingActive
          )
          enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
      elif roll > sumMon.ACC:
          print_slow(f'The summon {sumMon.name} misses their attack!\n', typingActive)

    def summon_turnUpdate(sumMon,  typingActive):
      global summon_active
      sumMon.turnsLeft -= 1
      if sumMon.turnsLeft <= 0:
          summon_active = 0
          sumMon.turnsLeft = sumMon.turns
          print_slow(f'The summon {sumMon.name} has vanished!\n', typingActive)


    while True:       
      scommand = random.randrange(1, 101)
      #Attack command
      if scommand <= 60:
        summon_attack(p1, sumMon, foe, typingActive)
        summon_turnUpdate(sumMon, typingActive)
        break
      elif 60 < scommand:
        summon_skills(p1, sumMon, foe, typingActive, SoundsOn)
        summon_turnUpdate(sumMon, typingActive)
        break
        

def enemy_Turn(p1, foe, enemy_turn, foe_wait, typingActive, SoundsOn):
   global foe_defensedebuff_turns

   while enemy_turn == 1:
          command2 = random.randrange(1, 101)
          #Enemy Commands [1]
          #ATTACK
          if foe_wait == 0:
            if command2 <= 40:  
                roll = random.randrange(1, 101)
                if roll <= foe.ACC:
                  dam = random.randrange(foe.ATK // 3, foe.ATK)
                  damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
                  p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
                  soundFile = str(enemy_weapon_sound(foe))
                  play_sound_effect(soundFile, SoundsOn)
                  print_slow(f'The enemy {foe.name} ATTACKS.\n', typingActive)
                  print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
                  p1.TDEF = playerDefault_TDEF
                  enemy_turn = 0
                  break
                elif roll > foe.ACC:
                  if p1.mainHand == 'MAIN GAUCHE':
                    soundFile = str(battle_sounds['pDefend'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(f"{p1.name} parries the enemy {foe.name}'s attack!\n", typingActive)
                  else:
                    soundFile = str(battle_sounds['eMiss'])
                    play_sound_effect(soundFile, SoundsOn)
                    print_slow(f'The enemy {foe.name} misses their attack!\n', typingActive)
                  p1.TDEF = playerDefault_TDEF
                  enemy_turn = 0
                  break
            #DEFEND
            elif 40 < command2 <= 55:  
                foe_defensedebuff_turns +=2
                foe.TDEF = max(min(foe.DEF * 1.2, 85), 50)
                soundFile = str(battle_sounds['eDefend'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'The enemy {foe.name} DEFENDS\n', typingActive)
                print_slow(f'The enemy {foe.name} has raised its defenses!\n', typingActive)
                p1.TDEF = playerDefault_TDEF
                enemy_turn = 0
                break
            #HEAL
            elif (55 < command2 <= 65 and foe.POTS > 0) and foe.HP < foe.MaxHP:  
                print_slow(f'The enemy {foe.name} HEALS\n', typingActive)
                heal = random.randrange(foe.MaxHP // 20, foe.MaxHP // 5)
                foe.HP = min(max(foe.HP + heal, 0), foe.MaxHP)
                foe.POTS -= 1
                soundFile = str(battle_sounds['eHeal'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'The enemy {foe.name} has healed {heal} HP. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive)
                p1.TDEF = playerDefault_TDEF
                enemy_turn = 0
                break
            #SKILL
            elif 65 < command2 and foe.MP > 0:  
                enemy_skills(p1, foe,  typingActive, SoundsOn)
                enemy_turn = 0
                break
            else:
                pass
          if foe_wait >= 1:
            enemy_skills(p1, foe,  typingActive, SoundsOn)
            enemy_turn = 0
            break


def turn_update(p1, foe, typingActive, SoundsOn):
  global player_turn
  global enemy_turn
  global foe_defensedebuff_turns
  global haste
  global command

  if haste > 0 and command == 'HASTE':
    pass
  if haste > 0 and command != 'HASTE':
    haste -= 1
    if haste != 0:
      print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)
  if haste == 0:
    if foe_defensedebuff_turns > 0:
      foe_defensedebuff_turns -= 1
      if foe_defensedebuff_turns == 0:
        print_slow(f'\nThe enemy {foe.name} defense has returned to normal!\n',typingActive)
        foe.TDEF = enemyDefault_TDEF
      else:
        pass  
    player_turn = 0
    enemy_turn = 1
  
    
def equipment_augments(p1, foe, sumMon, typingActive, SoundsOn):
  global playerDefault_ATK
  global playerDefault_DEF
  global enemyDefault_ATK
  global playerDefaultFOC

  foe.ACC = foe.MACC
  
  if p1.mainHand == 'AETHON':
    p1.ATK = playerDefault_ATK
    if p1.HP == p1.MaxHP:
      p1.ATK += 0
    elif (p1.MaxHP * .8) < p1.HP < p1.MaxHP:
      p1.ATK += 2
    elif (p1.MaxHP * .6) < p1.HP < (p1.MaxHP * .8):
      p1.ATK += 4
    elif (p1.MaxHP * .4) < p1.HP < (p1.MaxHP * .6):
      p1.ATK += 6
    elif (p1.MaxHP * .2) < p1.HP < (p1.MaxHP * .4):
      p1.ATK += 8
    elif 1 < p1.HP < (p1.MaxHP * .2):
      p1.ATK += 16
  if p1.mainHand == 'FULGUR':
    if focus_turns == 0:
      if p1.MP == p1.MaxMP:
          p1.FOC = playerDefaultFOC + 2
      elif (p1.MaxMP * .5) < p1.MP < p1.MaxMP:
          p1.FOC = playerDefaultFOC + 1
      else:
          p1.FOC = playerDefaultFOC - .25
  if p1.mainHand == 'MIDAS':
    p1.ATK = playerDefault_ATK
    if p1.GP <= 100:
      p1.ATK -= 8
    elif 100 < p1.GP < 250:
      p1.ATK -= 3
    elif 250 < p1.GP < 500:
      p1.ATK += 0
    elif 500 < p1.GP < 750:
      p1.ATK += 6
    elif 750 < p1.GP < 1000:
      p1.ATK += 9
    elif p1.GP >= 1000:
      p1.ATK += 12
  if p1.mainHand == 'DELPHI':
      try:
        sumMon.FOC = sumMon.DFOC + 2
      except:
        pass
  if p1.mainHand == 'SILVER BLADE' and 'UNDEAD' in foe.fam:
    p1.ATK += 5
  if p1.mainHand == 'SILVER BLADE' and 'VAMPIRE' in foe.fam:
    if focus_turns == 0:
      p1.FOC = playerDefaultFOC + .5
  if p1.offHand == 'CLOAK':
    foe.ACC -= 12
  if p1.offHand == 'MAIN GAUCHE':
    foe.ACC -= 8


def serpent_dagger_poison(p1, foe, typingActive, SoundsOn):
    if p1.mainHand == 'SERPENT DAGGER':
        roll = random.randrange(0, 11)
        if roll > 7:
          foe.POISON += 2
          print_slow(f"{foe.name} is now poisoned for {foe.POISON} turns!\n", typingActive)


def poison_effect(p1, foe, typingActive, SoundsOn):
  command = None
  if p1.POISON > 0:
      damage = round(p1.MaxHP // 12.5)
      p1.HP = p1.HP - damage
      p1.POISON = max(p1.POISON - 1, 0)
      print_slow(f"{p1.name} is suffering from the effects of poison! {p1.name} takes {damage} poison damage. {p1.name} has {p1.HP}/{p1.MaxHP}HP\n", typingActive)
  if foe.POISON > 0:
      damage = round(foe.MaxHP // 11)
      foe.HP = foe.HP - damage
      foe.POISON = max(foe.POISON - 1, 0)
      print_slow(f"{foe.name} is suffering from the effects of poison! {foe.name} takes {damage} poison damage. {foe.name} has {foe.HP}/{foe.MaxHP}HP\n", typingActive)
      enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
    

def blind_effect(p1, foe, typingActive, SoundsOn):
  if p1.BLIND > 0:
      print_slow(f"{p1.name} is temporarily blinded! {p1.name}'s accuracy has been reduced!\n", typingActive)
      p1.ACC = playerDefaultACC // 2
  
  if p1.BLIND < 0:
      p1.BLIND += 1
      if p1.BLIND == 0:
        print_slow(f"{p1.name}'s accuracy has returned to normal.\n",typingActive)
        p1.ACC = playerDefaultACC

  if foe.BLIND > 0:
      foe.ACC = foe.MACC // 2
      foe.BLIND = max(foe.BLIND - 1, 0)
      if foe.BLIND > 0:
        print_slow(f"{foe.name} is temporarily blinded! {foe.name}'s accuracy is reduced for {foe.BLIND} more turns.\n", typingActive)
      if foe.BLIND == 0:
        print_slow(f"{foe.name}'s vision has cleared!\n",typingActive)
        foe.ACC = foe.MACC
 

def stop_effect(p1, typingActive, SoundsOn):
  global haste
  global player_turn
  global enemy_turn

  if haste >= 0:
      player_turn = 1
  else:
      print_slow(f'\n{p1.name} is unable to move and cannot act this turn!\n',typingActive)
      print_slow(f'{p1.name} is disabled for {haste * -1} turns.\n',typingActive)
      enemy_turn = 1
      haste += 1


def player_death(p1, typingActive, SoundsOn, foe):
  if p1.HP <= 0:
    print_slow(f'\n{p1.name} is DEAD\n', typingActive)
    play_sound_effect(battle_sounds['Defeat'], SoundsOn)
    print_slow('**********[GAME OVER]**********\n', typingActive)
    combat_end_reset(p1, foe)


def enemy_death(p1, foe, command, damage, typingActive, SoundsOn):
  global battle
  global enemy_turn
  global player_turn
  global playerDefault_ATK
  global playerDefault_DEF
  global enemyDefault_ATK
  global captured
  
  if foe.HP == 0:
      enemy_turn = 0
      player_turn = 0
      GPE = round(random.randrange(foe.MinGP, foe.MaxGP) * p1.GR)
      p1.GP = p1.GP + GPE
      p1.xp = p1.xp + foe.exp
      if "GOBLIN" in foe.fam:
          p1.gobCount += 1
      if "FAE" in foe.fam:
          p1.faeCount += 1
      if foe.name == 'Shadow Snatcher':
          captured = 2
      if command == "BOLT":
          print_slow(f'{p1.name} vaporized the enemy!\n', typingActive)
      elif command == "STRIKE":
          print_slow(f'{p1.name} pulverised the enemy!\n', typingActive)
      elif command == "SEPPUKU":
          print_slow(f'{foe.name} defeated themself!\n', typingActive)
      elif damage >= foe.MaxHP // 2:
          print_slow(f'{p1.name} obliterated the enemy!\n', typingActive)
      else:
          print_slow(f'{p1.name} defeated the enemy.\n', typingActive)
      print_slow(
          f'{p1.name} gained {GPE}GP and {foe.exp}EXP. {p1.name} has {p1.GP}GP\n', typingActive
      )
      mugging_active = 1
      p1.enemiesKilled += 1
      item_drop(p1, foe, mugging_active, typingActive, SoundsOn)
      p1.level_up(typingActive, SoundsOn)
      print_slow("\n********** VICTORY!!! **********\n", typingActive)
      play_sound_effect(battle_sounds['Victory'], SoundsOn)
      combat_end_reset(p1, foe)
    

def combat_end_reset(p1, foe):
  global battle
  global playerDefault_ATK
  global playerDefault_DEF
  global playerDefaultACC
  global enemyDefault_ATK
  global enemyDefault_DEF
  global enemyDefaultACC

  exempt = ['Shadow Snatcher', 'Donkey', "Dark Warlock, Smeldar"]
  try:
    if foe.name not in exempt:
      foe.HP = foe.MaxHP
      foe.MP = foe.MaxMP
    foe.POTS = foe.MaxPOTS
    foe.ATK = enemyDefault_ATK
    foe.DEF = enemyDefault_DEF
    foe.TDEF = enemyDefault_TDEF
    foe.ACC = enemyDefaultACC
    foe.POISON = 0
    foe.BLIND = 0
    p1.ATK = playerDefault_ATK
    p1.DEF = playerDefault_DEF
    p1.TDEF = playerDefault_TDEF
    p1.ACC = playerDefaultACC
    p1.FOC = playerDefaultFOC
    battle = 'INACTIVE'
  except:
    pass
  
  
def item_drop(p1, foe, mugging_active, typingActive, SoundsOn):
    crafting_list = ['PLANT PART', 'MONSTER PART', 'RARE MONSTER PART', 'FAE DUST', 'DRAGON SCALE']
    consumables_list = ['POTION', 'ANTIDOTE', 'ETHER', 'SALINE', 'SMOKE BOMB', 'WARP CRYSTAL', 'KINDLING']
    equipment_list = []
    key_list = ['WAFFLE']

    inv_message = ""

    item_Drop_Rate = random.randrange(1,100)
    itemDrop = random.choice(foe.item)

    if item_Drop_Rate > foe.drop // mugging_active:

      if itemDrop in crafting_list:
         if 'CRAFTING POUCH' not in p1.inventory:
            inv_message = "CC"
         else:
            if itemDrop == 'PLANT PART':
              p1.PlantP += 1
            if itemDrop == 'MONSTER PART':
              p1.MonP += 1
            if itemDrop == 'RARE MONSTER PART':
              p1.RareP += 1
            if itemDrop == 'FAE DUST':
              p1.FaeP += 1
            if itemDrop == 'DRAGON SCALE':
              p1.DragonP += 1
            inv_message = "D"  
          
      if itemDrop in consumables_list:
        if itemDrop == 'POTION':
          if p1.POTS < p1.MaxPOTS:
            p1.POTS = min(p1.POTS + 1, p1.MaxPOTS)
            inv_message = "D" 
          else:
            inv_message = "F"
        if itemDrop == 'ANTIDOTE':
          if p1.ANT < p1.MaxANT:
            p1.ANT = min(p1.ANT + 1, p1.MaxANT)
            inv_message = "D"
          else:
            inv_message = "F"
        if itemDrop == 'ETHER':
          if p1.ETR < p1.MaxETR:
            p1.ETR = min(p1.ETR + 1, p1.MaxETR)
            inv_message = "D"
          else:
            inv_message = "F"
        if itemDrop == 'SALINE':
          if p1.SAL < p1.MaxSAL:
            p1.SAL = min(p1.SAL + 1, p1.MaxSAL)
            inv_message = "D"
          else:
            inv_message = "F"
        if itemDrop == 'SMOKE BOMB':  
          if p1.SMB < p1.MaxSMB:
            p1.SMB = min(p1.SMB + 1, p1.MaxSMB)
            inv_message = "D"
          else:
            inv_message = "F"
        if itemDrop == 'WARP CRYSTAL':
          if p1.WCR < p1.MaxWCR:
            p1.WCR = min(p1.WCR + 1, p1.MaxWCR)
            inv_message = "D"
          else:
            inv_message = "F"
        if itemDrop == 'KINDLING':
          if p1.KND < p1.MaxKND:
            p1.KND = min(p1.KND + 1, p1.MaxKND)
            inv_message = "D"
          else:
            inv_message = "F"

      if itemDrop in key_list or itemDrop in equipment_list:
        p1.inventory.append(itemDrop)
        inv_message = "D"

      if inv_message == "F":
        if mugging_active == 2:
          print_slow(f"{p1.name} tried to steal a {itemDrop}, however {p1.name}'s inventory is full. You cannot carry more of this item.\n", typingActive)
        else:
          print_slow(f"{foe.name} dropped a {itemDrop}, however {p1.name}'s inventory is full. You cannot carry more of this item.\n", typingActive)

      if inv_message == "CC":
          print_slow(f"{foe.name} dropped a {itemDrop}, however {p1.name}'s has nowhere to put it. You need a CRAFTING POUCH to store this item.\n", typingActive)

      if inv_message == "D":
          if mugging_active == 2:
            print_slow(f'{p1.name} stole a {itemDrop} from the enemy {foe.name}!\n', typingActive)
            print_slow(f'{p1.name} has added the {itemDrop} to their inventory.\n', typingActive)
          else:
              print_slow(f'The enemy {foe.name} dropped a {itemDrop}.\n', typingActive)
              print_slow(f'{p1.name} adds the {itemDrop} to their inventory.\n', typingActive)
          
    else:
      if mugging_active == 2:
        print_slow(f'{p1.name} failed to steal anything.\n', typingActive)


#Basic player actions
def player_attack(p1, foe, typingActive, SoundsOn):
    roll = random.randrange(0, 101)
    if roll <= p1.ACC:
      dam = random.randrange((p1.ATK // 4), p1.ATK) 
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      soundFile = str(player_weapon_sound(p1))
      play_sound_effect(soundFile, SoundsOn)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      serpent_dagger_poison(p1, foe, typingActive, SoundsOn)

    elif roll > p1.ACC:
        print_slow(f'{p1.name} misses their attack!\n', typingActive)
        soundFile = str(battle_sounds['pMiss'])
        play_sound_effect(soundFile, SoundsOn)


def player_defend(p1, foe, typingActive, SoundsOn):
    block = max(min(cDEF * .8, 85), 50)
    p1.TDEF -= block
    if p1.job == 'WIZARD' or p1.job == 'WITCH': 
      mpUp = random.randrange(3, 16)
    else:
      mpUp = random.randrange(1, 6)
    p1.MP = min(max(p1.MP + mpUp, 0), p1.MaxMP)
    print_slow(f'{p1.name} is defending!\n', typingActive)
    print_slow(f'{p1.name} has raised their defenses for the next turn and restored {mpUp} MP. {p1.name} has {p1.MP}/{p1.MaxMP} MP. \n', typingActive)
    soundFile = str(battle_sounds['pDefend'])
    play_sound_effect(soundFile, SoundsOn)


def player_flee(p1, foe, typingActive, SoundsOn):
  if foe.boss == 0:
    if p1.SMB > 0:
      p1.SMB -= 1
      print_slow(f'{p1.name} threw a SMOKE BOMB and escaped from combat! \n', typingActive)
      combat_end_reset(p1, foe)
      soundFile = str(battle_sounds['smoke'])
      play_sound_effect(soundFile, SoundsOn)
    elif p1.SMB <= 0:
      roll = random.randrange(0, 101)
      if p1.job == 'THIEF':
        roll += 50
      if roll <= 75:
        print_slow(f'{p1.name} successfully escaped from combat! \n', typingActive)
        combat_end_reset(p1, foe)
        soundFile = str(battle_sounds['smoke'])
        play_sound_effect(soundFile, SoundsOn)
      else:
        print_slow(f'{p1.name} failed to escape this time!\n', typingActive)
  else:
    print_slow(f'{p1.name} is unable to escape from the boss!\n', typingActive)


def use_item(p1, typingActive, SoundsOn): 
  global item_used 
  items_list = "ON"

  item_used = True
  while items_list == "ON":
      print_slow(f"Select item to use or BACK to return to battle commands:\nPOTION: {p1.POTS}\nANTIDOTE: {p1.ANT}\nETHER: {p1.ETR}\n", typingActive)
      command = (input().upper().strip())

      if command in potion_Terms and p1.POTS > 0:
          heal = random.randrange(25, max(50,  (p1.MaxHP // 3)) * (p1.RJ+1))
          p1.POTS -= 1
          p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
          items_list = "OFF"
          item_used = True
          print_slow(f'{p1.name} drinks a POTION and heals {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
          soundFile = str(battle_sounds['potion'])
          play_sound_effect(soundFile, SoundsOn)
      elif command in antidote_Terms and p1.ANT > 0:
          p1.ANT -= 1
          p1.POISON = 0
          items_list = "OFF"
          item_used = True
          print_slow(f"{p1.name} drinks an ANTIDOTE and is relieved of POISON!\n", typingActive)
          soundFile = str(battle_sounds['antidote'])
          play_sound_effect(soundFile, SoundsOn)
      elif command in ether_Terms and p1.ETR > 0:
          if p1.MaxMP >= 44:
            heal = random.randrange(10, (p1.MaxMP // 4))
          else:
            heal = 10
          p1.ETR -= 1
          p1.MP = min(max(p1.MP + heal, 0), p1.MaxMP)
          items_list = "OFF"
          item_used = True
          print_slow(f"{p1.name} drinks an ETHER and restores {heal} MP. {p1.name} has {p1.MP}/{p1.MaxMP} MP. \n", typingActive)
          soundFile = str(battle_sounds['ether'])
          play_sound_effect(soundFile, SoundsOn)
      elif command in saline_Terms and p1.SAL > 0:
          p1.SAL -= 1
          p1.BLIND = 0
          items_list = "OFF"
          item_used = True
          print_slow(f"{p1.name} uses a SALINE and is relieved of BLINDNESS!\n", typingActive)
          soundFile = str(battle_sounds['saline'])
          play_sound_effect(soundFile, SoundsOn)


      elif command in potion_Terms and p1.POTS == 0:
          print_slow('Unable to use a POTION at this time.\n', typingActive)
      elif command in antidote_Terms and p1.ANT == 0:
          print_slow('Unable to use an ANTIDOTE at this time.\n', typingActive)
      elif command in ether_Terms and p1.ETR == 0:
          print_slow('Unable to use an ETHER at this time.\n', typingActive)
      elif command in saline_Terms and p1.SAL == 0:
          print_slow('Unable to use SALINE at this time.\n', typingActive)
      elif command in back_Terms:
          items_list = "OFF"
          item_used = False
      else:
          soundFile = str(battle_sounds['Error'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('Invalid command. Try again.\n', typingActive)


#Warrior skill effects
def warrior_harden(p1, foe, typingActive, SoundsOn):
    heal = random.randrange(p1.MaxHP // 10, p1.MaxHP // 3)
    p1.HP = min(max(p1.HP + heal, 0), p1.MaxHP)
    p1.TDEF = max(cDEF, 3) 
    p1.MP -= combat_skills['HARDEN']['MP']
    print_slow(
        f'{p1.name} has bolstered their constitution. {p1.name} healed {heal} HP and shielded themself this turn. {p1.name} has {p1.HP}/{p1.MaxHP} HP \n', typingActive
    )


def warrior_wildstrikes(p1, foe, typingActive, SoundsOn):
    print_slow(f'{p1.name} strikes at the enemy {foe.name} with a mighty blow!\n', typingActive)
    roll = random.randrange(0, 101)
    if roll <= p1.ACC - 30:
        dam = random.randrange(p1.ATK // 3, p1.ATK) * p1.FOC
        damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)) * 2, 0)
        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
        print_slow(f'{p1.name} strikes for {damage} damage!\n', typingActive)
        soundFile = str(player_weapon_sound(p1))
        play_sound_effect(soundFile, SoundsOn)
    else:
      print_slow(f'{p1.name} swings and misses completely!\n', typingActive)
      soundFile = str(battle_sounds['pMiss'])
      play_sound_effect(soundFile, SoundsOn)
    p1.MP -= combat_skills['WILDSTRIKES']['MP']


def warrior_berserk(p1, foe, typingActive, SoundsOn):
    global player_special
    global player_wait
    
    if player_wait >= 1:
      dam = random.randrange((p1.ATK // 2), round(p1.ATK * 1.8)) * p1.FOC
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'{p1.name} attacks madly!\n',typingActive)
      print_slow(f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      soundFile = str(player_weapon_sound(p1))
      play_sound_effect(soundFile, SoundsOn)
      player_wait -= 1
      if player_wait == 0:
        print_slow(f'{p1.name} has calmed down and is no longer BERSERK.\n', typingActive)
        return
    if player_wait == 0:
      player_wait = random.randrange(2, 4)
      player_special = warrior_berserk
      p1.MP -= combat_skills['BERSERK']['MP']
      print_slow(f'{p1.name} is fueled by rage. {p1.name} has gone BERSERK for {player_wait} turns!\n', typingActive)


def warrior_bloodlust(p1, foe, typingActive, SoundsOn):
        dam = random.randrange((p1.ATK // 3), round(p1.ATK * 1.3)) * p1.FOC
        damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01)), 0)
        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
        p1.HP = min(p1.HP + (damage // 2), p1.MaxHP)
        print_slow(f'{p1.name} is filled with a bloodlust!\n',typingActive)
        print_slow(f"{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.{p1.name} has absorbed the enemy {foe.name}'s life force! {p1.name} gains {damage // 2} HP. {p1.name} has {p1.HP}/{p1.MaxHP}\n", typingActive)
        soundFile = str(battle_sounds['Spiked'])
        play_sound_effect(soundFile, SoundsOn)
        p1.MP -= combat_skills['BLOOD']['MP']


def warrior_battlecry(p1, foe, typingActive, SoundsOn):
        print_slow(f"{p1.name} looks to the sky and unleashes a mighty BATTLECRY!\n", typingActive)
        roll = random.randrange(2,5)
        roll2 = random.randrange(1,4)
        foe_powerdebuff_turns += roll
        if roll2 == 1:
          foe.ATK *= .9
          print_slow(f"{p1.name}'s BATTLECRY confuses the enemy {foe.name}. The enemy {foe.name}'s attack is reduced for {foe_powerdebuff_turns - 1} turns.\n", typingActive)
        elif roll2 == 2:
          foe.ATK *= .75
          print_slow(f"{p1.name}'s BATTLECRY intimidates the enemy {foe.name}! The enemy {foe.name}'s attack is reduced for {foe_powerdebuff_turns - 1} turns.\n", typingActive)
        elif roll2 == 3:
          foe.ATK *= .5
          print_slow(f"{p1.name}'s BATTLECRY strikes fear into the heart of the enemy {foe.name}! The enemy {foe.name}'s attack is reduced for {foe_powerdebuff_turns - 1} turns.\n", typingActive)
        soundFile = str(battle_sounds['Battlecry'])
        play_sound_effect(soundFile, SoundsOn)
        p1.MP -= combat_skills['BATTLECRY']['MP']


#Wizard skill effects
def wizard_focus(p1, foe, typingActive, SoundsOn):
    global focus_turns
    p1.FOC += (p1.lvl * .03) 
    focus_turns = random.randrange(2, 6)
    p1.MP -= combat_skills['FOCUS']['MP']
    print_slow(f'{p1.name} focuses their power. {p1.name} is powered up for {focus_turns - 1} turns!\n', typingActive)
    soundFile = str(battle_sounds['Focus'])
    play_sound_effect(soundFile, SoundsOn)


def wizard_bolt(p1, foe, typingActive, SoundsOn):
    dam = random.randrange(p1.ATK, round(p1.ATK * 1.5))
    damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC), 0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    p1.MP -= combat_skills['BOLT']['MP']
    print_slow(f'{p1.name} casts a magical bolt at the enemy {foe.name}. The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
    soundFile = str(battle_sounds['Bolt'])
    play_sound_effect(soundFile, SoundsOn)


def wizard_storm(p1, foe, typingActive, SoundsOn):
    print_slow(f'{p1.name} conjuers a fierce lightning storm!\n', typingActive)
    storm_rolls = 0
    tl_damage = 0
    while storm_rolls < 3:
      roll = random.randrange(0, 4)
      if roll >= 1:
          dam = round(random.randrange(p1.ATK // 2.5, p1.ATK))
          damage = round(max(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC, 0))
          tl_damage = tl_damage + damage
          storm_rolls += 1
          print_slow(f'Lighting strikes for {damage} damage!\n', typingActive)
      else:
          print_slow('lightning strikes and misses!\n', typingActive)
          storm_rolls += 1
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    p1.MP -= combat_skills['STORM']['MP']
    print_slow(f'{foe.name} has taken {tl_damage} total damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
    soundFile = str(battle_sounds['Storm'])
    play_sound_effect(soundFile, SoundsOn)


def wizard_blast(p1, foe, typingActive, SoundsOn):
    print_slow(f'{p1.name} concentrates their magic!\n', typingActive)
    roll = random.randrange(0, 6) * p1.FOC
    if roll >= 4:
        damage = foe.HP // 8
        foe.HP -= damage
        print_slow(f'{p1.name} blasts the enemy {foe.name} away for {damage} damage! {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
        soundFile = str(battle_sounds['Blast'])
        play_sound_effect(soundFile, SoundsOn)
    else:
        print_slow(f"{p1.name}'s magical energy fizzles out...\n", typingActive)
        soundFile = str(battle_sounds['Fizzle'])
        play_sound_effect(soundFile, SoundsOn)
    p1.MP -= combat_skills['BLAST']['MP']


def wizard_shock(p1, foe, typingActive, SoundsOn):
  global haste
  print_slow(f'{p1.name} conjures a ball of magical lightning!\n', typingActive)
  roll = random.randrange(0,101)
  dam = round(random.randrange(p1.ATK * 1.5, round(p1.ATK * 2)))
  damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC), 0)
  foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
  if roll <= 10:
    p1.TDEF += 100
    p1.HP = min(max(p1.HP - (dam // 4), 0), p1.MaxHP)
    print_slow(f"{p1.name}'s lightning ball errupts across the battlefield too soon, shocking everything in the area!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.{p1.name} is shocked for {dam // 4} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. {p1.name}'s DEF is temporarily reduced!'\n", typingActive)
    
  if 10 < roll <= 65:
    print_slow(f"{p1.name}'s lightning ball explodes just ahead of the enemy {foe.name}!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n", typingActive)
    
  if 65 < roll <= 100:
    haste += random.randrange(2, 4)
    print_slow(f"{p1.name}'s lightning ball discharges directly into the the enemy {foe.name}!\n", typingActive)
    print_slow(f"The enemy {foe.name} is shocked for {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\nThe enemy {foe.name} is paralyzed! {p1.name} has {haste - 1} more actions this turn.\n", typingActive)
  soundFile = str(battle_sounds['Shock'])
  play_sound_effect(soundFile, SoundsOn)
  p1.MP -= combat_skills['SHOCK']['MP']


#Thief skill effects
def thief_steal(p1, foe, typingActive, SoundsOn):
    roll = random.randrange(0, 6)
    if roll == 5:
        GPE = round(random.randrange(foe.MinGP, round(foe.MaxGP * 0.8)) * p1.GR)
        p1.GP = p1.GP + GPE
        soundFile = str(battle_sounds['Steal'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'{p1.name} manages to steal {GPE} GP from the enemy {foe.name}. {p1.name} now has {p1.GP}GP.\n', typingActive)
    elif 0 < roll < 5:
        GPE = round(random.randrange(round(foe.MinGP * 0.5), round(foe.MaxGP * 0.5)) * p1.GR)
        p1.GP = p1.GP + GPE
        soundFile = str(battle_sounds['Steal'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'{p1.name} manages to steal {GPE} GP from the enemy {foe.name}. {p1.name} now has {p1.GP}GP.\n', typingActive)
    elif roll == 0:
        soundFile = str(battle_sounds['pMiss'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'{p1.name} failed to steal anything! \n', typingActive)
    p1.MP -= combat_skills['STEAL']['MP']
    


def thief_poisondagger(p1, foe, typingActive, SoundsOn):
    dagger = 0
    print_slow(f'{p1.name} throws a handful of poison daggers!\n', typingActive)
    roll = random.randrange(0, 101)
    if roll <= p1.ACC - 25:
        foe.POISON += 2
        dagger += 1
        damage1 = round(p1.ATK // 8)
    else:
        damage1 = 0
    roll = random.randrange(0, 3)
    if roll <= p1.ACC - 25:
        foe.POISON += 2
        dagger += 1
        damage2 = round(p1.ATK // 8)
    else:
        damage2 = 0
    roll = random.randrange(0, 3)
    if roll <= p1.ACC - 25:
        foe.POISON += 2
        dagger += 1
        damage3 = round(p1.ATK // 8)
    else:
        damage3 = 0
    tl_damage = damage1 + damage2 + damage3
    foe.HP = min(max(foe.HP - tl_damage, 0), foe.MaxHP)
    p1.MP -= combat_skills['THROW']['MP']
    print_slow(f'{p1.name} roll the enemy {foe.name} with {dagger} poison dagger(s)! The enemy {foe.name} has taken {tl_damage} total damage and is poisoned for {foe.POISON} turns. {foe.name} has {foe.HP}/{foe.MaxHP} HP\n', typingActive)
    soundFile = str(battle_sounds['Throw'])
    play_sound_effect(soundFile, SoundsOn)


def thief_mug(p1, foe, typingActive, SoundsOn):
    print_slow(f'{p1.name} mugs the enemy {foe.name}!\n', typingActive)
    dam = random.randrange((p1.ATK // 3.5), p1.ATK) * p1.FOC
    damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC), 0)
    foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    print_slow(f'{foe.name} has taken {damage} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
    soundFile = str(player_weapon_sound(p1))
    play_sound_effect(soundFile, SoundsOn)
    p1.MP -= combat_skills['MUG']['MP']
    mugging_active = 2
    item_drop(p1, foe, mugging_active, typingActive, SoundsOn)


def thief_haste(p1, foe, typingActive, SoundsOn):
  global haste
  if haste == 0:
    print_slow(f"{p1.name}'s adrenalin is pumping! {p1.name} gains additional actions this turn.\n", typingActive)
    haste = 2
    p1.MP -= combat_skills['HASTE']['MP']
    print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)
    soundFile = str(battle_sounds['Haste'])
    play_sound_effect(soundFile, SoundsOn)
  else:
    print_slow('Unable to use skill twice in a row.\n', typingActive)
    print_slow(f'{p1.name} has {haste} more action(s) this turn.\n',typingActive)


def thief_cointhrow(p1, foe, typingActive, SoundsOn):
  while True:
    print_slow(f"Input amount of GP you would like to throw (0-{p1.GP})\n", typingActive)
    toss = input()   
    if toss.isdigit():
      toss = int(toss)
      if 0 <= toss <= p1.GP:
        if toss == 0:
          dam = 0
        elif 0 < toss <= 50:
          dam = random.randrange(1, 6)
          foe.HP -= dam
        elif 50 < toss <= 100:
          dam = random.randrange(5, 11)
          foe.HP -= dam
        elif 100 < toss <= 250:
          dam = random.randrange(10, 21)
          foe.HP -= dam
        elif 250 < toss <= 500:
          dam = random.randrange(20, 36)
          foe.HP -= dam
        elif 500 < toss:
          dam = random.randrange(35, 51)
          foe.HP -= dam
        print_slow(f"{p1.name} tosses {toss} GP at the enemy {foe.name}! The enemy {foe.name} takes {dam} damage!\n", typingActive)
        p1.MP -= combat_skills['$THROW']['MP']
        battle_sounds['$Throw']
        break
      else:
        soundFile = str(battle_sounds['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"Invalid selection. Please select an amount between (0-{p1.GP})\n", typingActive)
    else:
        soundFile = str(battle_sounds['Error'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"Invalid selection. Please select an amount between (0-{p1.GP})\n", typingActive)
          

#Summoner skill effects
def summoner_ember(p1, foe, typingActive, SoundsOn):
    global summon_active
    global sumMon

    print_slow(f'{p1.name} evokes Ember!\n', typingActive)
    summon_active = 1
    p1.MP -= combat_skills['EMBER']['MP']
    roll = random.randrange(0, 101) + p1.lvl // 2
    if roll <= 60:
      sumMon = s1
    else:
      sumMon = s2
    print_slow(f"{p1.name} has summoned {sumMon.name} to the battlefield!\n", typingActive)
    soundFile = str(battle_sounds['Summon'])
    play_sound_effect(soundFile, SoundsOn)

def summoner_aqua(p1, foe, typingActive, SoundsOn):
    global summon_active
    global sumMon

    print_slow(f'{p1.name} evokes Aqua!\n', typingActive)
    summon_active = 1
    p1.MP -= combat_skills['AQUA']['MP']
    roll = random.randrange(0, 101) + p1.lvl // 2
    if roll <= 65:
      sumMon = s3
    else:
      sumMon = s4
    print_slow(f"{p1.name} has summoned {sumMon.name} to the battlefield!\n", typingActive)
    soundFile = str(battle_sounds['Summon'])
    play_sound_effect(soundFile, SoundsOn)

def summoner_terra(p1, foe, typingActive, SoundsOn):
    global summon_active
    global sumMon

    print_slow(f'{p1.name} evokes Terra!\n', typingActive)
    summon_active = 1
    p1.MP -= combat_skills['TERRA']['MP']
    roll = random.randrange(0, 101) + p1.lvl // 2
    if roll <= 70:
      sumMon = s5
    else:
      sumMon = s6
    print_slow(f"{p1.name} has summoned {sumMon.name} to the battlefield!\n", typingActive)
    soundFile = str(battle_sounds['Summon'])
    play_sound_effect(soundFile, SoundsOn)

def summoner_aero(p1, foe, typingActive, SoundsOn):
    global summon_active
    global sumMon

    print_slow(f'{p1.name} evokes Aero!\n', typingActive)
    summon_active = 1
    p1.MP -= combat_skills['AERO']['MP']
    roll = random.randrange(0, 101) + p1.lvl // 2
    if roll <= 75:
      sumMon = s7
    else:
      sumMon = s8
    print_slow(f"{p1.name} has summoned {sumMon.name} to the battlefield!\n", typingActive)
    soundFile = str(battle_sounds['Summon'])
    play_sound_effect(soundFile, SoundsOn)

def summoner_aether(p1, foe, typingActive, SoundsOn):      
    global summon_active
    global sumMon

    print_slow(f'{p1.name} evokes Aether!\n', typingActive)
    summon_active = 1
    p1.MP -= combat_skills['AETHER']['MP']
    roll = random.randrange(0, 101) + p1.lvl // 2
    if roll <= 80:
      sumMon = s9
    else:
      sumMon = s10
    print_slow(f"{p1.name} has summoned {sumMon.name} to the battlefield!\n", typingActive)
    soundFile = str(battle_sounds['Summon'])
    play_sound_effect(soundFile, SoundsOn)

#summon monster skill effects
def summon_skills(p1, sumMon, foe, typingActive, SoundsOn):
    global focus_turns
    global foe_defensedebuff_turns

    # 1. Fox Fire
    # 2. Healing Warmth
    # 3. Blaze
    # 4. Restoration
    # 5. Water Spout
    # 6. Toxic Fangs
    # 7. Fridged Kiss
    # 8. Frostbite Snap
    # 9. Rock Slide
    # 10. Barrier Wall
    # 11. Mereorain
    # 12. Barrier Shell
    # 13. Razor Gale 
    # 14. Windscar
    # 15. Updraft
    # 16. Hurricane
    # 17. Holy Light
    # 18. Regain
    # 19. Astral Storm
    # 20. Void Pulse

    s_Skill = random.choice(sumMon.skill)

    if s_Skill == 1:  #Fox Fire
      dam = random.randrange(sumMon.ATK, round(sumMon.ATK + 30))
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * p1.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Fox Fire at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)

    if s_Skill == 2:  #Healing Warmth
      heal = random.randrange(40, max(60,  (p1.MaxHP // 4)))
      p1.HP = min(p1.HP + heal, p1.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Healing Warmth. {p1.name} recovers {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)

    if s_Skill == 3:  #Blaze
      dam = random.randrange(sumMon.ATK, round(sumMon.ATK + 60))
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Blaze at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)

    if s_Skill == 4:  #Restoration
      heal = random.randrange(100, max(150,  (p1.MaxHP // 2)))
      p1.HP = min(p1.HP + heal, p1.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Restoration. {p1.name} recovers {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)

    if s_Skill == 5:  #Water Spout
      hits = random.randrange(2, 6) + (p1.lvl // 10) 
      dam = hits * 25
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Water Spout at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)

    if s_Skill == 6:  #Toxic Fangs
      foe.POISON += random.randrange(2, 5)
      print_slow(f'The summon {sumMon.name} bites the enemy {foe.name} with Toxic Fangs. The enemy {foe.name} is poisoned for {foe.POISON} turns.\n', typingActive)

    if s_Skill == 7:  #Fridged Kiss
      dam = random.randrange(sumMon.ATK + 10, round(sumMon.ATK * 1.7))
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Fridged Kiss at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)

    if s_Skill == 8:  #Frostbite Snap
      foe.BLIND += 5
      dam = random.randrange(round(sumMon.ATK * 1.5), round(sumMon.ATK * 2.4))
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Frostbite Snap at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      print_slow(f'The enemy {foe.name} is BLINDED for {foe.BLIND} turns!\n', typingActive)

    if s_Skill == 9:  #Rock Slide
      roll = random.randrange(0, 101)
      if roll >= 20:
        dam = foe.HP // 12
        damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
        foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
        print_slow(f'The summon {sumMon.name} casts Rock Slide at the enemy {foe.name}.\n', typingActive)
        print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      else:
        print_slow(f'The summon {sumMon.name} casts Rock Slide at the enemy {foe.name}, but it misses!\n', typingActive)

    if s_Skill == 10:  #Barrier Wall
      p1.TDEF += (p1.lvl * 1.5)
      print_slow(f'The summon {sumMon.name} casts Barrier Wall. {p1.name} DEF is increased for 1 turn.\n', typingActive)

    if s_Skill == 11:  #Meteorain
      hits = random.randrange(4, 8) + turn_count // 5 
      dam = hits * round(random.randrange(sumMon.ATK, sumMon.ATK *2))
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)

    if s_Skill == 12:  #Barrier Shell  
      p1.TDEF += (p1.lvl * 2.5)   
      print_slow(f'The summon {sumMon.name} casts Barrier Shell. {p1.name} DEF is increased for 1 turn.\n', typingActive)

    if s_Skill == 13:  #Razor Gale
      hits = foe.SPD // 5 + p1.SPD // 5 
      dam = hits * sumMon.ATK
      damage = max(round(dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Razor Gale at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      roll = random.randrange(0, 6)
      if roll == 5:
        sumMon.turnsLeft = min(sumMon.turnsLeft + 1, sumMon.turns)
        print_slow(f'The summon {sumMon.name} is invigorated by the wind and extends its stay by 1 turn!\n', typingActive)
       
    if s_Skill == 14:  #Windscar
      dam = random.randrange(round(sumMon.ATK * 1.2), round(sumMon.ATK * 1.8)) + p1.lvl * 1.5
      damage = max(round((dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC)), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      foe_defensedebuff_turns += 2
      foe.TDEF += foe.TDEF + foe.SPD
      print_slow(f'The summon {sumMon.name} casts Windscar. The enemy {foe.name}\'s defenses are temporarily reduced.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)

    if s_Skill == 15:  #Updraft
      dam = random.randrange(round(sumMon.ATK * 1.5), round(sumMon.ATK * 2.4))
      damage = max(round((dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC) + foe.SPD * 2), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Updraft at the enemy {foe.name}.\n', typingActive)
      print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      if p1.BLIND <= 0:
        p1.BLIND += 4
        p1.ACC *= 2
        print_slow(f'Harbok shares his power with {p1.name} for {p1.BLIND +1} turns! {p1.name}\'s accuracy is increased temporarily.\n', typingActive)
      else:
        print_slow(f'{p1.name} is blinded and Harbok is unable to share his power with {p1.name} at this time.\n', typingActive)

    if s_Skill == 16:  #Hurricane
      if foe.boss == 0:
        if foe.HP <= (foe.MaxHP // 100)*15:
            foe.HP = 0
            print_slow(f'The summon {sumMon.name} casts Hurricane. The enemy {foe.name} is swept away in a torrent of wind!\n', typingActive)
        else:
            dam = foe.SPD * 5 + random.randrange(round(sumMon.ATK // 2), round(sumMon.ATK * 1.5))
            damage = max(round((dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC)), 0)
            foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
            print_slow(f'The summon {sumMon.name} casts Hurricane at the enemy {foe.name}.\n', typingActive)
            print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
          
      else:
          dam = foe.SPD * 8 + random.randrange(round(sumMon.ATK // 2), round(sumMon.ATK * 1.5))
          damage = max(round((dam * (foe.DEF * 0.01 * foe.TDEF * 0.01) * sumMon.FOC)), 0)
          foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
          print_slow(f'The summon {sumMon.name} casts Hurricane at the enemy {foe.name}.\n', typingActive)
          print_slow(f'The enemy {foe.name} has taken {damage} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
          
    if s_Skill == 17:  #Holy Light
      focus_turns += 3
      p1.FOC += (p1.lvl * .025)
      print_slow(f'The summon {sumMon.name} casts Holy Light. {p1.name} is powered up for {focus_turns - 1} turns!\n', typingActive)

    if s_Skill == 18:  #Regain
      heal = random.randrange(p1.MaxHP // 2, p1.MaxHP)
      p1.HP = min(p1.HP + heal, p1.MaxHP)
      print_slow(f'The summon {sumMon.name} casts Regain. {p1.name} recovers {heal} HP. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
 
    if s_Skill == 19:  #Astral Storm
      hits = p1.lvl // 10
      dam = hits * round(random.randrange(sumMon.ATK * 1.5, sumMon.ATK * 3))
      damage = max(round(dam * sumMon.FOC), 0)
      foe.HP = min(max(foe.HP - damage, 0), foe.MaxHP)
    
    if s_Skill == 20:  #Void Pulse
      if foe.boss == 0:
        roll = random.randrange(0, 101) + (p1.lvl // 5)
        if roll >= 55:
          foe.HP = 0
          print_slow(f'The summon {sumMon.name} casts Void Pulse. The enemy {foe.name} is cast into an endless void!\n', typingActive)
        else:
           dam = foe.HP // 2
           foe.HP = min(max(foe.HP - dam, 0), foe.MaxHP)
           print_slow(f'The summon {sumMon.name} casts Void Pulse. The enemy {foe.name} resists the effect and takes {dam} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)
      else:
          dam = foe.HP // 10
          foe.HP = min(max(foe.HP - dam, 0), foe.MaxHP)
          print_slow(f'The summon {sumMon.name} casts Void Pulse. The enemy {foe.name} resists the effect and takes {dam} damage. The enemy {foe.name} has {foe.HP}/{foe.MaxHP} HP.\n', typingActive)


#Enemy skill effects
def enemy_skills(p1, foe, typingActive, SoundsOn):
    global battle
    global foe_wait
    global focus_turns
    global wait_skill
    global cDEF
    global captured
    global haste
    global foe_defensedebuff_turns

    # 1.  Flee
    # 2.  Cleave
    # 3.  Maul
    # 4.  Magic Bolt
    # 5.  Steal
    # 6.  Fire Breath
    # 7.  Sting
    # 8.  Poison Mist
    # 9.  Quake
    # 10. Summon Swarm
    # 11. Roar
    # 12. Kancho
    # 13. Poison Bite
    # 14. Dales Pocket-sand
    # 15. Skewer
    # 16. Gunk Shot
    # 17. Cripple
    # 18. Assualt
    # 19. Root
    # 20. Vampire Bite
    # 21. Spirit Drain
    # 22. Vanish
    # 23. Self-Destruct
    # 24. Whirlwind
    # 25. Peck
    # 26. Snatch
    # 27. Tail Whip
    # 28. Demon's Gaze
    # 29. Stone Gaze
    # 30. Nova
    # 31. Acid Spit

    if foe_wait == 0:
      f_Skill = random.choice(foe.skill)
    if foe_wait >= 1:
      f_Skill = wait_skill
    
    if f_Skill == 1:  #Flee
        escape = random.randrange(0, 4)
        if escape >= 2:
            soundFile = str(battle_sounds['Flee'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} scuttles away! You earn nothing. Sucks to suck.\n', typingActive)
            print_slow("**********Enemy Escape!**********\n", typingActive)
            combat_end_reset(p1, foe)
        else:
            soundFile = str(battle_sounds['Flee_fail'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'Enemy {foe.name} attempted to escape but stumbled and failed!\n', typingActive)
            p1.TDEF = playerDefault_TDEF
            foe.MP -= 1

    elif f_Skill == 2:  #Cleave
        dam = random.randrange(round(foe.ATK // 1.5), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        soundFile = str(battle_sounds['Cleave'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} strikes with a cleaving blow!\n', typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 3:  #Maul
        dam = random.randrange(foe.ATK // 2, foe.ATK)
        damage = max(round(dam + 3 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        soundFile = str(battle_sounds['Maul'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} charges wildly and mauls {p1.name}!\n', typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 4:  #Magic Bolt
        dam = random.randrange(foe.ATK, round(foe.ATK * 1.3))
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        soundFile = str(battle_sounds['MagicBolt'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} concentrates their power into a magic bolt and hurls it at {p1.name}!\n', typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 5:  #Steal
        pilfer = random.randrange(0, 3)
        if pilfer >= 2:
            GPL = random.randrange(foe.MinGP, round(foe.MaxGP // 1.5))
            p1.GP = p1.GP + GPL
            soundFile = str(battle_sounds['eSteal'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} manages to steal {GPL}GP from {p1.name}. {p1.name} now has {p1.GP}GP.\n', typingActive)
        elif pilfer < 2:
            soundFile = str(battle_sounds['eSteal_fail'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'{foe.name} attempted to steal but failed to grab anything!\n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 6:  #Fire Breath
      while True:
        if foe_wait == 1:
          dam = random.randrange(foe.ATK, round(foe.ATK * 1.2))
          soundFile = str(battle_sounds['FireBreath'])
          play_sound_effect(soundFile, SoundsOn)
          damage = max(round(dam + 6 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
          p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
          if any(fam in foe.fam for fam in ["DRAGON", "DEMON", "MYTHIC", "BEAST"]):
            print_slow(f"Flames erupt from the enemy {foe.name}'s mouth, scorching '{p1.name}!\n", typingActive)
          else:
            print_slow(f"Flames erupt from the enemy {foe.name}'s hands, engulfing '{p1.name}!\n", typingActive)

          print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining. \n', typingActive)
          foe_wait = 0
          p1.TDEF = playerDefault_TDEF
          break
        if foe_wait == 0:
          soundFile = str(battle_sounds['Fire Breath Charge'])
          play_sound_effect(soundFile, SoundsOn)
          if any(fam in foe.fam for fam in ["DRAGON", "DEMON", "MYTHIC", "BEAST"]):
            print_slow(f'Smoke begins raising from {foe.name} mouth...\n', typingActive)
          else:
            print_slow(f'Smoke begins raising from {foe.name} hands...\n', typingActive)
          foe_wait = 1
          wait_skill = 6
          p1.TDEF = playerDefault_TDEF
          foe.MP -= 1
          break

    elif f_Skill == 7:  #Sting
        dam = random.randrange(foe.ATK // 2 + 4, foe.ATK + 4)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        pdamage = random.randrange(1, 3)
        p1.POISON += pdamage
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        damage2 = 5
        foe.HP = min(max(foe.HP - damage2, 0), foe.MaxHP)
        soundFile = str(battle_sounds['Sting'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} rushes at {p1.name} with their stinger!\n', typingActive)
        print_slow( f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        print_slow(f'{foe.name} has taken {damage2} damage. {foe.name} has {foe.HP}/{foe.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
        if foe.HP <= 0:
            print_slow(f'{foe.name} killed themself.\n', typingActive)
            command = "SEPPUKU"
            enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
          
    elif f_Skill == 8:  #Poison Mist
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        soundFile = str(battle_sounds['PoisonMist'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'{foe.name} sprays a poison mist at {p1.name}! {p1.name} is poisoned for {pdamage} turns.\n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 9:  #Quake
        damage = max(
            random.randrange(round(foe.ATK // 2), round(foe.ATK * 0.8)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        soundFile = str(battle_sounds['Quake'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} strikes with the ground causing a mighty quake!\n', typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 10:  #Summon Swarm
        print_slow(f'{foe.name} summons a swarm of smaller BEES to attack {p1.name}.\n', typingActive)
        bee_rolls = 0
        tl_damage = 0
        while bee_rolls < 3:
          roll = random.randrange(0, 4)
          time.sleep(0.5)
          if roll >= 1:
              dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
              damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
              tl_damage = tl_damage + damage
              p1.POISON += 1
              bee_rolls += 1
              soundFile = str(battle_sounds['Summon Swarm'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow(f'{p1.name} is stung for {damage} damage and is poisoned!\n', typingActive)
          else:
              soundFile = str(battle_sounds['Fist'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow(f'{p1.name} swats a BEE away!\n', typingActive)
        p1.HP = min(max(p1.HP - tl_damage, 0), p1.MaxHP)    
        print_slow(f'{p1.name} has taken {tl_damage} total damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. {p1.name} is poisoned for the next {p1.POISON} turns.\n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 11:  #Roar
        if foe.name == "Dire Wolf":
          soundFile = str(battle_sounds['Roar1'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{foe.name} lets out a tremendous howl reducing {p1.name}'s defenses temporarily!\n", typingActive)
          p1.TDEF = 150
          foe.MP -= 1

        elif foe.name == "Dragon King, Tanninim":
          soundFile = str(battle_sounds['Roar4'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{foe.name} lets out an ear shattering shriek reducing {p1.name}'s defenses temporarily!\n", typingActive)
          p1.TDEF = 200

        elif foe.name == "Tiger":
          soundFile = str(battle_sounds['Roar2'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{foe.name} lets out a Terrifying roar reducing {p1.name}'s defenses temporarily!\n", typingActive)
          p1.TDEF = 125

        else:
          soundFile = str(battle_sounds['Roar3'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{foe.name} lets out a ferocious roar reducing {p1.name}'s defenses temporarily!\n", typingActive)
          p1.TDEF = 125
          foe.MP -= 1

    elif f_Skill == 12:  #Kancho
        print_slow(
            f"{foe.name} grabs {p1.name} from behind!\n", typingActive
        )
        roll = random.randrange(0, 4)
        if roll >= 2:
            dam = random.randrange(foe.ATK // 3, foe.ATK // 1.5)
            damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            foe.HP = min(max(foe.HP + damage // 2, 0), foe.MaxHP)
            soundFile = str(battle_sounds['Kancho'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'{p1.name} has their life force ripped from their body and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.{foe.name} consumes the life force and gains {damage//2} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n', typingActive)
        else:
            soundFile = str(battle_sounds['eMiss'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f"{p1.name} escapes the {foe.name}'s hold!\n", typingActive)      
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 13:  #Poison Bite
        dam = random.randrange(foe.ATK // 2.5, foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)        
        if foe.name == 'Harpy':
          pdamage = random.randrange(2, 6)
          p1.POISON += pdamage
          soundFile = str(battle_sounds['Claw'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f'The {foe.name} claws at {p1.name} with their toxic talons! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
        if foe.name == 'Orc Archer':
          pdamage = random.randrange(1, 5)
          p1.POISON += pdamage
          soundFile = str(battle_sounds['Stab'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f'The {foe.name} shoots {p1.name} with a poisoned arrow! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
        else:
          pdamage = random.randrange(1, 4)
          p1.POISON += pdamage
          soundFile = str(battle_sounds['ToxicBite'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f'The {foe.name} bites down on {p1.name} with their toxic fangs! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 14:  #Dale's Pocket-sand
        p1.FOC *= .7
        focus_turns += 4
        soundFile = str(battle_sounds['Dales Pocket-sand'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"{foe.name} throws a blue powder in {p1.name}'s face! {p1.name} has their power lowered for {focus_turns - 1} turns!\n", typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
      
    elif f_Skill == 15:  #Skewer
        if foe.name == 'Unicorn':
          print_slow(f'The enemy {foe.name} charges forward with their horn and skewers {p1.name}!\n', typingActive)
        else:
          print_slow(f'The enemy {foe.name} charges forward with their weapon and skewers {p1.name}!\n', typingActive)
        roll = random.randrange(0, 4)
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        if roll >= 2:
          soundFile = str(battle_sounds['Skewer'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"The enemy {foe.name} manages to break through {p1.name}'s armor'! {p1.name}'s defenses are temporarily lowered.\n", typingActive)
          p1.TDEF += 50
        elif roll < 2:
          soundFile = str(battle_sounds['pDefend'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{p1.name}'s armor saved them from being impaled!\n", typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        foe.MP -= 1

    elif f_Skill == 16:  #Gunk Shot
        soundFile = str(battle_sounds['Gunk Shot'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"The enemy {foe.name} spews a tar-like gunk at {p1.name}'s face!\n", typingActive)
        roll = random.randrange(0, 4)
        if roll >= 1:
          p1.BLIND += 3
          print_slow(f"The enemy {foe.name} has temporarily blinded {p1.name}! {p1.name} is blinded for {p1.BLIND - 1} turns.\n", typingActive)
        elif roll < 1:
          soundFile = str(battle_sounds['eMiss'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{p1.name} manages to avoid the gunk!\n", typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1

    elif f_Skill == 17:  #Cripple
      dam = random.randrange(round(foe.ATK // 2), foe.ATK)
      damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
      p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
      roll = random.randrange(0, 101)
      soundFile = str(battle_sounds['Cripple'])
      play_sound_effect(soundFile, SoundsOn)
      if "BEAST" in foe.fam or foe.name == 'Jaw Demon':
        print_slow(f'The enemy {foe.name} bites down with crippling force!\n', typingActive)
      else:
        print_slow(f'The enemy {foe.name} strikes with a crippling blow!\n', typingActive)
      print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
      if roll <= 65:
        p1.FOC /= 2
        focus_turns += random.randrange(2, 4)
        print_slow(f"{p1.name}'s damage dealt has been reduced for {focus_turns - 1} turns.\n", typingActive)
      p1.TDEF = playerDefault_TDEF
      foe.MP -= 1

    elif f_Skill == 18: #Assault
      soundFile = str(battle_sounds['Assault'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(f'The enemy {foe.name} launches an all out assault!\n',typingActive)
      roll = random.randrange(0, 101)
      roll2 = random.randrange(0, 101)
      roll3 = random.randrange(0, 101)
      if roll <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.FOC = p1.FOC/2
        focus_turns += 2
        print_slow(f"The first Rogue strikes {p1.name} and flings a blue powder in their face! {p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.  {p1.name}'s damage dealt has been reduced for {focus_turns - 1} turns.\n", typingActive)
      if roll > 50:
        print_slow(f'{p1.name} dodges the first attack!\n',typingActive)
      if roll2 <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        print_slow(f'The second Rogue stabs {p1.name} with a poison dagger! {p1.name} is poisoned for {pdamage} turns and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
      if roll2 > 50:
        print_slow(f'{p1.name} dodges the second attack!\n',typingActive)
      if roll3 <= 50:
        dam = random.randrange(round(foe.ATK // 2), foe.ATK)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.BLIND += 3
        print_slow(f"The third Rogue throws a TAR BOMB at {p1.name}! {p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.{p1.name} is blinded for {p1.BLIND - 1} turns.\n", typingActive) 
      if roll3 > 50:
        print_slow(f'{p1.name} dodges the final attack!\n',typingActive)
      p1.TDEF = playerDefault_TDEF
      foe.MP -= 1

    elif f_Skill == 19: # Root
      heal = foe.MaxHP // 100 * 15
      foe.HP = min(foe.HP + heal, foe.MaxHP)
      foe_defensedebuff_turns += 2
      foe.TDEF -= 30
      soundFile = str(battle_sounds['Root'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(f'{foe.name} takes root and restores {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}. {foe.name} is braced for the next attack.\n',typingActive)
      p1.TDEF = playerDefault_TDEF
      foe.MP -= 1

    elif f_Skill == 20: # Vampire Bite
      roll = random.randrange(0, 3)
      dam = random.randrange(foe.ATK // 2, foe.ATK )
      damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
      p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
      if roll == 0:
        heal = round(damage * .25)
      elif roll == 1:
        heal = round(damage * .50)
      elif roll == 2:
        heal = round(damage * .75)
      foe.HP = min(max(foe.HP + heal, 0), foe.MaxHP)
      if foe.name == 'Crescent Pond Naga' or foe.name == 'Ripper':
        pdamage = random.randrange(1, 4)
        p1.POISON += pdamage
        soundFile = str(battle_sounds['Sting'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The {foe.name} injects {p1.name} with venom and drains their blood!\n{p1.name} takes {damage} damage and is poisoned for {pdamage} turns! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} has gained {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.\n{p1.name}', typingActive) 
      else:
        soundFile = str(battle_sounds['Vampire Bite'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The {foe.name} bites {p1.name}, sucking their blood!\n{p1.name} has their blood drained and takes {damage} damage! {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n{foe.name} has gained {heal} HP! {foe.name} has {foe.HP}/{foe.MaxHP}.', typingActive) 
      p1.TDEF = playerDefault_TDEF
      foe.MP -= 1

    elif f_Skill == 21: # Spirit drain
      roll = random.randrange(0, 6)    
      if 0 <= roll <= 2:
        drain = round(p1.MaxMP * .75)
      elif 3 <= roll <= 4:
        drain = round(p1.MaxMP * .50)
      elif roll == 5:
        drain = round(p1.MaxMP * .25)
      p1.MP = min(max(p1.MP - drain, 0), p1.MaxMP)
      soundFile = str(battle_sounds['Spirit Drain'])
      play_sound_effect(soundFile, SoundsOn)
      print_slow(f"{foe.name} drains {p1.name}'s spirit! {p1.name} losses {drain} MP. {p1.name} has {p1.MP}/{p1.MaxMP} MP remaining.\n", typingActive)
      p1.TDEF = playerDefault_TDEF
      foe.MP -= 1

    elif f_Skill == 22: # Vanish
      if foe.MP >= 2:
        foe_defensedebuff_turns += 2
        foe.TDEF = 0
        soundFile = str(battle_sounds['Vanish1'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"{foe.name} becomes incorporeal! {foe.name} cannot be damaged!\n", typingActive)
        foe.MP -= 2
      else:
        foe_defensedebuff_turns += 2
        foe.TDEF = 30
        soundFile = str(battle_sounds['Vanish2'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f"{foe.name} becomes partially incorporeal! {foe.name} will take reduced damage!\n", typingActive)
        foe.MP -= 1
      p1.TDEF = playerDefault_TDEF

    elif f_Skill == 23: # Self-Destruct
      while True:
        if foe_wait >= 1:
          foe_wait -= 1 
          soundFile = str(battle_sounds['Self-Destruct CD'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f'"...S E L F...D E S T R U C T...I N... {foe_wait}..."', typingActive) 
          if foe_wait == 0:
            damage = random.randrange(round(foe.ATK * 1.5), foe.ATK * 3)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
            foe.HP = 0
            command = 'SEPPUKU'
            soundFile = str(battle_sounds['Self-Destruct'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} errupts into an explosion of shrapnel!',typingActive)
            print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining. \n', typingActive)
            player_death(p1, typingActive, SoundsOn, foe)
            enemy_death(p1, foe, command, damage, typingActive, SoundsOn)
          p1.TDEF = playerDefault_TDEF
          break
        elif foe_wait == 0:
          wait_skill = 23
          foe_wait = 3
          soundFile = str(battle_sounds['Self-Destruct CD'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow('"...S E L F...D E S T R U C T...I N I T I A T E D..."', typingActive)
          print_slow(f'"...S E L F...D E S T R U C T...I N... {foe_wait}...\n"', typingActive)
          p1.TDEF = playerDefault_TDEF
          foe.MP -= 1
          break
          
    elif f_Skill == 24:  #Whirlwind
        soundFile = str(battle_sounds['Whirlwind'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} flaps their wings and creates a massive gust of wind!\n', typingActive)
        while True:
          if foe.name == 'Roc':
            escape = random.randrange(0, 7)
            break
          else:
            escape = random.randrange(0, 4)
            break
        if escape >= 3:
            damage = max(round(foe.ATK * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP) 
            battle = 'INACTIVE'
            print_slow(f'The enemy {foe.name} blows {p1.name} away! {p1.name} takes {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. You earn nothing. Sucks to suck.\n', typingActive)
            player_death(p1, typingActive, SoundsOn, foe)
            soundFile = str(battle_sounds['Flee'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow("**********Enemy Escape!**********\n", typingActive)
            combat_end_reset(p1, foe)
        else:
            damage = max(round(foe.ATK // 2 * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
            p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP) 
            print_slow(f'The enemy {foe.name} blows {p1.name} back! {p1.name} takes {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. ', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
      
    elif f_Skill == 25:  #Peck
        print_slow(f'The enemy {foe.name} swoops in from above and begins pecking wildly!\n', typingActive)
        peck_rolls = 0
        tl_damage = 0
        while peck_rolls < 5:
          roll = random.randrange(0, 5)
          if roll >= 2:
              dam = random.randrange(foe.ATK // 2, foe.ATK // 1.5)
              damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
              tl_damage = tl_damage + damage
              peck_rolls += 1
              if peck_rolls == 1:
                soundFile = str(battle_sounds['Peck'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'{p1.name} is pecked for {damage} damage!\n', typingActive)
              else:
                soundFile = str(battle_sounds['Peck'])
                play_sound_effect(soundFile, SoundsOn)
                print_slow(f'{p1.name} is pecked again for {damage} damage!\n', typingActive)
          else:
              soundFile = str(battle_sounds['eMiss'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow(f'The {foe.name} misses their attack and flies back!\n', typingActive)
              peck_rolls = 5
        p1.HP = min(max(p1.HP - tl_damage, 0), p1.MaxHP)    
        print_slow(f'{p1.name} has taken {tl_damage} total damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP.\n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
      
    elif f_Skill == 26:  #Snatch
      while True:
        if foe_wait >= 1:
          p1.TDEF = playerDefault_TDEF
          foe_wait -= 1 
          if foe_wait == 2:
            soundFile = str(battle_sounds['Snatch Charge1'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} takes the sack slung over its shoulder and begins untying it...\n',typingActive)
          if foe_wait == 1:
            soundFile = str(battle_sounds['Snatch Charge2'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} holds out its sack and begins approaching you...\n',typingActive)
          print_slow(f'', typingActive) 
          if foe_wait == 0:
            soundFile = str(battle_sounds['Snatch'])
            play_sound_effect(soundFile, SoundsOn)
            print_slow(f'The enemy {foe.name} extends its bony arm and lifts you by the collar before stuffing you in the sack and throwing you over its shoulder... It becomes hard to breath and you pass out...\n',typingActive)
            print_slow("**********Combat Over?**********\n", typingActive)
            time.sleep(3)
            print_slow(f"You wake up and find yourself in the castle dungeon. It would appear you've been dumped in a cell and left to rot... Lucky for you theres a massive gap in the rusted out bars you can easily slip through. You escape the cell and carefully look around.\n",typingActive)
            captured = 1
            combat_end_reset(p1, foe)
          break
        elif foe_wait == 0:
          wait_skill = 26
          foe_wait = 3
          print_slow(f'The enemy {foe.name} is staring at you with its pitch black eyes...\n', typingActive)
          p1.TDEF = playerDefault_TDEF
          foe.MP -= 1
          break
        
    elif f_Skill == 27:  #Tail Whip
        dam = random.randrange(foe.ATK // 2, foe.ATK * 2)
        damage = max(round(dam * (cDEF * 0.01 * p1.TDEF * 0.01)), 0)
        p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
        soundFile = str(battle_sounds['Tail Whip'])
        play_sound_effect(soundFile, SoundsOn)
        print_slow(f'The enemy {foe.name} swings its tail with great force at {p1.name}!\n', typingActive)
        print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP. \n', typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
    
    elif f_Skill == 28:  #Demon's Gaze
        roll = random.randrange(0, 4)
        if roll >= 1:
          p1.BLIND += 4
          soundFile = str(battle_sounds["Demon's Gaze"])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"The enemy {foe.name} locks eyes with {p1.name}, filling them with terror! {p1.name} is blinded for {p1.BLIND - 1} turns.\n", typingActive)
        elif roll < 1:
          soundFile = str(battle_sounds['eMiss'])
          play_sound_effect(soundFile, SoundsOn)
          print_slow(f"{p1.name} manages to avoid the gaze!\n", typingActive)
        p1.TDEF = playerDefault_TDEF
        foe.MP -= 1
    
    elif f_Skill == 29:  #Stone Gaze
        if haste >= 0: 
          roll = random.randrange(0, 7)
          if roll >= 2:
            soundFile = str(battle_sounds['Stone Gaze'])
            play_sound_effect(soundFile, SoundsOn)
            if foe.name == 'Vampire Lord' or foe.name == 'Lamia':
              haste -= 3
              print_slow(f"The enemy {foe.name} locks eyes with {p1.name}, Hypnotizing them! {p1.name} is mezmerized!\n", typingActive)
            if foe.name == 'Spider-Lady':
              haste -= random.randrange(1,4)
              print_slow(f"The enemy {foe.name} shoots a sticky web at {p1.name}, ensnaring them! {p1.name} is ensnared!\n", typingActive)
            else:
              haste -= random.randrange(2,4)
              print_slow(f"The enemy {foe.name} locks eyes with {p1.name}, turning them to stone! {p1.name} is petrified!\n", typingActive)
          else:
            print_slow(f"{p1.name} manages to avoid the {foe.name}'s gaze!\n", typingActive)
          p1.TDEF = playerDefault_TDEF
          foe.MP -= 1
        else:
          soundFile = str(battle_sounds['eMiss'])
          play_sound_effect(soundFile, SoundsOn)
          if foe.name == 'Vampire Lord' or foe.name == 'Lamia':
            print_slow(f"The enemy {foe.name} tries hypnotizing {p1.name}! It fails, as {p1.name} is already mezmerized!\n", typingActive)
          elif foe.name == 'Spider-Lady':
            print_slow(f"The enemy {foe.name} tries ensnaring {p1.name} in webs! It fails, as {p1.name} is already ensnared!\n", typingActive)  
          else:
            print_slow(f"The enemy {foe.name} tries turning {p1.name} to stone! It fails, as {p1.name} is  already petrified!\n", typingActive)

    elif f_Skill == 30:  #Nova
        while True:
          if foe_wait >= 1:
            foe_wait -= 1 
            print_slow(f'{foe.name} continues to gather energy...', typingActive) 
            if foe_wait == 0:
              damage = round((p1.HP // 4) * 3)
              p1.HP = min(max(p1.HP - damage, 0), p1.MaxHP)
              soundFile = str(battle_sounds['Nova'])
              play_sound_effect(soundFile, SoundsOn)
              print_slow(f'{foe.name} unleashes a devastating attack! A power wave of dark energy crashes into {p1.name}!',typingActive)
              print_slow(f'{p1.name} has taken {damage} damage. {p1.name} has {p1.HP}/{p1.MaxHP} HP remaining. \n', typingActive)
            p1.TDEF = playerDefault_TDEF
            break
          elif foe_wait == 0:
            wait_skill = 30
            foe_wait = 2
            print_slow(f'The {foe.name} begins gathering energy for a massive attack!\n', typingActive)
            p1.TDEF = playerDefault_TDEF
            foe.MP -= 1
            break


#Help menu for combat
def combat_menu(p1, typingActive):
  if p1.job == "WARRIOR":
      warrior_menu = "+++++[Battle commands]+++++\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n[Skills]\nHARDEN: Restore some HP, temp. increase def for 1 turn."
      if p1.lvl >= 2:
        warrior_menu += 'STRIKE: Wildy strike foe for high damage. Chance to miss.'
      if p1.lvl >= 5:
        warrior_menu += 'BERSERK: Become blinded by range for several turns. Can only attack while berserk, but damage is increased.'
      if p1.lvl >= 10:
        warrior_menu += 'BLOOD: Become filled with a lust for blood. Absorb 50% of damage dealt as HP.'
      if p1.mainHand == 'AETON':
        warrior_menu =+ 'BATTLECRY: Spend 2 MP to unleash a mighty BATTLECRY to temporarily reduce enemy attack.'
      print_slow(warrior_menu + "\n", typingActive)
  
  elif p1.job == "WIZARD" or p1.job == "WITCH":
      wizard_menu = "+++++[Battle commands]+++++\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n[Skills]\nFOCUS: Concentrates to increase damage of follow up attacks for several turns."
      if p1.lvl >= 2:
        wizard_menu += "\nBOLT: Cast magical bolt dealing high damage."
      if p1.lvl >= 5:
        wizard_menu += "\nSTORM: Cast magical storm, rollting the enemy multiple times. Chance to miss."
      if p1.lvl >= 10:
        wizard_menu += "\nBLAST: Send a concentrated magical blast at the enemy. Damaged based on enemy HP; high chance to miss."
      if p1.mainHand == 'FULGUR':
        wizard_menu =+ 'SHOCK: Spend 3 MP to conjure a massive ball of lightning to shock the enemy for high damamge. Chance to paralyze enemy. Low chance to backfire.'
      print_slow(wizard_menu + "\n", typingActive)

  elif p1.job == "THIEF":
      thief_menu = "+++++[Battle commands]+++++\nATK: Regular attack.\nDEF: Temp. increase DEF for 1 turn.\nITEM: Open items menu.\nFLEE: Use a SMOKE BOMB to escape combat. Does not work in Boss fights.\n[Skills]\nSTEAL: Steal GP from enemy. Chance to fail."
      if p1.lvl >= 2:
        thief_menu =+ 'THROW: Throw up to 3 poison daggers at the enemy. Deals damage and poisons.'
      if p1.lvl >= 5:
        thief_menu =+ 'MUG: Attack enemy and steal item from enemy. Chance stealing may fail.'
      if p1.lvl >= 10:
        thief_menu =+ 'HASTE: Spend 2 MP to use 2 actions in the same turn. Does not stack.'
      if p1.mainHand == 'MIDAS':
        thief_menu =+ '$TOSS: Throw GP at the enemy for direct damage.'
      print_slow(thief_menu + "\n", typingActive)


#Command terms
attack_Terms = ["A", "ATK","ATTACK","HIT",] # attack responses
defense_Terms = ['D','DEF', 'DEFEND'] # defense responses
item_Terms = ['I','ITEM', 'ITEMS'] # item responses
flee_Terms = ['F', 'FLEE', 'RUN', 'ESCAPE'] # flee responses
stat_Terms = ['S', 'STATS', 'STAT', 'STATUS'] # stat responses
help_Terms = ['H', 'HELP', 'COMMANDS'] # help responses
aff_Terms = ["YES","Y"] # affirmative responses
neg_Terms = ["NO","N"] # negative responses
back_Terms = ["BACK","B","LEAVE"] # back responses

potion_Terms = ['POTION', 'POT', 'P', 'HEALING POTION','HEAL POTION','HEAL'] # healing potion terms
ether_Terms = ['ETHER','ETR','E',] # ether terms
antidote_Terms = ['ANTIDOTE','ANTI', 'ANT','A',] # antidote terms
saline_Terms = ['SALINE','SALI', 'SAL', 'S', 'EYE DROP', 'EYE DROPS'] # saline terms
smoke_Terms = ['SMOKE BOMB','SMOKE','BOMB', 'SMB'] # smoke bomb terms

#Skill dictionary
combat_skills = {
  'HARDEN' : {'MP' : 1, 's_Funk': warrior_harden,}, 
  'STRIKE': {'MP' : 3, 's_Funk': warrior_wildstrikes,},
  'BERSERK': {'MP' : 4, 's_Funk': warrior_berserk,}, 
  'BLOOD': {'MP' : 6, 's_Funk': warrior_bloodlust,}, 
  'BATTLECRY': {'MP' : 5, 's_Funk': warrior_battlecry,}, 
  'FOCUS': {'MP' : 1, 's_Funk': wizard_focus,}, 
  'BOLT': {'MP' : 5, 's_Funk': wizard_bolt,}, 
  'STORM': {'MP' : 7, 's_Funk': wizard_storm,}, 
  'BLAST': {'MP' : 9, 's_Funk': wizard_blast,}, 
  'SHOCK': {'MP' : 15, 's_Funk': wizard_shock,}, 
  'STEAL': {'MP' : 1, 's_Funk': thief_steal,}, 
  'THROW': {'MP' : 2, 's_Funk': thief_poisondagger,}, 
  'MUG': {'MP' : 4, 's_Funk': thief_mug,}, 
  'HASTE': {'MP' : 8, 's_Funk': thief_haste,}, 
  '$TOSS': {'MP' : 3, 's_Funk': thief_cointhrow,}, 
  'EMBER': {'MP' : 3, 's_Funk': summoner_ember,}, 
  'AQUA': {'MP' : 6, 's_Funk': summoner_aqua,}, 
  'TERRA': {'MP' : 11, 's_Funk': summoner_terra,}, 
  'AERO': {'MP' : 15, 's_Funk': summoner_aero,}, 
  'AETHER': {'MP' : 18, 's_Funk': summoner_aether,}, }
      

class summon:
    def __init__(self, name, skill, MaxHP, HP, ATK, DEF, MACC, ACC, DFOC, FOC, MaxPOTS, POTS, turns, turnsLeft):
        self.name = name
        self.skill = skill
        self.MaxHP = MaxHP
        self.HP = HP
        self.ATK = ATK
        self.DEF = DEF
        self.MACC = MACC
        self.ACC = ACC
        self.FOC = FOC
        self.MaxPOTS = MaxPOTS
        self.POTS = POTS
        self.turns = turns
        self.turnsLeft = turnsLeft

s1 = summon("Kitsune", # name
            [1,2], # skills
            300, # MaxHP
            300, # HP
            10, # ATK
            50, # DEF
            95, # MACC
            95, # ACC
            1, # DFOC
            1, # FOC
            0, # MaxPOTS
            0, # POTS
            3, # turns
            3) # turnsLeft
s2 = summon("Djinn", # name
            [3,4], # skills
            300, # MaxHP
            300, # HP
            28, # ATK
            55, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            4, # turns
            4) # turnsLeft
s3 = summon("Gargoyle", # name
            [5,6], # skills
            350, # MaxHP
            350, # HP
            18, # ATK
            60, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            4, # turns
            4) # turnsLeft
s4 = summon("Yukihime", # name
            [7,8], # skills
            280, # MaxHP
            280, # HP
            26, # ATK
            40, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            5, # turns
            5) # turnsLeft
s5 = summon("Cyclopes", # name
            [9,10], # skills
            320, # MaxHP
            320, # HP
            24, # ATK
            45, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            5, # turns
            5) # turnsLeft
s6 = summon("Alicanto", # name
            [11,12], # skills
            320, # MaxHP
            320, # HP
            35, # ATK
            50, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            5, # turns
            5) # turnsLeft
s7 = summon("Lindwyrm", # name
            [13,14], # skills
            300, # MaxHP  
            300, # HP
            30, # ATK
            45, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            6, # turns
            6) # turnsLeft
s8 = summon("Harbok", # name
            [15,16], # skills
            300, # MaxHP
            300, # HP
            42, # ATK
            50, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            6, # turns
            6) # turnsLeft
s9 = summon("Eos", # name
            [17,18], # skills
            350, # MaxHP
            350, # HP
            37, # ATK
            60, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS 
            5, # turns
            5) # turnsLeft
s10 = summon("Nyx", # name
            [19,20], # skills
            320, # MaxHP
            320, # HP
            55, # ATK
            50, # DEF
            90, # MACC
            90, # ACC
            1, # DFOC
            1, # FOC
            2, # MaxPOTS
            2, # POTS
            5, # turns
            5) # turnsLeft


def player_weapon_sound(p1):

  weapon_groups =  {
  'Sword': ['MESSER', 'ARMING SWORD', 'BROAD SWORD', 'HANGER', 'ADAMANTITE SWORD'],
  'Light Sword': ['SIDE SWORD', 'RAPIER', 'SILVER BLADE', 'DELPHI'],
  'Katana':['KATANA'],
  'Dagger': ['RUSTY DAGGER', 'OBSIDIAN DAGGER', 'SERPENT KNIFE'],
  'Axe': ['GOBLIN CHOPPER'],
  'Mace':['MACE',],
  'Spiked': ['MORNING STAR', 'WAR PICK', 'FLAIL'],
  'Fist': ['EMPTY', None],

  'Aethon': ['AETHON'],
  'Fulgur': ['FULGUR', "SMELDARS BANE"],
  'Midas': ['MIDAS'],
  }


  if p1.mainHand in weapon_groups['Sword']:
      soundFile = battle_sounds['Sword']
      return soundFile
  elif p1.mainHand in weapon_groups['Light Sword']:
      soundFile = battle_sounds['Light Sword']
      return soundFile
  elif p1.mainHand in weapon_groups['Katana']:
      soundFile = battle_sounds['Katana']
      return soundFile
  elif p1.mainHand in weapon_groups['Dagger']:
      soundFile = battle_sounds['Dagger']
      return soundFile
  elif p1.mainHand in weapon_groups['Axe']:
      soundFile = battle_sounds['Axe']
      return soundFile
  elif p1.mainHand in weapon_groups['Mace']:
      soundFile = battle_sounds['Mace']
      return soundFile
  elif p1.mainHand in weapon_groups['Spiked']:
      soundFile = battle_sounds['Spiked']
      return soundFile
  elif p1.mainHand in weapon_groups['Fist']:
      soundFile = battle_sounds['Fist']
      return soundFile
  

  elif p1.mainHand in weapon_groups['Fist']:
      soundFile = battle_sounds['Fist']
      return soundFile
  elif p1.mainHand in weapon_groups['Aethon']:
      soundFile = battle_sounds['Aethon']
      return soundFile
  elif p1.mainHand in weapon_groups['Fulgur']:
      soundFile = battle_sounds['Fulgur']
      return soundFile
  elif p1.mainHand in weapon_groups['Midas']:
      soundFile = battle_sounds['Midas']
      return soundFile
  
def enemy_weapon_sound(foe):

# 1.Cut 2.Slash 3.Claw 4.Stab 5.Smash 6.Crunch 7.Bite 8.Magic 9.Ooze 10.Mist 11.Bite2 12.Magic2
  if foe.ASFX == 1:
      soundFile = battle_sounds['Cut']
      return soundFile
  elif foe.ASFX == 2:
      soundFile = battle_sounds['Slash']
      return soundFile
  elif foe.ASFX == 3:
      soundFile = battle_sounds['Claw']
      return soundFile
  elif foe.ASFX == 4:
      soundFile = battle_sounds['Stab']
      return soundFile
  elif foe.ASFX == 5:
      soundFile = battle_sounds['Smash']
      return soundFile
  elif foe.ASFX == 6:
      soundFile = battle_sounds['Crunch']
      return soundFile
  elif foe.ASFX == 7:
      soundFile = battle_sounds['Bite']
      return soundFile
  elif foe.ASFX == 8:
      soundFile = battle_sounds['Magic']
      return soundFile
  elif foe.ASFX == 9:
      soundFile = battle_sounds['Ooze']
      return soundFile
  elif foe.ASFX == 10:  
      soundFile = battle_sounds['Mist']
      return soundFile
  elif foe.ASFX == 11:  
      soundFile = battle_sounds['Bite2']
      return soundFile
  elif foe.ASFX == 12:  
      soundFile = battle_sounds['Magic2']
      return soundFile  
  


battle_sounds = {
  "Sword": Path(sys.argv[0]).parent / 'sounds' / "Sword_Slash.wav",
  "Light Sword": Path(sys.argv[0]).parent / 'sounds' / "Light_Sword_Slash.wav",
  "Katana": Path(sys.argv[0]).parent / 'sounds' / "Katana_Slash.wav",
  "Dagger": Path(sys.argv[0]).parent / 'sounds' / "Dagger_Slash.wav",
  "Axe": Path(sys.argv[0]).parent / 'sounds' / "Axe_Chop.wav",
  "Mace": Path(sys.argv[0]).parent / 'sounds' / "Mace.wav",
  "Spiked": Path(sys.argv[0]).parent / 'sounds' / "Spiked_Smash.wav",
  "Fist": Path(sys.argv[0]).parent / 'sounds' / "Fist_Punch.wav",

  "Aethon": Path(sys.argv[0]).parent / 'sounds' / "Aethon_Slash.wav",
  "Fulgur": Path(sys.argv[0]).parent / 'sounds' / "Fulgur_Slash.wav",
  "Midas": Path(sys.argv[0]).parent / 'sounds' / "Midas_Slash.wav",
  
  #Player action sounds
  "pMiss": Path(sys.argv[0]).parent / 'sounds' / "Miss.wav",
  "pDefend": Path(sys.argv[0]).parent / 'sounds' / "Player_Defend.wav",
  "smoke": Path(sys.argv[0]).parent / 'sounds' / "Flee.wav",

  #Item sounds
  "potion": Path(sys.argv[0]).parent / 'sounds' / "Potion.wav",
  "ether": Path(sys.argv[0]).parent / 'sounds' / "Ether.wav",
  "antidote": Path(sys.argv[0]).parent / 'sounds' / "Antidote.wav",
  "saline": Path(sys.argv[0]).parent / 'sounds' / "Saline.wav",

  #Player skill sounds
  #warrior skills
  "Harden": Path(sys.argv[0]).parent / 'sounds' / "Harden.wav",
  # "Strike": Path(sys.argv[0]).parent / 'sounds' / "Strike.wav",  # placeholder if needed
  # "Berserk": Path(sys.argv[0]).parent / 'sounds' / "Berserk.wav", # placeholder if needed
  "Blood": Path(sys.argv[0]).parent / 'sounds' / "Blood.wav",
  "Battlecry": Path(sys.argv[0]).parent / 'sounds' / "Battlecry.wav",

  #wizard skills
  "Focus": Path(sys.argv[0]).parent / 'sounds' / "Focus.wav",
  "Bolt": Path(sys.argv[0]).parent / 'sounds' / "Bolt.wav",
  "Storm": Path(sys.argv[0]).parent / 'sounds' / "Storm.wav",
  "Blast": Path(sys.argv[0]).parent / 'sounds' / "Blast.wav",
  "Fizzle": Path(sys.argv[0]).parent / 'sounds' / "Fizzle.wav",
  "Shock": Path(sys.argv[0]).parent / 'sounds' / "Shock.wav",

  #thief skills
  "Steal": Path(sys.argv[0]).parent / 'sounds' / "Steal.wav",
  "Throw": Path(sys.argv[0]).parent / 'sounds' / "Throw.wav",
  "Haste": Path(sys.argv[0]).parent / 'sounds' / "Haste.wav",
  "$Throw": Path(sys.argv[0]).parent / 'sounds' / "CoinThrow.wav",

  #summoner skills
  "Summon": Path(sys.argv[0]).parent / 'sounds' / "Summon.wav",

  "Fox Fire": Path(sys.argv[0]).parent / 'sounds' / "FoxFire.wav",
  "Healing Warmth": Path(sys.argv[0]).parent / 'sounds' / "HealingWarmth.wav",
  "Blaze": Path(sys.argv[0]).parent / 'sounds' / "Blaze.wav",
  "Restoration": Path(sys.argv[0]).parent / 'sounds' / "Restoration.wav",
  "Water Spout": Path(sys.argv[0]).parent / 'sounds' / "WaterSpout.wav",
  "Toxic Fangs": Path(sys.argv[0]).parent / 'sounds' / "ToxicBite.wav",
  "Fridged Kiss": Path(sys.argv[0]).parent / 'sounds' / "FridgedKiss.wav",
  "Frostbite Snap": Path(sys.argv[0]).parent / 'sounds' / "FrostbiteSnap.wav",
  "Rock Slide": Path(sys.argv[0]).parent / 'sounds' / "RockSlide.wav",
  "Barrier Wall": Path(sys.argv[0]).parent / 'sounds' / "BarrierWall.wav",
  "Meteorain": Path(sys.argv[0]).parent / 'sounds' / "Meteorain.wav",
  "Barrier Shell": Path(sys.argv[0]).parent / 'sounds' / "BarrierShell.wav",
  "Razor Gale": Path(sys.argv[0]).parent / 'sounds' / "RazorGale.wav",
  "Windscar": Path(sys.argv[0]).parent / 'sounds' / "Windscar.wav",
  "Updraft": Path(sys.argv[0]).parent / 'sounds' / "Updraft.wav",
  "Hurricane": Path(sys.argv[0]).parent / 'sounds' / "Hurricane.wav",
  "Holy Light": Path(sys.argv[0]).parent / 'sounds' / "HolyLight.wav",
  "Regain": Path(sys.argv[0]).parent / 'sounds' / "Regain.wav",
  "Astral Storm": Path(sys.argv[0]).parent / 'sounds' / "AstralStorm.wav",
  "Void Pulse": Path(sys.argv[0]).parent / 'sounds' / "VoidPulse.wav",

  #Enemy skill sounds
  "Flee": Path(sys.argv[0]).parent / 'sounds' / "eFlee.wav",
  "Flee_fail": Path(sys.argv[0]).parent / 'sounds' / "eFleeFail.wav",
  "Cleave": Path(sys.argv[0]).parent / 'sounds' / "Cleave.wav",
  "Maul": Path(sys.argv[0]).parent / 'sounds' / "Maul.wav",
  "Magic Bolt": Path(sys.argv[0]).parent / 'sounds' / "MagicBolt.wav",
  "eSteal": Path(sys.argv[0]).parent / 'sounds' / "eSteal.wav",
  "eSteal_fail": Path(sys.argv[0]).parent / 'sounds' / "eStealFail.wav",
  "Fire Breath": Path(sys.argv[0]).parent / 'sounds' / "FireBreath.wav",
  "Fire Breath Charge": Path(sys.argv[0]).parent / 'sounds' / "FireBreathC.wav",
  "Sting": Path(sys.argv[0]).parent / 'sounds' / "Sting.wav",
  "Poison Mist": Path(sys.argv[0]).parent / 'sounds' / "PoisonMist.wav",
  "Quake": Path(sys.argv[0]).parent / 'sounds' / "Quake.wav",
  "Summon Swarm": Path(sys.argv[0]).parent / 'sounds' / "SummonSwarm.wav",
  "Roar1": Path(sys.argv[0]).parent / 'sounds' / "Roar1.wav",
  "Roar2": Path(sys.argv[0]).parent / 'sounds' / "Roar2.wav",
  "Roar3": Path(sys.argv[0]).parent / 'sounds' / "Roar3.wav",
  "Roar4": Path(sys.argv[0]).parent / 'sounds' / "Roar4.wav",
  "Kancho": Path(sys.argv[0]).parent / 'sounds' / "Kancho.wav",
  "Poison Bite": Path(sys.argv[0]).parent / 'sounds' / "ToxicBite.wav",
  "Dales Pocket-sand": Path(sys.argv[0]).parent / 'sounds' / "PocketSand.wav",
  "Skewer": Path(sys.argv[0]).parent / 'sounds' / "Skewer.wav",
  "Gunk Shot": Path(sys.argv[0]).parent / 'sounds' / "GunkShot.wav",
  "Cripple": Path(sys.argv[0]).parent / 'sounds' / "Cripple.wav",
  "Assault": Path(sys.argv[0]).parent / 'sounds' / "Assault.wav",
  "Root": Path(sys.argv[0]).parent / 'sounds' / "Root.wav",
  "Vampire Bite": Path(sys.argv[0]).parent / 'sounds' / "VBite.wav",
  "Spirit Drain": Path(sys.argv[0]).parent / 'sounds' / "SpiritDrain.wav",
  "Vanish1": Path(sys.argv[0]).parent / 'sounds' / "Vanish1.wav",
  "Vanish2": Path(sys.argv[0]).parent / 'sounds' / "Vanish2.wav",
  "Self-Destruct": Path(sys.argv[0]).parent / 'sounds' / "SelfDestruct.wav",
  "Self-Destruct CD": Path(sys.argv[0]).parent / 'sounds' / "SelfDestructCD.wav",
  "Whirlwind": Path(sys.argv[0]).parent / 'sounds' / "Whirlwind.wav",
  "Peck": Path(sys.argv[0]).parent / 'sounds' / "Peck.wav",
  "Snatch": Path(sys.argv[0]).parent / 'sounds' / "Snatch.wav",
  "Snatch Charge1": Path(sys.argv[0]).parent / 'sounds' / "SnatchCharge1.wav",
  "Snatch Charge2": Path(sys.argv[0]).parent / 'sounds' / "SnatchCharge2.wav",
  "Tail Whip": Path(sys.argv[0]).parent / 'sounds' / "TailWhip.wav",
  "Demon's Gaze": Path(sys.argv[0]).parent / 'sounds' / "DemonsGaze.wav",
  "Stone Gaze": Path(sys.argv[0]).parent / 'sounds' / "StoneGaze.wav",
  "Nova": Path(sys.argv[0]).parent / 'sounds' / "Nova.wav",
  "Acid Spit": Path(sys.argv[0]).parent / 'sounds' / "AcidSpit.wav",

  "Cut": Path(sys.argv[0]).parent / 'sounds' / "Cut.wav",
  "Slash": Path(sys.argv[0]).parent / 'sounds' / "Chop.wav",
  "Claw": Path(sys.argv[0]).parent / 'sounds' / "Claw.wav",
  "Stab": Path(sys.argv[0]).parent / 'sounds' / "Stab.wav",
  "Smash": Path(sys.argv[0]).parent / 'sounds' / "Smash.wav",
  "Crunch": Path(sys.argv[0]).parent / 'sounds' / "Crunch.wav",
  "Bite": Path(sys.argv[0]).parent / 'sounds' / "Bite.wav",
  "Magic": Path(sys.argv[0]).parent / 'sounds' / "Magic.wav",
  "Ooze": Path(sys.argv[0]).parent / 'sounds' / "Ooze.wav",
  "Mist": Path(sys.argv[0]).parent / 'sounds' / "Mist.wav",
  "Bite2": Path(sys.argv[0]).parent / 'sounds' / "Bite(low).wav",
  "Magic2": Path(sys.argv[0]).parent / 'sounds' / "Magic2.wav",

  "eMiss": Path(sys.argv[0]).parent / 'sounds' / "eMiss.wav",
  "eDefend": Path(sys.argv[0]).parent / 'sounds' / "eDefend.wav",
  "eHeal": Path(sys.argv[0]).parent / 'sounds' / "eHeal.wav",

  "Encounter": Path(sys.argv[0]).parent / 'sounds' / "Encounter.wav",
  "Victory": Path(sys.argv[0]).parent / 'sounds' / "Victory.wav",
  "Defeat": Path(sys.argv[0]).parent / 'sounds' / "Defeat.wav",
  "Error": Path(sys.argv[0]).parent / 'sounds' / "Error.wav",
}
