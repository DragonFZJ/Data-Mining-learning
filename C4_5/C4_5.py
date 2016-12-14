#coding = utf-8

import math

__author__ = "clogos"


#载入数据
def loadData():
	try:
		with open("C4_5.in", "r") as f:
			flines = f.readlines()
		labels = flines[0].split()
		del labels[0], labels[-1]
	except:
		print("数据载入出错！")
	dataSet = []
	for line in flines[1:]:
		item = line.split("\n")[0].split()
		del item[0]
		dataSet.append(item)
	return dataSet, labels;

#没有剩余属性可以用来进一步划分样本，用剩余样本中出现最多的类型作为叶子节点的类型，即选择最普通的类'''
def mostCommonLabel(classList):
	maxCount = 0
	ret = classList[0]
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
		if classCount[vote] >= maxCount:
			maxCount = classCount[vote]
			ret = vote
	return ret

#根据具体属性和值来计算熵
def computeEntropy(dataSet):
	numItems = len(dataSet)
	labelCounts = {}
	for items in dataSet:
		currentLabel = items[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	entropy = 0.0	
	for label in labelCounts:
		prob = labelCounts[label] / numItems
		entropy -= prob * math.log(prob, 2)
	return entropy

#根据给出属性划分数据样本
def splitDataSet(dataSet, curID, value):
	retDataSet = []
	for items in dataSet:
		if items[curID] == value:
			newItems = items[:curID]
			newItems.extend(items[curID+1:])
			retDataSet.append(newItems)
	return retDataSet

#选择具有最高信息增益率的属性
def bestFeatureToSplit(dataSet):
	numFeature = len(dataSet[0]) - 1;
	baseEntropy = computeEntropy(dataSet)

	bestGainRatio = 0.0
	bestFeature = -1

	'''对dataSet中的每一个属性A计算信息增益率gain_ratio'''
	for i in range(numFeature): 
		featureList = [items[i] for items in dataSet]
		'''构建该属性下的去重可取值'''
		uniqueVals = set(featureList)
		'''计算根据该属性划分的子集的熵currentEntropy和关于该属性值的熵currentsplitInfo'''
		currentEntropy = 0.0
		currentsplitInfo = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / len(dataSet)
			currentEntropy += prob * computeEntropy(subDataSet)
			currentsplitInfo -= prob * math.log(prob, 2)

		'''计算因为知道属性A的值后导致的熵的期望压缩，即关于A的信息增益'''
		infoGain = baseEntropy - currentEntropy
		'''计算信息增益率， 并更新导致最大增益率的属性'''
		'''避免除零错误'''
		if currentsplitInfo == 0:
			continue
		gainRatio = infoGain / currentsplitInfo 
		if (gainRatio > bestGainRatio):
			bestGainRatio = gainRatio 
			bestFeature = i
	
	return bestFeature


#决策树生成(递归层)
def buildDecisonTreeDFS(dataSet, labels):
	classList = [attributes[-1] for attributes in dataSet]
	'''给定节点的所有样本属于同一类，则节点作为叶子节点，并以该类标记，程序结束'''
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	
	'''没有剩余属性可以用来进一步划分样本，采用多数表决'''
	if len(dataSet[0]) == 1:
		return mostCommonLabel(classList)

	'''选择具有最高信息增益率的属性作为节点的测试属性'''
	bestFeature = bestFeatureToSplit(dataSet)
	bestFeatureLabel = labels[bestFeature]

	del labels[bestFeature]

	featureList = [items[bestFeature] for items in dataSet]
	uniqueVals = set(featureList)

	curTree = {bestFeatureLabel:{}}
	for value in uniqueVals:
		subDataSet = splitDataSet(dataSet, bestFeature, value)
		subLabels = labels[:]
		curTree[bestFeatureLabel][value] = buildDecisonTreeDFS(subDataSet, subLabels)

	return curTree


#ID3算法主流程
def ID3(dataSet, labels):
	decisionTree = buildDecisonTreeDFS(dataSet, labels)
	return decisionTree

def printTab(times, value):
	for i in range(times):
		print("\t", end = "")
	print(value)

def printTree(root, dep):
	'''输出当前节点标签'''
	for key, value in root.items():
		printTab(dep, key)
		'''对于非叶子节点，继续递归输出'''
		if isinstance(value, dict):
			printTree(value, dep+1)
		else:
			printTab(dep+1, value)

#输出决策树
def showDecisionTree(decisionTree):
	print("the decision tree is :")
	printTree(decisionTree, 0)

def main():
	dataSet, labels = loadData()
	decisionTree = ID3(dataSet, labels)
	showDecisionTree(decisionTree)

if __name__ == "__main__":
	main()
