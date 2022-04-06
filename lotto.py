import requests
import random
import datetime

def GetWinNumbers(drwNo):
    url = f'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={drwNo}'
    try:
        json_result = requests.get(url).json()
    except:
        GetWinNumbers(drwNo)
    if json_result.get('returnValue', 'fail') == 'fail': return None, None
    res = []
    res.append(json_result.get('drwtNo1', None))
    res.append(json_result.get('drwtNo2', None))
    res.append(json_result.get('drwtNo3', None))
    res.append(json_result.get('drwtNo4', None))
    res.append(json_result.get('drwtNo5', None))
    res.append(json_result.get('drwtNo6', None))
    res.append(json_result.get('bnusNo', None))
    drwNoDate = json_result.get('drwNoDate', None)
    return res, drwNoDate

def GetCurrentCountFile():
    try:
        f = open('count.txt', 'r')
    except FileNotFoundError:
        print("[Error] count.txt 파일이 없습니다!!!")
        return None
    res = []
    res.append(int(f.readline().split('=')[1]))
    lines = f.readlines()    
    for l in lines: res.append(int(l.split('=')[1].split('\n')[0]))
    f.close()
    if len(res) < 46:
        print("[Error] count.txt 파일이 잘못되었습니다!!!")
        return None
    return res

def UpdateCountFile():
    r = {x:0 for x in range(1,46)}
    f_res = GetCurrentCountFile()
    if f_res == None: return
    drwNo = f_res[0]
    for i in range(1,46): r[i] = f_res[i]

    while 1:
        drwNo += 1
        winnums, drwNoDate = GetWinNumbers(drwNo)
        if winnums == None: break
        for n in winnums: r[n] += 1

        f = open("count.txt", "w")
        f.write(f"drwNo={drwNo}\n")
        for k,v in r.items():
            f.write(f"{k}={v}\n")
        f.close()
        print(f"drwNo={drwNo} Success!")
    return drwNo-1

def GetRecentlyNum(drwNo):
    result = ""
    drwNoDate = ""
    while 1:
        winnums, date = GetWinNumbers(drwNo)
        if winnums == None: break
        drwNoDate = date
        result = f"{winnums[0]} {winnums[1]} {winnums[2]} {winnums[3]} {winnums[4]} {winnums[5]} + {winnums[6]}"
        drwNo += 1
    drwNo -= 1
    print(f"[{drwNo} 회차]\n날짜 : {drwNoDate}\n당첨 번호 : {result}")
    return drwNo

def GetNumSortedProbabilityBase():
    f_res = GetCurrentCountFile()
    if f_res == None: return
    d = dict()
    for i in range(1,46): d[i] = f_res[i]
    sorted_d = sorted(d, key = lambda x : d[x], reverse=True)
    for i in range(45):
        print(sorted_d[i], end=" ")

def GetRandomNum(is_weight):
    w = []
    result = []
    if is_weight == True:
        f_res = GetCurrentCountFile()
        if f_res == None: return
        for i in range(1,46): w.append(float(f_res[i]))
    elif is_weight == False:
        w = [1]*45
    for i in range(5):
        nums = []
        while len(nums) < 6:
            num = random.choices(range(1, 46), weights = w)
            if num[0] in nums: continue
            else: nums.extend(num)        
        result.append(nums)
    return result

def CountTimeLoop(winnums, filename, drwNo, res):
    cnt = 0
    while 1:
        cnt += 1
        RanNums = GetRandomNum(False)
        for rannum in RanNums:
            rannum = sorted(rannum)
            if rannum == winnums:
                f = open(filename,'a')
                f.write(f"\n{drwNo}={cnt}")
                f.close()
                res.append(cnt)
                return

def GetExceCntToWin(StartNo, EndNo):
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    filename = f"No.{StartNo}_{EndNo}_{date}.txt"
    drwNo = StartNo
    res = []
    while drwNo <= EndNo:
        winnums, drwNoDate = GetWinNumbers(drwNo)
        winnums = sorted(winnums[:6])
        print(f"{drwNo}회 {winnums}")
        CountTimeLoop(winnums, filename, drwNo, res)
        drwNo += 1
    print(f"{filename} 파일이 생성되었습니다.")
    return min(res), max(res)

def GetRanNumNTimes(times):
    now = datetime.datetime.now()
    filename = now.strftime("%Y%m%d_%H%M.txt")
    for i in range(times):
        print(f"{i+1}번째 진행중")
        data = ""
        result = GetRandomNum(False)
        for nums in result:
            nums = sorted(nums)
            data += f"{nums[0]},{nums[1]},{nums[2]},{nums[3]},{nums[4]},{nums[5]},"
        data = data[:-1] + "\n"
        f = open(filename, "a")
        f.write(data)
        f.close()
        if i == times-1: res = data
    print(f"{filename} 파일이 생성되었습니다.")
    return res