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


def not_equal(val, limit):  # invert of equal
    return True if val != limit else False


def get_sensor_val_by_name(datetime, sensors_table, sensor_name):
    result = sensors_table.loc[sensors_table['DATE'] == datetime]
    return result[sensor_name].iloc[0]  # sensorsvalue


def another_sensor(row, sensors_table,
                   datetime):  # if another condition => True mean pass to main sensor
    if row['On/Off_sensor'] == 'not-use' or (
            row.isnull().values.any() and type(row['On/Off_sensor']) != str):  # not use another sensors to compare
        return True
    # compare
    if (type(row['On/Off_condition']) == str):
        # define variable
        compare_cond = row['On/Off_condition']
        compare_name = row['On/Off_sensor']
        compare_val = row['On/Off_value']  # from input
        compare_sensor_val = get_sensor_val_by_name(datetime, sensors_table, compare_name)  # from sensors api
        # print(f'value : {compare_val} type : {type(compare_val)}')
        # condition
        if compare_cond == 'equal':
            return equal(compare_sensor_val, compare_val)
        if compare_cond == 'not-equal':
            return not_equal(compare_sensor_val, compare_val)
        elif compare_cond == 'lower':
            return lower(compare_sensor_val, compare_val)
        elif compare_cond == 'higher':
            return higher(compare_sensor_val, compare_val)
        elif compare_cond == 'between':
            left, right = -1, -1
            if type(compare_val) != str or ':' not in compare_val:  # incorrect pattern
                print("wrong input pattern")
                return str(compare_val)
            if ':' in compare_val:
                left, right = compare_val.split(":")
                right = float(right)
                left = float(left)
            return between(compare_sensor_val, left, right)
        elif compare_cond == 'out of range':
            left, right = -1, -1
            if type(compare_val) != str or ':' not in compare_val:  # incorrect pattern
                print("wrong input pattern")
                return str(compare_val)
            if ':' in compare_val:
                left, right = compare_val.split(":")
                right = float(right)
                left = float(left)
            return out_of_range(compare_sensor_val, left, right)
    return False
