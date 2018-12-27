#!/usr/bin/python
##-*- encoding: utf-8 -*-
import socket	# 網路服務程式函式庫
import sys		# 系統標準函式庫，命令列程式
import getopt	# 處理命令行指令
import binascii
import time
import sqlite3
#sys.setdefaultencoding('utf-8')
# 版本
VERSION = 0.9
INFO_ONLY = 0
PORT = 5200
HOSTNAME = '192.168.1.188'
# 1W340 感測器計算溫溼度設備規格常數
# 相關計算公式請參考官方文件附錄A
C1 = -4.0
C2 = 0.0405
C3 = -0.0000028
T1 = 0.01
T2 = 0.00008

# 計算溫溼度數值
def getTempHumibyHex(readHex):
  # print "TEMP:  " + binascii.b2a_hex(readHex[0:2])	# 取得溫度 2 Bytes 數據，十六進位
  # print "HUMI:  " + binascii.b2a_hex(readHex[2:4])	# 取得濕度 2 Bytes 數據，十六進位
  # 計算攝氏溫度
  t_C = int("0x"+binascii.b2a_hex(readHex[0:2]),16)/100.00 - 40
  # 解析濕度數據
  rh = int("0x"+binascii.b2a_hex(readHex[2:4]),16)
  rh_lin = C3*rh*rh + C2*rh + C1
  rh_true = (t_C - 25) * (T1 + T2*rh) + rh_lin
  # 判斷真實濕度數據
  if rh_true > 100:							# 如果相對溼度值大於 100
	rh_true = 100							# 設定相對濕度為 100
  if rh_true < 0.1:							# 如果相對溼度小於 0.1
	rh_true = 0.1							# 設定相對溼度為 0.1
  return round(t_C, 2), round(rh_true, 2)	# 取小數兩位，傳回溫溼度值

# 命令列使用法
def usage():
    sys.stderr.write("""USAGE: %s [options]
    iw340 Reader for Linux/Unix
    options:
    -p, --port=PORT: port, a number, must be 5200 now.
    -h, --help:      show this usage.
    -i, --info:      Show information of the sensor
    -H, --host=:     Hostname or IP address. default is 192.168.1.188
    -v, --version:   show version.
""" % (sys.argv[0], ))
if __name__ == '__main__':
  try:
    opts, args = getopt.getopt(sys.argv[1:],
    "ih:H:p:v",
     ["info","help", "host=","port=","version"]
    )
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h","--help"):
      usage()
      sys.exit()
    if o in ("-i","--info"):
      INFO_ONLY=1
    elif o in ("-v", "--version"):
      print "1W340 Reader for Windows/OSX/Linux/Unix, Version ", VERSION
      sys.exit()
    elif o in ("-p", "--port"):
      try:
        PORT = int ( a )
      except ValueError:
        PORT = 5200
    elif o in ("-H", "--host"):
      HOSTNAME = a

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  try:
    s.connect((HOSTNAME, PORT))
    if (INFO_ONLY==1):
      s.send("display configs!")	# 這是傳到 1W340 的預設文字指令，會回傳設備預設設定
      result=s.recv(1024)			# 取得 1024 B
      print result;
      s.close()
      sys.exit()
    s.send("\xbb\x80\x05") 			# 查詢 1W340 安裝 SHT10 的溫溼度感測器數據的指令
    result=s.recv(1024)
    s.close()
  except socket.error,msg:
    print 'Fail to connect the PCsensor 1W340, Error code: '+  msg[1],', ', HOSTNAME,':',PORT
    sys.exit()
  Num=int(binascii.b2a_hex(result[3:4])) #Number of SHT10 Sensors
  print binascii.b2a_hex(result)
  # 取得相關數據
  # 1. 1W340 上的感測器順序 index
  # 2. 詢問時間
  # 3. 1W340 返回之原始數據
  # 4. 計算後的溫溼度資料
  conn = sqlite3.connect("1W340.db")
  print "Connected DB Successful!"
  for i in range(0,Num):
   first = 4+i*4
   # print HOSTNAME;
   # print getTempHumibyHex(result[first:(first+4)])[1]
   # print HOSTNAME, i, time.strftime("%Y-%m-%d %H:%M:%S"), binascii.b2a_hex(result[first:(first+4)]), getTempHumibyHex(result[first:(first+4)])	
   myTime = time.strftime("%Y-%m-%d %H:%M:%S")
   RAWDATA = binascii.b2a_hex(result[first:(first+4)])
   TEMP = getTempHumibyHex(result[first:(first+4)])[0]
   HUMI = getTempHumibyHex(result[first:(first+4)])[1]
   insertData = [HOSTNAME, i,  myTime, RAWDATA, TEMP, HUMI]
   #print insertData
   c = conn.cursor()
   c.execute('insert into TempHumi(HOSTNAME, NO, Time, RAWDATA, Temperature, Humidity) values (?, ?, ?, ?, ?, ?);', insertData)
   conn.commit()
  conn.close() 
