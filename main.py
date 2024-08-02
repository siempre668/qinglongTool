"""
任务名称
name: qinglongTool
定时规则
cron: 1 9 * * *
"""

import json
import traceback
import time

import requests
from json import dumps as jsonDumps
import os

api_host = "localhost:5700"
api_host1 = "192.168.50.70:5700"

api_Path = "/api"
api_Path1 = "/open"

client_id = "ZHJDK_0kO1g0"
client_secret = "EOGn7Kt-Bhq2r8BvkOWqfNfu"

api_headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Content-Type":"application/json"
}


class QL:
    def __init__(self, id: str, secret: str) -> None:
        """
        初始化
        """
        self.id = id
        self.secret = secret

        self.log(f"")
        self.log(f"正在初始化")
        self.log(f"尝试本地文件获取token")

        self.api_Path = api_Path
        self.api_url = f"http://{api_host}" + self.api_Path
        token = self.get_token()
        if (token is None):
            self.log(f"尝试使用应用密钥登录获取token")
            self.api_Path = api_Path1
            self.api_url = f"http://{api_host1}" + self.api_Path
            self.login()
        else:
            self.auth= f"Bearer {token}"
            self.log(f'本地文件获取token成功：{token}')

        api_headers["Authorization"] = self.auth

        self.api_headers=api_headers
        self.log(f'self_headers：{self.api_headers}')


    def log(self, content: str) -> None:
        """
        日志
        """
        print(content)

    def get_token(self) -> str or None:
        path = '/ql/config/auth.json'  # 设置青龙 auth文件地址
        if not os.path.isfile(path):
            path = '/ql/data/config/auth.json'  # 尝试设置青龙 auth 新版文件地址

        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("token")
            except Exception:
                self.log(f"❌无法获取 token!!!\n{traceback.format_exc()}")
                return None
        else:
            self.log(f"❌文件不存在：{path}")

    def login(self) -> None:
        """
        登录
        """
        url = f"{self.api_url}/auth/token?client_id={self.id}&client_secret={self.secret}"
        try:
            self.log(f"登录青龙")
            rjson = requests.get(url).json()
            self.log(f"登录地址：{url}")
            self.log(f"登录结果：{rjson}")
            if (rjson['code'] == 200):
                self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
                self.log(f"登录成功：{self.auth}")
            else:
                self.log(f"登录失败：{rjson['message']}")
        except Exception as e:
            self.valid = False
            self.log(f"登录失败：{str(e)}")

    def getEnvs(self) -> list:
        """
        获取环境变量
        """
        url = f"{self.api_url}/envs?searchValue="
        try:
            rjson = requests.get(url, headers=self.api_headers).json()
            if (rjson['code'] == 200):
                return rjson['data']
            else:
                self.log(f"获取环境变量失败：{rjson['message']}")
        except Exception as e:
            self.log(f"获取环境变量失败：{str(e)}")

    def deleteEnvs(self, ids: list) -> bool:
        """
        删除环境变量
        """
        url = f"{self.api_url}/envs"
        try:
            rjson = requests.delete(url, headers=self.api_headers, data=jsonDumps(ids)).json()
            if (rjson['code'] == 200):
                self.log(f"删除环境变量成功：{len(ids)}")
                return True
            else:
                self.log(f"删除环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"删除环境变量失败：{str(e)}")
            return False

    def addEnvs(self, envs: list) -> bool:
        """
        新建环境变量
        """
        url = f"{self.api_url}/envs"
        try:
            rjson = requests.post(url, headers=self.api_headers, data=jsonDumps(envs)).json()
            if (rjson['code'] == 200):
                self.log(f"新建环境变量成功：{len(envs)}")
                return True
            else:
                self.log(f"新建环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"新建环境变量失败：{str(e)}")
            return False

    def updateEnv(self, env: dict) -> bool:
        """
        更新环境变量
        """
        url = f"{self.api_url}/envs"
        try:
            rjson = requests.put(url, headers=self.api_headers, data=jsonDumps(env)).json()
            if (rjson['code'] == 200):
                self.log(f"更新环境变量成功")
                return True
            else:
                self.log(f"更新环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"更新环境变量失败：{str(e)}")
            return False

    def getLogList(self) -> list:
        """
        获取日志列表
        """
        url = f"{self.api_url}/logs"
        try:
            rjson = requests.get(url, headers=self.api_headers).json()
            if (rjson['code'] == 200):
                return rjson['data']
            else:
                self.log(f"获取日志列表异常:{str(rjson)}")
        except Exception as e:
            self.log(f"获取日志列表出错:{str(e)}")

    def getLogContent(self, urlParam: str) -> list:
        """
        获取日志内容
        """
        url = f"{self.api_url}{urlParam}"
        try:
            rjson = requests.get(url, headers=self.api_headers).json()
            if (rjson['code'] == 200):
                return rjson['data']
            else:
                self.log(f"获取日志内容异常:{str(rjson)}")
        except Exception as e:
            self.log(f"获取日志内容出错:{str(e)}")

    def deleteLog(self, filename: str, path: str):
        """
        删除日志
        """
        data = {
            "filename": filename,
            "path": path,
            "type": "directory"
        }
        t = round(time.time() * 1000)
        url = f"{self.api_url}/logs?t={t}"
        try:
            rjson = requests.delete(url, headers=self.api_headers, data=jsonDumps(data)).json()
            if (rjson['code'] == 200):
                self.log(f"删除日志文件夹:{filename}")
            else:
                self.log(f"删除日志内容异常:{str(rjson)}")
        except Exception as e:
            self.log(f"删除日志内容出错:{str(e)}")

    def getLogKeyWord(self,keyWord:str) -> list:
        """
        查找日志
        """
        result = ql.getLogList()
        # print(result)
        for index, value in enumerate(result):
            if 'title' in value:
                if 'children' in value:
                    for index, children in enumerate(value['children']):
                        if 'key' in children:
                            urlParam = f"/logs/detail?file={children['title']}&path={children['parent']}"
                            content = ql.getLogContent(urlParam)
                            if content.find(keyWord) > -1:
                                self.log(f"已找到日志文件:{urlParam}")
                                self.log(content)

    def deleteLogAll(self) -> list:
        """
        删除日志文件
        """
        result = ql.getLogList()
        # self.log(f":{result}")
        for index, value in enumerate(result):
            if 'title' in value:
                self.log(f"即将删除：{value['title']}")
                ql.deleteLog(value['title'], "")


if __name__ == "__main__":
    # 登录即初始化参数
    ql = QL(client_id, client_secret)

    # 查找日志
    ql.getLogKeyWord("Jd转赚红包_抽奖提现")

    # 删除日志
    # ql.deleteLogAll()

    # envs = ql.getEnvs()
    # print(envs)
