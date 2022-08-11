def binarySearchAsc(mItem, mList):
    
    startIndex = 0
    endIndex = len(mList) - 1
    
    while(startIndex <= endIndex):
        target = int((startIndex + endIndex) / 2)
        
        if(mItem == mList[target]):
            return [True, target]
        elif(mItem < mList[target]):
            endIndex = target - 1
        else:
            startIndex = target + 1
            
    if(endIndex == -1):
        return [False, startIndex]
    if(startIndex > endIndex):
        return [False, startIndex]
    return [False, target]

def binarySearchtuple(mItem, mList, key):

    startIndex = 0
    endIndex = len(mList) - 1
    
    while(startIndex <= endIndex):
        target = int((startIndex + endIndex) / 2)
        
        if(mItem == mList[target][key]):
            return [True, target]
        elif(mItem < mList[target][key]):
            endIndex = target - 1
        else:
            startIndex = target + 1
            
    if(endIndex == -1):
        return [False, startIndex]
    if(startIndex > endIndex):
        return [False, startIndex]
    return [False, target]