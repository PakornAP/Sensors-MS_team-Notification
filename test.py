from math import comb
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
import numpy as np
from yaml import serialize

from get_value_yaml import get_value
import matplotlib.pylab as plt

def get_sensor_val(datetime, sensors_table, sensor_name):
    result = sensors_table.loc[sensor_table['DATE'] == datetime]
    return result[sensor_name].iloc[0]  # sensorsvalue

def sensors_frame(table,threshold,name):
    result = table.loc[:,name].tail(threshold)
    return result
def expo_moving(df,threshold):
    df = df.ewm(span=int(threshold/6)).mean()
    return df
def history_by_date(sensors_table, sensors_name, datetime, threshold=None):  # select sensors_name from sensors_table
    table = sensors_table.loc[sensor_table["DATE"]==datetime]  # query by datetime
    result = sensor_table.loc[:table.index[0]-1]
    return result[['DATE',sensors_name]].tail(threshold)  # recent threshold rowd

def plot_3(df,sensorname,threshold):
    tdi = pd.DatetimeIndex(df.DATE)
    df.set_index(tdi,inplace=True)
    df.drop(columns='DATE',inplace=True)
    analysis = df[[sensorname]].copy()
    result = seasonal_decompose(analysis,model='multiplicative',period=int(threshold/6))
    trend = result.trend
    print(f'ss_trend mean : {trend.mean()}')
    # print(f'trend\n{trend}')
    seasonal = result.seasonal
    residual = result.resid
    result.plot()
if __name__ == '__main__':
    sensordata = get_value('Sensors_Data')
    sensor_table = pd.read_csv(sensordata)
    datetime = get_value("DATE")
    sensor_name = 'H4-AI7202-02C.PV'
    test_table = history_by_date(sensor_table,sensor_name,datetime,threshold=1440)
    # print(test_table)
    ts = test_table
    expo_moving(ts,1440).plot()
    print(expo_moving(ts,1440).mean())
    # ts[sensor_name] = pd.Series(list(range(len(test_table))))
    ts.plot(x='DATE')
    plot_3(test_table,sensor_name,threshold=1440)
    plt.show()
    # expo_moving(sensors_frame(sensor_table,20,sensor_name))
