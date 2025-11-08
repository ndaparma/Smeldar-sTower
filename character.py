import random
from Settings import *

class player:
#instance player
    def __init__(self, name, job, skills, inventory, materials, lvl, Nlvl, xp, MaxHP, HP, MaxMP, MP, ATK, DEF, GDEF, TDEF, ACC, FOC, SPD, GP, MaxPOTS, POTS, MaxANT, ANT, MaxETR, ETR, MaxSAL, SAL, MaxSMB, SMB, MaxWCR, WCR, MaxKDL, KDL, RJ, GR, mainHand, offHand, head, body, legs, accs1, accs2, GrLvl, gobCount, faeCount, PlantP, MonP, RareP, FaeP, DragonP, POISON, BLIND, roomMoves, enemiesKilled, keys, win, FT):
        self.name = name #player name
        self.job = job #player class
        self.skills = skills #list of skills
        self.inventory = inventory #items
        self.materials = materials #crafting materials
        self.lvl = lvl #Current Level
        self.Nlvl = Nlvl #Next Level EXP
        self.xp = xp #Current EXP
        self.MaxHP = MaxHP #Current Max HP
        self.HP = HP #Current HP
        self.MaxMP = MaxMP #Current Max MP
        self.MP = MP #Current MP
        self.ATK = ATK #Base Attack
        self.DEF = DEF #Base Defense
        self.GDEF = GDEF #Gear Defense
        self.TDEF = TDEF #Temporary Defense
        self.ACC = ACC #Accuracy
        self.FOC = FOC #Focus
        self.SPD = SPD #Speed
        self.GP = GP #Gold Pieces
        self.MaxPOTS = MaxPOTS #Max Potions
        self.POTS = POTS #Potions
        self.MaxANT = MaxANT #Max Antidotes
        self.ANT = ANT  # Antidotes
        self.MaxETR = MaxETR #Max Ethers
        self.ETR = ETR #Ethers
        self.MaxSAL = MaxSAL #Max Saline
        self.SAL = SAL  # Saline
        self.MaxSMB = MaxSMB #Max Smoke Bombs
        self.SMB = SMB  # Smoke Bombs
        self.MaxWCR = MaxWCR #Max Warp Crystals
        self.WCR = WCR  # Warp Crystals
        self.MaxKDL = MaxKDL #Max Kindling
        self.KDL = KDL  # Kindling
        self.RJ = RJ # Royal Jelly (healing bonus)
        self.GR = GR # Gold Ring (GP bonus)
        self.mainHand = mainHand #main weapon
        self.offHand = offHand #off-hand weapon
        self.head = head #head armor
        self.body = body #body armor
        self.legs = legs #leg armor
        self.accs1 = accs1 #accessory 1
        self.accs2 = accs2 #accessory 2
        self.GrLvl = GrLvl #current weapon level
        self.gobCount = gobCount #number of goblins killed
        self.faeCount = faeCount #number of faeries killed
        self.PlantP = PlantP  #crafting materials
        self.MonP = MonP #crafting materials
        self.RareP = RareP #crafting materials
        self.FaeP = FaeP #crafting materials
        self.DragonP = DragonP #crafting materials
        self.POISON = POISON #status effects
        self.BLIND = BLIND #status effects
        self.roomMoves = roomMoves #number of moves made by the player
        self.enemiesKilled = enemiesKilled #number of enemies killed
        self.keys = keys #number of keys collected/Defunct
        self.win = win #Game complete status
        self.FT = FT #Fast travel points unlocked

#check player stats
    def stat_check(self, typingActive):
        cDEF = max(self.DEF - self.GDEF, 25)
        print_slow(f'\nCurrent Stats:\n{self.name}\n{self.job}\nLvl {self.lvl}\n{self.xp}/{self.Nlvl} EXP\n{self.HP}/{self.MaxHP} HP\n{self.MP}/{self.MaxMP} MP\n{self.ATK} ATK\n{(100 - cDEF)}% DEF\n{self.SPD} SPD', typingActive)
    def stat_sCheck(self, typingActive): #Abbreviated stat check
        cDEF = max(self.DEF - self.GDEF, 25)
        print_slow(f'\nCurrent Stats:\n{self.name}\n{self.job}\nLvl {self.lvl}\n{self.xp}/{self.Nlvl}EXP\n{self.HP}/{self.MaxHP} HP\n{self.MP}/{self.MaxMP} MP\n{self.ATK} ATK\n{(100 - cDEF)}% DEF\n{self.SPD} SPD', typingActive)
      
