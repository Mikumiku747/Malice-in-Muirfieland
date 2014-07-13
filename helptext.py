general = """Welcome to Malice in muirfiland!
This is version 1.2 of the game.
Use "help credits" to see the credits and "help changelog" for a breif list of
features added since the last version.

Malice in muirfieland is about saving the ruined land of muirfieland from the
clutches of utter boringness. Seriously, this place is a boring old wasteland.
Anyways, you might be able to save muirfieland if you go to a certain spot, but
it won't be easy!

Type "vocab" for a list of commands you can use.
Type "help {word}" to get help for a certain command.
Stuck? Try buying our player's guide! Only $99,999.99! That's less than 100
grand! What a deal! Call now and get a second copy free! Call us now:
0118 999 881 999 119 7253."""

move = """Move action

Usage:
move {direction}

Options:
dirction :== [north, south, east, west, up, down]

Examples:
move west
move down

Aliases:
go, walk, move

Description:
Lets you use your legs, (and arms, and possibly other body parts)
to get around in the world of muirifland. Quite obviously, you can only move in
the six directions listed above. Who knew it would be so easy to learn to walk?"""

exit = """Exit command

Usage:
exit

Examples:
exit

Aliases:
exit, quit

Description:
Quits the game. Are you a quitter? Are you? You better have saved the world (or
at least the game) before you quit, otherwise all is lost (your progress will be
lost) and you'll just be a lousy quitter!"""

look="""Look command

Uasge:
look

Examples:
look

Aliases:
look, observe

Description:
I hope you know what looking is, or you're going to need some serious help when
you go to save muirfieland. (I hope you bought a dictionary!) Looking around
lets you see where you are, how to get out, and if there are any items around.
(Don't ask me how you can tell where you carejust by being there, I don't know?"""

vocab="""Vocabulary command

Usage:
vocab

Examples:
vocab

Aliases:
vocab, commands, vocabulary

Description:
Tells you every word the game knows. If you need help on one of the words, type
"help {word}" and help will come to the rescue!"""

directions = """Directions command

Usage:
directions

Examples:
directions

Aliases:
directions, exits

Description:
Tells you the different directions you can move in to exit this room. Using the
look command also does the same thing as this. Useful if you don't know your way
around muirfieland."""

quiet = """Quiet command

Usage:
quiet

Exmaples:
quiet

Aliases:
quiet, ssh, shh

Description:
This command makes the game less verbose (It talks less). When in quiet mode,
the description will not be shown when you go somewhere, however, you can still
see the name of the area and the exits to it. The description will always be
shown when you go somewhere you've never been before. Opposite of "verbose"."""

verbose = """Verbose command

Usage:
verbose

Examples:
verbose

Aliases:
verbose, loud

Description:
This command makes the game more verbose (It talks more). Every time you move
somewhere, the game tells you about where you have moved to. Opposite of "quiet"."""

save = """Save command

Usage:
save

Examples:
save

Description:
Saves your game so you can quit without losing progress. Use "restore" to get
back to where you were when you last saved. Note tha saving still takes a turn
to do.
WARNING: You can only save the game if you have write-access to where the game
         is being run from, so be careful where you run the game from,
         especially if you are running the game as a python script.
WARNING: The game is saved to save.malice, so if you want to transfer your saved
         game, make sure you move that file along with the game. 
The general idea is don't run the game from C: or on a flash drive, saving may
not work."""


restore = """Restore command

Usage:
restore

Examples:
restore

Aliases:
load, restore

Description:
Loads the game at the point where you last saved. You can't load a game if you
haven't saved yet. Also, the same rules that apply to saving apply to loading
a game, see "help save" for more info."""

examine = """Examine action

Usage:
examine {object}

Options:
object - The name of the object you want to examine

Examples:
examine monkey
examine bin

Description:
Lets you take a closer look at an item. The name of an object is one word, best
describing what the object is. For example, "some stinky debris" is named
"debris", and if you wanted to examine it, you would use "examine debris", not
"examine stinky debris".
Examining items can sometimes reveal hidden things, but it also tells you more
about the item and how heavy it looks. You can also examine things you are
carrying if you want to know more about them and how heavy they are."""

get = """Get action

Usage:
get {object}

Options:
object - The name of the object you want to take

Examples:
take money
take banana

Aliases:
get, take, 'grab'

Description:
Lets you take an object nearby (in this room to be precise). You have to be able
to carry it if you want to take it. You can also only carry 4 items, so keep
that in mind.
The name of an object is one word, best describing what the object is. For
example, "some stinky debris" is named "debris", and if you wanted to take it,
you would use "take debris", not "take stinky debris"."""

drop = """Drop action

Usage:
drop {object}

Options:
object - The name of the object you want to drop

Exmaples:
drop anvil
drop pockets      <--(Wat?)

Alaises:
drop, take

Description:
Lets you drop an item you are currently carrying. You can only drop an item you
are already carrying (I thought that was obvious). To see what items you are
carrying, use "inventory" and to see how much something you are carrying weighs,
use "examine {thing}".
The name of an object is one word, best describing what the object is. For
example, "some stinky debris" is named "debris", and if you wanted to drop it,
you would use "drop debris", instead of "drop stinky debris"."""

inventory = """Inventory command

Usage:
inventory

Examples:
inventory

Alaises:
inventory, items

Description:
Tells all the things you are carrying (if anything at all). If you want find out
more about something you are carrying, use "examine {thing}" and if you want to
drop something, use "drop {thing}". Remember you can only carry 4 things, and
that you can only carry a certain amount of items as well. Manage your items
wisely. """

use = """Use action

Usage:
use {object}

Options:
object - The name of the object you want to drop

Exmaples:
use paper
use rope

Description:
Lets you use an object. Using objects is context-sensitive, so you don't have to
worry about the actualy way of using an item, only that it will be used. Be on
the lookout for good opportunities to use your items, but be careful, some items
are one-time use.
The name of an object is one word, best describing what the object is. For
example, "some stinky debris" is named "debris", and if you wanted to use it,
you would use "use debris", instead of "use stinky debris"."""

help = """[You'd better not type google into google, you'll break the internet!] 

Help command

Usage:
help {topic}
help {word}

Options:
topic :== [version, changelog, credits}
word - A command, use "vocab" for a list of commands

Examples:
help credits
help move

Aliases:
help, ?

Description:
Provides detailed help on different commands, or special information about the
game. Use "vocab" for a list of commands. Great for if you're confused. """
