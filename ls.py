ls = ['item', 'item2', 'item3', 'item3', 'item5']

for i in ls: 
	print(i) 
	if ls.index(i) != ls.index(ls[-1]): print("----------")
