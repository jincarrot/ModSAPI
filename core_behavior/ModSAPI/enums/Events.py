
class ScriptEventSource:
    """
    Describes where the script event originated from.
    """

    Block = "Block"
    """The script event originated from a Block such as a Command Block."""

    Entity = "Entity"
    """The script event originated from an Entity such as a Player, Command Block Minecart or Animation Controller."""

    NPCDialogue = "NPCDialogue"
    """The script event originated from an NPC dialogue."""

    Server = "Server"
    """The script event originated from the server, such as from a runCommand API call or a dedicated server console."""