import os
file = os.popen("date --date=\"2 day ago\"").read()
print(file)
'''
f = open("new.log","r")
mensaje = f.readlines()
f.close()
f = open("new.log","w")
for x in mensaje:
    if "Created file" in x:
        f.write(x)
f.close
f = open("new.log","r")
mensaje = f.readlines()
for z in mensaje:
    cut = z.split("file:")
    borrar = cut[1]
    os.system('rm -rf%s'%borrar)
f.close
'''