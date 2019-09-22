'''
    登录药智网 https://www.yaozh.com/
    有以下几点需要注意
        1 requests.Session() 真是个好东西。自动跟着session
        2 同一个URL，这里是特指登录的url，（有可能是一类，一叶知秋），客户端以GET/POST 不同的方式请求时，服务福返回不同的内容
        3 这个网站服务器就用到了表单中的隐藏字段（hidden field），将登录URL以POST向服务器发起请求，只有账户名，密码，但没有隐藏字段的值 ，服务器认定登录不成功
            隐藏字段在登录url 以GET请求访问时，查看网页源代码会有。（不知道是不是一大类）


'''



import requests
from bs4 import BeautifulSoup
# 登录成功后的页面。必须有cookie才能看到相关信息
target_url = 'https://www.yaozh.com/member/'
headers = {
    'User-Agent':'User-Agent',
}
#对同一个登录url，当时GET请求时，服务器返回登录的界面，当是POST请求是，服务器返回登录结果（成功/失败）

login_url = 'https://www.yaozh.com/login/'

def get_formhash_and_backurl(session,url):

    r_login_get = session.get(url=login_url,headers=headers)
    if r_login_get.status_code == 200:
        bs_login_get = BeautifulSoup(r_login_get.text,'lxml')
        formhash = bs_login_get(name='input',id='formhash')[0].attrs['value']
        backurl = bs_login_get(name='input',id='backurl')[0].attrs['value']

        return {'formhash':formhash,'backurl':backurl}

#用requests的会话对象记录cookies
session= requests.Session()

res = get_formhash_and_backurl(session,login_url)

#下面两个字段就是 表单内容中的隐藏字段（hidden field），如果post的时候，没有这些值，登录不会成功

formhash = res.get('formhash')
backurl = res.get('backurl')

data = {
    'username':'zuoguoliang',
    'pwd':'654321cc',
    'formhash':formhash,
    'backurl':backurl,
}

#带上data，给登录url发送POST请求。
session.post(url=login_url,data=data,headers=headers)
#登录成功后，自然就带着相关的cookie。在访问其它的url，就不再是未登录的状态。
r = session.get(url=target_url,headers=headers)

if r.status_code == 200:
    f = open('day4_1.html','w',encoding='UTF-8')
    f.write(r.text)
    f.close()
