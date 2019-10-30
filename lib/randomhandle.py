"""随机相关模块"""
import random
import time


def create_code(en=2, num=2):
    """
    生成随机编码，可用于验证码或者用户id
    :param en: 英文单词的数量
    :param num: 数字的数量
    :return: type-str，随机编码，由en个英文与num个数字组成
    例如cs49
    """
    code = str()
    # 生成en个英文
    for i in range(en):
        asc_num = random.randint(97, 122)   # 随机一个ascii
        one_word = chr(asc_num)     # 得到一个词
        code += one_word  # 拼上
    # 生成num个数字
    for i in range(num):
        n = random.randint(0, 9)
        code += str(n)
    return code


if __name__ == '__main__':
    for i in range(10):
        res = create_code(2,3)
        print(res)