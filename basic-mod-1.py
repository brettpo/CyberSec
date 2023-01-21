list = [91,322,57,124,40,406,272,147,239,285,353,272,77,110,296,262,299,323,255,337,150,102] 
upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
mod =[]
y=0
i="picoCTF{"

for x in list:
	
	mod.insert(y, x%37)
	y=y+1
	
for f in mod:
	i = i+upper[f]
	
print(i+"}")
	
	
	
