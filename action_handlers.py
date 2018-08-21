### THIS FILE CONTAINS ACTION HANDLERS FOR YOUR ACTIONS ###

# To add a new action handler, first create a function for your action
#  and then "bind" the handler to your action in the bottom section of the file.

# Note that location handlers run first ... then item handlers ... then action handlers ... and then default behavior

from random import random
from random import choice
from random import randint

def Get(context, item):
    if item["key"] == "ALL":
        context.items.GetAll()
    elif item["key"] in context.player.inventory:
        context.PrintItemInString("You're already carrying @.", item)
    elif (not item.get("takeable?")):
        context.Print("You can't pick that up!")
    else:
        context.items.GetItem(item["key"])

def Drop(context, item):
    if item["key"] == "ALL":
        context.items.DropAll()
    elif not (item["key"] in context.player.inventory):
        context.PrintItemInString("You're not carrying @.", item)
    else:
        context.items.DropItem(item["key"])

def Examine(context, item):
    examine_string = item.get("examine_string")
    if (not examine_string == None) and (len(examine_string) > 0):
        context.Print(examine_string)
    else:
        context.PrintItemInString("You see nothing special about @.", item)

def Read(context, item):
    if item.get("readable?"):
        Examine(context, item)
    else:
        context.Print("You can't read that.")

def Inventory(context):
    context.Print("You are carrying:")
    if len(context.player.inventory) == 0:
        context.Print("  Nothing")
    else:
        for item_key in context.player.inventory:
            context.Print("  a " + context.items.GetLongDescription(item_key))

def Help(context):
    context.Print("This is a text adventure game.")
    context.Print("Enter commands like \'GO NORTH\' or \'TAKE ROCK\' to tell the computer what you would like to do.")
    context.Print("Most commands are either one or two words.")
    context.Print("For a full list of commands, type \'ACTIONS\'.")

def Actions(context):
    print("Available actions:")
    for action_key in sorted(context.actions.actions_dictionary):
        if context.actions[action_key].get("suppress_in_actions_list?"):
            continue

        print_string = "  "
        i = 0
        for word in context.actions.actions_dictionary[action_key]["words"]:
            if i > 0:
                print_string += " / "
            print_string += word
            i += 1
        context.Print(print_string)

def Quit(context):
    context.state.quit_pending = True
    context.Print("Are you sure you want to quit (Y/N)?")

def Restart(context):
    context.state.restart_pending = True
    context.Print("Are you sure you want to restart (Y/N)?")

def Yes(context):
    context.Print("You sound really positive!")

def No(context):
    context.Print("You sound awfully negative!")

def Wait(context):
    context.Print("Time passes...")

def Eat(context, item):
    if item["key"] == "BREAD":
        context.Print("Mmmm. The bread is delicious!")
        context.RemoveItemFromGame("BREAD")

        # Homework assignment 1: replace this print statement with something that actually decreases your hunger level instead of just printing it!
        context.Print("Hunger level is " + str(context.player.hunger))

        # Homework assignment 2: add the "edible?" flag to the items so that you can add other things that can be eaten.
        # Hint: The line 'if item["key"] == "BREAD":' will change to 'if item.get("edible?"):' ... look at how the takeable flag works -- it's similar.
    else:
        context.Print("That doesn't look very appetizing!")

def Attack(context, item):
    if "SWORD" in context.player.inventory:
        context.Print("(With the Elvish Sword)")
    else:
        context.Print("(With your bare hands)")
    context.Print("")

    if item["key"] == "ORC":
        if "SWORD" in context.player.inventory:
            attack_success_strings = ["You slash the orc across the arm.",
                                      "The orc attempts to parry, but your attach is too swift for him.",
                                      "You spin and slash the orc's leg with your elven blade.",
                                      "Your blade rakes across the orc's chest."]
            attack_fail_strings = ["You stab weakly with the sword, but the orc easily parries.",
                                      "Your attack misses the mark.",
                                      "Your blade glances off the orc's chainmail sleeve with a flash of sparks but no other damage.",
                                      "The orc dodges your swing nimbly."]
            attack_rnd = random()
            if attack_rnd > 0.95:
                context.Print("You deliver a massive blow with the elvish blade, and the orc crumples to the floor dead.")
                context.RemoveItemFromGame("ORC")
                context.player.GetPlayerLocation()["items"].append("DEAD_ORC")
                context.ClearItemFlag("ORC","is_alive?")
            elif attack_rnd > 0.5:
                combat_message = choice(attack_success_strings)
                context.items["ORC"]["hp"] = context.items["ORC"]["hp"] - randint(1,40)
                if context.items["ORC"]["hp"] >= 90:
                    combat_message = combat_message + " The orc still looks strong."
                elif context.items["ORC"]["hp"] >= 70:
                    combat_message = combat_message + " The orc now looks weakened but continues to fight."
                elif context.items["ORC"]["hp"] >= 40:
                    combat_message = combat_message + " You've clearly hurt the orc."
                elif context.items["ORC"]["hp"] >= 10:
                    combat_message = combat_message + " The orc looks badly hurt now."
                elif context.items["ORC"]["hp"] > 0:
                    combat_message = combat_message + " The orc is now barely alive."
                else:
                    combat_message = combat_message + " The orc drops to one knee, then collapses dead."
                    context.RemoveItemFromGame("ORC")
                    context.player.GetPlayerLocation()["items"].append("DEAD_ORC")
                    context.ClearItemFlag("ORC","is_alive?")
                context.Print(combat_message)
            elif attack_rnd > 0.03:
                combat_message = choice(attack_fail_strings)
                context.Print(combat_message)
            else:
                context.Print("The orc parries your blow with such force that it knocks you off balance and you drop your sword.")
                MoveItemToPlayerLoc("SWORD")
        else:
            context.Print("You do your best, but your fist just glances off the orc's armor.")
    else:
        context.Print("You need anger management training.")
    return True

# Here is where you "bind" your action handler function to a specific action.
def Register(context):
    actions = context.actions
    actions.AddActionHandler("GET", Get)
    actions.AddActionHandler("DROP", Drop)
    actions.AddActionHandler("EXAMINE", Examine)
    actions.AddActionHandler("READ", Read)
    actions.AddActionHandler("INVENTORY", Inventory)
    actions.AddActionHandler("HELP", Help)
    actions.AddActionHandler("ACTIONS", Actions)
    actions.AddActionHandler("QUIT", Quit)
    actions.AddActionHandler("RESTART", Restart)
    actions.AddActionHandler("YES", Yes)
    actions.AddActionHandler("NO", No)
    actions.AddActionHandler("WAIT", Wait)
    actions.AddActionHandler("EAT", Eat)
    actions.AddActionHandler("ATTACK", Attack)