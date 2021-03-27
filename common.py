import urllib
import urllib.request as request
import urllib.parse as parse
from urllib3 import encode_multipart_formdata


def dprint(*args,**kwargs):
  print(*args, **kwargs)


def GET(url, data={}, header={}):
  header = dict(header)
  header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
  data = parse.urlencode(data)
  req = request.Request(url + '?' + data, headers=header, method='GET')
  res = request.urlopen(req)
  return res.read().decode()


def POST(url, data={}, header={}):
  header = dict(header)
  header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
  data = parse.urlencode(data).encode()
  req = request.Request(url, data=data, headers=header, method='POST')
  try:
    res = request.urlopen(req)
  except urllib.error.HTTPError as err:
    print(err)
    print('url:', url)
    print('data:', data)
    print('header', header)
    raise err
  return res.read().decode()


def FORM(url, data={}, header={}):
  header = dict(header)
  encode = encode_multipart_formdata(data)
  header['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
  header['Content-Type'] = encode[1]
  data = encode[0]
  req = request.Request(url, data=data, headers=header, method='POST')
  req = request.urlopen(req)
  return req.read().decode()
