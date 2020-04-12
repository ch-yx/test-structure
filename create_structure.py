import nbtlib
from nbtlib.tag import *
schema=nbtlib.schema




a_block=schema("block",{"pos":List[Int],"state":Int})

class Properties(Compound):
    def __setitem__(self,key,value):
        if isinstance( value,String):
            return super().__setitem__(key,value)
        return super().__setitem__(key,String(value))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k,v in list(self.items()):
            self[k]=v
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        for k,v in list(self.items()):
            self[k]=v

_Structure = schema('Structure', {
    #'DataVersion': Int,
    #'author': String,
    'size': List[Int],
    'palette': List[schema('State', {
        'Name': String,
        'Properties': Properties,
    })],
    'blocks': List[a_block]
})

class Structure(_Structure):
    def __init__(self):
        self["palette"]=[]
        self["blocks"]=[]
        self["size"]=[1]*3
        super().__init__()
    def add_block(self,id,pos,state={},nbt=None):
        if (pal:={"Name":id,"Properties":state}) in self["palette"]:
            ind=self["palette"].index(pal)
        else:
            self["palette"].append(pal)
            ind=len(self["palette"])-1
        block_data={"pos":pos,"state":ind}
        if nbt is not None:
            block_data["nbt"]=nbtlib.parse_nbt(nbt)
        self["blocks"].append(block_data)

    def final(self,filename):
        return nbtlib.File({"":self},gzipped=True).save(filename=filename)

del _Structure
    
#下面是使用的部分了        
x=Structure()
import math

for i in range(-100,100):
    for j in range(-100,100):
        x.add_block("stone",[i,50*math.sin(0.1*math.dist((0,0),(i,j))),j])

x.add_block("stone",[2,3,4])

x.add_block("chest",[9,9,9],{"waterlogged":"true"},"{Items:[{Slot:1b,Count:1b,id:apple}]}")
for i in range(6):
    x.add_block("chest",[9+i,3,3],{},"{Items:[{Slot:"  +str(i)+ "b,Count:1b,id:apple}]}")
x.final("wave.nbt")
