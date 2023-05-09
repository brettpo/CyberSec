list = [91,322,57,124,40,406,272,147,239,285,353,272,77,110,296,262,299,323,255,337,150,102] 
library = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
mod =[]
index=0
flag="picoCTF{"

for x in list:
	
	mod.insert(index, x%37)
	index=index+1
	
for num in mod:
	flag = flag+library[num]
	
print(flag+"}")
	
	
	
