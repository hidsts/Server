#!/usr/bin/python3
def decode(inp):
    if inp:
        inp = inp.rstrip()  # 去尾部空格
        s = ''
        r = ''
        i = 0
        if len(inp)%4 == 0:
            max = len(inp)/4
            while i < max:
                j = 0
                k = 0
                if i == 0:
                    j = 0
                    k = 4
                else:
                    j = i * 4
                    k = j + 4

                s ='\\u' + inp[j:k] 
                r += s
                i += 1
        # print('Unicode Style:')
        # print(r)
        else:
            print('短信内容不是4的倍数!短信长度为：%s' %len(inp))
        r = r.encode('latin-1').decode('unicode_escape')
        
        return r




if __name__ == "__main__":
    print('Unicode数字格式化转中文,现在输入数据:')
    insert = input()
    result = decode(insert)
    print(result)