#define level gains
    def level_up(self, typingActive, SoundsOn):
      if self.lvl == 99:
        print_slow(f'{self.name} has reached the max level.', typingActive)
      elif self.lvl < 99:
        while self.xp < self.Nlvl:
            print_slow(f'{self.name} has {self.xp}/{self.Nlvl} EXP.', typingActive)
            break
        while self.xp >= self.Nlvl:
            self.lvl += 1
            self.xp -= self.Nlvl
            if self.lvl < 99:
              self.Nlvl = round(self.Nlvl * 1.25)
            elif self.lvl == 99:
              self.Nlvl = 'MAX'
            soundFile = r"C:\Users\ndapa\Desktop\smeldarstowerCopy2\sounds\LevelUp.wav"
            play_sound_effect(soundFile, SoundsOn)
            print_slow("*****LEVEL UP!*****", typingActive)
            print_slow(f'{self.name} Leveled up! {self.name} is now {self.lvl}', typingActive)

            if (self.lvl % 3) != 0:
              if self.job == "WARRIOR": 
                self.MaxHP += 60
                self.ATK += 1
                self.DEF = max(self.DEF - 1, 25)
                self.SPD += 1
                self.HP = self.MaxHP
                self.MP = self.MaxMP
              elif self.job in ['WIZARD', 'WITCH']:
                self.MaxHP += 35
                self.MaxMP += 1
                self.ATK += 2
                self.SPD += 1
                self.HP = self.MaxHP
                self.MP = self.MaxMP
              elif self.job == 'THIEF':
                self.MaxHP += 45
                self.ATK += 1
                self.SPD += 2
                self.HP = self.MaxHP
                self.MP = self.MaxMP
              elif self.job == 'SUMMONER':
                self.MaxHP += 25
                self.MaxMP += 1
                self.SPD += 1
                self.HP = self.MaxHP
                self.MP = self.MaxMP

            if (self.lvl % 3) == 0:
              if self.job == "WARRIOR": 
                self.MaxHP += 80
                self.MaxMP += 2
                self.DEF = max(self.DEF - 1, 25)
                self.ATK += 2
                self.SPD += 1
                self.HP = self.MaxHP 
                self.MP = self.MaxMP
              elif self.job in ['WIZARD', 'WITCH']:
                self.MaxHP += 50
                self.MaxMP += 3
                self.ATK += 3
                self.SPD += 2
                self.DEF = max(self.DEF - 1, 25)
                self.HP = self.MaxHP
                self.MP = self.MaxMP
              elif self.job == 'THIEF':
                self.MaxHP += 65
                self.MaxMP += 3
                self.ATK += 2
                self.SPD += 3
                self.DEF = max(self.DEF - 1.5, 25)
                self.HP = self.MaxHP
                self.MP = self.MaxMP
              elif self.job == 'SUMMONER':
                self.MaxHP += 45
                self.MaxMP += 2
                self.ATK += 3
                self.DEF = max(self.DEF - 1, 25)
                self.HP = self.MaxHP
                self.MP = self.MaxMP
                
            if self.lvl == 5:
              if self.job == 'WARRIOR':
                self.skills.append('STRIKE')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned STRIKE.', typingActive)
              elif self.job in ['WIZARD', 'WITCH']:
                self.skills.append('BOLT')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned BOLT.', typingActive)
              elif self.job == 'THIEF':
                self.skills.append('THROW')     
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned THROW.', typingActive) 
              elif self.job == 'SUMMONER':
                self.skills.append('AQUA')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned AQUA.', typingActive)

            if self.lvl == 12:
              if self.job == 'WARRIOR':
                self.skills.append('BERSERK')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned BERSERK.', typingActive)
              elif self.job in ['WIZARD', 'WITCH']:
                self.skills.append('STORM')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned STORM.', typingActive)
              elif self.job == 'THIEF':
                self.skills.append('MUG') 
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned MUG.', typingActive)
              elif self.job == 'SUMMONER':
                self.skills.append('TERRA')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned TERRA.', typingActive)

            if self.lvl == 22:
              if self.job == 'WARRIOR':
                self.skills.append('BLOOD')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned BLOOD.', typingActive)
              elif self.job in ['WIZARD', 'WITCH']:
                self.skills.append('BLAST')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned BLAST.', typingActive)
              elif self.job == 'THIEF':
                self.skills.append('HASTE')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned HASTE.', typingActive)
              elif self.job == 'SUMMONER':
                self.skills.append('AERO')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned AERO.', typingActive)

            if self.lvl == 34:
              if self.job == 'WARRIOR':
                self.skills.append('BATTLECRY')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned BATTLECRY.', typingActive)
              elif self.job in ['WIZARD', 'WITCH']:
                self.skills.append('SHOCK')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned SHOCK.', typingActive)
              elif self.job == 'THIEF':
                self.skills.append('$TOSS')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned $TOSS.', typingActive)
              elif self.job == 'SUMMONER':
                self.skills.append('AETHER')
                print_slow(f'{self.name} has learned a new skill! {self.name} has learned AETHER.', typingActive)

            self.stat_check(typingActive)
            break


    def materials_list(self):
      if self.PlantP > 0 and 'PLANT PARTS' not in self.materials:
        self.materials.append('PLANT PARTS')
      if self.MonP > 0 and 'MONSTER PARTS' not in self.materials:
        self.materials.append('MONSTER PARTS')
      if self.RareP > 0 and 'RARE MONSTER PARTS' not in self.materials:
        self.materials.append('RARE MONSTER PARTS')
      if self.FaeP > 0 and 'FAE DUST' not in self.materials:
        self.materials.append('FAE DUST')
      if self.DragonP > 0 and 'DRAGON SCALES' not in self.materials:
        self.materials.append('DRAGON SCALES')

    
        
    def material_print(self, typingActive):
      if "PLANT PARTS" in self.materials:
        print_slow(f'\nPLANT PARTS: {self.PlantP}', typingActive)
      if "MONSTER PARTS" in self.materials:
        print_slow(f'\nMONSTER PARTS: {self.MonP}', typingActive)
      if "RARE MONSTER PARTS" in self.materials:
        print_slow(f'\nRARE MONSTER PARTS: {self.RareP}', typingActive)
      if "FAE DUST" in self.materials:
        print_slow(f'\nFAE DUST: {self.FaeP}', typingActive)
      if "DRAGON SCALES" in self.materials:
        print_slow(f'\nDRAGON SCALES: {self.DragonP}', typingActive)

    def equip_stat_update(self, playerInput, previous_gear, key_items):
      if previous_gear != None and previous_gear != 'EMPTY':
        self.ATK += key_items[previous_gear]['ATK'] * -1
        self.GDEF += (key_items[previous_gear]['DEF'] * -1)
        self.MaxHP += key_items[previous_gear]['HP'] * -1
        self.MaxMP += key_items[previous_gear]['MP'] * -1
        try:
          self.SPD += key_items[previous_gear]['SPD'] * -1
        except KeyError:
          pass
        try:
          self.FOC -= key_items[previous_gear]['FOC']
        except KeyError:
          pass

        if previous_gear == 'AETHON':
          if self.lvl < 34:
            self.skills.remove('BATTLECRY')
        if previous_gear == 'FULGUR':
          if self.lvl < 34:
            self.skills.remove('SHOCK')
        if previous_gear == 'MIDAS':
          if self.lvl < 34:
            self.skills.remove('$TOSS')

      self.ATK += key_items[playerInput]['ATK']
      self.GDEF += key_items[playerInput]['DEF']
      self.MaxHP += key_items[playerInput]['HP'] 
      self.MaxMP += key_items[playerInput]['MP']
      try:
        self.SPD += key_items[playerInput]['SPD']
      except KeyError:
        pass
      try:
        self.ACC = key_items[playerInput]['ACC']
      except KeyError:
        pass
      try:
        self.FOC = key_items[playerInput]['FOC']
      except KeyError:
        pass

      if self.MaxHP < 1:
        self.MaxHP = 1
      if self.MaxMP < 1:
        self.MaxMP = 1
      if self.HP > self.MaxHP:
        self.HP = self.MaxHP
      if self.MP > self.MaxMP:
        self.MP = self.MaxMP

      if playerInput == 'AETHON':
        if self.lvl < 34:
          self.skills.append('BATTLECRY')
      if playerInput == 'FULGUR':
        if self.lvl < 34:
          self.skills.append('SHOCK')
      if playerInput == 'MIDAS':
        if self.lvl < 34:
          self.skills.append('$TOSS')
      if playerInput == 'DELPHI':
        if self.lvl < 34:
          self.skills.append('AETHER')

    def equipment_check(self, typingActive):
      print_slow(f"\n**********{self.name}'s Equipment**********\n", typingActive)
      print_slow(f"\nRight Hand: {self.rightHand}\n", typingActive)
      print_slow(f"\nLeft Hand: {self.leftHand}\n", typingActive)
      print_slow(f"\nHead: {self.head}\n", typingActive)
      print_slow(f"\nBody: {self.body}\n", typingActive)
      print_slow(f"\nLegs: {self.legs}\n", typingActive) 
      print_slow(f"\Accs 1: {self.accs1}\n", typingActive)
      print_slow(f"\Accs 2: {self.accs2}\n", typingActive)
      
def stat_check_menu(typingActive):
    print_slow(
       '''Starting STATS:
WARRIOR:
Lvl: 1
70 HP 
3 MP
16 ATK
30% DEF
10 SPD
100 GP
5 POTIONS
1 ANTIDOTE
0 ETHER
0 SALINE
1 SMOKE BOMBS
0 WARP CRYSTALS
1 KINDLING
Starting skill: HARDEN: Restores HP and raises Temp. DEF

WIZARD:
Lvl 1
45 HP
8 MP
22 ATK
11% DEF
10 SPD
100 GP
3 POTIONS
1 ANTIDOTE
1 ETHER
0 SALINE
2 SMOKE BOMBS
0 WARP CRYSTALS
0 KINDLING
Starting skill: FOCUS: Concentrate power to increase damage for next few turns.

THIEF:
Lvl 1
55 HP
5 MP
19 ATK
22% DEF
15 SPD
200 GP
5 POTIONS
2 ANTIDOTES
1 ETHER
3 SALINE
5 SMOKE BOMBS
1 WARP CRYSTALS
0 KINDLING
Starting skill: STEAL: Steals GP. Chance to fail.

SUMMONER:
Lvl 1
35 HP
12 MP
10 ATK
8% DEF
10 SPD
100 GP
3 POTIONS
1 ANTIDOTE
3 ETHER
0 SALINE
1 SMOKE BOMBS
0 WARP CRYSTALS
0 KINDLING
Starting skill: EMBER: Summons a fire element creature for a few turns.

       ''', typingActive)


class enemy:
    def __init__(self, name, skill, item, drop, exp, MaxHP, HP, MaxMP, MP, ATK, DEF, TDEF, MACC, ACC, SPD, MaxGP, MinGP, MaxPOTS, POTS, POISON, BLIND, boss, fam, ASFX):
        self.name = name
        self.skill = skill
        self.item = item
        self.drop = drop
        self.exp = exp
        self.MaxHP = MaxHP
        self.HP = HP
        self.MaxMP = MaxMP
        self.MP = MP
        self.ATK = ATK
        self.DEF = DEF
        self.TDEF = TDEF
        self.MACC = MACC
        self.ACC = ACC
        self.SPD = SPD
        self.MaxGP = MaxGP
        self.MinGP = MinGP
        self.MaxPOTS = MaxPOTS
        self.POTS = POTS   
        self.POISON = POISON
        self.BLIND = BLIND
        self.boss = boss
        self.fam = fam
        self.ASFX = ASFX

    def stat_check(self, typingActive):
          print_slow(f'\n{self.name}\n{self.HP}/{self.MaxHP} HP', typingActive)

#enemy instances
p0 = enemy("TEMPLATE", # name
      [1, 2], # skills - Skill correspond to skill list in combat.py
      ['MONSTER PART'], #Itemdrops - material/consumable drops == 1==plantp 2==monp 3==rarep 4==faep 5==dragp 6==pot 7==ant 8==etr 9==smkb
      100, # drop rate - inverse percentage chance to drop item (i.e 00 = 100% to drop, 80 = 20% to drop, ect)
      20, # EXP - EXP given when defeated
      25, # MAXHP - Maximum HP
      25, # HP - Current HP
      3, # MAXMP - Maximum MP
      3, # MP - Current MP
      10, # ATK - Attack power
      95, # DEF - Defense is inverted percentage (i.e 100 = 0% damage taken, 90 = 10% damage taken, ect)
      100, # TDEF - Temporary Defense is inverted percentage modified during combat and interacts multiplicitavely with DEF
      95, # MACC - Max Accuracy currently used to blind accuracy effect
      95, # ACC - Accuracy chance to hit is regular % (ie 95 = 95% chance to hit)
      10, # SPD - Speed determines turn order in combat
      20, # MaxGP - Maximum GP that can be dropped
      5, # MinGP - Minimum GP that can be dropped
      0, # MaxPOTS - Maximum heals the enemy can use 
      0, # POTS - Current heals the enemy has left
      0, # POISON - Active poison turns
      0, # BLIND - Active blind turns
      0, # BOSS - Is Boss (1 == Boss, 0 == Normal)
      ['FAMILY'], # family - enemy family type
      1) # ASFX - Attack Sound Effect
      #Enemy family types: 'GOBLIN', 'UNDEAD', 'BEAST', 'AQUATIC', 'DRAGON', 'FAE', 'PLANT', 'HUMAN', 'VAMPIRE', 'GIANT', 'DEMON', 'CONSTRUCT', 'SLIME', 'ORC', 'MYTHIC', 'WARLOCK'
      #Attack Sound Effects: 1.Cut 2.Slash 3.Claw 4.Stab 5.Smash 6.Crunch 7.Bite 8.Magic 9.Ooze 10.Mist 11.Bite2 12.Magic2
