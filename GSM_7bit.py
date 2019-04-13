#!/usr/bin/python3

gsm_7bit_alphabet_table =  ['@','£','$','¥','è','é','ù','ì','ò','Ç','\n','Ø','ø','\r','Å','å','Δ','_','Φ','Γ','Λ','Ω','Π','Ψ','Σ','Θ','Ξ','\x1b','Æ','æ','ß','É',' ','!','\"','#','¤','%','&','\'','(',')','*','+',',','-','.','/','0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','i','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Ä','Ö','Ñ','Ü','§','¿','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ä','ö','ñ','ü','à']



def string2hex(string):  
    result = []     
    lens = len(string)

    if lens % 2 == 0:

        i = 0
        while i < lens:
            result.append(string[i:i+2])
            i += 2
        
        return result



def string2dec(string):
    result = []
    for x in string:
        r = gsm_7bit_alphabet_table.index(x)
        result.append(r)

    return result



def string2dec_test(string):
    result = []
    for x in string:
        r = ord(x)
        result.append(r)

    return result



def hex2bin(lists):
    result = []
    for x in lists:
        tmp = str(x)        # 数字转换成字符串
        tmp = int(tmp,16)   # 十六进制转十进制
        tmp = bin(tmp)      # 十进制转二进制
        
        lens = len(tmp)     # 获取

        tmp = tmp[2:lens]      # 去除 '0b'
        i = 0
        a = ''
        while lens - 2 + i < 8:     # 这里犯了两个低级错误导致转出的二进制不足八位。1是没用while用了if，2是没用8用的7判断，小于7就是说当字符串有7位就不用添零了，但是后期必须要八位才能解码不出错！！
            # if x == lists[len(lists) - 1]:      # 这里加判断是因为解码的时候其他字节不足8位都要用0填充，但最后一位必须保持纯净，不能填充，不然解码的时候会出错！（注：之前用的是倒序解码，所以这里要判断，现在用的顺序解码，不存在此问题）
            #     break
            a += '0'
            i += 1
        tmp = a + tmp

        result.append(tmp)

    return result



def hex2bin_test(lists):
    result = []
    for x in lists:
        tmp = str(x)        # 数字转换成字符串
        tmp = int(tmp,16)   # 十六进制转十进制
        tmp = bin(tmp)      # 十进制转二进制
        
        lens = len(tmp)     # 获取

        tmp = tmp[2:lens]      # 去除 '0b'
        i = 0
        a = ''
        while lens - 2 + i < 8:     # 这里犯了两个低级错误导致转出的二进制不足八位。1是没用while用了if，2是没用8用的7判断，小于7就是说当字符串有7位就不用添零了，但是后期必须要八位才能解码不出错！！
            if x == lists[len(lists) - 1]:      # 这里加判断是因为解码的时候其他字节不足8位都要用0填充，但最后一位必须保持纯净，不能填充，不然解码的时候会出错！
                break
            a += '0'
            i += 1
        tmp = a + tmp

        result.append(tmp)

    return result



def bin2hex(lists):
    result = []
    for x in lists:
        tmp = int(x,2)      # 先转十进制
        tmp = hex(tmp)      # 转十六进制
        tmp = tmp[2:4]      # 取后两位
        if len(tmp) < 2:        # 必须有两位 ，不足后期会出错
            tmp = str(0) + tmp

        result.append(tmp)
    
    return result



def bit_7_to_8(lists):
    result = []
    i = 0
    while len(lists) - 1 > 0:
        current_byte = lists[i]

        if current_byte:
            current_len = len(current_byte)

            next_byte = lists[i + 1]

            next_len = len(next_byte)

            need = 8 - current_len

            if need < next_len:
                tmp = next_byte[:next_len - need]

                next_byte = next_byte[next_len - need:]

            else:
                tmp = ''

            current_byte = next_byte + current_byte
            
            result.append(current_byte)

            lists[i + 1] = tmp

            del lists[i]
        else:
            del lists[i]
            continue
    if lists[i]:
        result.append(lists[i])

    return result



