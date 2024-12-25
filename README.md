<div align="center">
  <div style="display: inline-flex; align-items: center;">
    <img src="docs/images/logo.png" width="200" height="200" alt="AndPy Logo" style="margin-right: 20px;"/>
    <h1 style="margin: 0;">AndPy</h1>
  </div>
</div>

> A toy that runs Python scripts on Android devices.

AndPy 名字来源于 Android（“And”） 和 Python（“Py”） 的结合，意寓着 Android 和 Python 的结合。
AndPy 是一个基于 Python-for-Android 的 打包的 Android App，可以让你在 Android 上简单运行 Python 语言编写的脚本。

AndPy 使用Xtermjs模拟简单的终端界面，意味着你的命令行脚本无需其他改动即可在 Android 环境下与用户进行交互。
同时，AndPy 也支持你为脚本编写对应的前端界面，以便更好地展示你的脚本功能。

AndPy 在开发层面面向高级开发者，提供自由的 Python 环境，支持大量 Python 库的使用。
但在使用层面面向普通用户，提供了简单的界面，让用户可以轻松下载运行配置好的脚本。

## 特性
- **开发自由**：支持大量 Python 库的使用，且不限制Python脚本的编写格式
- **简单易用**：提供简单的界面，支持从在线脚本库、本地文件、Github仓库等方式一键导入脚本
- **多种运行方式**：同时支持命令行和前端界面两种运行方式
- **无需打包**：不需要编译打包的过程，即可在 Android 上运行 Python 脚本

## Python 库支持
我们将Python库分为三类：**Python标准库** 、**纯粹Python库** 和 **C扩展库或其他依赖的库**。

对于第一种标准库以及第二种纯粹使用Python语言编写的第三方库如requests，可以在AndPy中直接使用。

对于第三种C扩展库或其他依赖的库，的支持列表见Python-for-Android的支持列表[recipes列表](https://github.com/kivy/python-for-android/tree/develop/pythonforandroid/recipes)

> 补充：由于某些库仍然未能支持，AndPy 还提供调用js接口的方法（利用WebView），以便弥补python库的不足。
> 

## Terminal 限制
AndPy 使用Xtermjs模拟了一个终端界面提供给用户，但实际上只是重定向了Python的标准输入输出流，由前端Xtermjs进行显示，不具备终端的大部分功能。

## Android 环境下脚本编写限制
AndPy 尽最大努力允许用户自由编写 Python 脚本，但由于运行在 Android 环境下， 因此受到 Android 系统的限制，例如：可读写目录、网络访问等。
具体可见Python-for-Android的官方文档[Working on Android](https://python-for-android.readthedocs.io/en/latest/apis.html)