from numpy import *


def loadDataSet(filename):
    dataMat = []
    fr = open(filename)

    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)

    return dataMat


def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[nonzero(dataSet[:, feature] > value)[0], :]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0, mat1


def regLeaf(dataSet):
    return mean(dataSet[:, -1])


def regErr(dataSet):
    return var(dataSet[:, -1]) * shape(dataSet)[0]


def linearSolve(dataSet):
    """
    模型树的节点生成函数
    """
    m, n = shape(dataSet)
    X = mat(ones((m, n)))
    Y = mat(ones((m, 1)))
    X[:, 1:n] = dataSet[:, 0:n-1]
    Y = dataSet[:, -1]
    xTx = X.T * X

    if linalg.det(xTx) == 0:
        raise NameError("This matrix is singular, cannot do inverse, tryincreasing the seconed value of ops")

    ws = xTx.T * (X.T * Y)
    return ws, X, Y


def modelLeaf(dataSet):
    """
    返回数据集的回归系数
    """
    ws, X, Y = linearSolve(dataSet)
    return ws


def modelErr(dataSet):
    ws, X, Y = linearSolve(dataSet)
    yHat = X * ws

    return sum(power(Y - yHat, 2))


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    """
    找到数据的最佳二元切分方式

    Parameters
    -------------------
    dataSet : 数据集合
    leafType : 生成叶节点的函数
    errtype : 误差估计函数
    ops : 用户定义的参数构成的元组

    Returns
    ----------------
    bestIndex : 最佳切分特征
    bestValue : 最佳特征值
    """
    tolS = ops[0]    # 允许的误差下降值
    tolN = ops[1]    # 切分的最小样本

    # 如果当前所有值相等，则退出（根据set的特性只保留不重复的元素）
    if len(set(dataSet[:, -1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)

    m, n = shape(dataSet)
    S = errType(dataSet)

    bestS = float('inf')
    bestIndex = 0
    bestValue = 0

    for featIndex in range(n - 1):
        for splitVal in set(dataSet[:, featIndex].T.A.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)

            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
                continue

            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS

    if (S - bestS) < tolS:
        return None, leafType(dataSet)

    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)

    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
        return None, leafType(dataSet)

    return bestIndex, bestValue


def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops)

    if feat == None:
        return val

    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val

    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)

    return retTree


def isTree(obj):
    """
    判断测试输入变量是否是一棵树
    """
    return (type(obj).__name__ == 'dict')


def getMean(tree):
    """
    对树进行塌陷处理

    Parameters
    --------------
    tree : 树

    Returns
    -----------
    树的平均值
    """
    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])

    return (tree['left'] + tree['right']) / 2.0


def prune(tree, testData):
    """
    后剪枝
    """
    if shape(testData)[0] == 0:
        return getMean(tree)

    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])

    if isTree(tree['left']):
        tree['left'] = prune(tree['left'], lSet)
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rSet)

    # 如果当前节点的左右节点为叶节点
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])

        errorNoMerge = sum(power(lSet[:, -1] - tree['left'], 2)) + \
            sum(power(rSet[:, 1] - tree['right'], 2))
        treeMean = (tree['left'] + tree['right']) / 2.0
        errorMerge = sum(power(testData[:, -1] - treeMean, 2))

        if errorMerge < errorNoMerge:
            return treeMean
        else:
            return tree
    else:
        return tree


    
