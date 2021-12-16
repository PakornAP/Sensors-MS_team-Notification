import json
from datetime import datetime

# json -> python dict : process : python dict -> json


def read_log():
    f = open("./data/filelog.json", "r")
    # deserialize
    a = json.load(f)
    f.close()
    return a


def write_log(data):
    f = open("./data/filelog.json", "w")
    # serialize
    json.dump(data, f)
    f.close()


def has_log(row, mode):  # has this row in file log ?
    log = read_log()
    id = str(row["Event"]) + str(row["tag"]) + str(row["Message"])
    # id = "1.1"
    if not log[mode]:
        return False, -1
    for value in log[mode]:
        if value["id"] == id:
            return True, value["lasttime"]
    return False, -1


def add_log(mode, row):  # new input row to file log
    log = read_log()
    lasttime = datetime.now()
    lasttime = lasttime.strftime("%H:%M")
    id = str(row["Event"]) + str(row["tag"]) + str(row["Message"])
    log[mode].append({"id": id, "lasttime": lasttime})
    write_log(log)


def update_log(row, mode):  # update lasttime to file log
    log = read_log()
    lasttime = datetime.now()
    lasttime = lasttime.strftime("%H:%M")
    id = str(row["Event"]) + str(row["tag"]) + str(row["Message"])  # row id
    for value in log[mode]:
        if value["id"] == id:  # check with log id
            value["lasttime"] = lasttime
    write_log(log)


# To check did massage has been sent in o'clock ago
def is_sent(lasttime):  # True => sent it , False => do not sent it
    # time now transfromation
    time_now = datetime.now()
    time_now = time_now.strftime("%H:%M")
    now_h, now_m = time_now.split(":")
    now_h, now_m = int(now_h) * 60, int(now_m)
    now_total = now_h + now_m
    # lasttime transfromation
    last_h, last_m = lasttime.split(":")
    last_h, last_m = int(last_h) * 60, int(last_m)
    last_total = last_h + last_m
    # print(f'now : {now_total} , last : {last_total}')
    # one hour check
    return True if abs(now_total - last_total) >= 60 else False
