import login
import upload

import re
import os
import sys
import subprocess

basedir = sys.path[0]
# 在 pyinstaller 打包后为 base_library.zip， 因此需要特殊处理
if os.path.split(basedir)[1] == 'base_library.zip':
  basedir = os.path.split(basedir)[0]
print('Xelatex upload wrapper v0.1 -- installed at {}'.format(basedir))
print('[Info] args:', sys.argv)

try:
  cmd = subprocess.run(['{}/../xelatex'.format(basedir), *sys.argv[1:]], stdout=sys.stdout, stderr=sys.stderr)
  if cmd.returncode != 0:
    print('[Error] xelatex 返回值不为零')
    sys.exit(cmd.returncode)
except FileNotFoundError:
  print('[Error] 在 `{}/../xelatex` 处找不到 xelatex ，请确认安装位置正确！'.format(basedir))
  sys.exit(1)


print('[Info] 正在准备上传')
username = ''
password = ''
try:
  with open(os.path.join(basedir, 'password.txt'), 'r') as f:
    username = f.readline()
    password = f.readline()
  assert username != '' and password != ''
except Exception:
  print('[Error] 在 `{}` 处读取登录账号密码失败'.format(os.path.join(basedir, 'password.txt')))
  sys.exit(0)

src = [x for x in sys.argv[1:] if x[0] != '-']
for x in src:
  pdf = os.path.splitext(x)[0] + '.pdf'
  if os.access(pdf, os.R_OK):
    res = re.match('^(\d+-\d+)-', os.path.split(pdf)[1])
    if res is None:
      print('[Info] PDF 文件 `{}` 已忽略'.format(pdf))
      continue
    homework = res.group(1)
    with open(pdf, 'rb') as f:
      pdfdata = f.read()
    print('[Info] 正在上传 `{}` 至 {}'.format(pdf, homework))
    session = login.login(username, password)
    # 在上传的文件名后增加学号
    filename = os.path.split(pdf)[1]
    filename = '{}-{}.pdf'.format(os.path.splitext(filename)[0], username)
    upload.upload(homework, session, filename, pdfdata)
