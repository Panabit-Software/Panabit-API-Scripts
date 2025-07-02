<p>
中文<a/>| <a href="README.md"> English   
</p>

# 接口流量采集脚本（Prometheus 格式）

## 简介  
这是一个轻量级的 PHP 脚本工具，基于 Panabit 智能应用网关的 RESTful API，定时获取指定接口的上下行速率（bps），并以 Prometheus 兼容格式输出到文本文件，供监控系统采集使用。

## 🧰 使用场景  
- 将 Panabit 设备状态数据接入统一的 Prometheus 监控体系  
- 实现关键接口流量的可视化与告警  
- 使用标准工具采集设备运行指标，无需复杂开发

## 🔁 脚本功能  
- 通过 RESTful API 自动登录 Panabit 网关并获取 token  
- 每 5 秒轮询一次接口数据  
- 获取接口的上下行速率（单位：bps）  
- 将数据输出为 Prometheus `textfile` 格式  
- 可配合 `node_exporter` 的 `textfile` 模块使用

## 📦 脚本位置  
- `panabit_flow_export.php`

## ⚙ 使用方法

### 1. 修改配置项  
打开脚本文件，修改顶部的 5 个配置参数：

```php
$ip = "panabitipmgt";         // Panabit 设备管理口 IP 地址  
$username = "user";           // 登录用户名  
$password = "pwd";            // 登录密码  
$file = "path for metrics";   // Prometheus 读取的输出文件路径  
$int = "interface";           // 要监控的接口名称  
```

### 2. 启动脚本  
确保系统已安装 PHP 且启用了 curl 扩展，运行命令：

```bash
php panabit_flow_export.php
```

脚本将持续运行，并每 5 秒更新一次数据。

## 🔗 Prometheus 采集建议配置  

推荐结合 `node_exporter` 的 `textfile` 模块使用。示例如下：

**启动 node_exporter 添加参数：**
```bash
--collector.textfile.directory=/tmp
```

**Prometheus job 配置示例：**
```yaml
- job_name: 'panabit-metrics'
  static_configs:
    - targets: ['your_node_exporter_host:9100']
```

更多部署配置说明可参考：https://github.com/prometheus

## 📝 输出格式  
输出文件为标准 Prometheus 指标格式：

```
panabit_out 123456  
panabit_in 234567
```

## 🚧 注意事项  
- 接口名称需与设备配置中保持一致  
- 确保 API 用户具有足够权限  
- 建议结合 `systemd` 或 `supervisor` 实现后台守护运行  
- 若接口名称错误或不存在，可能导致数据为空

## 📣 贡献与反馈  
欢迎使用、修改、二次开发本脚本。如有问题，欢迎提交 Issue。  
更多 Panabit API 示例脚本将陆续开放，欢迎关注本项目。

