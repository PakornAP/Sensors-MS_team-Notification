# condition happens => True

def higher(val, limit):
    return True if val > limit else False


def lower(val, limit):
    return True if val < limit else False


def between(val, lower, upper):
    return True if (val >= lower) and (val <= upper) else False

def out_of_range(val, lower, upper):
    return True if val <= lower and val >= upper else False


def equal(val, limit):
    return True if val == limit else False


def another_sensor(row, sensors_table,
                   datetime):  # if another sensor is through condition => True mean pass to main sensor
    if (row.isnull().values.any() and type(row['On/Off_sensor']) != str):  # not use another sensors to compare
        return True
    # compare
    if (type(row['On/Off_condition']) == str and type(row['On/Off_value']) == str):
        compare_cond = row['On/Off_condition']
        compare_name = row['On/Off_sensor']
        compare_val = row['On/Off_value'] # from input
        compare_sensor_val = sensors_table.loc[sensors_table['DATE'] == datetime]
        compare_sensor_val = compare_sensor_val[compare_name].iloc[0] # from sensors api
        if compare_cond.lower() == 'equal':
            return equal(compare_sensor_val, compare_val)
        elif compare_cond.lower() == 'lower':
            return lower(compare_sensor_val, compare_val)
        elif compare_cond.lower() == 'higher':
            return higher(compare_sensor_val, compare_val)
        elif compare_cond.lower() == 'between':
            left,right = -1,-1
            if ',' in compare_val:
                left,right = compare_val.split(",")
                right = float(right)
                left = float(left)
            return between(compare_sensor_val,left,right)
        elif compare_cond.lower() == 'out of range':
            left,right = -1,-1
            if ',' in compare_val:
                left,right = compare_val.split(",")
                right = float(right)
                left = float(left)
            return out_of_range(compare_sensor_val,left,right)
    return False
