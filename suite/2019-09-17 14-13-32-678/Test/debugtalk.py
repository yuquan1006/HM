# debugtalk.py
# import requests.utils.dict_from_cookiejar
import re,time

def get_token(content):
    '''
    获取文本中token值
    '''
    print(content)
    result = re.findall("XSRF-TOKEN=(.{36})", content)[0]
    return result


def getTime_Foryyyyddmm():
    '''
    获取当前时间 yyyy-mm-dd
    '''
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))


def sum_status_code(status_code, expect_sum):
    """ sum status code digits
        e.g. 400 => 4, 201 => 3
    """
    sum_value = 0
    for digit in str(status_code):
        sum_value += int(digit)

    assert sum_value == expect_sum
