from common import *
import login
import json

def parse_info(data):
  anchor = 'http://cslabcms.nju.edu.cn/repository/draftfiles_manager.php'
  l = data.find(anchor)
  assert l != -1
  r = data.find('\'', l)
  assert r != -1
  info = {}
  for x in data[l+len(anchor)+1:r].split('&amp;'):
    [k, v] = x.split('=')
    info[k] = v
  
  pos = data.find('"author":')
  assert pos != -1
  l = data.find('"', pos + 8)
  assert l != -1
  r = data.find('"', l + 1)
  assert r != -1
  info['author'] = json.loads(data[l:r+1])
  return info


def upload(homework, session, filename, filedata):
  header = {'Cookie': 'MoodleSession={}'.format(session)}

  # 获取作业id
  dprint('正在获取作业{}的id'.format(homework))
  res = GET('http://cslabcms.nju.edu.cn/course/view.php',
    data={'id': 843}, header=header)
  pos = res.find(homework)
  assert pos != -1
  anchor = 'http://cslabcms.nju.edu.cn/mod/assign/view.php?id='
  pos = res.rfind(anchor, 0, pos)
  assert pos != -1
  homework_id = res[pos + len(anchor):res.find('"', pos)]
  dprint('作业{}的id为{}'.format(homework, homework_id))

  # 开始提交，获取上传所需的临时容器
  res = GET('http://cslabcms.nju.edu.cn/mod/assign/view.php',
    data={'id': homework_id, 'action': 'editsubmission'},
    header=header)
  info = parse_info(res)
  dprint('上传相关信息:', info)

  # 删除已有提交
  existed = POST('http://cslabcms.nju.edu.cn/repository/draftfiles_ajax.php?action=list',
    data={'sesskey': info['sesskey'], 'filepath': '/', 'itemid': info['itemid']},
    header=header)
  existed = json.loads(existed)
  for file in existed['list']:
    dprint('正在删除提交', file['filepath'], file['filename'])
    res = POST('http://cslabcms.nju.edu.cn/repository/draftfiles_ajax.php?action=delete',
      data={'sesskey': info['sesskey'], 'filepath': file['filepath'], 'itemid': info['itemid'], 'filename': file['filename']},
      header=header)

  # 上传文件
  dprint('正在上传{}'.format(filename))
  data = {
    'action': (None, 'upload'),
    'repo_upload_file': (filename, filedata),
    'sesskey': (None, info['sesskey']),
    'repo_id': (None, 4),
    'itemid': (None, info['itemid']),
    'author': (None, info['author']),
    'savepath': (None, '/'),
    'title': (None, filename),
    'ctx_id': (None, info['ctx_id'])
  }
  res = FORM('http://cslabcms.nju.edu.cn/repository/repository_ajax.php',
    data=data, header=header)

  # 提交，保存更改
  dprint('正在保存更改')
  data = {
    'id': homework_id,
    'action': 'savesubmission',
    'sesskey': info['sesskey'],
    '_qf__mod_assign_submission_form': "1",
    'files_filemanager': info['itemid'],
    'submitbutton': '保存更改',
  }
  result = POST('http://cslabcms.nju.edu.cn/mod/assign/view.php',
    data=data, header=header)

if __name__ == '__main__':
  import os
  import sys
  import getopt

  homework = ''
  username = ''
  password = ''
  filename = ''
  filedata = ''

  opts, args = getopt.getopt(sys.argv[1:], 'u:p:h:f:', ['username=', 'password=', 'homework=', "file="])
  
  for opt, arg in opts:
    if opt in ('-h', '--homework'):
      homework = arg
    elif opt in ('-f', '--file'):
      filename = arg
    elif opt in ('-u', '--username'):
      username = arg
    elif opt in ('-p', '--password'):
      password = arg
  
  if homework == '' or filename == '':
    raise getopt.GetoptError('参数不能为空')
  
  session = login.login(username, password)

  with open(filename, 'rb') as f:
    filedata = f.read()
  
  upload(homework, session, os.path.split(filename)[1], filedata)
