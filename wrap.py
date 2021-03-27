import login
import upload

import re
import os
import sys
import subprocess

dir = sys.path[0]
print('Xeletax upload wrapper v0.1 -- ', dir)

try:
  cmd = subprocess.run(['{}/../xelatex'.format(dir), *sys.argv[1:]], stdout=sys.stdout, stderr=sys.stderr)
  if cmd.returncode != 0:
    print('执行失败')
    sys.exit(cmd.returncode)
except FileNotFoundError:
  print('在 `{}/../xelatex` 处找不到 xelatex ，请确认安装位置正确！'.format(dir))

username = ''
password = ''
try:
  with open(os.path.join(dir, 'password.txt'), 'r') as f:
    username = f.readline()
    password = f.readline()
  assert username != '' and password != ''
except Exception:
  print('在 `{}` 处读取登录账号密码失败'.format(os.path.join(dir, 'password.txt')))
  sys.exit(0)

src = [x for x in sys.argv[1:] if os.path.splitext(x)[1] == '.tex']
for x in src:
  pdf = os.path.splitext(x)[0] + '.pdf'
  if os.access(pdf, os.R_OK):
    res = re.match('^(\d+-\d+)-', os.path.split(pdf)[1])
    if res is None:
      print('PDF 文件 `{}` 已忽略'.format(pdf))
      continue
    homework = res.group(1)
    with open(pdf, 'rb') as f:
      pdfdata = f.read()
    print('正在上传 `{}` 至 {}'.format(pdf, homework))
    session = login.login(username, password)
    upload.upload(homework, session, os.path.split(pdf)[1], pdfdata)
