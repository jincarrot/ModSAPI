import mod.server.extraServerApi as serverApi
from system import systems

ServerSystem = serverApi.GetServerSystemCls()
comp = serverApi.GetEngineCompFactory()

class CoreSystem(ServerSystem):
    
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "GlobalCommandServerEvent", self, self.commandHandler)

    def setScoreboard(self, playerName, objective, score):
        scoreboard = systems.world.getDynamicProperty("scoreboard.%s" % objective)
        if not scoreboard:
            scoreboard = {}
        scoreboard[playerName] = score
        systems.world.setDynamicProperty("scoreboard.%s" % objective, scoreboard)

    def getScoreboard(self, playerName, objective):
        scoreboard = systems.world.getDynamicProperty("scoreboard.%s" % objective)
        if not scoreboard:
            return 0
        return scoreboard.get(playerName, 0)

    def commandHandler(self, data):
        if 'scoreboard' in data['command']:
            """scoreboard players [set | add | remove] <player: target> <objective: string> <count: int>"""
            params = data['command'].split('scoreboard')[1].split(" ")
            del params[0]
            if params[0] == 'players':
                if params[1] in ['set', 'add', 'remove']:
                    objective = params[3]
                    count = int(params[4])
                    if "@" in params[2]:
                        players = comp.CreateEntityComponent(data['entityId']).GetEntitiesBySelector(params[2])
                        for player in players:
                            if params[1] == 'set':
                                self.setScoreboard(player, objective, count)
                            elif params[1] == 'add':
                                self.setScoreboard(player, objective, self.getScoreboard(player, objective) + count)
                            elif params[1] == 'remove':
                                self.setScoreboard(player, objective, self.getScoreboard(player, objective) - count)
                        return
                    player = params[2]
                    if params[1] == 'set':
                        self.setScoreboard(player, objective, count)
                    elif params[1] == 'add':
                        self.setScoreboard(player, objective, self.getScoreboard(player, objective) + count)
                    elif params[1] == 'remove':
                        self.setScoreboard(player, objective, self.getScoreboard(player, objective) - count)
