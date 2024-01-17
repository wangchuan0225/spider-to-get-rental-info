from lxml import  etree
import requests
from fake_useragent import UserAgent
import random  #随机模块

def find_house_rent(location,low,high):
    dict={
        '南山':'house-a087',
        '福田':'house-a085',
        '宝安':'house-a089',
        '龙华':'house-a091',
        '龙岗':'house-a093',
    }
    # 根据输入的地点找到对应的url编码，这里为了省力少写了点，将地点编码存在str1
    str1=dict[location]
    # 根据输入价格将价格的url部分编码组合在str2
    str2='/c2'+str(low)+'-d2'+str(high)
    # 加上rfss否则不让访问
    str3='/?rfss=1-260527b901a12e8422-25'
    # 初始url
    ini_url='https://sz.zu.fang.com/'
    # 组合
    url=ini_url+str1+str2+str3
    # 输出url方便检查
    print(url)
    # 创建User-Agent对象并创建随机报头
    ua = UserAgent()
    useragent = ua.random
    headers = {'User-Agent': useragent}
    # requests发送请求
    s=requests.get(url,headers=headers).text
    # 将传回的文件转化为html
    html=etree.HTML(s)
    # 根据lxml匹配原则找到每个标签下所需信息
    title_result = html.xpath('//dd[@class="info rel"]/p[@class="title"]')
    size_result=html.xpath('//dd[@class="info rel"]/p[@class="font15 mt12 bold"]/span[@class="splitline"]')
    price_result=html.xpath('//dd[@class="info rel"]/div[@class="moreInfo"]/p/span')
    # 创建list存储信息
    size_list=[]
    new_size=[]
    title_list=[]
    price_list=[]
    float_size=[]
    # size_result存储房子大小和朝向信息
    for i in size_result:
        text_content = etree.tostring(i, method='text', encoding='utf-8').decode('utf-8')
        new_size.append(text_content.strip().replace('|',''))
    for i in range(0,len(size_result),3):
        all=new_size[i]+' '+new_size[i+1].replace('�O','m2')+' '+new_size[i+2]
        float_size.append(float(new_size[i+1].replace('�O','')))
        size_list.append(all)
    # title存放标题信息
    for i in title_result:
        text_content = etree.tostring(i, method='text', encoding='utf-8').decode('utf-8')
        title_list.append(text_content.strip())
    # price存放价格信息
    for i in price_result:
        text_content = etree.tostring(i, method='text', encoding='utf-8').decode('utf-8')
        price_list.append(text_content.strip())
    # 将上述信息写入文档
    sum=0
    with open('rentprice.txt','w',encoding='utf-8') as f:
        for i in range(0,len(title_list)):
            f.write(str(sum)+'\n')
            print(sum)
            f.write(title_list[i]+'\n'+size_list[i]+'\n'+price_list[i]+ '\n')
            f.write('\n')
            sum+=1
    f.close()

if __name__=="__main__":
    location=input("输入深圳租房的区：")
    low=input("输入最低价格（1000-8000）：")
    high=input("输入最高价格（1000-8000）：")
    find_house_rent(location,low,high)










