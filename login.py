import collections
import requests
from PIL import Image
import io

from common import *
import captcha

def remove_background(img):
  cnt = collections.defaultdict(lambda: 0)

  for y in range(img.size[0]):
    for x in range(img.size[1]):
      color = img.getpixel((y, x))
      cnt[color] += 1

  colors = sorted(cnt, key=lambda x:cnt[x], reverse=True)
  for y in range(img.size[0]):
    for x in range(img.size[1]):
      if img.getpixel((y, x)) != colors[1]:
          img.putpixel((y, x), (255, 255, 255))
  return img


def login(username, password):
  sess = requests.Session()
  sess.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'})

  req = sess.get('http://cslabcms.nju.edu.cn/login/captcha.php?r=')
  # img = ''
  # session = ''
  # try:
  #   res = request.urlopen(req)
  # except urllib.error.HTTPError as err:
  #   header = str(err.headers)
  #   l = header.find('MoodleSession=') + len('MoodleSession=')
  #   r = header.find(';', l)
  #   session = header[l:r]
  #   img = err.read()
  #   img = Image.open(io.BytesIO(img))
  img = Image.open(io.BytesIO(req.content))
  
  img = remove_background(img)
  capt = captcha.recognize(img)
  

  data = {'username': username, 'password': password, 'captcha': capt}
  res = sess.post('http://cslabcms.nju.edu.cn/login/index.php', data=data)
  # req = request.Request('http://cslabcms.nju.edu.cn/login/index.php',
  #   data=data, headers=header, method='POST')
  # res = request.urlopen(req)
  # header = str(res.headers)
  # print(header)
  # if res.read().decode().find('loginerrors') != -1:
  #   raise Exception('登录失败')
  if res.text.find('loginerrors') != -1:
    raise Exception('登录失败')
  return sess.cookies['MoodleSession']
