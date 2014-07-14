#! /bin/python
# -*- coding: cp1252 -*-
print("Malice in muirifeland version 1.2")
print("By Daniel Selmes.")

#-------
#imports
#-------
import json
import math
import copy
import helptext

#-------------------
#adjust input method
#-------------------

from sys import version_info
#adjust input method based on the cersion of python
if version_info[0]<3: 
    input = raw_input #we should shadow input() if neccesary
    print("Python version is less than 3, switching to raw_input mode...")
else:
    print("Warning: Python version 3 or higher.")


#---------
#constants
#---------
    
world = json.load(open('world.json')) #Load in the game world from a JSON file

DIRECTIONS      = ['north', 'south', 'east', 'west', 'up', 'down']
EXIT_COMS       = ['exit', 'quit']
MOVE_COMS       = ['go', 'walk', 'move']
LOOK_COMS       = ['look', 'observe']
VOCAB_COMS      = ['vocab', 'commands', 'vocabulary']
DIRECTIONS_COMS = ['directions', 'exits']
QUIET_COMS      = ['quiet', 'shh', 'ssh']
VERBOSE_COMS    = ['verbose', 'loud']
SAVE_COMS       = ['save']
RESTORE_COMS    = ['restore', 'load']
EXAMINE_COMS    = ['examine']
GET_COMS        = ['get', 'take', 'grab']
DROP_COMS       = ['drop', 'place']
INVENTORY_COMS  = ['inventory', 'items']
USE_COMS        = ['use']
HELP_COMS       = ['help', '?']

inv_weight_limit = 10
inv_items_limit  = 4


#----------------------
#Command list (Dynamic)
#----------------------
COMS = []
for com in EXIT_COMS:
    COMS.append(com)
for com in MOVE_COMS:
    COMS.append(com)
for com in LOOK_COMS:
    COMS.append(com)
for com in VOCAB_COMS:
    COMS.append(com)
for com in DIRECTIONS_COMS:
    COMS.append(com)
for com in QUIET_COMS:
    COMS.append(com)
for com in VERBOSE_COMS:
    COMS.append(com)
for com in SAVE_COMS:
    COMS.append(com)
for com in RESTORE_COMS:
    COMS.append(com)
for com in EXAMINE_COMS:
    COMS.append(com)
for com in GET_COMS:
    COMS.append(com)
for com in DROP_COMS:
    COMS.append(com)
for com in INVENTORY_COMS:
    COMS.append(com)
for com in USE_COMS:
    COMS.append(com)
for com in HELP_COMS:
    COMS.append(com)

#---------
#shortcuts
#---------
    
name = 'name'
description = 'description'
items = 'items'
visible = 'visible'
weight = 'weight'
print_name = 'print name'
north, south, east, west, up, down = 'north', 'south', 'east', 'west', 'up', 'down'
can_go = 0
inventory = []
destination = 1
impass_reason = 2

#----------------
#Player variables
#----------------

location = 1
visited = []
command_list = []
verbose_mode = True

current_event=None

concept_timeleft = 0

#-----------
#Subroutines
#-----------

def checkexits(location): #Checks possible exits, returns string and list
                          #of valid directions
    dirs = "You can go "
    valid_directions = []
    for direction in ('north', 'south', 'east', 'west', 'up', 'down'):
        if world[location][direction][can_go]:
            dirs+=direction+', '
            valid_directions.append(direction)
    dirs = dirs[:-2]+'.'
    if dirs == "You can g.":
        dirs = "You can't see a way out of this place!"
    if dirs == "You can go north, south, east, west, up, down.":
        dirs = "You can go in any direction."
    return dirs, valid_directions

def checkinventory(itemname): #Checks if an item is in the player's inventory
    for item in inventory:
        if item[name] == itemname: return True
    return False

def loseitem(itemname): #Destroys an item in the player's inventory (Moves it to room 0)
    for item in inventory:
        if item[name] == itemname:
            world[0][items].append(inventory.pop(inventory.index(item)))

def itemreference(room, itemname): #Returns a copy of the requested item from the requested room. Read-only.
    for item in world[room][items]:
        if item[name] == itemname:
            return item

