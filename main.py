from lotto import *
import os

def CmdInit():
    print("==============================")
    print("1. 랜덤 번호 생성 - 5게임")
    print("2. 최근 당첨 번호")
    print("3. 당첨된 횟수 기준 번호 정렬 (count.txt)")
    print("4. 파일 업데이트 (count.txt)")
    print("5. 랜덤 번호 생성 - N번 (월일_시분.txt 파일)")
    print("6. 당첨까지 돌린 횟수 (No.시작회차_종료회차_날짜.txt 파일)")
    print("0. 종료")
    print("==============================")
    n = input(">> ")
    os.system('cls')
    return n

def BackupFile():
    try:
        f = open('count.txt', 'r')
        lines = f.readlines()
        drwNo = int(lines[0].split("=")[1].split("\n")[0])
        f.close()
    except FileNotFoundError:
        f = open('count.txt', 'w')
        data = "drwNo=0\n"
        for i in range(1,46): data += f"{i}=0\n"
        f.write(data)
        f.close()
        return 0
    f = open('count_backup.txt', 'w')
    for line in lines: f.write(line)
    f.close()
    return drwNo

def PrintRandomNum():
    print("1. 가중치 적용")
    print("2. 가중치 미적용")
    print("0. 뒤로")
    key = input(">> ")
    os.system('cls')
    if key == '1':
        print("# 가중치 적용하여 난수 생성 (count.txt 파일 기준)")
        result = GetRandomNum(True)
        i=0
        for nums in result: i += 1; print(f"{i}게임 : {nums[0]} {nums[1]} {nums[2]} {nums[3]} {nums[4]} {nums[5]}")
    elif key == '2':
        print("# 모두 동등한 확률을 가진 채로 난수 생성.")
        result = GetRandomNum(False)
        i=0
        for nums in result: i += 1; print(f"{i}게임 : {nums[0]} {nums[1]} {nums[2]} {nums[3]} {nums[4]} {nums[5]}")
    elif key == '0':
        return 0
    else:
        print("[Error] 잘못된 번호 입력!!!")
    return 1

def PrintRanNumNTimes():
    while 1:
        print("0. 뒤로")
        try:
            times = int(input("돌릴 횟수를 입력해주세요 : "))
            if times == 0: os.system("cls"); return 0
            break
        except:
            os.system("cls")
            print("[Error] 숫자를 입력해주세요.\n")
            continue
    result = GetRanNumNTimes(times)
    print("\n", result.replace(',',' '))
    return 1

def PrintExceCntToWin():
    while 1:
        print("0. 뒤로")
        try:
            StartNo = int(input("시작회차를 입력해주세요 : "))
            if StartNo == 0: os.system("cls"); return 0
            str = f"0. 뒤로\n시작회차를 입력해주세요 : {StartNo}"
            break
        except:
            os.system("cls")
            print("[Error] 숫자를 입력해주세요.\n")
            continue
    while 1:
        try:
            EndNo = int(input("종료회차를 입력해주세요 : "))
            if EndNo == 0: os.system("cls"); return 0
            break
        except:
            os.system("cls")
            print(f"[Error] 숫자를 입력해주세요.\n\n{str}")
            continue
    if StartNo > EndNo:
        os.system("cls")
        print("[Error] 시작회차 > 종료회차.\n\t시작회차에 더 작은 수를 입력해주세요.")
        return PrintExceCntToWin()
    min, max = GetExceCntToWin(StartNo, EndNo)
    print(f"Min : {min}\nMax : {max}")
    return 1

if __name__ == "__main__":
    drwNo = BackupFile()
    while 1:
        n = CmdInit()
        if n == '1':
            if PrintRandomNum() == 0: continue
        elif n == '2':
            drwNo = GetRecentlyNum(drwNo)
        elif n == '3':
            GetNumSortedProbabilityBase()
        elif n == '4':
            drwNo = UpdateCountFile()
        elif n == '5':
            if PrintRanNumNTimes() == 0: continue
        elif n == '6':
            if PrintExceCntToWin() == 0: continue
        elif n == '0':
            break
        else:
            print("[Error] 잘못된 번호 입력!!!")
        input("\n계속하시려면 Enter를 눌러주세요.")
        os.system('cls')