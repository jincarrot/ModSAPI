import mod.client.extraClientApi as clientApi
compClient = clientApi.GetEngineCompFactory()

class LevelClient:
    def __init__(self):
        levelId = clientApi.GetLevelId()
        localPlayerId = clientApi.GetLocalPlayerId()

        self.levelId = levelId
        self.localPlayerId = localPlayerId

        self.localPlayer = compClient.CreatePlayer(levelId)
        self.achievement = compClient.CreateAchievement(levelId)
        self.actorRender = compClient.CreateActorRender(levelId)
        self.biome = compClient.CreateBiome(levelId)
        self.block = compClient.CreateBlock(levelId)
        self.blockGeometry = compClient.CreateBlockGeometry(levelId)
        self.blockInfo = compClient.CreateBlockInfo(levelId)
        self.blockUseEventWhiteList = compClient.CreateBlockUseEventWhiteList(levelId)
        self.camera = compClient.CreateCamera(levelId)
        self.chunkSource = compClient.CreateChunkSource(levelId)
        self.configClient = compClient.CreateConfigClient(levelId)
        self.customAudio = compClient.CreateCustomAudio(levelId)
        self.dimension = compClient.CreateDimension(levelId)
        self.drawing = compClient.CreateDrawing(levelId)
        self.fog = compClient.CreateFog(levelId)
        self.game = compClient.CreateGame(levelId)
        self.model = compClient.CreateModel(levelId)
        self.neteaseShop = compClient.CreateNeteaseShop(levelId)
        self.operation = compClient.CreateOperation(levelId)
        self.playerView = compClient.CreatePlayerView(levelId)
        self.postProcess = compClient.CreatePostProcess(levelId)
        self.recipe = compClient.CreateRecipe(levelId)
        self.skyRender = compClient.CreateSkyRender(levelId)
        self.textBoard = compClient.CreateTextBoard(levelId)
        self.textNotify = compClient.CreateTextNotifyClient(levelId)
        self.virtualWorld = compClient.CreateVirtualWorld(levelId)

    @staticmethod
    def getInst():
        if not hasattr(LevelClient, '_inst'):
            LevelClient._inst = LevelClient()
        return LevelClient._inst