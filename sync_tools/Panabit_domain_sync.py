import os
import requests
import json
import time
import urllib3
from requests_toolbelt.multipart.encoder import MultipartEncoder

urllib3.disable_warnings()

class PanabitAPI:
    def __init__(self, ip, username, password):
        self.base_url = f"https://{ip}/api/panabit.cgi"
        self.username = username
        self.password = password
        self.token = self.login()

    def login(self):
        """登录获取token"""
        payload = {
            "api_action": "api_login",
            "username": self.username,
            "password": self.password
        }
        response = requests.post(self.base_url, data=payload, verify=False)
        result = response.content.decode('gbk')
        data = json.loads(result)
        if data.get("code") == 0:
            print("[+] 登录成功")
            return str(data.get("data"))  # 确保token转为字符串
        else:
            raise Exception(f"[-] 登录失败: {data.get('msg')}")

    def clear_group_domains(self, group_id):
        """清空域名群组中的所有域名"""
        payload = {
            "api_route": "object@urlgrp",
            "api_action": "btnrmv_grpurl",
            "items": ";",  # 使用空分号表示清空所有域名
            "id": str(group_id),
            "api_token": self.token
        }
        response = requests.post(self.base_url, data=payload, verify=False)
        result = response.content.decode('gbk')
        data = json.loads(result)
        if data.get("code") == 0:
            print("[+] 域名群组已清空")
        else:
            raise Exception(f"[-] 清空域名群组失败: {data.get('msg')}")

    def upload_domains_file(self, group_id, file_path):
        """通过文件上传批量添加域名"""
        with open(file_path, 'rb') as f:
            mp_encoder = MultipartEncoder(
                fields={
                    'api_route': 'object@urlgrp',
                    'api_action': 'add_grpurl',
                    'id': str(group_id),
                    'file': ('domains.txt', f, 'text/plain'),
                    'api_token': self.token
                }
            )
            headers = {
                'Content-Type': mp_encoder.content_type,
                'Connection': 'close'
            }
            response = requests.post(
                self.base_url,
                data=mp_encoder,
                headers=headers,
                verify=False,
                timeout=30
            )
            result = response.content.decode('gbk')
            data = json.loads(result)
            if data.get("code") == 0:
                print("[+] 域名文件上传成功")
            else:
                raise Exception(f"[-] 域名文件上传失败: {data.get('msg')}")

    def sync_domains_from_url(self, group_id, url):
        """从URL同步域名到域名群组"""
        temp_file = "domains.txt" # 定义临时文件名
        try:
            # 下载域名列表
            print("[*] 正在从URL获取域名列表...")
            response = requests.get(url, timeout=15)
            response.raise_for_status() # 检查HTTP响应状态

            # 处理并保存域名列表到临时文件，跳过注释行
            print("[*] 正在处理域名列表并保存到临时文件...")
            valid_domains = []
            for line in response.text.splitlines():
                line = line.strip() # 移除前后空白
                if line and not line.startswith("#"): # 检查非空且不是注释行
                    valid_domains.append(line)
            
            if not valid_domains:
                print("[-] 警告: 下载的域名列表中没有有效域名。")
                # 可以选择在此处退出或继续，取决于你希望的行为
                # raise Exception("域名列表为空或仅包含注释。")


            with open(temp_file, 'w', encoding='utf-8') as f: # 明确指定编码
                f.write("\n".join(valid_domains))
            
            print(f"[+] 已过滤并保存 {len(valid_domains)} 个有效域名到 {temp_file}")

            # 清空现有域名
            print("[*] 正在清空现有域名...")
            self.clear_group_domains(group_id)

            # 上传域名文件
            print("[*] 开始上传域名文件...")
            self.upload_domains_file(group_id, temp_file)

            print("[√] 域名同步完成")
        except requests.exceptions.RequestException as e:
            print(f"[-] 网络请求异常: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            print(f"[-] JSON解析失败: {str(e)}")
            raise
        except Exception as e:
            print(f"[-] 同步异常: {str(e)}")
            raise
        finally:
            # 无论是否发生异常，都尝试删除临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)
                print("[*] 已清理临时文件")

if __name__ == "__main__":
    # 配置参数
    CONFIG = {
	"gateway_ip": "你的Panabit设备IP",     # 例如: "192.168.0.100"
	"username": "你的Panabit用户名",       # 例如: "admin"
	"password": "你的Panabit密码",       # 例如: "panabit123"
	"group_id": 你的域名群组ID,          # **重要！** 可在Panabit WEB UI查看，例如: 1
	"domain_list_url": "包含域名列表的URL" # 例如: "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/domains/light.txt"
    }

    # 执行同步
    print(f"🚀 开始同步任务 {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        api = PanabitAPI(
            CONFIG["gateway_ip"],
            CONFIG["username"],
            CONFIG["password"]
        )
        api.sync_domains_from_url(
            CONFIG["group_id"],
            CONFIG["domain_list_url"]
        )
        print("✅ 同步任务完成")
    except Exception as e:
        print(f"❌ 任务异常终止: {str(e)}")
    finally:
        print(f"⏱️ 任务结束 {time.strftime('%H:%M:%S')}")