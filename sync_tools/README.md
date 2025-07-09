
# Panabit Auto Sync Toolkit  |Panabit 自动化同步工具集

This toolkit provides a set of Python scripts that automatically fetch the latest malicious domain or IP blacklist data from online sources and update designated **domain groups** or **IP groups** on the Panabit Intelligent Application Gateway via its RESTful API.  
It supports scheduled execution and enables dynamic maintenance of millions of threat entries with ease.  

本工具集包含了一系列 Python 脚本，这些脚本可自动从在线恶意域名或 IP 黑名单源获取最新数据，并通过 Panabit 智能应用网关的 RESTful API 接口动态更新指定的 **域名群组** 或 **IP 群组**，用于网络内容过滤与安全防护。支持定时运行，轻松实现百万级威胁地址动态维护。

---

## ⭐️ Key Features  |主要功能

- **Panabit Authenticated Login**: All scripts include secure API login to retrieve access tokens.
- **Panabit 认证登录**：所有脚本都封装了安全的 API 登录过程，获取操作所需的 Token。  
- **IP/Domain Group Synchronization**:
- **IP/域名群组同步**：  
  - Downloads IP/domain list from specified URL.
  - 从指定 URL 下载 IP/域名列表；
  - **Automatically filters comment lines** (starting with `#`) and blank lines, keeping only valid entries.
  -  **自动过滤注释行**（以 `#` 开头）和空行； 
  - Clears all existing IPs/domains in the specified Panabit group.
  - 清空 Panabit 上目标群组现有的条目；
  - Uploads the cleaned list to the target group in bulk.
  - 将处理后的列表批量上传。
- **Error Handling**: Handles request failures, JSON parsing errors, and Panabit API error responses to ensure script stability.
- **错误处理**：捕获网络异常、JSON 解析错误及 API 返回异常，提升脚本稳定性。


---

## 🚀 Quick Start  | 快速开始

### Requirements  |前提条件

- **Python 3.x environment**  |**Python 3.x 环境**  
- Libraries: `requests`, `requests-toolbelt`
- 已安装 `requests`, `requests-toolbelt` 库：  
  ```bash
  pip install requests requests-toolbelt urllib3
  ```
- A Panabit gateway device with API access and admin credentials.
- 一台已启用 API 的 Panabit 网关设备  
- Pre-created domain/IP group IDs in Panabit, visible via the web UI.
- 已在 Panabit 上创建好对应的 **域名群组 ID** 或 **IP 群组 ID**


---

### Configuration  |配置

Edit the desired script [(`Panabit_domain_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_domain_sync.py)  or [(`Panabit_ip_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_ip_sync.py) and fill in the `CONFIG` section:

打开你想要运行的脚本文件 [(`Panabit_domain_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_domain_sync.py) 或 [(`Panabit_ip_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_ip_sync.py)  ，修改 `CONFIG` 字典中的参数以适应你的环境：
#### Domain Sync Example ([`Panabit_domain_sync.py`](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_domain_sync.py))  
#### 域名同步脚本  ([`Panabit_domain_sync.py`](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_domain_sync.py)) 配置示例

```python
CONFIG = {
    "gateway_ip": "Your Panabit IP",
    "username": "Your username",
    "password": "Your password",
    "group_id": 1,
    "domain_list_url": "https://example.com/domainlist.txt"
}
```

#### IP Sync Example [(`Panabit_ip_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_ip_sync.py)  
#### IP 地址同步脚本[(`Panabit_ip_sync.py`)](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/sync_tools/Panabit_ip_sync.py)   配置示例

```python
CONFIG = {
    "gateway_ip": "Your Panabit IP",
    "username": "Your username",
    "password": "Your password",
    "group_id": 1,
    "firehol_url": "https://example.com/iplist.txt"
}
```

- `gateway_ip`: The management IP address of your Panabit device.  
- `gateway_ip`：Panabit 设备的管理 IP 地址。

- `username` / `password`: The login credentials for accessing the Panabit API.  
- `username` / `password`：用于登录 Panabit 的账户凭据。

- `group_id`: **Critical field** – the unique ID of the domain or IP group you've created in the Panabit web UI. Make sure to enter it correctly.  
- `group_id`：**非常重要**，这是你在 Panabit 后台创建的域名群组或 IP 地址群组的唯一标识 ID，请务必填写正确。

- `domain_list_url` / `firehol_url`: URL of the remote list file. The file should be plain text, one entry per line, and support comments starting with `#`.  
- `domain_list_url` / `firehol_url`：远程列表文件的 URL，必须是纯文本格式，每行一个条目，支持以 `#` 开头的注释行。

---

### Running the Script  | 运行脚本

```bash
# Domain sync
python panabit_domain_sync.py

# IP sync
python panabit_ip_sync.py
```

You will see detailed logs in the terminal after execution.

执行脚本后，将在终端看到同步过程的详细日志输出。

---

## 🛠️ Automation Example  | 使用示例与自动化

You can use `cron` on Linux or `Task Scheduler`on Windows to automate regular synchronization, keeping Panabit rules up to date.  
你可以结合 `cron`（Linux）或`任务计划程序`（Windows）来实现定时自动同步，保持 Panabit 规则的最新状态。

For example, to sync the domain list daily at 3:00 AM on a Linux system, you can add the following Cron job:  
例如，要在 Linux 上每天凌晨 3 点自动同步域名列表，可以这样添加 Cron 任务：

```bash
# Edit crontab| 编辑 crontab
crontab -e


# Add the following line (replace with your actual script path) |添加以下行 (请替换为你的脚本实际路径)
0 3 * * * /usr/bin/python3 /path/to/your/panabit_domain_sync.py >> /var/log/panabit_domain_sync.log 2>&1

```

---

## ⚠️ Notes  | 注意事项

- Double-check the `group_id`. A wrong ID may cause errors or affect the wrong group.
- 请务必确认 `group_id` 正确，否则可能影响错误的群组或导致同步失败；  
- Remote lists must be plain text, one entry **per line**. Lines starting with `#` will be ignored.
- 远程列表文件应为纯文本格式，**每行一个条目**。脚本会自动忽略以 `#` 开头的注释行和空行。
- Avoid syncing too frequently to reduce API load on Panabit.
- 请勿过度频繁地执行同步，以免对 Panabit 设备造成不必要的压力或触发其 API 限流机制。


---

## 🤝 Contributing  | 贡献

Feel free to submit pull requests or issues to improve the tool, request features, or report bugs.

欢迎通过 Pull Request 或 Issue 提交改进建议、功能请求或问题反馈，你的参与能让这个工具更好用！

---

