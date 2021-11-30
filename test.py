import json
from datetime import date, datetime, time
from condition import mode_1
from controller import read_log, write_log, is_sent, has_log

a = read_log()
print(a["Mode_1"])
# log = read_log()
# # for val in log["Mode_1"]:
# #     if val["id"] == "1.1":
# #         print(val)
# print(log["Mode_1"])
# log["Mode_1"].append({"id": "1.3", "sent": False, "lasttime": -1})
# print(log["Mode_1"])
# write_log(log)


# now = datetime.now()
# now = now.strftime("%H:%M")
# h, m = now.split(":")
# h = int(h)
# m = int(m)
# print(h, m)
