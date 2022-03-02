import os
import re
fecha = os.popen("date +%d --date=\"2 day ago\"").read()
fechaa = [int(s) for s in re.findall(r'-?\d+\.?\d*', fecha)]
file = str(fechaa[0])
print(file)
f = open(file,"r")
mensaje = f.readlines()
f.close()
f = open(file,"w")
for x in mensaje:
    if "Moved file:" in x:
        f.write(x)
f.close
f = open(file,"r")
mensaje = f.readlines()
for z in mensaje:
    cut = z.split("Moved file: from")
    borrar = cut[1]
    #print(f"rm -rf{borrar}")
    os.system('rm -rf%s'%borrar)
f.close

