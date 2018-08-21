# This function is called as the game is starting. Use it to print introduction text.
def IntroText(context):
    context.Print("Welcome adventurer!")
    print()

# This function is called as the game is starting. Use it to initialize game settings
#  like the player's starting location.
def InitialSetup(context):
    context.player.SetPlayerLocation("CASTLE_GATE")
    context.player.hunger = 0

def YouDie(context):
    context.Print("")
    context.Print("*** You have died. ***")
    context.state.restart_confirmed = True
    context.Print("")
    context.Print("Restarting...")
    context.Print("")
    context.Print("")

# Use this function to do anything that happens every single turn (e.g. checking for hunger)
def EveryMoveEvents(context):
    # Handle hunger
    context.player.hunger = context.player.hunger + 1
    hunger = context.player.hunger
    if hunger==60:
        context.Print("")
        context.Print("You're starting to feel a bit hungry.")
    elif hunger==70:
        context.Print("")
        context.Print("You're beginning to feel faint. You'd better eat something soon!")
    elif hunger==90:
        context.Print("")
        context.Print("You're famished. If you don't eat something soon you are done for!")
    elif hunger==105:
        context.Print("")
        context.Print("You black out from hunger. ")
        YouDie(context)