p2 = enemy("Goblin", # name
      [1, 2], # skills
      ['MONSTER PART'],
      80, # drop rate
      20, # EXP
      25, # MAXHP
      25, # HP
      3, # MAXMP
      3, # MP
      10, # ATK
      95, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      10, # SPD
      20, # MaxGP
      5, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GOBLIN'], # family
      1) # ASFX

p3 = enemy("Hobgoblin", # name
      [2, 2], # skills
      ['MONSTER PART', 'MONSTER PART', 'MONSTER PART', 'GOBLIN CHOPPER'],
      80, # drop rate
      25, # EXP
      35, # MAXHP
      35, # HP
      4, # MAXMP
      8, # MP
      13, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      12, # SPD
      30, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GOBLIN'], #family
      1) # ASFX

p3b = enemy("Hobgoblin", # name
      [2, 2], # skills
      ['MONSTER PART'],
      65, # drop rate
      25, # EXP
      35, # MAXHP
      35, # HP
      4, # MAXMP
      8, # MP
      13, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      12, # SPD
      30, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['GOBLIN'], # family
      1) # ASFX

p4 = enemy("Skeleton", # name
      [2, 2], # skills
      ['MONSTER PART', 'MONSTER PART', 'POTION'],
      85, # drop rate
      35, # EXP
      40, # MAXHP
      40, # HP
      2, # MAXMP
      2, # MP
      14, # ATK
      80, # DEF
      100, # TDEF
      40, # MACC
      95, # ACC
      15, # SPD
      95, # MaxGP
      10, # MinGP
      2, # MaxPOTS
      2, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['UNDEAD'], # family
      1) # ASFX

p5 = enemy("Cute 'lil Bunny", # name
      [1, 1], # skills
      ['MONSTER PART'],
      100, # drop rate
      5, # EXP
      5, # MAXHP
      5, # HP
      1, # MAXMP
      1, # MP
      3, # ATK
      100, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      15, # SPD
      5, # MaxGP
      1, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      3) # ASFX

p6 = enemy("Troll", # name
      [3, 3], # skills
      ['RARE MONSTER PART'],
      85, # drop rate
      70, # EXP
      80, # MAXHP
      80, # HP
      2, # MAXMP
      2, # MP
      16, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      16, # SPD
      40, # MaxGP
      15, # MinGP
      2, # MaxPOTS
      2, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GIANT'], # family
      5) # ASFX

p7 = enemy("Honey Badger", # name
      [3, 3], # skills
      ['MONSTER PART'],
      50, # drop rate
      55, # EXP
      55, # MAXHP
      55, # HP
      2, # MAXMP
      2, # MP
      11, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      13, # SPD
      15, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      3) # ASFX

