from math import log10, floor

def is_use(use):
    return True if use == 'on' else False

def mode_1(val,limit): # High mode 1 => True over limit
    return True if val > limit else False

def mode_2(val,limit): # Low mode 2 => True below limit
    return True if val < limit else False

def expo_moving(table): #exponential weight moving (1-alpha)^t * xn / (1-alpha)^t
    res = table.ewm(com=0.5).mean()
    # print(f'resmean\n {res.mean()}')
    return round(res.mean(), 5-int(floor(log10(abs(res.mean()))))-1) # average value by weight

def mode_3(weight,val): # Trend Up
    # print(f'weigth : {weight} , current val : {val}')
    return True if weight < val else False

def mode_4(weight,val): # Trend Down
    # print(f'weigth : {weight} , current val : {val}')
    return True if weight > val else False

def threshold_check(results): # it was happens as long as threshold period
    for res in results:
        if res == False:
            return False
    return True
