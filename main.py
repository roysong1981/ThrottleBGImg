import datetime
import json
import win32api,win32con,win32gui
import os

TIME_PATTERN = '%Y-%m-%d %H:%M:%S'

# 获取当前年份
def current_year():
    return datetime.datetime.now().year

# 获取当前时间，到秒
def current_time():
    return datetime.datetime.now().strftime(TIME_PATTERN)

# 比较两个时间字符串是否在同一天
def compare_date(current_time,start_time,end_time): 
    c = datetime.datetime.strptime(current_time,TIME_PATTERN)
    s = datetime.datetime.strptime(start_time,TIME_PATTERN)
    e = datetime.datetime.strptime(end_time,TIME_PATTERN)
    return s < c < e

# 根据年份在节气日期文件夹date中找到对应的JSON数据，返回字典列表
def year_json(year): 
    f = open('./date/' + str(year) + '.json')
    json_str = f.read()
    contents = json.loads(json_str)
    contents.sort(key=lambda o: o['time'],reverse=False)
    return contents

# 根据当前日期找到对应的节气
def get_throttle(now_day):
    year_arr = year_json(current_year())
    for idx in range(len(year_arr) -1): 
        if compare_date(now_day,year_arr[idx]['time'],year_arr[idx+1]['time']):
            return year_arr[idx]
    return None

def setWallPaper(pic):
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey,"WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # refresh screen
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,pic, win32con.SPIF_SENDWININICHANGE)

def main():
    json_item = get_throttle(current_time())
    if json_item is None:
        return
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pic = current_dir + '/img/' + json_item['name'] + '.jpg'
    setWallPaper(pic)

if __name__ == "__main__":
    main()