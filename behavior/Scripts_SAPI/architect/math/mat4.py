from mod.common.utils.mcmath import Matrix, Vector3
from .vec3 import normalize, dot, cross
import math

def identity():
    return Matrix.Create([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def lookAt(eye, target, up):
    # type: (Vector3, Vector3, Vector3) -> Matrix
    # 右手系：相机看向 -Z 方向
    zaxis = normalize(eye - target).ToTuple()
    xaxis = normalize(Vector3.Cross(up, zaxis)).ToTuple()
    yaxis = cross(zaxis, xaxis).ToTuple()
    return Matrix.Create([
        [xaxis[0], yaxis[0], zaxis[0], 0],
        [xaxis[1], yaxis[1], zaxis[1], 0],
        [xaxis[2], yaxis[2], zaxis[2], 0],
        [-dot(xaxis, eye), -dot(yaxis, eye), -dot(zaxis, eye), 1]
    ])

def perspective(fov, aspect, near, far):
    # type: (float, float, float, float) -> Matrix
    tanHalfFov = math.tan(fov / 2)
    return Matrix.Create([
        [1 / (aspect * tanHalfFov), 0, 0, 0],
        [0, 1 / tanHalfFov, 0, 0],
        [0, 0, -(far + near) / (far - near), -1],
        [0, 0, -2 * far * near / (far - near), 0]
    ])

def multiply(a, b):
    # type: (Matrix, Matrix) -> Matrix
    return Matrix.matrix4_multiply(a, b)

def transpose(m):
    # type: (Matrix) -> Matrix
    return m.Transpose()

def inverse(m):
    # type: (Matrix) -> Matrix
    return m.Inverse()

def translate(v):
    # type: (Vector3) -> Matrix
    x, y, z = v.ToTuple()
    return Matrix.Create([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ])

def rotateAxis(axis, angle):
    # type: (Vector3, float) -> Matrix
    x, y, z = normalize(axis).ToTuple()
    c = math.cos(angle)
    s = math.sin(angle)
    return Matrix.Create([
        [c + (1 - c) * x * x, (1 - c) * x * y - s * z, (1 - c) * x * z + s * y, 0],
        [(1 - c) * x * y + s * z, c + (1 - c) * y * y, (1 - c) * y * z - s * x, 0],
        [(1 - c) * x * z - s * y, (1 - c) * y * z + s * x, c + (1 - c) * z * z, 0],
        [0, 0, 0, 1]
    ])

def rotateX(angle):
    # type: (float) -> Matrix
    c = math.cos(angle)
    s = math.sin(angle)
    return Matrix.Create([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

def rotateY(angle):
    # type: (float) -> Matrix
    c = math.cos(angle)
    s = math.sin(angle)
    return Matrix.Create([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

def rotateZ(angle):
    # type: (float) -> Matrix
    c = math.cos(angle)
    s = math.sin(angle)
    return Matrix.Create([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def rotateXYZ(roll, yaw, pitch):
    # type: (float, float, float) -> Matrix
    # 先Z、再Y、最后X（矩阵乘法从右到左应用）
    """
    右手系摄像机正方向为 -Z 轴
    """
    return rotateZ(roll) * rotateY(yaw) * rotateX(pitch)

def scale(s):
    # type: (Vector3) -> Matrix
    x, y, z = s.ToTuple()
    return Matrix.Create([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])

def transform(m, t, r, s):
    # type: (Matrix, Vector3, Vector3, Vector3) -> Matrix
    """
    标准模型变换矩阵：先缩放(S)，再旋转(R)，最后平移(T)
    旋转顺序：绕Z轴(r.z)、绕Y轴(r.y)、绕X轴(r.x)（右手系，逆时针为正）
    矩阵乘法顺序：M_final = M_parent * T * R * S
    其中 M_parent 为输入矩阵 m（通常为单位矩阵或父节点变换）
    """
    # 注意：rotateXYZ 函数期望参数顺序为 (roll, yaw, pitch)
    # 其中 roll = r.z（绕Z轴）, yaw = r.y（绕Y轴）, pitch = r.x（绕X轴）
    rx, ry, rz = r.ToTuple()
    return m * translate(t) * rotateXYZ(rz, ry, rx) * scale(s)

def transformPoint(m, point):
    # type: (Matrix, Vector3) -> Vector3
    """
    使用矩阵变换一个点（包含平移影响）
    将点表示为齐次坐标 [x, y, z, 1] 并进行矩阵乘法
    返回变换后的 Vector3
    """
    # 手动矩阵-向量乘法
    # 矩阵访问方法：m[row, col]，4x4矩阵，row和col从0到3
    x, y, z = point.ToTuple()
    # 计算齐次坐标结果
    rx = m[0,0]*x + m[0,1]*y + m[0,2]*z + m[0,3]*1
    ry = m[1,0]*x + m[1,1]*y + m[1,2]*z + m[1,3]*1
    rz = m[2,0]*x + m[2,1]*y + m[2,2]*z + m[2,3]*1
    rw = m[3,0]*x + m[3,1]*y + m[3,2]*z + m[3,3]*1
    # 透视除法（如果w不为1）
    if rw != 1 and rw != 0:
        rx /= rw
        ry /= rw
        rz /= rw
    return Vector3(rx, ry, rz)

def transformVector(m, vector):
    # type: (Matrix, Vector3) -> Vector3
    """
    使用矩阵变换一个向量（忽略平移影响）
    将向量表示为齐次坐标 [x, y, z, 0] 并进行矩阵乘法
    返回变换后的 Vector3，适用于法线、方向等
    """
    x, y, z = vector.ToTuple()
    # 忽略平移部分（因为w=0）
    rx = m[0,0]*x + m[0,1]*y + m[0,2]*z
    ry = m[1,0]*x + m[1,1]*y + m[1,2]*z
    rz = m[2,0]*x + m[2,1]*y + m[2,2]*z
    return Vector3(rx, ry, rz)

def localToWorld(modelMatrix, localPoint):
    # type: (Matrix, Vector3) -> Vector3
    """
    将模型局部坐标系中的点转换到世界坐标系
    modelMatrix: 模型到世界的变换矩阵（即模型的世界矩阵）
    localPoint: 在模型局部坐标系中的点
    返回世界坐标系中的点
    """
    return transformPoint(modelMatrix, localPoint)

def worldToLocal(modelMatrix, worldPoint):
    # type: (Matrix, Vector3) -> Vector3
    """
    将世界坐标系中的点转换到模型局部坐标系
    modelMatrix: 模型到世界的变换矩阵（即模型的世界矩阵）
    worldPoint: 在世界坐标系中的点
    返回模型局部坐标系中的点（相对于模型的本地坐标）
    """
    invMatrix = inverse(modelMatrix)
    return transformPoint(invMatrix, worldPoint)

def worldToScreen(modelMatrix, viewMatrix, projectionMatrix, viewport, worldPoint):
    # type: (Matrix, Matrix, Matrix, Vector3, Vector3) -> Vector3
    """
    将世界坐标系中的点转换到屏幕坐标系
    modelMatrix: 模型到世界的变换矩阵（即模型的世界矩阵）
    viewMatrix: 世界到视图的变换矩阵（即摄像机矩阵）
    projectionMatrix: 视图到投影的变换矩阵（即投影矩阵）
    viewport: 屏幕视口（即窗口）
    worldPoint: 在世界坐标系中的点
    返回屏幕坐标系中的点（x, y为屏幕坐标，z为深度值）
    """
    # 先将世界坐标转换到裁剪空间
    mvpMatrix = multiply(projectionMatrix, multiply(viewMatrix, modelMatrix))
    clipPoint = transformPoint(mvpMatrix, worldPoint)
    # 再将裁剪空间坐标转换到屏幕坐标
    screenPoint = Vector3(
        (clipPoint[0] / clipPoint[3] + 1) * 0.5 * viewport[0],
        (1 - (clipPoint[1] / clipPoint[3] + 1) * 0.5) * viewport[1],
        clipPoint[2] / clipPoint[3]
    )
    return screenPoint

def screenToWorld(modelMatrix, viewMatrix, projectionMatrix, viewport, screenPoint, depth):
    # type: (Matrix, Matrix, Matrix, Vector3, Vector3, float) -> Vector3
    """
    将屏幕坐标系中的点转换到世界坐标系
    modelMatrix: 模型到世界的变换矩阵（即模型的世界矩阵）
    viewMatrix: 世界到视图的变换矩阵（即摄像机矩阵）
    projectionMatrix: 视图到投影的变换矩阵（即投影矩阵）
    viewport: 屏幕视口（即窗口）
    screenPoint: 在屏幕坐标系中的点（x, y为屏幕坐标，z为深度值）
    depth: 深度值（从摄像机到点的距离）
    返回世界坐标系中的点
    """
    # 先将屏幕坐标转换到裁剪空间
    clipPoint = Vector3(
        (screenPoint[0] / viewport[0] * 2 - 1) * depth,
        (1 - screenPoint[1] / viewport[1] * 2) * depth,
        depth
    )
    # 再将裁剪空间坐标转换到世界坐标
    invMvpMatrix = inverse(multiply(projectionMatrix, multiply(viewMatrix, modelMatrix)))
    worldPoint = transformPoint(invMvpMatrix, clipPoint)
    return worldPoint
