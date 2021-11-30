import pandas as pd
from datetime import datetime
import sensor_data
from condition import mode_1, mode_2, mode_3, mode_4,expo_moving, threshold_check, is_use
from another_condition import  another_sensor,get_sensor_val_by_name
from notification import send_text
from get_value_yaml import get_value


# API USE not excel file
def sensors_history(sensors_table, sensors_name, threshold):  # select sensors_name from sensors_table
    if len(sensors_table) < threshold:
        return sensors_table[sensors_name]
    return sensor_table[sensors_name].tail(threshold)  # recent threshold row

# Query by date
def history_by_date(sensors_table, sensors_name, datetime, threshold=None):  # select sensors_name from sensors_table
    table = sensors_table.loc[sensor_table["DATE"] == datetime]  # query by datetime
    result = sensor_table.loc[:table.index[0]-1] # get index
    result = result[sensors_name]
    if len(result) < threshold:
        return result
    return result.tail(threshold)  # recent threshold row


def query_events(events, sensors_table, mode):
    for index, row in events.iterrows():  # process each row of input
        datetime = DATE #Change date to time now
        #datetime = get_value('DATE')  # get test_datetime value from config.yaml 
        # select sensorsname from sensors_table
        # his_bydate = sensors_history(sensor_table, sensors_name=row['tag'], threshold=row['Threshold(min.)'])
        his_bydate = history_by_date(sensors_table, sensors_name=row.tag, threshold=row["Threshold(min.)"],
                                     datetime=datetime)  # sensors history
        # print(f'hisbydate\n {his_bydate}')
        status = row['Status']  
        # another sensor condition
        is_another_conditon = another_sensor(row, sensors_table, datetime)
        if type(is_another_conditon) == str: # another sensors wrong input pattern
            text = 'mode : ' + mode + '   \n' + 'row : ' + str(index + 1) + '   \n' + 'value : ' + is_another_conditon
            # wrong_input(text)  # notify wrong pattern input
            print(f'wrong pattern : {text}')
            is_another_conditon == False
        # main sensors
        if is_use(status.lower()) and is_another_conditon:  # another condition with another sensors
            line1, line2, line3, line4 = 'Alert : ' + str(row.Message), 'Sensors Name : ' + str(row.tag), '', ''
            if mode == 'Mode_1' or mode == "Mode_2":  # mode 1 , 2
                temp = []  # create to collect events
                for val in his_bydate:  # process each sensors value in threshold
                    if mode == 'Mode_1':
                        temp.append(mode_1(val, row.High_limit))  # check with mode high condition
                        line3 = 'Limit value : ' + str(row['High_limit'])
                    elif mode == 'Mode_2':
                        temp.append(mode_2(val, row.Low_limit))  # check with mode low condition
                        line3 = 'Limit value : ' + str(row['Low_limit'])
                    line4 = 'Sensors value: ' + str(val)
                if threshold_check(temp):  # happens continue as threshold min.
                    send_text(line1,line2,line3,line4,mode) # notification!!!!
                    print(f'Sent => {line1} \n {line2} \n {line3} \n {line4}')
            elif mode == 'Mode_3' or mode == 'Mode_4':
                value = get_sensor_val_by_name(datetime,sensors_table,row.tag)
                line4 = 'Sensors value: ' + str(value)
                if mode == 'Mode_3':
                    if mode_3(expo_moving(his_bydate),value):
                        line3 = 'Weight average value : ' + str(expo_moving(his_bydate))
                        print(f'Sent => {line1} \n {line2} \n {line3} \n {line4}')
                        send_text(line1,line2,line3,line4,mode) # notification!!!!
                elif mode == 'Mode_4':
                    if mode_4(expo_moving(his_bydate), value):
                        line3 = 'Weight average value : ' + str(expo_moving(his_bydate))
                        print(f'Sent => {line1} \n {line2} \n {line3} \n {line4}')
                        send_text(line1,line2,line3,line4,mode) # notification!!!!

# input_event => query_each_sheet => row of events =>
# 1 check on-off and check compared sensors => another condition.pys
# 2 check main sensors value on condition with input value ( period = threshold )
# 3 if yes => noti the message to chanels , no => pass

if __name__ == "__main__":
    input_path = get_value('Input_Path')
    sensordata = get_value('Sensors_Data')
    data_now = sensor_data.get_IP21()
    read = pd.read_csv('sensor_data.csv')
    DATE = read.iloc[-1,0] 
    for mode in get_value("ALL_Mode"):  # each sheet
        print(f'{mode} _______')
        # read input excel file
        events = pd.read_excel(input_path, sheet_name=mode)
        # read All sensors data
        sensor_table = pd.read_csv(sensordata)
        # sensor_table = pd.read_excel(sensordata)
        query_events(events, sensor_table, mode=mode)  # query each rows in input file


