import requests
from urllib.parse import urljoin
import json

# 配置区（必须修改！！）=================================
BASE_URL = "https://jw1.hustwenhua.net/jwglxt/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N2151&layout=default"  # 教务系统基础地址
API_PATH = "https://jw1.hustwenhua.net/jwglxt/kbcx/xskbcx_cxXsgrkb.html?gnmkdm=N2151"  # API相对路径
COOKIE = "JSESSIONID=3967058E5821674BB119E5AB5DFCC9C6; route= a4672ac87716ba996012ae61bccbd880"  # 从浏览器Application→Cookies复制

# 从浏览器Network面板复制的完整参数
PARAMS = {
    "xnm": "2024",  # 学年
    "xqm": "3",  # 学期代码
    "kzlx": "ck"  # 查询类型
}


# ====================================================

def format_course(course):
    """格式化单门课程信息"""
    return f"""
课程名称: {course.get('kcmc', '无')}
教师: {course.get('xm', '无')}
时间: 周{course.get('zcd', '')} {course.get('xqjmc', '')} {course.get('jc', '')}节
地点: {course.get('cdmc', '无')}
周数: {course.get('zcd', '')}
""".strip()


def get_timetable():
    try:
        # 拼接完整URL（避免手动拼接错误）
        api_url = urljoin(BASE_URL, API_PATH)

        # 完整请求头（从浏览器Network面板复制）
        headers = {
            "Cookie": COOKIE,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Referer": urljoin(BASE_URL, "jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"),
            "X-Requested-With": "XMLHttpRequest"
        }

        # 发送请求（POST/GET根据实际情况修改）
        response = requests.post(
            api_url,
            headers=headers,
            data=PARAMS,  # 如果是GET请求改为 params=PARAMS
            timeout=10
        )
        response.raise_for_status()  # 检查HTTP错误

        # 解析JSON数据
        data = response.json()

        # 检查是否有课表数据
        if 'kbList' not in data:
            print("返回数据中没有找到课表信息")
            return

        print("\n=== 我的课表 ===")
        print(f"学期: {PARAMS['xnm']}-{PARAMS['xqm']}")
        print("=" * 40)

        # 按课程输出
        for course in data['kbList']:
            print(format_course(course))
            print("-" * 40)

    except requests.exceptions.ConnectionError:
        print("\n⚠ 网络连接失败！请检查：")
        print("1. 是否连接到校园网/VPN（教务系统通常需内网访问）")
        print("2. 浏览器直接访问以下URL测试是否可达：")
        print(f"   {urljoin(BASE_URL, API_PATH)}")
        print("3. 关闭电脑代理/防火墙临时测试")

    except Exception as e:
        print(f"\n⚠ 发生错误: {type(e).__name__}")
        print(f"错误详情: {str(e)}")
        if hasattr(e, 'response'):
            print(f"HTTP状态码: {e.response.status_code}")
            print("服务器返回:", e.response.text[:500])


if __name__ == "__main__":
    get_timetable()