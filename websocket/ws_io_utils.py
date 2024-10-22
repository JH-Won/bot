from datetime import datetime
import copy

def get_current_time():
    return datetime.now().strftime("%Y%m%d_%H_%M_%S")

def get_current_day():
    return datetime.now().strftime("%Y%m%d")



def print_orderbook(data):
    recvvalue = data.split('^')  # 수신데이터를 split '^'

    print("유가증권 단축 종목코드 [" + recvvalue[0] + "]")
    print("영업시간 [" + recvvalue[1] + "]" + "시간구분코드 [" + recvvalue[2] + "]")
    print("======================================")
    print("매도호가10 [%s]    잔량10 [%s]" % (recvvalue[12], recvvalue[32]))
    print("매도호가09 [%s]    잔량09 [%s]" % (recvvalue[11], recvvalue[31]))
    print("매도호가08 [%s]    잔량08 [%s]" % (recvvalue[10], recvvalue[30]))
    print("매도호가07 [%s]    잔량07 [%s]" % (recvvalue[9], recvvalue[29]))
    print("매도호가06 [%s]    잔량06 [%s]" % (recvvalue[8], recvvalue[28]))
    print("매도호가05 [%s]    잔량05 [%s]" % (recvvalue[7], recvvalue[27]))
    print("매도호가04 [%s]    잔량04 [%s]" % (recvvalue[6], recvvalue[26]))
    print("매도호가03 [%s]    잔량03 [%s]" % (recvvalue[5], recvvalue[25]))
    print("매도호가02 [%s]    잔량02 [%s]" % (recvvalue[4], recvvalue[24]))
    print("매도호가01 [%s]    잔량01 [%s]" % (recvvalue[3], recvvalue[23]))
    print("--------------------------------------")
    print("매수호가01 [%s]    잔량01 [%s]" % (recvvalue[13], recvvalue[33]))
    print("매수호가02 [%s]    잔량02 [%s]" % (recvvalue[14], recvvalue[34]))
    print("매수호가03 [%s]    잔량03 [%s]" % (recvvalue[15], recvvalue[35]))
    print("매수호가04 [%s]    잔량04 [%s]" % (recvvalue[16], recvvalue[36]))
    print("매수호가05 [%s]    잔량05 [%s]" % (recvvalue[17], recvvalue[37]))
    print("매수호가06 [%s]    잔량06 [%s]" % (recvvalue[18], recvvalue[38]))
    print("매수호가07 [%s]    잔량07 [%s]" % (recvvalue[19], recvvalue[39]))
    print("매수호가08 [%s]    잔량08 [%s]" % (recvvalue[20], recvvalue[40]))
    print("매수호가09 [%s]    잔량09 [%s]" % (recvvalue[21], recvvalue[41]))
    print("매수호가10 [%s]    잔량10 [%s]" % (recvvalue[22], recvvalue[42]))
    print("======================================")
    print("총매도호가 잔량        [%s]" % (recvvalue[43]))
    print("총매도호가 잔량 증감   [%s]" % (recvvalue[54]))
    print("총매수호가 잔량        [%s]" % (recvvalue[44]))
    print("총매수호가 잔량 증감   [%s]" % (recvvalue[55]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[45]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[46]))
    print("시간외 총매도호가 잔량 [%s]" % (recvvalue[56]))
    print("시간외 총매수호가 증감 [%s]" % (recvvalue[57]))
    print("예상 체결가            [%s]" % (recvvalue[47]))
    print("예상 체결량            [%s]" % (recvvalue[48]))
    print("예상 거래량            [%s]" % (recvvalue[49]))
    print("예상체결 대비          [%s]" % (recvvalue[50]))
    print("부호                   [%s]" % (recvvalue[51]))
    print("예상체결 전일대비율    [%s]" % (recvvalue[52]))
    print("누적거래량             [%s]" % (recvvalue[53]))
    print("주식매매 구분코드      [%s]" % (recvvalue[58]))


menustr = "file_no,유가증권단축종목코드,주식체결시간,주식현재가,전일대비부호,전일대비,전일대비율,가중평균주식가격,주식시가,주식최고가,주식최저가,매도호가1,매수호가1,체결거래량,누적거래량,누적거래대금,매도체결건수,매수체결건수,순매수체결건수,체결강도,총매도수량,총매수수량,체결구분,매수비율,전일거래량대비등락율,시가시간,시가대비구분,시가대비,최고가시간,고가대비구분,고가대비,최저가시간,저가대비구분,저가대비,영업일자,신장운영구분코드,거래정지여부,매도호가잔량,매수호가잔량,총매도호가잔량,총매수호가잔량,거래량회전율,전일동시간누적거래량,전일동시간누적거래량비율,시간구분코드,임의종료구분코드,정적VI발동기준가\n"

def format_csv_purchased(data_cnt, data):
    ret = copy.deepcopy(menustr)
    for cnt in range(data_cnt):
        value_row = ""
        value_row += f"{cnt},"

        values = data.split('^')
        for value in values:
            value_row += f"{value},"
        value_row = value_row[:-1] 
        value_row += "\n"
        ret += value_row
    return ret
    # menulist = menustr.split('|')
    # pValue = data.split('^')
    # ret = ""
    # for cnt in range(data_cnt): 
    #     ret += f"file_no,"
    #     for menu in menulist:
    #         if menu == menulist[-1]: ret += f"{menu}\n" 
    #         else: ret += f"{menu},"
            
    #     ret += f"{cnt+1},"
    #     for i in range(len(menulist)):
    #         if menu == menulist[-1]: ret += f"{pValue[i]}\n"
    #         else: ret += f"{pValue[i]},"

# def aes_cbc_base64_dec(key, iv, cipher_text):
#     """
#     :param key:  str type AES256 secret key value
#     :param iv: str type AES256 Initialize Vector
#     :param cipher_text: Base64 encoded AES256 str
#     :return: Base64-AES256 decodec str
#     """
#     cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
#     return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))