from math import comb

import pandas as pd
import numpy as np
from get_value_yaml import get_value


def get_sensor_val(datetime, sensors_table, sensor_name):
    result = sensors_table.loc[sensor_table['DATE'] == datetime]
    return result[sensor_name].iloc[0]  # sensorsvalue

def sensors_frame(table,threshold,name):
    result = table.loc[:,name].tail(threshold)
    print(f'result: \n{result}')
    return result
def expo_moving(df):
    df = df.ewm(com=0.5).mean()
    print(f'df: \n{df}')
    print(f'mean : {df.mean()}')
    return df

if __name__ == '__main__':
    sensordata = get_value('Sensors_Data')
    sensor_table = pd.read_csv(sensordata)
    datetime = get_value("DATE")
    sensor_name = 'H4-PDI7732.PV'
    # print(f'table: \n {sensor_table.tail(10)}')
    expo_moving(sensors_frame(sensor_table,20,sensor_name))
