try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from math import sin,cos,atan2
from os import X_OK

class Geometry:
    """用来存储道路中心线的几何形状及参数\n
        type : 几何形状，一般为 line 或 paramPoly3\n

    """
    type = "" #几何形状
    s = 0.0 #起始位置的s坐标(参考线坐标系)
    x = 0.0 #起始位置(x 惯性)
    y = 0.0 #起始位置(y 惯性)
    hdg = 0.0 #起始方向 (惯性航向角/偏航角)
    length = 0.0 #元素的参考线长度(参考线坐标系)

    def __init__(self,type,s,x,y,hdg,length,paramPoly3) -> None:
        self.type = type 
        self.s = s
        self.x = x
        self.y = y
        self.hdg = hdg
        self.length = length
        if(self.type == "paramPoly3"): #如果形状是参数形式的三次多项式
            self.paramPoly3 = paramPoly3
        
# a = Geometry(1,1,1,1,1,1,None) 
# print(a.paramPoly3)
class Point():
    """坐标点\n
        x ： 横坐标\n
        y ： 纵坐标\n
        hdg ： 航向角\n
        s : 
    """
    def __init__(self,x,y,hdg,s) -> None:
        self.x = x
        self.x = y
        self.hdg = hdg
        self.s = s
def LocalToGlobal(origin,local):
    """局部坐标转换为全局坐标,返回当前坐标的全局坐标\n
        origin : 局部坐标的原点的全局坐标\n
        local ： 局部坐标\n
    """
    #这块应该不对
    return Point(local.x + origin.x,local.y + origin.y, local.hdg + origin.hdg,0)


class Road:
    """Road
    """
    id = "" #道路ID
    junction_id = "" #道路所属的交叉口ID
    length = 0.0 #道路长度
    link = 0  #道路连接
    reference_line = [] #道路中心线的几何形状，存储Geometry
    reference_line_points = [] #道路中心线离散坐标点（计算获得）
    type = [] #道路类型
    road_sections = [] #道路段
    def __init__(self) -> None:
        self.ParseToDiscretePoints()
        pass
    def ParseToDiscretePoints(self):
        """解析成离散点
        """
        for geometry in self.reference_line: #遍历道路中心线
            
            if(geometry.type == "line"):
                #如果是直线
                s = 0.0
                delta_s = 0.2 #△s，采样间隔
                sample_num = int(geometry.length / delta_s) #采样的点数
                for i in range(0,sample_num+1): #最末端也要
                    x = geometry.x + delta_s * i * cos(geometry.hdg)
                    y = geometry.y + delta_s * i * sin(geometry.hdg)
                    self.reference_line_points.append(Point(x,y,geometry.hdg,s))
                    s += delta_s
            elif(geometry.type == "paramPoly3"):
                #如果是参数的三次多项式
                paramPoly3 = geometry.paramPoly3
                delta_s = 0.2 #△s，采样间隔
                sample_num = int(geometry.length / delta_s) #采样的点数
                delta_normalize_s = 1.0 / sample_num

                for i in range(0,sample_num+1): #最末端也要
                    t = delta_normalize_s * i
                    u = paramPoly3.aU + paramPoly3.bU * t + paramPoly3.cU * t * t + paramPoly3.dU * t * t * t
                    v = paramPoly3.aV + paramPoly3.bV * t + paramPoly3.cV * t * t + paramPoly3.dV * t * t * t
                    du_dt = paramPoly3.bU + 2 * paramPoly3.cU * t + 3 * paramPoly3.dU * t * t
                    dv_dt = paramPoly3.bV + 2 * paramPoly3.cV * t + 3 * paramPoly3.dV * t * t
                    hdg = atan2(dv_dt, du_dt) #通过一阶导数求朝向角
                    origin = Point(geometry.x,geometry.y,geometry.hdg,0)
                    local = Point(u,v,hdg,0)
                    self.reference_line_points.append(Point(LocalToGlobal(origin,local)))
                    s += delta_s


class Lane:
    road_id = "NONE" #车道所属的道路ID
    road_section = "NONE"#车道所属的道路段ID
    id = "NONE" #车道的本地ID
    predecessor_id = "NONE" #车道连接—前驱
    successor_id = "NONE" #车道连接—后继
    type = "" #车道类型
    lane_change = "" #允许的变道类型
    width = [] #车道宽度参数
    center_line_points = []	# 车道中心线离散坐标点（计算获得）
    length = 0.0 # 车道长度

class Junction:
    id = "" #交叉口ID
    connection = [] #交叉口内的道路连接



class MXYZ:
    """笛卡尔空间XYZ坐标系下表示的位置
    """
    x = 0.0
    y = 0.0
    z = 0.0
    def __init__(self,x,y,z) -> None:
        self.x = x
        self.y = y
        self.z = z

class MSLZ:
    """基于道路参考线的Frenet坐标系下表示的位置
    """
    lane_uid = 0 #
    s = 0
    l = 0.0
    z = 0.0
    def __init__(self,lane_uid,s,l,z) -> None:
        self.lane_uid = lane_uid
        self.s = s
        self.l = l
        self.z = z

#估计用不上
class Poly3:
    """三次多项式
    """
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
class ParamPoly3:
    """参数形式的三次多项式
    """
    aU = 0.0
    bU = 0.0
    cU = 0.0
    dU = 0.0
    aV = 0.0
    bV = 0.0
    cV = 0.0
    dV = 0.0

def FineNextRoad(road_node):
    pass

data = open("borregasave.xodr").read()
root = ET.fromstring(data) 
print(root.tag,root.attrib)
for child in root:
    print(child.tag,child.attrib)
    #print(type(child))