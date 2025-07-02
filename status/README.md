
# status — 设备运行状态采集脚本 
# status — Device Status Collection Scripts

本目录用于存放通过 Panabit RESTful API 获取设备运行状态的各类脚本，包括但不限于：  
This directory contains various scripts that retrieve device operational status via the Panabit RESTful API. These scripts cover, but are not limited to:

- 接口上下行速率  
  Interface bandwidth (upstream and downstream rates)

- CPU 使用率  
  CPU usage

- 连接数统计  
  Connection statistics

- 系统负载信息  
  System load information

目前子目录：  
Current Subdirectories:

- [`flow_prometheus`](https://github.com/Panabit-Software/Panabit-API-Scripts/blob/main/status/flow_prometheus/README.md)：Interface traffic collection scripts (Prometheus Format)  | 接口流量采集脚本（Prometheus 格式)

