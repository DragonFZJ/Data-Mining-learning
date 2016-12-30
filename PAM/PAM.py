#coding = utf-8
import math

__author__ = "clogos"


def loadData():
	try:
		with open("PAM.in", "r") as f:
			flines = f.readlines()
			k = int(flines[0])
			dataSet = []
			for item in flines[1:]:
				dataSet.append(item.split())
			dimen = len(dataSet[0])
			return k, dimen, dataSet
	except:
	  	print("载入数据错误！")

'''曼哈顿距离'''
def distance(A, B):
	dist = 0
	for i in range(len(A)):
		dist += math.fabs(float(A[i]) - float(B[i]))
	return dist 


'''把每一个样本点划分到距离它最近的聚类中心所在的类'''
def getBelong(dataSet, center):
	belong = []
	for i in range(len(center)):
		belong.append([])
	'''分别考虑每一个样本点'''
	for item in dataSet:
		blID = 0
		minDist = distance(item, center[0])
		'''在所有的聚类中找到一个距离最近的'''
		for i in range(len(center)):
			dist = distance(item, center[i])
			if(dist < minDist):
				minDist = dist
				blID = i
		belong[blID].append(item)
	return belong

'''A和B是否是同一点'''
def same(A, B):
	for index, val in enumerate(A):
		if val != B[index]:
			return False
	return True

'''计算A被B替换的代价'''
def getS(A, B, dataSet, center, belong):
	ret = 0.0
	'''对于所有的非中心点考虑'''
	for item in dataSet:
		blItem = B
		minDist = distance(item, B)
		for index, currentCenter in enumerate(center):	
			'''A已经不是中心点'''
			if currentCenter == A:
				continue
			dist = distance(currentCenter, item)
			if(dist < minDist):
				blItem = currentCenter
				minDist = dist
		oldItem = 0
		'''找到原来的归于点'''
		for index, currentCenter in enumerate(center):
			if item in belong[index]:
				oldItem = currentCenter
				break
		'''四种情况可以归到一起考虑，那就是现在属于的减去原来属于的'''
		ret += distance(item, blItem) - distance(item, oldItem)
	return ret
		 	
def PAM(dataSet, center, dimen):
	while(True):
		#print(">>>", center)
		belong = getBelong(dataSet, center)
		minS = 1.0 #最小替换代价
		A2B = [[],[]] #B替换A
		for currentCenter in center:
			for item in dataSet:
				if item in center:
					continue
				tempS = getS(currentCenter, item, dataSet, center, belong)
				if tempS < minS:
					minS = tempS
					A2B = [currentCenter, item]
		'''是否有总代价小于0的存在,此时minS已经是最小的'''
		if minS < 0:
			for index, currentCenter in enumerate(center):
				if same(currentCenter, A2B[0]):
					center[index] = A2B[1]
					break
			print(">>>", minS, center)
		else:
		   return center, belong

def show(center, belong):
	for index, currentCenter in enumerate(center):
		print(currentCenter, "->", belong[index])

def main():
	k, dimen, dataSet = loadData()
	center = []
	'''初始聚类中心'''
	for i in range(k):
		center.append(dataSet[i][:])
	'''迭代运算'''
	center, belong = PAM(dataSet, center, dimen)
	show(center, belong)
	

if __name__ == "__main__":
	main()
