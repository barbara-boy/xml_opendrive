try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

    
class Road:
    id = ""
    junction_id = ""
    length = 0.0
    link = 0
    reference_line = []
    reference_line_points = []
    type = []
    road_sections = []

class Lane:
    road_id = "NONE"    	#车道所属的道路ID
    road_section = "NONE"	#车道所属的道路段ID
    id = "NONE"            	#车道的本地ID
    predecessor_id = "NONE" #车道连接—前驱
    successor_id = "NONE"   #车道连接—后继
    type = ""               #车道类型
    lane_change = ""        #允许的变道类型
    width = []              #车道宽度参数
    center_line_points = []	# 车道中心线离散坐标点（计算获得）
    length = 0.0          	# 车道长度

class Junction:
    id = ""
    connection = []
    pass
class MXYZ:
    pass
class MSLZ:
    pass

data = open("borregasave.xodr").read()
root = ET.fromstring(data) 
print(root.tag,root.attrib)
for child in root:
    print(child.tag,child.attrib)