# xelatex wrapper

对 `xelatex` 进行包装。`wrapper` 在执行时会将参数原样传给 `xelatex` 以生成 `pdf` 文件，后将生成的 `pdf` 文件自动上传至 `cslabcms` 。

### 安装流程

以 `Windows` 为例。

1. 获取 `xelatex` 的安装目录。`Windows` 下可以在 `cmd` 环境下运行 `where xelatex` 得到。以下假设 `xelatex` 所在目录为 `C:\texlive\2019\bin\win32\xelatex.exe`。

2. 下载 `wrap.zip` 后解压，将 `wrap` 文件夹整体复制到 `xelatex` 目录中。此时原本的 `xelatex` 仍位于 `C:\texlive\2019\bin\win32\xelatex.exe`，而此 `wrapper` 中的 `xelatex` 应该位于 `C:\texlive\2019\bin\win32\wrap\xelatex.exe`。

3. 设置环境变量，在 `PATH` 的最前方（`GUI`界面的最上方）添加目录 `C:\texlive\2019\bin\win32\wrap`。

4. 设置完成后，在 `cmd` 环境下运行 `where xelatex` 应该得到 `wrap` 中的 `xelatex` 显示在原本的 `xelatex` 的上方。如：

   ```
   C:\>where xelatex
   C:\texlive\2019\bin\win32\wrap\xelatex.exe
   C:\texlive\2019\bin\win32\xelatex.exe
   ```

   如果命令的结果不正确，请确认环境变量设置正确。

5. 修改 `C:\texlive\2019\bin\win32\wrap\password.txt` ，将第一行改成 `cslabcms` 的用户名，第二行改成 `cslabcms` 的密码。

### 构建流程

从本仓库的源码构建 `wrapper`，需要安装以下环境：

```
pillow
urllib3
requests
tflite-runtime @ https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-win_amd64.whl
pyinstaller
```

需要注意 `tflite-runtime` 不支持某些版本的 python。详情请见 [tflite guide](https://tensorflow.google.cn/lite/guide/python?hl=zh-cn)。

安装完成后需要更改 `Lib\site-packages\tflite_runtime\interpreter.py` 中的内容：
```diff
- # pylint: disable=g-import-not-at-top
- if not __file__.endswith(os.path.join('tflite_runtime', 'interpreter.py')):
-   # This file is part of tensorflow package.
-   from tensorflow.python.util.lazy_loader import LazyLoader
-   from tensorflow.python.util.tf_export import tf_export as _tf_export
- 
-   # Lazy load since some of the performance benchmark skylark rules
-   # break dependencies. Must use double quotes to match code internal rewrite
-   # rule.
-   # pylint: disable=g-inconsistent-quotes
-   _interpreter_wrapper = LazyLoader(
-       "_interpreter_wrapper", globals(),
-       "tensorflow.lite.python.interpreter_wrapper."
-       "tensorflow_wrap_interpreter_wrapper")
-   # pylint: enable=g-inconsistent-quotes
- 
-   del LazyLoader
- else:
-   # This file is part of tflite_runtime package.
-   from tflite_runtime import tensorflow_wrap_interpreter_wrapper as _interpreter_wrapper
- 
-   def _tf_export(*x, **kwargs):
-     del x, kwargs
-     return lambda x: x
+ # This file is part of tflite_runtime package.
+ from tflite_runtime import tensorflow_wrap_interpreter_wrapper as _interpreter_wrapper
+ 
+ def _tf_export(*x, **kwargs):
+   del x, kwargs
+   return lambda x: x
```

可以看到此处检测了代码的文件名以判断归属和需要引入的包。但是 `pyinstaller` 在打包时会修改代码的文件名，因此需要修改该部分代码以强制选择引入 `tflite_runtime`。

此外还需要更改 `Lib\site-packages\urllib3\response.py` 

```diff
- try:
-     import brotli
- except ImportError:
-     brotli = None
+ brotli = None
```

否则在某些环境下可能会出现 `Module brotli has no member named ``error`` `。

接下来执行 `pyinstaller wrap.py` 完成打包。

随后复制 `password.txt` 和训练完成的 `model.tflite` 到包中。