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
