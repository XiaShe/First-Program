#爬取知乎网站“女生什么样的身材算是好身材”问题下所有图片，保存在本地文件夹内
#图片名为知乎答主昵称
#正则表达式
#实时显示爬取进度
#知乎界面为异步加载，本程序截获浏览器发给服务器的请求，分析出请求规律，伪装成浏览器不断向服务器发送请求
#如果第一个问题为视频，会弹出错误，更改页数即可
import requests
import os
import re

def get_Text(url):#获取html界面
    # user-agent 与 cookie: : 右键检查或者F12 Network - all 下拉
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        # r = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # 可修改，加速
        return r.text
    except:
        return ''

def get_Pictures(Purl):#获取图片链接并下载到本地
    count = 0
    html = get_Text(Purl)
    urls = re.findall(r'\"name\":\"\w*\"|https://pic\d.zhimg.com/v2-\w*r.jpg', html)#正则表达式
    scale = len(urls)
    for i in range(scale):
        count = count + 1
        print("\r当前页图片爬取进度: {:.2f}%".format(count * 100 / scale), end="")
        url = urls[i]#列表->字符串
        if url.startswith("\"name\""):#挑选出开头为"name"的字符串，赋值于name
            name = url
        else:
            root = "D://pics//"
            path = root + name.replace('\"', '').replace(':','').replace('name','') + "  " + url.split('/')[-1]
            # 答主名字+链接名字作为图片名字（链接名称为了去重），去掉多余字符
            try:
                if not os.path.exists(root):  # 判断文件夹是否存在
                    os.mkdir(root)  # 创建文件夹
                if not os.path.exists(path):
                    # 判断图片是否存在,由于本程序爬取知乎为异步加载，因此产生许多重复链接，元素去重用集合也可，不过会打乱顺序，不适合本程序
                    r = requests.get(url)
                    with open(path, 'wb') as f:
                        f.write(r.content)
                        # 返回二进制型数据，一般取图片文件使用，取文本使用r.text
                        f.close()
                        #print("文件保存成功")
                #else:
                    #print("文件已存在")
                #由于获取页面采用正则表达式爬取，有两个完全相同的url链接，故第二个忽略
            except:
                #print("爬取失败")
                print("\r当前页图片爬取进度: {:.2f}%".format(count * 100 /scale), end="")
                continue

def main():
    number = 0
    pages = 1
    while (number <= 20):#爬取“页数”
        url = "https://www.zhihu.com/api/v4/questions/333026642/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=" \
              + str(number) + "&platform=desktop&sort_by=default"
#         url = "https://www.zhihu.com/api/v4/questions/299205851/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset= " \
#               + str(number) + "&platform=desktop&sort_by=default" # 问题《有什么美得不可方物的壁纸？》
        print("正在爬取第{}页".format(pages))
        get_Pictures(url)
        print("\n")
        pages += 1
        number += 5

#分析 Request URL
# https://www.zhihu.com/api/v4/questions/333026642/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=8&platform=desktop&sort_by=default
# https://www.zhihu.com/api/v4/questions/333026642/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=13&platform=desktop&sort_by=default
# https://www.zhihu.com/api/v4/questions/333026642/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=18&platform=desktop&sort_by=default

if __name__ == '__main__':
    main()
