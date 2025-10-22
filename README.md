# mcp_server_test

> github：https://github.com/modelcontextprotocol/python-sdk
>
> 参考教程：https://zhuanlan.zhihu.com/p/1892944764120310978
>
> 参考教程：https://www.51cto.com/aigc/5252.html

## 安装mcp开发库

```shell
pip install mcp
```

## 创建一个mcp服务

### 示例

```python
# custom_mcp.py
from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP()


@mcp.tool()
def list_desktop_files() -> list:
    """获取当前用户桌面上的所有文件列表（Linux和MacOS专属实现）"""
    desktop_path = os.path.expanduser("~/Desktop")
    return os.listdir(desktop_path)


@mcp.tool()
def opt_2_nums(a: int, b: int):
    """相交两个数字的结果"""
    # 相交是随便取的名字，方便测试验证
    ans = a * b
    return ans


if __name__ == "__main__":
    mcp.run(transport='sse')  # 启用调试模式

```

### 2种通信方式

* 本地通信：通过stdio传输数据，适用于在同一台机器上运行的客户端和服务器之间的通信

    ```python
    mcp.run(transport='stdio')
    ```

* 远程通信：利用SSE与HTTP结合，实现跨网络的实时数据传输，适用于需要访问远程资源或分布式部署的场景

    ```python
    mcp.run(transport='sse')
    ```

### 3种功能类型

* 资源（Resources）：类似文件的数据，可以被客户端读取，如 API 响应或文件内容

* 工具（Tools）：可以被 LLM 调用的函数（需要用户批准）

* 提示（Prompts）：预先编写的模板，帮助用户完成特定任务

## 本地验证效果

### 方式1：使用MCP inspector工具

安装必要工具

```shell
pip install "mcp[cli]"
```

执行命令：`mcp dev ./custom_mcp.py`

在网页中配置：

> Transport Type: stdio
>
> Command: python
>
> Arguments: ./custom_mcp.py

启动mcp服务： `Connect` -> `Tools` -> `List Tools`

选择需要测试tools，然后`Run Tool`


### 方式2：通过MCP客户端

这里以Cursor为例，在`Cursor Settings` -> `MCP` -> `New MCP Server`

修改文件：

```json
{
  "mcpServers": {
    "custom_mcp": {
      "command": "python",
      "args": ["/home/huatuo/github/mcp_server_test/custom_mcp.py"]
    }
  }
}
```

然后启动对话框，选择`Agent`，可以尝试输入以下内容

```
相交数字1和8的结果是什么
帮我看看桌面有什么文件
```

### 方式3：使用sse通信方式

这里以使用`Cline`工具为例，其他工具类似。

首先将mcp的通信方式改为`sse`，并启动服务，`python ./custom_mcp.py`

```log
INFO:     Started server process [161124]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:37390 - "GET /sse HTTP/1.1" 200 OK
```

在`Cline`中配置MCP服务，内容如下：

```json
{
  "mcpServers": {
    "custom_mcp": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    }
  }
}
```
