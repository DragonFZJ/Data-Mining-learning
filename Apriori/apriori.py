#coding=utf-8

__author__ = "clogos"

#载入相关数据
def loadData():
	with open("apriori2.in", "r") as f:
		flines = f.readlines()
		itemSize = int(flines[0])
		minSup = int(flines[1])
		dataSet = []
		for line in flines[2:]:
			dataSet.append(line.split())
	return itemSize, minSup, dataSet;

#显示输入的数据
def showInput(itemSize, minSup, dataSet):
	print("事务数为: ", itemSize)
	print("最小支持度为: ", minSup)
	for i in range(itemSize):
		print("第 ", str(i+1), " 个事务为: ", dataSet[i])

#扫描全部数据，产生候选1-项集的集合C1
def getC1(dataSet):
	C1 = {}
	for items in dataSet:
		for item in items:
			if item in C1:
				C1[item] += 1
			else:
				C1[item] = 1
	return C1

#根据最小支持度，由候选1-项集的集合C1产生频繁1-项集的集合L1
def getL1(C1, minSup):
	_L1 = list(C1.keys())
	_L1.sort()
	L1 = []
	sup1 = []

	for item in _L1:
		if C1[item] >= minSup:
			tempL1 = []
			tempsup1= []
			tempL1.append(item)
			L1.append(tempL1)
			sup1.append(C1[item])

	return L1, sup1

def cheakLink(item1, item2, cur_k):
	for i in range(cur_k-1):
		if(item1[i] != item2[i]):
			return False
	return True


#连接步。此处可以根据L_old是有序的进行优化，有时间再改进
def apriori_gen(L_old, cur_k):
	L_new = []
	for i in range(len(L_old)):
		j = i + 1
		while j < len(L_old):
			if cheakLink(L_old[i], L_old[j], cur_k):
				item = L_old[i][:]
				item.append(L_old[j][cur_k-1])
				L_new.append(item)
			j += 1

	return L_new

#剪枝步，根据项目集空间理论：频繁项目集的子集仍是频繁项目集；非频繁项目集的超集是非频繁项目集
def apriori_cut(Ckp_old, L_old, cur_k):
	Ckp_new = []
	for item in Ckp_old:
		flag = True
		i = 0
		while i < cur_k and flag:	
			temp = item[:]
			del temp[i]
			if temp not in L_old:
				flag = False
			i += 1

		if flag:
			Ckp_new.append(item)
	return Ckp_new

#根据最小支持度，扫描数据库由，候选(k+1)-项集的集合C(k+1)，产生频繁(k+1)-项集的集合L(k+1)
def getLkp(Ckp, dataSet, minSup):
	L = []
	sup = []
	for items in Ckp:
		cal = 0	
		for works in dataSet:
			flag = True
			for item in items:
				if item not in works:
					flag = False	
				if not flag:
					break
			if flag:
				cal += 1
		if cal >= minSup:
			L.append(items)
			sup.append(cal)

	return L, sup


#apriori算法主过程
def apriori(itemSize, minSup, dataSet):
	all_keys = []
	all_sups = []

	'''得到第一项'''
	C1 = getC1(dataSet)	
	L1, sup1 = getL1(C1, minSup)
	Lk = L1
	supk = sup1

	'''迭代'''
	k = 1
	while Lk != []:
		all_keys.append(Lk)	
		all_sups.append(supk)	
		Ckp = apriori_gen(all_keys[k-1], k)
		Ckp = apriori_cut(Ckp, all_keys[k-1], k+1)
		Lk, supk = getLkp(Ckp, dataSet, minSup)
		k += 1
	
	return all_keys, all_sups

#输出结果
def showOutput(all_keys, all_sups):
	print("---------- 运行结果如下: ----------\n\n")
	for i, keys in enumerate(all_keys):
		print("第 ", str(i+1), " 级频繁项集为:")
		print("项　集\t\t\t频率")
		for j, item in enumerate(keys):
			print(item, "\t\t\t", all_sups[i][j])

		print("\n\n")

def main():
	itemSize, minSup, dataSet = loadData()
	showInput(itemSize, minSup, dataSet)
	all_keys, all_sups = apriori(itemSize, minSup, dataSet)
	showOutput(all_keys, all_sups)

if __name__ == "__main__":
	main()
