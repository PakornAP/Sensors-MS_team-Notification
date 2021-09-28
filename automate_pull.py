import pandas as pd
from condition import mode_1, mode_2, threshold_check, is_use
from another_condition import equal, between, out_of_range, higher, lower, another_sensor
from notification import send_text
from get_value_yaml import get_value


# API USE not excel file
def sensors_history(sensors_table, sensors_name, threshold):  # select sensors_name from sensors_table
    if len(sensors_table) < threshold:
        return sensors_table[sensors_name]
    return sensor_table[sensors_name].tail(threshold)  # recent threshold row


def history_by_date(sensors_table, sensors_name, threshold, datetime):  # select sensors_name from sensors_table
    if len(sensors_table) < threshold:
        return sensors_table[sensors_name]
    table = sensors_table.loc[:datetime].head(threshold)  # query by datetime
    table = table[sensors_name]  # select by sensors_name
    return table  # recent threshold row


def query_events(events, sensors_table, mode):
    for index, row in events.iterrows():  # process each row of input
        # select sensorsname from sensors_table
        # history = sensors_history(sensor_table, sensors_name=row['tag'], threshold=row['Threshold(min.)'])
        datetime = get_value('DATE')  # get test_datetime value from config.yaml
        his_bydate = history_by_date(sensors_table, sensors_name=row.tag, threshold=row["Threshold(min.)"],
                                     datetime=datetime) # sensors history
        status = row['Status']  # method status
        # main sensors
        if is_use(status.lower()) and another_sensor(row,sensors_table,datetime):# another condition with another sensors
            temp = []  # create to collect events
            line1, line2, line3, line4 = '', '', '', ''
            for val in his_bydate:
                line1 = 'Alert : ' + str(row.Message)
                line2 = 'Sensors Name : ' + str(row.tag)
                if mode == 'Mode_1':
                    temp.append(mode_1(val, row.High_limit))  # check with mode high condition
                    line3 = 'Limit value : ' + str(row.High_limit)
                elif mode == 'Mode_2':
                    temp.append(mode_2(val, row.Low_limit))  # check with mode low condition
                    line3 = 'Limit value : ' + str(row.Low_limit)
                line4 = 'Sensors value: ' + str(val)
            if threshold_check(temp):  # happens continue as threshold min.
                # send_text(line1,line2,line3,line4,mode) # notification
                print(f'Sent => {line1} \n {line2} \n {line3} \n {line4}')
            # print(f' test :{his_bydate}')


# input_event => query_each_row => row of events =>
# compare with query sensors table => matching with sensors_name =>
# pass to mode condition => is long as threshold time ?
# yes => noti the message to chanels , no => pass

if __name__ == "__main__":
    sensors_name = 'H4-FIQ7865.PV'  # example sensors
    input_path = get_value('Input_Path')
    sensordata = get_value('Sensors_Data')
    # sheet_name = ['Mode_1','Mode_2']
    for mode in get_value("ALL_Mode"):  # each sheet
        print(mode)
        # read input excel file
        events = pd.read_excel(input_path, sheet_name=mode)
        # read All sensors data
        sensor_table = pd.read_csv(sensordata)
        # sensor_table = pd.read_excel(sensordata)
        query_events(events, sensor_table, mode=mode)  # query each rows in input file
