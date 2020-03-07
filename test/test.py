import sys
sys.path.append('../src')
#--
import * from calc

buyOrdr = calcBuyOrder(
    filledPrice=buyPrice,
    coinAmount=coinAmount,
    cashValue=cashValue,
    **kwargs)

sellOrdr = calcSellOrder(
    filledPrice=sellPrice,
    coinAmount=coinAmount,
    cashValue=cashValue,
    **kwargs)
