from .mat4 import worldToScreen, identity, lookAt, perspective, screenToWorld
from ..math.vec3 import vec, modulo, Vector3
from ..level.client import LevelClient

level = LevelClient.getInst()
screenWidth, screenHeight = level.game.GetScreenSize()

def localViewMatrix():
    camPos = level.camera.GetPosition()
    camForward = level.camera.GetForward()
    target = (
        camPos[0] + camForward[0],
        camPos[1] + camForward[1],
        camPos[2] + camForward[2]
    )
    return lookAt(
        vec(camPos),
        vec(target),
        vec((0, 1, 0))
    )

def localProjectionMatrix():
    return perspective(
        level.camera.GetFov(),
        screenWidth / screenHeight,
        0.1,
        100
    )

def worldPosToScreenPos(worldPoint):
    # type: (tuple[float, float, float]) -> Vector3
    mMat = identity()
    vMat = localViewMatrix()
    pMat = localProjectionMatrix()
    return worldToScreen(
        mMat, vMat, pMat,
        (screenWidth, screenHeight),
        vec(worldPoint)
    )

def screenPosToWorldPos(screenPoint, depth):
    # type: (tuple[float, float], float) -> Vector3
    mMat = identity()
    vMat = localViewMatrix()
    pMat = localProjectionMatrix()
    pointVec = vec((screenPoint[0], screenPoint[1], 0))
    return screenToWorld(
        mMat, vMat, pMat,
        (screenWidth, screenHeight),
        pointVec,
        depth
    )