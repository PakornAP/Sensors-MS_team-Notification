from os import startfile, write
import pandas as pd
from condition import (
    mode_1,
    mode_2,
    mode_3,
    mode_4,
    expo_moving,
    threshold_check,
    is_use,
)
from another_condition import another_sensor, get_sensor_val_by_name
from notification import send_text
from get_value_yaml import get_value
from math import log10, floor, nan
from controller import has_log, add_log, update_log, is_sent


# select sensors_name from sensors_table
def sensors_history(sensors_table, sensors_name, threshold):
    if len(sensors_table) < threshold:
        return sensors_table[sensors_name]
    return sensor_table[sensors_name].tail(threshold)  # recent threshold row


# Query by date


# select sensors_name from sensors_table
def history_by_date(sensors_table, sensors_name, datetime, threshold=None):
    table = sensors_table.loc[sensor_table["DATE"] == datetime]  # query by datetime
    result = sensor_table.loc[: table.index[0] - 1]  # get index
    result = result[sensors_name]
    if len(result) < threshold:
        return result
    return result.tail(threshold)  # recent threshold row


def query_events(events, sensors_table, mode):
    for index, row in events.iterrows():  # process each row of input
        # get test_datetime value from config.yaml
        datetime = get_value("DATE")
        # select sensorsname from sensors_table
        # his_bydate = sensors_history(sensor_table, sensors_name=row['tag'], threshold=row['Threshold(min.)'])
        his_bydate = history_by_date(
            sensors_table,
            sensors_name=row.tag,
            threshold=row["Threshold(min.)"],
            datetime=datetime,
        )  # sensors history
        status = row["Status"]  # method status
        is_another_conditon = another_sensor(row, sensors_table, datetime)  # On_sensor
        is_another_conditon2 = another_sensor(
            row, sensor_table, datetime, is_2=True
        )  # On_sensor2
        onsensors_gate = True
        if row["On_gate"] == "AND" or row["On_gate"].empty == True:
            onsensors_gate = is_another_conditon and is_another_conditon2
        elif row["On_gate"] == "OR":
            onsensors_gate = is_another_conditon or is_another_conditon2
        # main sensors use and on_sensors
        if is_use(status.lower()) and onsensors_gate:
            line1, line2, line3, line4 = (
                "Alert : " + str(row.Message),
                "Sensors Name : " + str(row.tag),
                "",
                "",
            )
            if mode == "Mode_1" or mode == "Mode_2":
                temp = []  # create to collect events
                for val in his_bydate:  # process each sensors value in threshold
                    if mode == "Mode_1":
                        # high condition
                        temp.append(mode_1(val, row.High_limit))
                        line3 = "Limit value : " + str(row["High_limit"])
                    elif mode == "Mode_2":
                        # low condition
                        temp.append(mode_2(val, row.Low_limit))
                        line3 = "Limit value : " + str(row["Low_limit"])
                    line4 = "Sensors value: " + str(
                        round(val, 10 - int(floor(log10(abs(val)))) - 1)
                    )
                if threshold_check(temp):  # happens continue as threshold min.
                    in_log, lasttime = has_log(row, mode)
                    if (
                        in_log and is_sent(row, lasttime) is False
                    ):  # Guard Statement 1 hr ago
                        continue
                    if in_log and is_sent:
                        update_log(row, mode)
                    elif in_log is False:
                        add_log(mode, row)
                    send_text(line1, line2, line3, line4, mode)  # Notification
                    print(f"Sent => {line1} \n {line2} \n {line3} \n {line4}")
            elif mode == "Mode_3" or mode == "Mode_4":
                value = get_sensor_val_by_name(datetime, sensors_table, row.tag)
                line4 = "Sensors value: " + str(
                    round(value, 10 - int(floor(log10(abs(value)))) - 1)
                )
                noti = False
                if mode == "Mode_3" and mode_3(expo_moving(his_bydate), value):
                    line3 = "Weight AVG value : " + str(expo_moving(his_bydate))
                    noti = True
                elif mode == "Mode_4" and mode_4(expo_moving(his_bydate), value):
                    line3 = "Weight AVG value : " + str(expo_moving(his_bydate))
                    noti = True
                if noti:
                    in_log, lasttime = has_log(row, mode)
                    if (
                        in_log and is_sent(row, lasttime) is False
                    ):  # Guard Statement 1 hr ago
                        continue
                    if in_log and is_sent:
                        update_log(row, mode)
                    elif in_log is False:
                        add_log(mode, row)
                    print(f"Sent => {line1} \n {line2} \n {line3} \n {line4}")
                    send_text(line1, line2, line3, line4, mode)  # notification!!!!

                    # input_event => query_each_sheet => row of events =>
                    # 1 check on-off and check compared sensors => another condition.pys
                    # 2 check main sensors value on condition with input value ( period = threshold )
                    # 3 if yes => noti the message to chanels , no => pass


if __name__ == "__main__":
    input_path = get_value("Input_Path")
    sensordata = get_value("Sensors_Data")
    for mode in get_value("ALL_Mode"):  # each sheet
        print(f"{mode} _______")
        # read input excel file
        events = pd.read_excel(input_path, sheet_name=mode)
        # read All sensors data
        sensor_table = pd.read_csv(sensordata)
        # sensor_table = pd.read_excel(sensordata)
        # query each rows in input file
        query_events(events, sensor_table, mode=mode)
