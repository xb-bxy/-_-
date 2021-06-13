import time
import requests
import re

proxies = {'https': '192.168.3.83:7890'}

def get_windows_request(url):
    hd = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    time.sleep(0.5)
    rst = requests.get(url, headers=hd, proxies=proxies)
    rst.encoding = "utf-8"

    return rst.text


def get_phone_request(url):
    hd = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36"}
    time.sleep(0.5)
    rst = requests.get(url, headers=hd, proxies=proxies)
    rst.encoding = "utf-8"
    # f = open('./hhh.html', 'w')
    # f.write(rst.text)
    # f.close()

    return rst.text


def playListID():
    """
    从 https://music.163.com/discover/playlist 网址获取歌单id
    :return: [歌单id,歌单名]
    """

    url = 'https://music.163.com/discover/playlist'
    html = get_windows_request(url)
    listid = re.findall(r'playlist[?]id=(\d+).*?tit.*?>(.*?)</a', html)

    print("歌单id获取成功")
    return listid



def playListUrl():
    """
      从 https://music.163.com/discover/playlist 网址获取歌单url
      :return: [歌单url,歌单名]
    """

    listurl = []
    url = 'https://music.163.com/discover/playlist'
    html = get_windows_request(url)
    list = re.findall(r'playlist[?]id=(\d+).*?tit.*?>(.*?)</a', html)
    # print(list)
    for i in range(len(list)):
        lp = 'https://music.163.com/#/playlist?id=' + list[i][0]
        listurl.append([lp,list[i][1]])
    return listurl




def songList(playListID):
    """
    :param playListID: 歌单id
    :return: [歌曲id,歌曲名称]
    """

    url = 'https://music.163.com/playlist?id=%s'
    # print(url % playListID)
    html = get_windows_request(url % playListID)
    song = re.findall(r'/song[?]id=(\d+).*?>(.*?)</a',html)
    print("歌曲获取成功")
    return song


def review(songID):
    """
    :param songID : 歌曲id
    :return: data:歌名，评论者名，评论内容，评论时间
    """
    url = "https://y.music.163.com/m/song?id=%s"
    data = []
    html = get_phone_request(url % songID)
    songname = re.findall(r':[{]"name":"(.*?)"',html)
    pin = re.findall(r'"nickname":"(.*?)".*?"content":"(.*?)".*?time":(\d+)',html)
    for i in pin:
        data.append([songname[0],i[0],i[1],i[2]])

    return data




if __name__ == '__main__':
    p = playListID()
    list = []
    a = [] # 数组格式[[[歌名,评论者名,评论内容,评论时间],...],...]
    for l in range(len(p)):
        list.append(songList(p[l][0]))
    for o in list:
        print("共%s个歌单" % range(len(list)))
        for i in o:
            print("第%s首歌的评论获取成功" % i)
            a.append(review(i[0]))


    print(a)



