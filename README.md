# 1W340
PCSensor 1W340感測器取得溫溼度數據

## 官方資訊

1. [軟體下載](http://www.pcsensor.com//uploadFile/APPsoftware/1W340%20V4.0.zip)
2. [技術手冊](http://www.goliinfo.com/palms/1W340_DIY_V1.6_en.doc)
3. [軟體操作手冊](https://www.pcsensor.cn/Resource20171116140212224.html)
4. [1W340G](https://www.pcsensor.cn/Resource20171115202252191.html)
5. [1W340C](https://www.pcsensor.cn/Resource20171115202121835.html)
6. [HS10](https://www.pcsensor.cn/Resource20180515171214357.html)
7. [TCPTest 工具](http://www.pcsensor.com/uploadFile/APPsoftware/TCP_UDPtest%20tool%20V1.1.zip)

## 網路上的參考資源

1. [pcsensor_1w340](https://github.com/ma-lu-yao/pcsensor_1w340.git)


## 官網手冊導讀

1. 1W340 預設為 TCP 協定的 Server 服務
  * 預設 IP 為: 192.168.1.188
  * 預設 Port 為: 5200
2. 可透過 TCPTest 工具來顯示 1W340 網路設定
  * 進入設定狀態
   - 輸入: call pcsensor!
   - 傳回: enter config state
  * 顯示設定
   - 輸入: display configs!
   - 傳回: 
   ```
   host ipaddress:192.168.1.4
   connection type:tcp
   host port:16000
   user name:RDing
   user password:111111
   firmware:1W340G_V1.4
   ```
  * 設定 IP
  * 設定 netmask
  * 設定 gateway
3. TCP/IP 資料傳輸單元
  * 命令格式
   - 0xbb 開始 Byte
   - cmd  讀資料、寫設定值、讀設定值、寫資料、重置網路、裝置重開機
   = type 根據不同機型設備指定特定值，1W340 為 0x05 使用 Hx-sensor 探頭
   - len  傳回設備上有多少個裝置
   - Data0 ~ n 有幾個裝置，即會傳回
   - 0xff 結束 Byte
  * 命令 0x80 讀取資料
  * 類別 0x05 Read Hx-sensor(SHT10) hygrometer For 1W340C 1W340D
4. 其他應用

