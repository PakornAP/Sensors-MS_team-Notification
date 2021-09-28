def is_use(use):
    return True if use == 'on' else False

def mode_1(val,limit): # High mode 1 => True over limit
    return True if val >= limit else False

def mode_2(val,limit): # Low mode 2 => True below limit
    return True if val <= limit else False

def mode_3(val,limit): # Trend Up
    return

def mode_4(val,limit): # Trend Down
    return

def threshold_check(results): # it was happens as long as threshold period
    for res in results:
        if res == False:
            return False
    return True
