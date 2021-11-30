# condition happens => True


def higher(val, limit):
    # if isinstance(val, (int, float)):
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
    result = sensors_table.loc[sensors_table["DATE"] == datetime]
    # print(result)
    return result[sensor_name].iloc[0]  # sensorsvalue


# if another condition => True mean pass to main sensor
def another_sensor(row, sensors_table, datetime, is_2=False):
    # not use on_sensor 1
    if is_2 is False and (row.isnull().values.any() or type(row["On_sensor"]) != str):
        return True
    # not use on_sensor 2
    elif is_2 and (row.isnull().values.any() or type(row["On_sensor2"]) != str):
        return True
    # variable for On_sensor1
    compare_cond, compare_name, compare_val = "", "", ""
    if is_2 is False and type(row["On_condition"]) == str:
        compare_cond = row["On_condition"]
        compare_name = row["On_sensor"]
        compare_val = row["On_value"]
    elif is_2 and type(row["On_condition2"] == str):
        compare_cond = row["On_condition2"]
        compare_name = row["On_sensor2"]
        compare_val = row["On_value2"]
    compare_sensor_val = get_sensor_val_by_name(
        datetime, sensors_table, compare_name
    )  # from sensors api
    # condition
    if compare_cond == "equal":
        return equal(compare_sensor_val, compare_val)
    if compare_cond == "not-equal":
        return not_equal(compare_sensor_val, compare_val)
    elif compare_cond == "lower":
        return lower(compare_sensor_val, compare_val)
    elif compare_cond == "higher":
        return higher(compare_sensor_val, compare_val)
    elif compare_cond == "between":
        left, right = -1, -1
        if type(compare_val) != str or ":" not in compare_val:  # incorrect pattern
            return False
        if ":" in compare_val:
            left, right = compare_val.split(":")
            right = float(right)
            left = float(left)
            return between(compare_sensor_val, left, right)
        elif compare_cond == "out of range":
            left, right = -1, -1
            if type(compare_val) != str or ":" not in compare_val:  # incorrect pattern
                return False
            if ":" in compare_val:
                left, right = compare_val.split(":")
                right = float(right)
                left = float(left)
            return out_of_range(compare_sensor_val, left, right)
    return False
