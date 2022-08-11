import pandas as pd
import pandas as pd
import numpy as np

def setTierScore(x):
    return int(x / 10) - 1 + (1 - (x % 10) * 0.2)

def getTierScore(x):
    return int(round((int(x) + 1) * 10 + (1 - (x % 1)) / 0.2))

def predictmean(predictList):
    df = pd.DataFrame(predictList)
    rankMean = getTierScore(df['currentRank'].apply(setTierScore).mean())
    df = df[['ranktier', 'result']].groupby('ranktier', as_index=False).mean()
    return rankMean, df