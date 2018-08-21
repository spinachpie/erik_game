### THIS FILE CONTAINS ACTION HANDLERS FOR YOUR ITEMS ###

# To add a new item handler, first create a function for your item
#  and then "bind" the handler to your item in the bottom section of the file.

# Note that location handlers run first ... then item handlers ... then action handlers ... and then default behavior
# Return TRUE to say "I've handled the user's input here, no need to run the action handler + default logic."
#  ... and return FALSE to say "I did NOT handle the input here, so try the action handler or default logic."

def Rock(context, action):
    if action["key"] == "EAT":
        context.Print("Didn't your mother ever warn you not to eat rocks?")
        return True
    return False

def DeadOrc(context, action):
    if ((action["key"] == "EXAMINE") or (action["key"] == "SEARCH")) and not context.CheckItemFlag("SCROLL","seen?"):
        context.SetItemFlag("SCROLL","seen?")
        context.Print("You rummage through the orc's body and find a crumpled scroll in his pocket. You take it.")
        context.MoveItemToInventory("SCROLL")
        return True
    return False

# Here is where you "bind" your item handler function to a specific item.
def Register(context):
    items = context.items
    items.AddItemHandler("ROCK", Rock)
    items.AddItemHandler("DEAD_ORC", DeadOrc)