def bit_8_to_7(lists): # 倒序解码，比较容易出问题，弃用，现在用顺序解码
    result = []
    lens = len(lists)
    while lens > 0:
        current_byte = lists[lens - 1]      # 获取最后一个数据

        if current_byte:                    # 判断是否为空

            if len(current_byte) == 8:      # 如果是8位直接取7位写入result 剩下一位做处理
                
                data = current_byte[:7]

                current_byte = current_byte[7:]

                result.append(data)

            if len(current_byte) < 7:
            
                need = 7 - len(current_byte)

                before_byte = lists[lens - 2]       # 得到前一字节

                before_len = len(before_byte)

                
                if need < before_len:
                    tmp = before_byte[need:]
                    before_byte = before_byte[:need]
                else:
                    before_byte = before_byte[:before_len]
                    tmp = ''
                
                current_byte += before_byte
                lists[lens - 2] = tmp

                result.append(current_byte)
            else:
                result.append(current_byte)
            del lists[lens - 1]
            tmp = ''
            lens -= 1
    result.reverse()        # 列表反转

    return result



def bit_8_to_7_test(lists):
    result = []
    lists.append('')
    while len(lists) > 0:
        i = 0
        current_byte = lists[i]    

        if current_byte:                  

            if len(current_byte) == 8:     
                
                extra = current_byte[:len(current_byte)-7]

                current_byte = current_byte[len(current_byte)-7:]

                result.append(current_byte)

                lists[i] = extra

            elif len(current_byte) == 7:
            
                result.append(current_byte)

                del lists[i]

            else:
                
                need = 7 - len(current_byte)

                next_byte = lists[i + 1]

                if next_byte:

                    next_byte += current_byte

                    extra = next_byte[:len(next_byte) - len(current_byte) - need]
                    
                    current_byte = next_byte[len(next_byte) - len(current_byte) - need:]


                    result.append(current_byte)

                    lists[i + 1] = extra

                    del lists[i]
                else:
                    result.append(current_byte)
                    del lists[i]
        else:
            del lists[i]
            continue

    return result



def bin2dec(lists):
    result = []
    for x in lists:
        result.append(int(x,2))

    return result



def dec2string(lists):
    result = []
    for x in lists:
        # print(alphabet[int(x)])
        result.append(gsm_7bit_alphabet_table[x])
    
    return result



def dec2bin(lists):
    result = []

    for x in lists:
        # if x == 32:             # 这里加了判断之后可以将 'Get Out' 解析成 'GetOut' 不加解析是 'ÅKiAOut'
        #     tmp = '0' + str(100000)
        #     result.append(tmp)
        #     continue
        tmp = bin(x)

        tmp = tmp[2:]

        if len(tmp) < 7:        # 必须有7位 ，后期编码位数不足，会编错
            tmp = str(0) + tmp

        result.append(tmp)

    return result



def encode(string):
    result = ''

    # 输入字符串转十进制列表
    lists = string2dec_test(string)

    # 十进制转换二进制
    lists = dec2bin(lists)

    # 编码，7bit 打包成 8bit
    lists = bit_7_to_8(lists)

    # 转十六进制
    lists = bin2hex(lists)

    # 十六进制列表打包成字符串
    for x in lists:
        result += x

    return result.upper()   # 全部转大写输出



def decode(string):
    result = ''

    # 输入字符串转十六进制列表
    lists = string2hex(string)

    # 十六进制转二进制
    lists = hex2bin(lists)

    # 解码，8bit 拆分为 7bit
    lists = bit_8_to_7_test(lists)

    # 转十进制
    lists = bin2dec(lists)

    # 十进制转对应的字符
    lists = dec2string(lists)

    # 字符列表打包成字符串
    for x in lists:
        result += x
    result = result[:len(result)-1]     # 现在的解码方式最后总是会有个@，暂时用这个方法去掉
    
    return result




if __name__ == "__main__":

    print('输入要解码的字符串如：\'CD72990EA2BF41ED72990ECABFEB2E50F2D406D9CBF23C081D86C3F3A15FE8E77201\'')
    inp = input()
    out = decode(inp)
    print('')
    print(out)


    # # inp = 'it\'s ok...and very good yes \'!@#$%^&*()\'a'
    # inp = 'This is English test'
    # print(inp)
    # print('上面是原字符串')
    # print('')



    # inp = encode(inp)
    # print(inp)
    # print('上面是编码后的十六进制数')
    # print('')


    # # inp = '54747A0E4ACF4145F7999D9EA341F4F29C0E'

    # # inp = '54747A0E4ACF4145'

    # out = decode(inp)
    # print('')
    # print(out)
    # print('上面是解码后的字符串')
