#!/usr/bin/python3

import UCS_2 as UCS2
import GSM_7bit as GSM


def decode(string):
    TP_SCA  = ''
    TP_OA   = ''
    TP_TYPE = ''
    TP_PID  = ''
    TP_DCS  = ''
    TP_SCTS = ''
    TP_UDL  = ''     # 当消息编码是GSM 7位默认字母表（取决于TP-DCS字段）时，TP-UDL以7位为单位给出TP-UD的长度; 否则TP-UDL以八位字节给出TP-UD的长度。
    TP_UD   = ''
    TP_UDHL = ''
    TP_UDH  = ''
    result = '0'
    if string:

        # sca:
        tmp = string[0:2]
        cnt = int(tmp)*2 +2                     # sca len

        TP_SCA = string[:cnt]
        i = 4
        if(int(TP_SCA[2:4]) == 91):
            a = '+'
        while( i < len(TP_SCA)):
            a += TP_SCA[i+1] + TP_SCA[i]
            i += 2
        if(str.rfind(a,"F")):
            a = a[:len(a) - 1]
        TP_SCA = a
        print('TP_SCA: %s' %TP_SCA)

        ## type:
        TP_TYPE = string[cnt:cnt+2]
        if TP_TYPE.isdigit():
            TP_TYPE = int(str(TP_TYPE),16)
        else:
            TP_TYPE = int(TP_TYPE,16)

        cnt += 2                                # type
        print('TP_TYPE: %s' %TP_TYPE)


        # oa:
        tmp = string[cnt:cnt+2]
        tmp = int(tmp,16)

        if tmp % 2 != 0:
            tmp += 1 

        # print(cnt)
        # print(tmp)
        # print('------------------------1')
        TP_OA = string[cnt:cnt + tmp + 4]                          
        i = 4
        # print(TP_OA)
        # print('------------------------2')
        if TP_OA[2:4].isdigit():
            if(int(TP_OA[2:4]) == 91):
                a = '+'
        a = ''
        while( i < len(TP_OA)):
            a += TP_OA[i+1] + TP_OA[i]
            i += 2
        if(str.rfind(a,"F")):
            a = a[:len(a) - 1]
        TP_OA = a

        cnt = cnt + tmp + 4                     # oa
        print('TP_OA: %s' %TP_OA)

        #  pid

        tmp = string[cnt:cnt+2]
        TP_PID = tmp

        cnt += 2                                # pid
        print('TP_PID: %s' %TP_PID)

        # dcs

        tmp = string[cnt:cnt+2]
        TP_DCS = tmp

        if TP_DCS.isdigit():                    # DCS转16进制
            TP_DCS = int(str(TP_DCS),16)
        else:
            TP_DCS = int(TP_DCS,16)

        cnt += 2                                # dcs
        print('TP_DCS: %s' %TP_DCS)

        # scts

        tmp = string[cnt:cnt+14]
        TP_SCTS = tmp

        i = 0
        a = '20'
        while(i < len(TP_SCTS)):
            a += TP_SCTS[i+1] + TP_SCTS[i]
            i += 2
            if  i == 2:
                a += '-'
            elif i == 4:
                a += '-'
            elif i == 6:
                a += ' '
            elif i == 8:
                a += ':'
            elif i == 10:
                a += ':'
            elif i == 12:
                break   # 不要时区
        TP_SCTS = a

        cnt += 14
        print('TP_SCTS: %s' %TP_SCTS)

        # udl

        tmp = string[cnt:cnt+2]

        if tmp.isdigit():
            TP_UDL = int(str(tmp),16)
        else:
            TP_UDL = int(tmp,16)

        cnt += 2                        # udl
        print('TP_UDL: %s' %TP_UDL)

        # ud

        if TP_TYPE & 64 == 64:      # 如果存在UDL
            TP_UDHL = string[cnt:cnt+2]
            print('TP_UDHL: %s' %TP_UDHL)

            TP_UDH  = string[cnt+2:cnt+2+int(TP_UDHL)*2]
            print('TP_UDH: %s' %TP_UDH)

            cnt = cnt + 2 + int(TP_UDHL) * 2

            tmp = string[cnt:cnt + TP_UDL*2]
            # tmp = string[cnt + 14:]

            TP_UD = tmp

        else:
            tmp = string[cnt:cnt + TP_UDL*2]
            # tmp = string[cnt:]

            TP_UD = tmp

        print('TP_UD: %s' %TP_UD)


        # decode
        if TP_DCS & 8 == 8:

            result = UCS2.decode(TP_UD)
            print('--------------------中文短信------------------------------')
            print(result)
            print('--------------------------------------------------')
        elif TP_DCS & 4 == 4:
            # 8bit
            print('8bit')
        else:
            result = GSM.decode(TP_UD)
            print('--------------------英文短信------------------------------')
            print(result)
            print('--------------------------------------------------')

    return result



if __name__ == "__main__":
    print('输入pdu编码:')
    string = input()
    r = decode(string)

    print('-----result-----')
    print(r)
    print('-----result-----')