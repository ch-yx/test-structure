import zipfile
import nbtlib

lists=[]
lists2=[]
f=zipfile.ZipFile("18w50a.jar")
structures=(x for x in f.namelist() if x.startswith("data/minecraft/structures/village"))

l=len("data/minecraft/structures/")
x=0;z=0;maxz=0
for structure in structures:
    lists.append(f'setblock ~{x} ~ ~{z} structure_block{{posX:1,posY:1,posZ:1,showboundingbox: 1b,mode: "LOAD",name:"{structure[l:-4]}"}}\n')
    lists2.append(f"setblock ~{x} ~ ~{z} redstone_block\n")
    x_,_,z_=nbtlib.File.load(f.open(structure),gzipped=1).root["size"]
    x+=x_+1
    maxz=max(maxz,z_)
    if x>100:
        x=0
        z+=maxz+1
        maxz=0
f.close()
file=open ("output.mcfunction","w")
file.writelines(lists)
file.close()

file=open ("output2.mcfunction","w")
file.writelines(lists2)
file.close()
