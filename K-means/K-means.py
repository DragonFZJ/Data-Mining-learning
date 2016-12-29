#coding = utf-8
import random
import math

__author__ = "clogos"


def loadData():
	try:
		with open("K-means.in", "r") as f:
			flines = f.readlines()
			k = int(flines[0])
			dataSet = []
			for item in flines[1:]:
				dataSet.append(item.split())
			dimen = len(dataSet[0])
			return k, dimen, dataSet
	except:
	  	print("载入数据错误！")

#欧拉距离的平方
def distance(A, B):
	sumOfSquare = 0
	for i in range(len(A)):
		dist = float(A[i]) - float(B[i])
		sumOfSquare += dist * dist
	return sumOfSquare


#把每一个样本点划分到距离它最近的聚类中心所在的类
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

#计算新的聚类中心
def getCenter(belong, dimen):
	center = []
	for items in belong:
		currentCenter = []
		for i in range(dimen):
			currentCenter.append(0.0)
		for item in items:
			for i in range(dimen):
				currentCenter[i] += float(item[i])
		if(len(items) != 0):
			for i in  range(dimen):
				currentCenter[i] /= len(items)
		center.append(currentCenter)
	return center

#准则函数：误差平方和
def getE(center, belong):
	err = 0
	for index, currentCenter in enumerate(center):
		for item in belong[index]:
			err += distance(item, currentCenter)
	return err


def KMeans(dataSet, center, dimen):
	eps = 0.000001 #精度要求
	err = random.random() * 1000000 #初始化准则函数的值
	while(True):
		belong = getBelong(dataSet, center)
		center = getCenter(belong, dimen)
		currentErr = getE(center, belong)
		'''如果收敛，就结束，否则继续迭代'''
		if(math.fabs(currentErr-err) < eps):
			return center, belong
		else:
		 	err = currentErr

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
	center, belong = KMeans(dataSet, center, dimen)
	show(center, belong)
	

if __name__ == "__main__":
	main()