#Initial info for the game that the player needs to know
print(
"\nYou open your eyes and find yourself in on of the C Block computer labs ... or, rather, the remnants of it. There are certainly no terminals here, just a pile of debris ... it reminds you of the aftermath of the 1997 Year 12 muck up - the one where they set fire to the electricity transformer causing the entire street to be blacked-out for three days. As you stand up, you start to wonder how you got here ... the stench of decay soon changes that thought to one of getting out...")

print('-'*70)
print(world[location][name])
print(world[location][description])
print(checkexits(location)[0])
visited.append(world[location][name])
print("There are items here.")

#----------------
#main parser loop
#----------------

exitcode = 0
while exitcode==0:
        
    #Check for and set the current event
    #-----------------------------------
    events = {"woke up": location==12, "teleport":location==11 and len(command_list)>0 and command_list[0]=='go' and command_list[1]=='up'} #We need to check the conditions of the events every turn!
    for event in events.keys():
        if events[event]==True:
            current_event=event
    if current_event=="woke up": #Check to see if the player won.
        exitcode=2 #Cause the program to exit next turn
        continue #Skip to the next turn
    if current_event=="teleport":
        print("You are sucked into an interdimensional portal of space-time and are spat out in the C-Block balcony. You seem to be uninjured, but you have a nagging feeling that people shoudln't normally have 14 fingers. Strange...")
        current_event=None
        
    #Handle concept slipperyness
    #---------------------------
    if len(command_list)>=2 and command_list[0] in GET_COMS and command_list[1]=='concept':
        concept_timeleft=9
        print("Got the concept.")
    if checkinventory('concept'):
        concept_timeleft-=1
        #DEBUG: print off how long the player can carry the concept for
        print("The concept is slowly slipping away...")
    if concept_timeleft<=0 and checkinventory('concept'):
        for item in inventory:
            if item[name]=='concept':
                world[10][items].append(inventory.pop(inventory.index(item)))
                print("The concept slips from your grasp. Darn.")
    
    #Get player input and process
    #----------------------------
    command_str = input("> ").lower() #Get the input
    if command_str == '': #Fix the bug handling no input
        command_str = "What do you want me to do"
    command_list = command_str.split() #Split into commands
    
    #Handle each of the commands
    #---------------------------
    if command_list[0] in EXIT_COMS:
        exitcode = 1 #Cause the program to exit next turn
        continue #Skip to next turn
    elif command_list[0] in MOVE_COMS:
        if len(command_list)>1 and (command_list[1] in DIRECTIONS):
            if world[location][command_list[1]][can_go]:
                print("You go {}.".format(command_list[1]))
                location = world[location][command_list[1]][destination]
                #print off room name
                print('-'*70)
                print(world[location][name])
                #Check if We've been here before
                if not world[location][name] in visited: #A new place
                    visited.append(world[location][name])
                    print(world[location][description])
                    print(checkexits(location)[0])
                    if world[location][items]: print("There's some things here as well.")
                else: #We have been here
                    if verbose_mode:
                        print(world[location][description])
                        print(checkexits(location)[0])
            else:
                if world[location][command_list[1]][impass_reason]:
                    print("You can't go {}: {}".format(command_list[1], world[location][command_list[1]][impass_reason]))
                else:
                    print("You can't go {}.".format(command_list[1]))
        elif len(command_list)>1:
            print("Sorry, I can't {}".format(command_str))
        else:
            print("Please tell me more�")
    elif command_list[0] in LOOK_COMS:
        print('-'*70)
        print(world[location][name])
        print(world[location][description])
        print(checkexits(location)[0])
        itemlist = ""
        for item in world[location][items]:
            if item[visible]:
                itemlist += item[print_name]
                itemlist += ", "
        if not itemlist == "":
            print("You can see "+itemlist[:-2]+'.')
    elif command_list[0] in VOCAB_COMS:
        printoff = ""
        comnum = 0
        #print("COM: "+str(COMS)) #DEBUG: Prints off commands
        for command in COMS:
            if comnum>4:
                printoff+="\n"
                comnum = 0
            printoff+=command+", "
            comnum+=1
        print("Commands:\n"+printoff[:-2])
    elif command_list[0] in DIRECTIONS_COMS:
        print(checkexits(location)[0])
    elif command_list[0] in QUIET_COMS:
        verbose_mode=False
        print("Verbose mode disabled.")
    elif command_list[0] in VERBOSE_COMS:
        verbose_mode=True
        print("Verbose mode enabled.")
    elif command_list[0] in SAVE_COMS:
        #Assemble a dictionary of the variables we need to save
        print("Assembling save data...")
        data = {}
        data["location" ] = copy.deepcopy(location)
        data["visited"  ] = visited
        data["verbose"  ] = verbose_mode
        data["c event"  ] = current_event
        data["inventory"] = inventory
        data["concepttm"] = concept_timeleft
        print("Assembling world save data...")
        data["world"    ] = world


    ##    print("Data to be saved:\n")
    ##    print(json.dumps(data)+"\n")
        
        #Save to save.malice
        print("Saving game to save.malice. Please wait...")
        try:
            with open("save.malice", mode='w') as state:
                json.dump(data, state)
        except Exception as err:
            print("Save failed: "+str(err))
        else:
            print("Saved successfully!")

    elif command_list[0] in RESTORE_COMS:
        #Assemble a dictionary to load into
        data = {}
        #load into it from the file
        try:
            with open("save.malice", mode='r') as state:
                data = json.load(state)
        except Exception as err:
            print("Falied to load file: "+str(err))
        else:
            print("Loaded save file, unpacking data...")
        location         = data["location" ]
        visited          = data["visited"  ]
        verbose_mode     = data["verbose"  ]
        current_event    = data["c event"  ]
        inventory        = data["inventory"]
        concept_timeleft = data["concepttm"]
        print("Loading world...")
        world         = data["world"]
        print("Successfully loaded game")

    elif command_list[0] in GET_COMS:
        if len(command_list)>1:
            #Check if the item is there and obtain it's index
            item_here = None
            item_index = None
            for item in world[location][items]:
                if item[name] == command_list[1]: #check if the name matches the name the player asked for
                    item_here = True              #and get it's index in the room, for use with the rest of the function
                    item_index = world[location][items].index(item)
                    break
                else:
                    item_here = False
            if item_here and world[location][items][item_index][visible]: #if it is here and visible...
                playerweight = 0
                for item in inventory:
                    playerweight += item[weight]
                if playerweight+world[location][items][item_index][weight]<=inv_weight_limit: #and it's not too heavy to carry
                    if len(inventory)<=inv_items_limit:
                        print("Da da da daaaa! You got {}.".format(world[location][items][item_index][print_name])) #YOU GOT THE THIIIIING!
                        inventory.append(world[location][items].pop(item_index)) #move it into our inventory
                    else:
                        print("You would take the {}, but you can only carry {} items!".format(world[location][items][item_index][name], inv_items_limit))
                elif world[location][items][item_index][weight]==100:
                    print("There's no way you could ever take the {}! Are you crazy?".format(command_list[1]))
                else:
                    print("You would take the {}, but you can't carry it!".format(world[location][items][item_index][name]))
            else:
                print("You don't see a {} that you could take...".format(command_list[1]))
                for item in inventory:
                    if item[name]==command_list[1]: #if they already have it, let them know!
                        print("But you already have one, so let's not be greedy!")
        else:
            print("What are you trying to take?")

    elif command_list[0] in EXAMINE_COMS:
        if len(command_list)>1:
            #Check if the item is there and obtain it's index
            item_here = None
            item_index = None
            for item in world[location][items]:
                if item[name] == command_list[1]: #check if the name matches the name the player asked for
                    item_here = "room"            #and get it's index in the room, for use with the rest of the function
                    item_index = world[location][items].index(item)
                    break
                else:
                    item_here = False
            if not item_here: #if it wasn't in the room search for it in the inventory
                for item in inventory:
                    if item[name] == command_list[1]: #check if the name matches the name the player asked for
                        item_here = "inventory"       #and get it's index in the room, for use with the rest of the function
                        item_index = inventory.index(item)
                        break
                    else:
                        item_here = False
            if item_here == "room" and world[location][items][item_index][visible]: #If in the room
                print(world[location][items][item_index][description]) #Show the description
                if world[location][items][item_index][weight]<4:
                    print("The {} looks pretty light.".format(world[location][items][item_index][name]))
                elif world[location][items][item_index][weight]<8:
                    print("The {} looks kinda heavy.".format(world[location][items][item_index][name]))
                elif world[location][items][item_index][weight]<10:
                    print("The {} looks is VERY heavy.".format(world[location][items][item_index][name]))
                elif world[location][items][item_index][weight]<11:
                    print("The {} looks is VERY heavy, you could probably only JUST carry it.".format(world[location][items][item_index][name]))
                else:
                    print("The {} looks way to heavy to take with you.".format(world[location][items][item_index][name]))
            elif item_here == "inventory" and inventory[item_index][visible]:#if in the inventory
                print(inventory[item_index][description]) #Show the description
                if inventory[item_index][weight]<4:
                    print("The {} feels pretty light.".format(inventory[item_index][name]))
                elif inventory[item_index][weight]<8:
                    print("The {} feels kinda heavy.".format(inventory[item_index][name]))
                elif inventory[item_index][weight]<10:
                    print("The {} feels is VERY heavy.".format(inventory[item_index][name]))
                elif inventory[item_index][weight]<11:
                    print("The {} feels is VERY heavy, you could probably only JUST carry it.".format(inventory[item_index][name]))
                else:
                    print("The {} is supposed to be Immovable, how come you have it?.".format(inventory[item_index][name]))
            #Reveal the abacus if the debris is examined        
            if command_list[1]=='debris' and location==1 and not(itemreference(1, 'abacus')==None) and not(itemreference(1, 'abacus')[visible]):
                world[1][items][world[1][items].index(itemreference(1, 'abacus'))][visible]=True
                print("You find an abacus - just what you've always wanted!")
            #Reveal the keyboard if the dumpster is examined        
            if command_list[1]=='dumpster' and location==6 and not(itemreference(6, 'keyboard')==None) and not(itemreference(6, 'keyboard')[visible]):
                world[6][items][world[6][items].index(itemreference(6, 'keyboard'))][visible]=True
                print("You see a keyboard wedged deep inside the dumpster.")
        else:
            print("What are you trying to examine?")
    elif command_list[0] in DROP_COMS:
        if len(command_list)>1:
            if command_list[1]=="pockets": print("Hahahahaha, you dropped your pockets, a winner is you. But seriously...")
            dropped = False
            for item in inventory:
                if item[name] == command_list[1]:
                    print(item[name][0].upper()+item[name][1:]+" dropped.")
                    world[location][items].append(inventory.pop(inventory.index(item)))
                    dropped = True
                    break
                else:
                    dropped = False
            if not dropped:
                print("You don't seem to be carrying a {}.".format(command_list[1]))
        else:
            print("What are you trying to drop?")
    
    elif command_list[0] in INVENTORY_COMS:
        outstring = "Inventory: "
        if inventory == []:
            outstring+="Nothing to speak of."
        else:
            for item in inventory:
                outstring+=item[print_name]
                outstring+=", "
                outstring = str(outstring)[:-2]+'.'
        print(outstring)

    elif command_list[0] in USE_COMS:
        if command_list[1]=='abacus' and checkinventory('abacus') and location==5:
            print("(In the box) From the box, four singing swedes emerge with a round-eyed arboreal marsupial (named Fernando). They all wander off towards the hall, singing 'When I kissed the teacher ...'. That's a little odd, you think.")
            loseitem('abacus')
        elif command_list[1]=='cipher' and checkinventory('cipher') and location==5:
            print("(In the box) The box emits an audible sigh and a few strands of animal fur ... strange.")
            loseitem('cipher')
        elif command_list[1]=='floppy' and checkinventory('floppy') and location==5:
            print("(In the box) The box emits a faint whirring sound� followed by several loud scratching and screeching sounds. The box emits an enormous 'CLUNK' and the floppy shoots out of the box and sails across the Quad.")
            loseitem('floppy')
            for item in inventory:
                if item[name]=='floppy':
                    inventory
        elif command_list[1]=='keyboard' and checkinventory('keyboard') and location==5:
            print("(In the box) You hear some faint digestive sounds taking place from within the box. Suddenly a vigorous belching action disgorges two objects, a key and a board.")
            loseitem('keyboard')
            world[5][items][world[5][items].index(itemreference(5, 'key'))][visible]=True #Reveal the key and board
            world[5][items][world[5][items].index(itemreference(5, 'board'))][visible]=True
        elif command_list[1]=='board' and checkinventory('board') and location==5:
            print("(In the box) You reach down to place the board into the box but are startled by a hand which is emerging. The Librarian climbs out and begins hassling you about an overdue book. With a deft hand and a graceful kick,� you slide the board into the Librarian's mouth and knock her back into the box.")
            loseitem('board')
        elif command_list[1]=='concept' and checkinventory('concept') and location==6 and itemreference(6, 'keyboard')[visible]:
            print("(On keyboard and dumpster) The keyboard seems a lot easier to move now.")
            loseitem('concept')
            world[6][items][world[6][items].index(itemreference(6, 'keyboard'))][weight]=2 #make the keyboard moveable, update description
            world[6][items][world[6][items].index(itemreference(6, 'keyboard'))][print_name]="a broken keyboard"
        elif command_list[1]=='key' and checkinventory('key') and location==6:
            world[6]['east'][0]=True
            world[6]['east'][2]="The door is now unlocked."
            print("You hear a click, and the door unlocks. You open it as well, just to make sure it's fully unlocked.")
        else:
            print("That doesn't appear to do anything useful.")
    elif command_list[0] in HELP_COMS:
        if len(command_list)<2:
            print(helptext.general)
        elif command_list[1] in MOVE_COMS: print(helptext.move)
        elif command_list[1] in LOOK_COMS: print(helptext.look)
        elif command_list[1] in EXIT_COMS: print(helptext.exit)
        elif command_list[1] in VOCAB_COMS: print(helptext.vocab)
        elif command_list[1] in DIRECTIONS_COMS: print(helptext.directions)
        elif command_list[1] in QUIET_COMS: print(helptext.quiet)
        elif command_list[1] in VERBOSE_COMS: print(helptext.verbose)
        elif command_list[1] in SAVE_COMS: print(helptext.save)
        elif command_list[1] in RESTORE_COMS: print(helptext.restore)
        elif command_list[1] in EXAMINE_COMS: print(helptext.examine)
        elif command_list[1] in GET_COMS: print(helptext.get)
        elif command_list[1] in DROP_COMS: print(helptext.drop)
        elif command_list[1] in INVENTORY_COMS: print(helptext.inventory)
        elif command_list[1] in USE_COMS: print(helptext.use)
        elif command_list[1] in HELP_COMS: print(helptext.help)
        elif command_list[1] == 'changelog': print(helptext.changes)
        elif command_list[1] == 'version': print(helptext.version)
        elif command_list[1] == 'credits': print(helptext.credits)

    else:
        print("Huh? {}?".format(command_str))

if exitcode == 1:
    print("OK ... but a small part of you may never leave until you have personally saved Muirfieland from the clutches of evil .. Bwahahahahahah (sinister laugh) ...")
    input("Press enter to quit.")

if exitcode == 2:
    print("Everything begins to shake and a white light envelopes the entire world. A voice is calling out to you; 'Wake up sleepy head.' You wake up in a fit of sweat in the middle of school, and the class is having a chuckle at 'sleepyhead'. They soon go back to thier normal shenanigans.")
    print("Was it all really just a dream ? Or, are you dreaming now Neo ... Who cares ! Somehow the experience has given you the answer you needed to finish your last programming assignment for the year. That means a well-earned rest is imminent. Or possibly some free time to write that adventure game you always wanted to write.")
    print("Congratulations, you have saved muirfieland... somehow. Anyway, well done, the place inside your head is peaceful oncemore. Good thing you ... uh, did that thing... anyways. Good job!")
    input("Press enter to quit.")