p8 = enemy("Crab", # name
      [1, 1], # skills
      ['MONSTER PART', 'BUCKLER'],
      90, # drop rate
      15, # EXP
      60, # MAXHP
      60, # HP
      1, # MAXMP
      1, # MP
      6, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      8, # SPD
      20, # MaxGP
      10, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p9 = enemy("Dark Mage", # name
      [4, 4], # skills
      ['ETHER', 'ETHER','POINTED HAT'],
      92, # drop rate
      90, # EXP
      90, # MAXHP
      90, # HP
      4, # MAXMP
      4, # MP
      18, # ATK
      95, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      14, # SPD
      45, # MaxGP
      25, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['HUMAN'], # family
      8) # ASFX

p10 = enemy("Wyrm", # name
      [3, 6], # skills
      ['DRAGON SCALE', 'RARE MONSTER PART', 'RARE MONSTER PART'],
      94, # drop rate
      100, # EXP
      120, # MAXHP
      120, # HP
      3, # MAXMP
      3, # MP
      35, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      18, # SPD
      110, # MaxGP
      75, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['DRAGON'], # family
      3) # ASFX

p11 = enemy("Death", # name
      [6, 6], # skills
      ['DRAGON SCALE'],
      99, # drop rate
      999, # EXP
      999, # MAXHP
      999, # HP
      99, # MAXMP
      99, # MP
      99, # ATK
      25, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      10, # SPD
      999, # MaxGP
      99, # MinGP
      9, # MaxPOTS
      9, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['UNDEAD'], # family
      2) # ASFX

p12 = enemy("Big Bear", # name
      [3, 3], # skills
      ['MONSTER PART'],
      55, # drop rate
      65, # EXP
      75, # MAXHP
      75, # HP
      3, # MAXMP
      3, # MP
      20, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      16, # SPD
      65, # MaxGP
      45, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['BEAST'], # family
      7) # ASFX

p12b = enemy("Bear", # name
      [3, 3], # skills
      ['MONSTER PART'],
      55, # drop rate
      65, # EXP
      75, # MAXHP
      75, # HP
      3, # MAXMP
      3, # MP
      18, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      16, # SPD
      65, # MaxGP
      45, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      7) # ASFX

p13 = enemy("Thief", # name
      [2, 5], # skills
      ['SMOKE BOMB', 'POTION', 'WARP CRYSTAL'],
      95, # drop rate
      35, # EXP
      55, # MAXHP
      55, # HP
      3, # MAXMP
      3, # MP
      12, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      20, # SPD
      65, # MaxGP
      40, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['HUMAN'], # family
      1) # ASFX

p14 = enemy("Giant Bee", # name
      [7, 7], # skills
      ['MONSTER PART'],
      85, # drop rate
      20, # EXP
      25, # MAXHP
      25, # HP
      2, # MAXMP
      2, # MP
      12, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      15, # SPD
      20, # MaxGP
      5, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      4) # ASFX

p14b = enemy("Giant Bee", # name
      [7, 7], # skills
      ['MONSTER PART'],
      85, # drop rate
      20, # EXP
      25, # MAXHP
      25, # HP
      2, # MAXMP
      2, # MP
      13, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      15, # SPD
      20, # MaxGP
      5, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['BEAST'], # family
      4) # ASFX

p15 = enemy("Giant Bee Swarm", # name
      [7, 7], # skills
      ['MONSTER PART'],
      80, # drop rate
      50, # EXP
      70, # MAXHP
      70, # HP
      3, # MAXMP
      3, # MP
      20, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      17, # SPD
      20, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      4) # ASFX

p15b = enemy("Giant Bee Swarm", # name
      [7, 7], # skills
      ['MONSTER PART'],
      80, # drop rate
      50, # EXP
      70, # MAXHP
      70, # HP
      3, # MAXMP
      3, # MP
      20, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      17, # SPD
      20, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['BEAST'], # family
      7) # ASFX

p16 = enemy("Mandragora", # name
      [8, 8], # skills
      ['PLANT PART', 'PLANT PART', 'KINDLING'],
      0, # drop rate
      90, # EXP
      120, # MAXHP
      120, # HP
      3, # MAXMP
      3, # MP
      28, # ATK
      75, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      19, # SPD
      80, # MaxGP
      65, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['PLANT'], # family
      5) # ASFX

p16b = enemy("Mandragora", # name
      [8, 8], # skills
      ['PLANT PART', 'KINDLING'],
      0, # drop rate
      100, # EXP
      135, # MAXHP
      135, # HP
      3, # MAXMP
      3, # MP
      34, # ATK
      72, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      19, # SPD
      80, # MaxGP
      65, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['PLANT'], # family
      5) # ASFX

p17 = enemy("'Shroomling", # name
      [8, 8], # skills
      ['PLANT PART', 'PLANT PART', 'KINDLING'],
      65, # drop rate
      30, # EXP
      95, # MAXHP
      95, # HP
      1, # MAXMP
      1, # MP
      24, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      24, # SPD
      30, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['PLANT'], # family
      3) # ASFX

p18 = enemy("Gnome", # name
      [1, 5], # skills
      ['FAE DUST'],
      80, # drop rate
      25, # EXP
      135, # MAXHP
      135, # HP
      2, # MAXMP
      2, # MP
      16, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      28, # SPD
      25, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['FAE'], # family
      8) # ASFX

p19 = enemy("Zomblin", # name
      [2, 13], # skills
      ['MONSTER PART'],
      80, # drop rate
      200, # EXP
      200, # MAXHP
      200, # HP
      30, # MAXMP
      2, # MP
      29, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      9, # SPD
      25, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GOBLIN', 'UNDEAD'], # family
      7) # ASFX

p20 = enemy("Kapa", # name
      [1, 12], # skills
      ['RARE MONSTER PART', 'MONSTER PART', 'KATANA'],
      85, # drop rate
      25, # EXP
      255, # MAXHP
      255, # HP
      3, # MAXMP
      3, # MP
      30, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      24, # SPD
      30, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p21 = enemy("Moldy Zomblin", # name
      [2, 13], # skills
      ['PLANT PART', 'MONSTER PART'],
      80, # drop rate
      65, # EXP
      240, # MAXHP
      240, # HP
      2, # MAXMP
      2, # MP
      37, # ATK
      75, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      11, # SPD
      30, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GOBLIN', 'UNDEAD'], # family
      7) # ASFX

p22 = enemy("Goblin Gang", # name
      [2, 2], # skills
      ['MONSTER PART', 'MONSTER PART', 'GOBLIN CHOPPER'],
      75, # drop rate
      40, # EXP
      60, # MAXHP
      60, # HP
      4, # MAXMP
      4, # MP
      25, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      19, # SPD
      50, # MaxGP
      20, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GOBLIN'], # family
      1) # ASFX

p22b = enemy("Goblin Gang", # name
      [2, 2], # skills
      ['MONSTER PART'],
      70, # drop rate
      40, # EXP
      60, # MAXHP
      60, # HP
      4, # MAXMP
      4, # MP
      25, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      19, # SPD
      50, # MaxGP
      20, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['GOBLIN'], # family
      1) # ASFX

p23 = enemy("Goblin Queen", # name
      [2, 9], # skills
      ['RARE MONSTER PART'],
      0, # drop rate
      120, # EXP
      200, # MAXHP
      200, # HP
      4, # MAXMP
      4, # MP
      28, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      18, # SPD
      80, # MaxGP
      40, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['GOBLIN'], # family
      2) # ASFX

p24 = enemy("Giant Bee Queen", # name
      [7, 10], # skills
      ['RARE MONSTER PART'],
      20, # drop rate
      130, # EXP
      175, # MAXHP
      175, # HP
      4, # MAXMP
      4, # MP
      26, # ATK
      80, # DEF
      95, # TDEF
      95, # MACC
      100, # ACC
      17, # SPD
      60, # MaxGP
      45, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['BEAST'], # family
      4) # ASFX

p25 = enemy("Killer Bee", # name
      [7, 7], # skills
      ['MONSTER PART'],
      80, # drop rate
      50, # EXP
      75, # MAXHP
      75, # HP
      5, # MAXMP
      5, # MP
      21, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      17, # SPD
      25, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      4) # ASFX

p26 = enemy("Mercenary Rat", # name
      [2, 15], # skills
      ['MONSTER PART', 'MONSTER PART', 'MACE'],
      85, # drop rate
      35, # EXP
      90, # MAXHP
      90, # HP
      3, # MAXMP
      3, # MP
      27, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      14, # SPD
      50, # MaxGP
      10, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      1) # ASFX

p27 = enemy("Hawk", # name
      [1, 25], # skills
      ['MONSTER PART', 'POTION'],
      100, # drop rate
      30, # EXP
      80, # MAXHP
      80, # HP
      2, # MAXMP
      2, # MP
      21, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      17, # SPD
      15, # MaxGP
      5, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      4) # ASFX

p28 = enemy("Traveling Merchant", # name
      [2, 5], # skills
      ['DRAGON SCALE'],
      0, # drop rate
      35, # EXP
      55, # MAXHP
      55, # HP
      3, # MAXMP
      3, # MP
      11, # ATK
      85, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      10, # SPD
      65, # MaxGP
      40, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['HUMAN'], # family
      1) # ASFX

p29 = enemy("Ozzing Slime", # name
      [8, 16], # skills
      ['RARE MONSTER PART', 'MONSTER PART',],
      90, # drop rate
      35, # EXP
      185, # MAXHP
      185, # HP
      3, # MAXMP
      3, # MP
      24, # ATK
      45, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      7, # SPD
      55, # MaxGP
      35, # MinGP
      2, # MaxPOTS
      2, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['SLIME'], # family
      9) # ASFX

p29b = enemy("Ozzing Slime", # name
      [8, 16], # skills
      ['RARE MONSTER PART'],
      0, # drop rate
      35, # EXP
      195, # MAXHP
      195, # HP
      3, # MAXMP
      3, # MP
      24, # ATK
      45, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      7, # SPD
      55, # MaxGP
      35, # MinGP
      2, # MaxPOTS
      2, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['SLIME'], # family
      9) # ASFX

p30 = enemy("Mandrake Child", # name
      [8, 8], # skills
      ['PLANT PART', 'KINDLING'],
      60, # drop rate
      45, # EXP
      165, # MAXHP
      165, # HP
      2, # MAXMP
      2, # MP
      24, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      22, # SPD
      45, # MaxGP
      35, # MinGP
      1, # MaxPOTS
      18, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['PLANT'], # family
      3) # ASFX

p31 = enemy("Ogre", # name
      [2, 11], # skills
      ['MONSTER PART', 'MONSTER PART', 'MONSTER PART', 'RARE MONSTER PART'],
      65, # drop rate
      70, # EXP
      200, # MAXHP
      200, # HP
      2, # MAXMP
      2, # MP
      30, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      21, # SPD
      55, # MaxGP
      25, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['GIANT'], # family
      5) # ASFX

p32 = enemy("Suiko", # name
      [12, 13], # skills
      ['RARE MONSTER PART', 'KATANA'],
      80, # drop rate
      80, # EXP
      210, # MAXHP
      210, # HP
      3, # MAXMP
      3, # MP
      32, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      26, # SPD
      70, # MaxGP
      25, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p33 = enemy("Imp", # name
      [13, 13], # skills
      ['FAE DUST', 'FAE DUST', 'ETHER'],
      75, # drop rate
      60, # EXP
      265, # MAXHP
      265, # HP
      4, # MAXMP
      4, # MP
      28, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      27, # SPD
      50, # MaxGP
      25, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['DEMON'], # family
      8) # ASFX

p34 = enemy("Donkey", # name
      [1, 1], # skills
      ['WAFFLE'],
      0, # drop rate
      35, # EXP
      45, # MAXHP
      45, # HP
      1, # MAXMP
      1, # MP
      10, # ATK
      90, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      12, # SPD
      20, # MaxGP
      10, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      7) # ASFX

p35 = enemy("Ogre Chief", # name
      [2, 11, 17], # skills
      ['RARE MONSTER PART', 'WARP CRYSTAL'],
      0, # drop rate
      175, # EXP
      450, # MAXHP
      450, # HP
      4, # MAXMP
      4, # MP
      42, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      28, # SPD
      105, # MaxGP
      85, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['GIANT'], # family
      5) # ASFX

p36 = enemy("Pixie", # name
      [5, 14], # skills
      ['FAE DUST', 'FAE DUST', 'VELVET SLIPPERS'],
      50, # drop rate
      45, # EXP
      265, # MAXHP
      265, # HP
      4, # MAXMP
      4, # MP
      24, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      31, # SPD
      35, # MaxGP
      15, # MinGP
      2, # MaxPOTS
      2, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['FAE'], # family
      8) # ASFX

p37 = enemy("Fairy", # name
      [1, 14], # skills
      ['FAE DUST', 'FAE DUST', 'FAE DUST', 'FAE DUST', 'SIDE SWORD'],
      60, # drop rate
      90, # EXP
      315, # MAXHP
      315, # HP
      4, # MAXMP
      4, # MP
      32, # ATK
      75, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      34, # SPD
      75, # MaxGP
      40, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['FAE'], # family
      8) # ASFX

p38 = enemy("Nymph", # name
      [4, 14], # skills
      ['FAE DUST'],
      55, # drop rate
      120, # EXP
      365, # MAXHP
      365, # HP
      4, # MAXMP
      4, # MP
      39, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      28, # SPD
      85, # MaxGP
      50, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['FAE'], # family
      4) # ASFX

p39 = enemy("Fish-Man", # name
      [15, 15], # skills
      ['MONSTER PART', 'MONSTER PART', 'HANGER'],
      70, # drop rate
      65, # EXP
      380, # MAXHP
      380, # HP
      3, # MAXMP
      3, # MP
      39, # ATK
      78, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      30, # SPD
      45, # MaxGP
      25, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      4) # ASFX

p40 = enemy("Dark Fairy Prince", # name
      [4, 14], # skills
      ['FAE DUST'],
      0, # drop rate
      355, # EXP
      195, # MAXHP
      195, # HP
      6, # MAXMP
      6, # MP
      48, # ATK
      75, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      36, # SPD
      85, # MaxGP
      65, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['FAE'], # family
      8) # ASFX

p41 = enemy("Hexopus", # name
      [1, 16], # skills
      ['MONSTER PART', 'MONSTER PART', 'RARE MONSTER PART'],
      50, # drop rate
      85, # EXP
      200, # MAXHP
      200, # HP
      1, # MAXMP
      1, # MP
      24, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      25, # SPD
      65, # MaxGP
      45, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['AQUATIC'], # family
      5) # ASFX

p42 = enemy("Sand Squid", # name
      [3, 16], # skills
      ['MONSTER PART', 'PARMA'],
      75, # drop rate
      90, # EXP
      310, # MAXHP
      310, # HP
      1, # MAXMP
      1, # MP
      29, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      26, # SPD
      80, # MaxGP
      50, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p43 = enemy("King Crab", # name
      [1, 17], # skills
      ['MONSTER PART', 'RARE MONSTER PART', 'HEATER SHIELD'],
      80, # drop rate
      95, # EXP
      430, # MAXHP
      430, # HP
      1, # MAXMP
      1, # MP
      41, # ATK
      60, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      12, # SPD
      60, # MaxGP
      30, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p44 = enemy("Murmaider", # name
      [15, 17], # skills
      ['RARE MONSTER PART', 'POTION'],
      95, # drop rate
      105, # EXP
      445, # MAXHP
      445, # HP
      2, # MAXMP
      2, # MP
      44, # ATK
      82, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      27, # SPD
      80, # MaxGP
      55, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      4) # ASFX

p45 = enemy("Mangy Pirate", # name
      [5, 17], # skills
      ['POTION', 'HANGER'],
      75, # drop rate
      95, # EXP
      480, # MAXHP
      480, # HP
      2, # MAXMP
      2, # MP
      39, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      25, # SPD
      75, # MaxGP
      50, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['HUMAN'], # family
      2) # ASFX

p46 = enemy("Wolverine", # name
      [3, 3], # skills
      ['MONSTER PART'],
      50, # drop rate
      50, # EXP
      155, # MAXHP
      155, # HP
      2, # MAXMP
      2, # MP
      28, # ATK
      86, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      21, # SPD
      35, # MaxGP
      15, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      3) # ASFX

p47 = enemy("Orc Scout", # name
      [2, 17], # skills
      ['MONSTER PART', 'ARMING SWORD'],
      70, # drop rate
      80, # EXP
      300, # MAXHP
      300, # HP
      3, # MAXMP
      3, # MP
      34, # ATK
      78, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      30, # SPD
      65, # MaxGP
      45, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['ORC'], # family
      1) # ASFX

p48 = enemy("Auroch", # name
      [3, 3], # skills
      ['MONSTER PART'],
      60, # drop rate
      75, # EXP
      275, # MAXHP
      275, # HP
      2, # MAXMP
      2, # MP
      36, # ATK
      75, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      14, # SPD
      40, # MaxGP
      30, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['MYTHIC'], # family
      6) # ASFX

p49 = enemy("Mountain Goat", # name
      [1, 3], # skills
      ['MONSTER PART'],
      70, # drop rate
      55, # EXP
      60, # MAXHP
      60, # HP
      2, # MAXMP
      2, # MP
      18, # ATK
      80, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      15, # SPD
      35, # MaxGP
      15, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      7) # ASFX

p50 = enemy("Killer Bunny", # name
      [3, 3], # skills
      ['SMOKE BOMB'],
      30, # drop rate
      180, # EXP
      800, # MAXHP
      800, # HP
      2, # MAXMP
      2, # MP
      60, # ATK
      100, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      45, # SPD
      50, # MaxGP
      10, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['BEAST'], # family
      7) # ASFX

p51 = enemy("River Serpent", # name
      [9, 13, 16], # skills
      ['DRAGON SCALE'],
      0, # drop rate
      285, # EXP
      555, # MAXHP
      555, # HP
      4, # MAXMP
      4, # MP
      55, # ATK
      77, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      36, # SPD
      115, # MaxGP
      100, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['DRAGON'], # family
      11) # ASFX

p52 = enemy("Rogue Gang", # name
      [2, 5, 18], # skills
      ['COWL'],
      35, # drop rate
      160, # EXP
      440, # MAXHP
      440, # HP
      6, # MAXMP
      6, # MP
      44, # ATK
      82, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      36, # SPD
      125, # MaxGP
      65, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['HUMAN'], # family
      2) # ASFX

p53 = enemy("Crescent Pond Naga", # name
      [8, 20], # skills
      ['BARBUTE'],
      0, # drop rate
      545, # EXP
      575, # MAXHP
      275, # HP
      5, # MAXMP
      5, # MP
      52, # ATK
      64, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      32, # SPD
      215, # MaxGP
      145, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      1, # BOSS
      ['AQUATIC'], # family
      4) # ASFX

p54 = enemy("Karrapa", # name
      [1, 12], # skills
      ['RARE MONSTER PART', 'WAND'],
      84, # drop rate
      95, # EXP
      415, # MAXHP
      415, # HP
      3, # MAXMP
      3, # MP
      46, # ATK
      70, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      37, # SPD
      75, # MaxGP
      35, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p55 = enemy("Enko", # name
      [3, 12], # skills
      ['RARE MONSTER PART', 'BROAD SWORD'],
      78, # drop rate
      110, # EXP
      445, # MAXHP
      445, # HP
      5, # MAXMP
      5, # MP
      50, # ATK
      68, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      38, # SPD
      80, # MaxGP
      55, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['AQUATIC'], # family
      6) # ASFX

p56 = enemy("Lamia", # name
      [8, 15, 29], # skills
      ['RARE MONSTER PART',  'SERPENT KNIFE', 'SERPENT KNIFE',  'DRAGON SCALE'],
      99, # drop rate
      145, # EXP
      575, # MAXHP
      575, # HP
      4, # MAXMP
      4, # MP
      45, # ATK
      84, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      40, # SPD
      115, # MaxGP
      45, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['DEMON'], # family
      1) # ASFX

p57 = enemy("Minotaur", # name
      [3, 9], # skills
      ['RARE MONSTER PART', 'BATTLE AXE'],
      78, # drop rate
      150, # EXP
      685, # MAXHP
      685, # HP
      5, # MAXMP
      5, # MP
      56, # ATK
      68, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      30, # SPD
      80, # MaxGP
      55, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['MYTHIC'], # family
      5) # ASFX

p58 = enemy("Unicorn", # name
      [1, 15], # skills
      ['RARE MONSTER PART'],
      25, # drop rate
      160, # EXP
      555, # MAXHP
      555, # HP
      4, # MAXMP
      4, # MP
      47, # ATK
      65, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      50, # SPD
      100, # MaxGP
      75, # MinGP
      1, # MaxPOTS
      1, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['MYTHIC'], # family
      4) # ASFX

p59 = enemy("Treant", # name
      [17, 19], # skills
      ['PLANT PART', 'KINDLING', 'KINDLING'],
      75, # drop rate
      125, # EXP
      635, # MAXHP
      635, # HP
      5, # MAXMP
      5, # MP
      38, # ATK
      60, # DEF
      100, # TDEF
      95, # MACC
      95, # ACC
      10, # SPD
      80, # MaxGP
      29, # MinGP
      0, # MaxPOTS
      0, # POTS
      0, # POISON
      0, # BLIND
      0, # BOSS
      ['PLANT'], # family
      5) # ASFX

p60 = enemy("Dryad", # name
  [4, 19], # skills
  ['FAE DUST', 'FAE DUST', 'KINDLING'],
  55, # drop rate
  150, # EXP
  620, # MAXHP
  620, # HP
  4, # MAXMP
  4, # MP
  50, # ATK
  75, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  41, # SPD
  90, # MaxGP
  60, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['PLANT'], # family
  3) # ASFX

p61 = enemy("Centaur", # name
  [3, 12], # skills
  ['RARE MONSTER PART', 'VAMBRACE'],
  88, # drop rate
  110, # EXP
  545, # MAXHP
  545, # HP
  2, # MAXMP
  2, # MP
  54, # ATK
  74, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  44, # SPD
  60, # MaxGP
  35, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['MYTHIC'], # family
  4) # ASFX

p62 = enemy("Specter", # name
  [21, 22], # skills
  ['ETHER', 'ETHER', 'ROGUE SLIPPERS'],
  70, # drop rate
  135, # EXP
  615, # MAXHP
  615, # HP
  5, # MAXMP
  5, # MP
  47, # ATK
  64, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  41, # SPD
  20, # MaxGP
  10, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['UNDEAD'], # family
  9) # ASFX

p63 = enemy("Cove Bat", # name
  [16, 20], # skills
  ['MONSTER PART'],
  77, # drop rate
  85, # EXP
  190, # MAXHP
  190, # HP
  2, # MAXMP
  2, # MP
  37, # ATK
  82, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  32, # SPD
  50, # MaxGP
  20, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['BEAST'], # family
  7) # ASFX

p64 = enemy("Salamander", # name
  [6, 13], # skills
  ['RARE MONSTER PART', 'HEATER SHIELD', 'DRAGON SCALE'],
  90, # drop rate
  115, # EXP
  310, # MAXHP
  310, # HP
  4, # MAXMP
  4, # MP
  41, # ATK
  72, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  20, # SPD
  100, # MaxGP
  70, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DRAGON'], # family
  11) # ASFX

p65 = enemy("Rusalka", # name
  [20, 21], # skills
  ['MONSTER PART'],
  90, # drop rate
  105, # EXP
  300, # MAXHP
  300, # HP
  5, # MAXMP
  5, # MP
  44, # ATK
  76, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  35, # SPD
  70, # MaxGP
  25, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DEMON'], # family
  10) # ASFX

p66 = enemy("Golem", # name
  [17, 23], # skills
  ['SMOKE BOMB', 'TOWER SHIELD'],
  85, # drop rate
  165, # EXP
  690, # MAXHP
  690, # HP
  3, # MAXMP
  3, # MP
  48, # ATK
  42, # DEF
  100, # TDEF
  90, # MACC
  90, # ACC
  11, # SPD
  140, # MaxGP
  25, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['CONSTRUCT'], # family
  5) # ASFX

p67 = enemy("Dire Wolf", # name
  [3, 11], # skills
  ['MONSTER PART'],
  35, # drop rate
  80, # EXP
  495, # MAXHP
  495, # HP
  6, # MAXMP
  6, # MP
  58, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  44, # SPD
  55, # MaxGP
  25, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['BEAST'], # family
  7) # ASFX

p67b = enemy("Dire Wolf", # name
  [3, 11], # skills
  ['MONSTER PART'],
  55, # drop rate
  80, # EXP
  395, # MAXHP
  395, # HP
  6, # MAXMP
  6, # MP
  42, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  42, # SPD
  55, # MaxGP
  25, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['BEAST'], # family
  7) # ASFX

p68 = enemy("Harpy", # name
  [3, 24], # skills
  ['MONSTER PART'],
  55, # drop rate
  100, # EXP
  395, # MAXHP
  395, # HP
  3, # MAXMP
  3, # MP
  35, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  50, # SPD
  85, # MaxGP
  35, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['MYTHIC'], # family
  3) # ASFX

p69 = enemy("Roc", # name
  [24, 25], # skills
  ['RARE MONSTER PART'],
  75, # drop rate
  145, # EXP
  435, # MAXHP
  435, # HP
  4, # MAXMP
  4, # MP
  47, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  51, # SPD
  105, # MaxGP
  35, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['MYTHIC'], # family
  4) # ASFX

p70 = enemy("Wyvern", # name
  [6, 13, 25], # skills
  ['RARE MONSTER PART', 'DRAGON SCALE'],
  94, # drop rate
  175, # EXP
  550, # MAXHP
  550, # HP
  4, # MAXMP
  4, # MP
  54, # ATK
  78, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  54, # SPD
  105, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DRAGON'], # family
  3) # ASFX

p71 = enemy("Drake", # name
  [6, 8, 11], # skills
  ['DRAGON SCALE'],
  93, # drop rate
  190, # EXP
  680, # MAXHP
  680, # HP
  4, # MAXMP
  4, # MP
  59, # ATK
  75, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  55, # SPD
  125, # MaxGP
  55, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DRAGON'], # family
  2) # ASFX

p72 = enemy("Dragon", # name
  [6, 8, 17], # skills
  ['ARMET','DRAGON SCALE'],
  92, # drop rate
  210, # EXP
  700, # MAXHP
  700, # HP
  5, # MAXMP
  5, # MP
  65, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  50, # SPD
  155, # MaxGP
  65, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DRAGON'], # family
  11) # ASFX

p72b = enemy("Dragon", # name
  [6, 8, 17], # skills
  ['DRAGON SCALE'],
  0, # drop rate
  715, # EXP
  1350, # MAXHP
  1350, # HP
  5, # MAXMP
  5, # MP
  75, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  60, # SPD
  155, # MaxGP
  65, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['DRAGON'], # family
  11) # ASFX

p73 = enemy("Dragon King, Tanninim", # name
  [6, 9, 11, 13, 17], # skills
  ['DRAGON SCALE'],
  0, # drop rate
  750, # EXP
  2100, # MAXHP
  2100, # HP
  10, # MAXMP
  10, # MP
  120, # ATK
  62, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  100, # SPD
  325, # MaxGP
  155, # MinGP
  2, # MaxPOTS
  2, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['DRAGON'], # family
  11) # ASFX

p74 = enemy("Giant Bee Larva", # name
  [7, 10], # skills
  ['RARE MONSTER PART'],
  20, # drop rate
  130, # EXP
  275, # MAXHP
  275, # HP
  4, # MAXMP
  4, # MP
  31, # ATK
  80, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  50, # SPD
  60, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['BEAST'], # family
  4) # ASFX

p75 = enemy("Giant Wasp", # name
  [7, 10], # skills
  ['RARE MONSTER PART'],
  20, # drop rate
  130, # EXP
  475, # MAXHP
  475, # HP
  4, # MAXMP
  4, # MP
  41, # ATK
  80, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  55, # SPD
  60, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['BEAST'], # family
  4) # ASFX

p76 = enemy("Owl", # name
  [24, 25], # skills
  ['MONSTER PART'],
  100, # drop rate
  30, # EXP
  140, # MAXHP
  140, # HP
  2, # MAXMP
  2, # MP
  25, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  40, # SPD
  15, # MaxGP
  5, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['BEAST'], # family
  4) # ASFX

p77 = enemy("Tiger", # name
  [3, 11, 17], # skills
  ['MONSTER PART'],
  75, # drop rate
  120, # EXP
  315, # MAXHP
  315, # HP
  6, # MAXMP
  6, # MP
  57, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  45, # SPD
  65, # MaxGP
  35, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['BEAST'], # family
  11) # ASFX

p78 = enemy("Orc Guard", # name
  [2, 14, 17], # skills
  ['MONSTER PART','MORNING STAR'],
  70, # drop rate
  155, # EXP
  375, # MAXHP
  375, # HP
  3, # MAXMP
  3, # MP
  44, # ATK
  71, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  44, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  2) # ASFX

p79 = enemy("Orc Pikeman", # name
  [2, 15], # skills
  ['MONSTER PART'],
  70, # drop rate
  160, # EXP
  400, # MAXHP
  400, # HP
  3, # MAXMP
  3, # MP
  47, # ATK
  78, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  45, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  4) # ASFX

p80 = enemy("Orc Archer", # name
  [1, 13], # skills
  ['MONSTER PART', 'MONSTER PART', 'MONSTER PART', 'WAR PICK'],
  70, # drop rate
  140, # EXP
  350, # MAXHP
  350, # HP
  3, # MAXMP
  3, # MP
  40, # ATK
  80, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  47, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  4) # ASFX

p81 = enemy("Orc Sorcerer", # name
  [4, 6, 8], # skills
  ['MONSTER PART', 'MONSTER PART', 'MAGUS HAT'],
  70, # drop rate
  140, # EXP
  300, # MAXHP
  300, # HP
  3, # MAXMP
  3, # MP
  49, # ATK
  90, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  43, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  8) # ASFX

p82 = enemy("Orc Commander", # name
  [2, 11, 17], # skills
  ['MONSTER PART', 'MONSTER PART', 'MONSTER PART', 'MONSTER PART', 'ADAMANTITE BOOTS'],
  70, # drop rate
  230, # EXP
  500, # MAXHP
  500, # HP
  3, # MAXMP
  3, # MP
  50, # ATK
  74, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  50, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  2) # ASFX

p83 = enemy("Varg", # name
  [3, 11], # skills
  ['MONSTER PART'],
  55, # drop rate
  115, # EXP
  395, # MAXHP
  395, # HP
  6, # MAXMP
  6, # MP
  48, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  49, # SPD
  55, # MaxGP
  25, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['BEAST'], # family
  11) # ASFX

p84 = enemy("Orc King, Kirgoth", # name
  [2, 3, 9, 11, 15, 17], # skills
  ['WAR PICK'],
  0, # drop rate
  560, # EXP
  800, # MAXHP
  800, # HP
  3, # MAXMP
  3, # MP
  65, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  63, # SPD
  565, # MaxGP
  345, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['ORC'], # family
  5) # ASFX

p85 = enemy("Spider-Lady", # name
  [13, 16, 29], # skills
  ['STILETTO'],
  0, # drop rate
  230, # EXP
  460, # MAXHP
  460, # HP
  3, # MAXMP
  3, # MP
  34, # ATK
  76, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  34, # SPD
  165, # MaxGP
  125, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['DEMON'], # family
  7) # ASFX

p86 = enemy("Shadow Snatcher", # name
  [26, 28], # skills
  ['BLACK COWL'],
  0, # drop rate
  300, # EXP
  999, # MAXHP
  999, # HP
  3, # MAXMP
  3, # MP
  64, # ATK
  85, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  60, # SPD
  285, # MaxGP
  145, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['DEMON'], # family
  6) # ASFX

p87 = enemy("Living Armor", # name
  [2, 15], # skills
  ['MONSTER PART'],
  70, # drop rate
  200, # EXP
  600, # MAXHP
  600, # HP
  3, # MAXMP
  3, # MP
  54, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  59, # SPD
  105, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['CONSTRUCT'], # family
  2) # ASFX

p87b = enemy("Living Armor", # name
  [2, 15], # skills
  ['MONSTER PART'],
  70, # drop rate
  250, # EXP
  650, # MAXHP
  650, # HP
  3, # MAXMP
  3, # MP
  54, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  59, # SPD
  185, # MaxGP
  105, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['CONSTRUCT'], # family
  2) # ASFX

p88 = enemy("Flesh Golem", # name
  [9, 11, 12, 17], # skills
  ['MONSTER PART'],
  70, # drop rate
  355, # EXP
  800, # MAXHP
  800, # HP
  3, # MAXMP
  3, # MP
  64, # ATK
  62, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  17, # SPD
  200, # MaxGP
  155, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['CONSTRUCT', 'UNDEAD'], # family
  5) # ASFX

p89 = enemy("Skeletal Soldier", # name
  [2, 15, 17], # skills
  ['MONSTER PART', 'RAPIER'],
  70, # drop rate
  225, # EXP
  550, # MAXHP
  550, # HP
  3, # MAXMP
  3, # MP
  55, # ATK
  82, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  61, # SPD
  105, # MaxGP
  65, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['UNDEAD'], # family
  4) # ASFX

p90 = enemy("Corpse Pile", # name
  [3, 8, 17], # skills
  ['DRAGON SCALE'],
  92, # drop rate
  240, # EXP
  720, # MAXHP
  720, # HP
  5, # MAXMP
  5, # MP
  35, # ATK
  50, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  12, # SPD
  155, # MaxGP
  65, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['UNDEAD', 'SLIME'], # family
  9) # ASFX

p91 = enemy("Vampire Queen", # name
  [4, 20], # skills
  ['MONSTER PART'],
  70, # drop rate
  460, # EXP
  1000, # MAXHP
  1000, # HP
  5, # MAXMP
  5, # MP
  64, # ATK
  72, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  70, # SPD
  345, # MaxGP
  215, # MinGP
  2, # MaxPOTS
  2, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['UNDEAD', 'VAMPIRE'], # family
  8) # ASFX

p92 = enemy("Vampire Lord", # name
  [4, 15, 20, 29], # skills
  ['MONSTER PART'],
  70, # drop rate
  800, # EXP
  1555, # MAXHP
  1555, # HP
  8, # MAXMP
  8, # MP
  74, # ATK
  70, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  80, # SPD
  685, # MaxGP
  505, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['UNDEAD', 'VAMPIRE'], # family
  2) # ASFX

p93 = enemy("Demon Statue", # name
  [6, 27, 28, 29], # skills
  ['MONSTER PART'],
  70, # drop rate
  810, # EXP
  1200, # MAXHP
  1200, # HP
  7, # MAXMP
  7, # MP
  75, # ATK
  65, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  82, # SPD
  335, # MaxGP
  245, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['DEMON'], # family
  4) # ASFX

p94 = enemy("WereWolf", # name
  [13, 20], # skills
  ['MONSTER PART'],
  70, # drop rate
  630, # EXP
  1100, # MAXHP
  1100, # HP
  6, # MAXMP
  6, # MP
  64, # ATK
  81, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  75, # SPD
  200, # MaxGP
  100, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['UNDEAD', 'MYTHIC'], # family
  11) # ASFX

p95 = enemy("Wall Demon", # name
  [2, 17], # skills
  ['MONSTER PART'],
  70, # drop rate
  400, # EXP
  1200, # MAXHP
  1200, # HP
  4, # MAXMP
  4, # MP
  74, # ATK
  65, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  75, # SPD
  205, # MaxGP
  20, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  1, # BOSS
  ['DEMON'], # family
  6) # ASFX

p96 = enemy("Cursed Book", # name
  [2, 17], # skills
  ['ETHER', 'ETHER', 'ETHER', 'WARP CRYSTAL', 'MAGUS SHOES'],
  75, # drop rate
  135, # EXP
  350, # MAXHP
  350, # HP
  5, # MAXMP
  5, # MP
  40, # ATK
  90, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  60, # SPD
  65, # MaxGP
  45, # MinGP
  1, # MaxPOTS
  1, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['CONSTRUCT'], # family
  10) # ASFX

p97 = enemy("Vampire Thrall", # name
  [3, 20], # skills
  ['MONSTER PART'],
  70, # drop rate
  190, # EXP
  570, # MAXHP
  570, # HP
  3, # MAXMP
  3, # MP
  44, # ATK
  75, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  62, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['UNDEAD', 'VAMPIRE'], # family
  7) # ASFX

p98 = enemy("Gorgon", # name
  [27, 29], # skills
  ['MONSTER PART'],
  70, # drop rate
  230, # EXP
  610, # MAXHP
  610, # HP
  8, # MAXMP
  8, # MP
  51, # ATK
  72, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  71, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['MYTHIC'], # family
  1) # ASFX

p99 = enemy("Giant Tarhandtula", # name
  [4, 5, 12], # skills
  ['MONSTER PART'],
  70, # drop rate
  210, # EXP
  590, # MAXHP
  590, # HP
  3, # MAXMP
  3, # MP
  49, # ATK
  80, # DEF
  100, # TDEF
  95, # MACC
  95, # ACC
  73, # SPD
  65, # MaxGP
  45, # MinGP
  0, # MaxPOTS
  0, # POTS
  0, # POISON
  0, # BLIND
  0, # BOSS
  ['UNDEAD'], # family
  6) # ASFX

p100 = enemy("Vampire Bat", # name
    [17, 20], # skills
    ['MONSTER PART'],
    70, # drop rate
    140, # EXP
    380, # MAXHP
    380, # HP
    2, # MAXMP
    2, # MP
    45, # ATK
    85, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    69, # SPD
    65, # MaxGP
    45, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['BEAST','VAMPIRE'], # family
    7) # ASFX

p101 = enemy("Chimera", # name
    [3, 6, 17], # skills
    ['MONSTER PART'],
    70, # drop rate
    320, # EXP
    700, # MAXHP
    700, # HP
    5, # MAXMP
    5, # MP
    54, # ATK
    64, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    72, # SPD
    100, # MaxGP
    65, # MinGP
    2, # MaxPOTS
    2, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['MYTHIC'], # family
    5) # ASFX

p102 = enemy("Warlock", # name
    [4, 6, 9], # skills
    ['ETHER', 'MAGUS ROBES'],
    70, # drop rate
    305, # EXP
    600, # MAXHP
    600, # HP
    6, # MAXMP
    6, # MP
    64, # ATK
    78, # DEF
    100, # TDEF
    95, # MACC
    205, # ACC
    70, # SPD
    165, # MaxGP
    45, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['WARLOCK'], # family
    8) # ASFX

p103 = enemy("Ripper", # name
    [20, 15], # skills
    ['MONSTER PART'],
    70, # drop rate
    360, # EXP
    730, # MAXHP
    730, # HP
    3, # MAXMP
    3, # MP
    74, # ATK
    75, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    77, # SPD
    215, # MaxGP
    145, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['DEMON'], # family
    2) # ASFX

p104 = enemy("Shadow Fiend", # name
    [3, 12, 27], # skills
    ['MONSTER PART'],
    70, # drop rate
    375, # EXP
    800, # MAXHP
    800, # HP
    5, # MAXMP
    5, # MP
    70, # ATK
    70, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    79, # SPD
    235, # MaxGP
    165, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['DEMON'], # family
    6) # ASFX

p105 = enemy("Bone Dragon", # name
    [6, 8, 17, 27], # skills
    ['RARE MONSTER PART', 'DRAGON SCALE'],
    70, # drop rate
    620, # EXP
    1100, # MAXHP
    1100, # HP
    8, # MAXMP
    8, # MP
    76, # ATK
    72, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    80, # SPD
    315, # MaxGP
    235, # MinGP
    1, # MaxPOTS
    1, # POTS
    0, # POISON
    0, # BLIND
    0, # BOSS
    ['DRAGON', 'UNDEAD'], # family
    11) # ASFX

p106 = enemy("Shadow Soldier", # name
    [2, 15], # skills
    ['MONSTER PART', 'TEMPERED GREAVES'],
    72, # drop rate
    330, # EXP
    820, # MAXHP
    820, # HP
    3, # MAXMP
    3, # MP
    64, # ATK
    76, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    82, # SPD
    195, # MaxGP
    105, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['DEMON'], # family
    1) # ASFX

p107 = enemy("Ghoul", # name
    [17, 20], # skills
    ['MONSTER PART'],
    70, # drop rate
    280, # EXP
    615, # MAXHP
    615, # HP
    3, # MAXMP
    3, # MP
    54, # ATK
    78, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    72, # SPD
    45, # MaxGP
    25, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['UNDEAD'], # family
    1) # ASFX

p108 = enemy("Dark Knight", # name
    [2, 6, 17], # skills
    ['MONSTER PART', 'SABATONS'],
    70, # drop rate
    390, # EXP
    900, # MAXHP
    900, # HP
    3, # MAXMP
    3, # MP
    74, # ATK
    68, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    75, # SPD
    265, # MaxGP
    100, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['HUMAN'], # family
    2) # ASFX

p109 = enemy("Imprisoned Soul", # name
    [1, 21, 22], # skills
    ['MONSTER PART'],
    70, # drop rate
    270, # EXP
    755, # MAXHP
    755, # HP
    4, # MAXMP
    4, # MP
    60, # ATK
    80, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    74, # SPD
    175, # MaxGP
    35, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['UNDEAD'], # family
    10) # ASFX

p110 = enemy("Unholy Mass", # name
    [8, 16], # skills
    ['MONSTER PART'],
    70, # drop rate
    300, # EXP
    660, # MAXHP
    660, # HP
    3, # MAXMP
    3, # MP
    66, # ATK
    44, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    13, # SPD
    100, # MaxGP
    60, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['SLIME'], # family
    9) # ASFX

p111 = enemy("Fat Goblin", # name
    [1, 2, 5], # skills
    ['ROGUES VEST'],
    0, # drop rate
    220, # EXP
    400, # MAXHP
    400, # HP
    3, # MAXMP
    3, # MP
    35, # ATK
    76, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    69, # SPD
    265, # MaxGP
    165, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['GOBLIN'], # family
    1) # ASFX

p112 = enemy("Abyssal Hound", # name
    [6, 17], # skills
    ['MONSTER PART'],
    70, # drop rate
    340, # EXP
    625, # MAXHP
    625, # HP
    3, # MAXMP
    3, # MP
    54, # ATK
    79, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    84, # SPD
    95, # MaxGP
    35, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['DEMON'], # family
    7) # ASFX

p113 = enemy("Jaw Demon", # name
    [11, 16, 17], # skills
    ['MONSTER PART'],
    70, # drop rate
    410, # EXP
    900, # MAXHP
    900, # HP
    3, # MAXMP
    3, # MP
    74, # ATK
    72, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    70, # SPD
    300, # MaxGP
    105, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['DEMON'], # family
    11) # ASFX

p114 = enemy("Phantom Painting", # name
    [4, 21], # skills
    ['MONSTER PART'],
    70, # drop rate
    220, # EXP
    555, # MAXHP
    555, # HP
    3, # MAXMP
    3, # MP
    54, # ATK
    73, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    68, # SPD
    225, # MaxGP
    145, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['UNDEAD', 'CONSTRUCT'], # family
    10) # ASFX

p115 = enemy("Lost Soul", # name
    [4, 21, 22], # skills
    ['MONSTER PART'],
    70, # drop rate
    240, # EXP
    410, # MAXHP
    410, # HP
    5, # MAXMP
    5, # MP
    50, # ATK
    75, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    67, # SPD
    95, # MaxGP
    65, # MinGP
    0, # MaxPOTS
    0, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['UNDEAD'], # family
    10) # ASFX

p666 = enemy("Dark Warlock, Smeldar", # name
    [4, 6, 8, 17, 21, 30], # skills
    ['MONSTER PART'],
    70, # drop rate
    999, # EXP
    2400, # MAXHP
    2400, # HP
    16, # MAXMP
    16, # MP
    95, # ATK
    69, # DEF
    100, # TDEF
    95, # MACC
    95, # ACC
    92, # SPD
    65, # MaxGP
    45, # MinGP
    3, # MaxPOTS
    3, # POTS
    0, # POISON
    0, # BLIND
    1, # BOSS
    ['WARLOCK'], # family
    12) # ASFX


enemy_spawnT = [p98,p98] #testing
enemy_spawn0 = [p2, p5, p7]  #cliff enemies
enemy_spawn1 = [p2, p3, p7, p13]  #forest enemies
enemy_spawn2 = [p2, p3, p4, p6]  #thicket enemies
enemy_spawn3 = [p5, p7, p14, p18]  #berry enemies
enemy_spawn4 = [p2, p4, p9, p19]  #shrine enemies
enemy_spawn5 = [p2, p3, p8, p20, p28]  #river enemies
enemy_spawn6 = [p2, p4, p7, p13,]  #hill enemies
enemy_spawn7 = [p2, p3, p17, p18, p21, p36]  #mushroom enemies
enemy_spawn8 = [p2, p2, p3, p3, p22]  #Goblin Den
enemy_spawn9 = [p14, p15, p26, p27, p28]  #meadow
enemy_spawn10 = [p14b, p15b] #hive enemies
enemy_spawn11 = [p3, p7, p17, p30, p36] #Rotted woods
enemy_spawn12 = [p18, p26, p29, p31, p32, p33] #Ogre Swamp 1
enemy_spawn13 = [p21, p26, p29, p31, p32, p33] #Ogre Swamp 2
enemy_spawn14 = [p21, p26, p29, p31, p32, p33, p34] #Ogre Swamp 3
enemy_spawn15 = [p4, p6, p9, p13, p15, p18, p36, ] #Misty Woods 1
enemy_spawn16 = [p41, p42, p43, p44, p45 ] #coast enemies
enemy_spawn17 = [p28, p46, p47, p48, p50] #plains enemies
enemy_spawn18 = [p6, p10, p47, p49,] #Foothills 
enemy_spawn19 = [p6, p31, p39, p43, p54,] #West lake
enemy_spawn20 = [p6, p39, p43, p54,] #west river
enemy_spawn21 = [p16b, p22, p37, p38, p55, p57, p60] #fae woods 1
enemy_spawn22 = [p28, p16b, p22, p37, p38, p46, p58, p57, p60, p62] #fae woods 2
enemy_spawn23 = [p43, p54, p63, p64, p65,] #Waterfall cave
enemy_spawn24 = [p6, p66, p67b, p68] #Mountain pass
enemy_spawn25 = [p10, p56, p66, p68, p69, p70, p71, p72,] #Drake Mountains
enemy_spawn26 = [p5, p46, p76] #kobold Special 1 
enemy_spawn27 = [p6, p12b, p77] #kobold Special 2 
enemy_spawn28 = [p47, p78, p79, p80, p81] #Orc Fort 1
enemy_spawn29 = [p78, p79, p80, p81, p83] #Orc Fort 2
enemy_spawn30 = [p62,p76, p115, p115, p83, p83, p100, p100] #Misty woods 
enemy_spawn30b = [p86, p115, p115, p83, p83, p100, p100]
enemy_spawn31 = [p86, p87, p87, p100, p100, p97, p97, p114, p114] #Vampire Castle 1
enemy_spawn32 = [p97, p97, p87, p87, p90, p90, p86] #Vampire Castle 2
enemy_spawn33 = [p89, p89, p100, p99, p99, p99, p97, p98] #Vampire Castle 3
enemy_spawn34 = [p111, p90, p90, p99, p87, p87, p114] #Vampire Castle 4
enemy_spawn35 = [p96, p96, p96, p87, p97, p97, p99, p114] #Vampire Castle 5
enemy_spawn36 = [p66, p107, p102, p104, p106, p109] #Tower 1
enemy_spawn37 = [p102, p101, p108, p108, p112, p103] #Tower 2
enemy_spawn38 = [p113, p105, p104, p110, p108, p102] #Tower 3



