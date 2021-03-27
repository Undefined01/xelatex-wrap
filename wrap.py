import upload

import os
import sys
import subprocess

dir = os.path.split(sys.path[0])[0]
print('Wrapper at', dir)
print('Wrapper get', sys.argv)
cmd = subprocess.run(['{}/../xelatex'.format(dir), *sys.argv[1:]], stdout=sys.stdout, stderr=sys.stderr)
if cmd.returncode != 0:
  print('执行失败')
  sys.exit(cmd.returncode)

src = [x for x in sys.argv[1:] if x.endswith('.tex')]
for x in src:
  pdf = x[:-4] + '.pdf'
  if os.access(pdf, os.R_OK):
    print('PDF 文件已找到：', pdf)
