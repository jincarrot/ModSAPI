# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ...interfaces.EntityOptions import *
from ...interfaces.Vector import *

CComp = clientApi.GetEngineCompFactory()

class Audio:
    "Contains a set of operations about audio (sounds and musics)"

    def playSound(self, soundId, soundOptions=PlayerSoundOptions):
        # type: (str, dict) -> None
        """播放音效"""

    def playMusic(self, trackId, musicOptions=MusicOptions):
        # type: (str, dict) -> None
        """播放音乐"""

