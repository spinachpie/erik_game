### THIS FILE CONTAINS HANDLERS FOR YOUR LOCATIONS ###

# There are two types of location handlers:
#   * An "ENTER" HANDLER is called whenever the player enters that location.
#   * A "WHEN HERE" HANDLER is called whenever the player does anything at that location

# Note that location handlers run first ... then item handlers ... then action handlers ... and then default behavior
# For either type of handler, return TRUE to bypass the other handler logic that would otherwise run
#  ...and return FALSE if you want the regular handler logic to do its thing.

# To add a new location handler, first create a function for your item
#  and then "bind" the handler to your item in the bottom section of the file.
# When you bind, make sure you choose the right Add function, depending on whether
#  you are adding an enter handler or when-here handler.

from random import random
from random import choice
from random import randint

### LOCATION HANDLERS (must bind each handler in the Register() function below

def EnterLookoutWalkway(context, first_time):
    if first_time:
        context.events.PrintBelow("You hear a faint moan coming from the tower to the south.")
        context.events.PrintStringInNMoves("You hear that moaning sound again.", 3)
        context.events.CreateEventInNMoves(GhostlyVisitEvent, 6)
    return False

def EnterCellblock2(context, first_time):
    if first_time:
        context.events.PrintBelow("An orc emerges from a shadowy cell and rushes at you with a whooping war cry!")
        context.events.CreateEventInNMoves(OrcAction, 1)

### EVENT FUNCTIONS (complex events can be created using event functions, which DO NOT need to be registered like handlers
#     These events are typically queued up using context.events.CreateEventInNMoves(MyNewEvent, N)

def GhostlyVisitEvent(context):
    context.Print("")
    context.Print("A ghostly, glowing apparition passes through the room and the chill makes you shudder. A moment later it vanishes, leaving behind a ghostly doll.")
    context.MoveItemToPlayerLoc("DOLL")

def OrcAction(context):
    if context.CheckItemFlag("ORC","is_alive?"):
        context.ClearItemFlag("ORC","do_not_list?")
        context.Print("")

        # If the orc is in the same room as the player, then the orc will attack the player...
        if context.ItemIsHere("ORC"):
            attack_success_strings = ["The orc jabs you with his spear, knocking you backward in pain.",
                                      "With a hideous scream, the orc drives his spear into your shoulder.",
                                      "The orc attacks, grazing your chin with the butt of his spear.",
                                      "The orc thrusts his spear into your legs and you wince in pain."]
            attack_fail_strings = ["The orc aims his spear for your head, but you duck out of the way.",
                                      "The orc attacks with his spear, but you block it just in time.",
                                      "With a shriek, the orc jabs his spear at your chest but you manage to dodge.",
                                      "The orc pokes you feebly but it does no damage."]
            attack_rnd = random()
            if attack_rnd > 0.6:
                combat_message = choice(attack_success_strings)
                context.player.hp = context.player.hp - randint(1,30)
                if context.player.hp >= 90:
                    combat_message = combat_message + " You are wounded but not badly."
                elif context.player.hp >= 70:
                    combat_message = combat_message + " You feel weakened by your wounds."
                elif context.player.hp >= 40:
                    combat_message = combat_message + " Your wounds have left you very weak."
                elif context.player.hp >= 10:
                    combat_message = combat_message + " You are badly hurt."
                elif context.player.hp > 0:
                    combat_message = combat_message + " You are barely alive. Somewhere close by, you hear a harp playing."
                else:
                    combat_message = combat_message + " The blow finishes you off."
                context.Print(combat_message)
                if context.player.hp <= 0:
                    context.player.YouDie()
            else:
                combat_message = choice(attack_fail_strings)
                context.Print(combat_message)

        # Otherwise, he follows you into the room
        else:
            follow_strings = ["The orc follows you. He's right on your heels!",
                                      "Screaming in anger, the orc runs after you!",
                                      "You can hear the orc's footsteps right behind you!",
                                      "The orc is following you and gaining ground!"]
            context.Print(choice(follow_strings))
            context.MoveItemToPlayerLoc("ORC")
        context.events.CreateEventInNMoves(OrcAction, 1)

### Here is where you "bind" your item handler function to a specific item.
#     Again, only location handlers get bound here ... event functions don't need to be bound.
def Register(context):
    locations = context.locations
    locations.AddEnterHandler("LOOKOUT_WALKWAY", EnterLookoutWalkway)
    locations.AddEnterHandler("CELLBLOCK_2", EnterCellblock2)