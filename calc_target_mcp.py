# custom_mcp.py
import os
import json
from mcp.server.fastmcp import FastMCP

HISTORY_JSON = 'history.json'

mcp = FastMCP()


def calc_target(target: int, numbers: list) -> bool:
    # 递归辅助函数，带过程追踪
    def helper(nums, exprs):
        if len(nums) == 1:
            # 允许浮点误差
            if nums[0] == target:
                return True, exprs[0]
            else:
                return False, None
        n = len(nums)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                # 剩下的数字和表达式
                next_nums = [nums[k] for k in range(n) if k != i and k != j]
                next_exprs = [exprs[k] for k in range(n) if k != i and k != j]
                a, b = nums[i], nums[j]
                ea, eb = exprs[i], exprs[j]
                # 四则运算
                for op in ['+', '-', '*', '/']:
                    # 除法时分母不能为0
                    if op == '/' and abs(b) < 1e-6:
                        continue
                    if op == '+':
                        val = a + b
                        exp = f'({ea}+{eb})'
                    elif op == '-':
                        val = a - b
                        exp = f'({ea}-{eb})'
                    elif op == 'x':
                        val = a * b
                        exp = f'({ea}*{eb})'
                    elif op == '/':
                        val = a / b
                        exp = f'({ea}/{eb})'
                    res, res_expr = helper(next_nums + [val], next_exprs + [exp])
                    if res:
                        return True, res_expr
        return False, None

    # 初始表达式为数字字符串
    res, expr = helper([int(x) for x in numbers], [str(x) for x in numbers])
    if res:
        return True, expr
    else:
        return False, ""


def init_history():
    def new_json():
        json_data = []
        json_str = json.dumps(json_data, indent=4, ensure_ascii=False)
        with open(HISTORY_JSON, 'w') as f:
            f.write(json_str)
        pass

    if not os.path.exists(HISTORY_JSON):
        new_json()
        return

    try:
        f = open(HISTORY_JSON, 'r', encoding='utf-8')
        json.load(f)
        f.close()
    except Exception as e:
        print(f"init_history: {e}")
        new_json()
    pass


@mcp.tool()
def calc_target_tool(target: int, numbers: list) -> dict:
    """计算给定数字是否可以通过加减乘除得到目标值"""
    sorted_numbers = sorted(numbers)
    success, expression = calc_target(target, numbers)

    init_history()
    with open(HISTORY_JSON, 'r') as f:
        history = json.load(f)
    history.append({
        "target": target,
        "numbers": sorted_numbers,
        "success": success,
        "expression": expression
    })
    json_str = json.dumps(history, indent=4, ensure_ascii=False)
    with open(HISTORY_JSON, 'w') as f:
        f.write(json_str)

    return {
        "target": target,
        "numbers": sorted_numbers,
        "success": success,
        "expression": expression
    }


@mcp.resource("calc://history")
def get_calc_target_history() -> list:
    """获取计算目标的历史记录"""
    init_history()
    with open(HISTORY_JSON, 'r') as f:
        history = json.load(f)
    return history


@mcp.prompt()
def format_calc24_report(result: dict) -> str:
    """将calc_target_tool计算结果用标准报告格式展示"""
    output_log = f"""
    计算报告：
    对于数字集合：{result.get('numbers')}
    目标值：{result.get('target')}
    计算结果：{"成功" if result.get('success') else "失败"}
    表达式：{result.get('expression') if result.get('success') else "无"}
    """
    return output_log


if __name__ == "__main__":
    mcp.run(transport='stdio')
