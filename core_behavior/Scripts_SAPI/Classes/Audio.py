# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
from ..Interfaces.EntityOptions import *
from ..Interfaces.Vector import *

CComp = clientApi.GetEngineCompFactory()

class Audio(object):
    "Contains a set of operations about audio (sounds and musics)"

    def __init__(self, playerId=clientApi.GetLocalPlayerId()):
        self.__id = playerId

    def playSound(self, soundId, soundOptions=PlayerSoundOptions):
        # type: (str, dict) -> None
        """播放音效"""
        if soundOptions == PlayerSoundOptions:
            soundOptions = {}
        if 'location' not in soundOptions:
            pos = CComp.CreatePos(self.__id).GetPos()
            soundOptions['location'] = Vector3({"x": pos[0], "y": pos[1], "z": pos[2]})
        options = PlayerSoundOptions(soundOptions) if type(soundOptions) == dict else soundOptions
        CComp.CreateCustomAudio(clientApi.GetLevelId()).PlayCustomMusic(soundId, options.location.getTuple(), options.volume, options.pitch)

    def playMusic(self, trackId, musicOptions=MusicOptions):
        # type: (str, dict) -> None
        """播放音乐"""
        if musicOptions == MusicOptions:
            musicOptions = {}
        musicOptions = MusicOptions(musicOptions) if type(musicOptions) == dict else musicOptions
        CComp.CreateCustomAudio(clientApi.GetLevelId()).PlayGlobalCustomMusic(trackId, musicOptions.volume, musicOptions.loop)

