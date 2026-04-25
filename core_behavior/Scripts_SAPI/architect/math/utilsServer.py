from .mat4 import identity, inverse, transformPoint, transform
from ..math.vec3 import vec, add, div, normalize
from ..level.server import LevelServer
from ..basic import compServer, serverApi, defaultFilters

import math


def pointInBox(point, box):
    # type: (tuple[float, float, float], tuple[float, float, float]) -> bool
    # box 参数是盒子的全尺寸 (width, height, depth)
    # 假设盒子以原点为中心，范围从 -size/2 到 size/2
    size = box
    half_x = size[0] / 2
    half_y = size[1] / 2
    half_z = size[2] / 2
    return -half_x <= point[0] <= half_x and -half_y <= point[1] <= half_y and -half_z <= point[2] <= half_z


def boxOverlap3dServer(pos, rot, size, dim):
    # type: (tuple[float, float, float], tuple[float, float, float], tuple[float, float, float], int) -> list[str]
    radius = math.ceil(math.sqrt(size[0] ** 2 + size[2] ** 2))
    x, y, z = pos
    xozProjStart = (
        x - radius,
        y - radius,
        z - radius
    )
    xozProjEnd = (
        x + radius,
        y + radius,
        z + radius
    )
    firstFind = LevelServer.game.GetEntitiesInSquareArea(None, xozProjStart, xozProjEnd, dim)
    worldMatrix = inverse(transform(
        identity(),
        vec(pos),
        vec(rot),
        vec(size)
    ))
    result = []
    for entityId in firstFind:
        posComp = compServer.CreatePos(entityId)
        centerPos = div(add(vec(posComp.GetPos()), vec(posComp.GetFootPos())), 2)
        modelCenterPos = transformPoint(worldMatrix, centerPos)
        if pointInBox(modelCenterPos, size):
            result.append(entityId)

    return result


def boxOverlap3dForward(entityId, size):
    length = size[2]
    pos = compServer.CreatePos(entityId).GetPos()
    rot = compServer.CreateRot(entityId).GetRot()
    dim = compServer.CreateDimension(entityId).GetEntityDimensionId()
    dir = serverApi.GetDirFromRot(rot)
    result = boxOverlap3dServer(
        add(vec(pos), vec(dir) * (length / 2)).ToTuple(),
        (rot[0], rot[1], 0), size, dim,
    )
    result.remove(entityId)
    return result


def facing(entityId):
    dir = serverApi.GetDirFromRot(compServer.CreateRot(entityId).GetRot())
    return vec(dir)


def forward(entityId):
    x, _, z = serverApi.GetDirFromRot(compServer.CreateRot(entityId).GetRot())
    return normalize(vec((x, 0, z)))