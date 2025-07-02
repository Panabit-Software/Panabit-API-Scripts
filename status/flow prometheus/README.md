# Interface Traffic Export Script (Prometheus Format)

## Overview  
This is a lightweight PHP script that retrieves upstream and downstream interface traffic (in bps) from the Panabit Intelligent Gateway using its RESTful API. The collected data is exported in a Prometheus-compatible text format for scraping.

## 🧰 Use Cases  
- Integrate Panabit device metrics into a centralized Prometheus monitoring system  
- Visualize and alert on traffic usage of key interfaces  
- Collect operational metrics using standard tools without complex development

## 🔁 Script Features  
- Automatically logs into the Panabit gateway via RESTful API to obtain an access token  
- Polls interface data every 5 seconds  
- Retrieves interface bandwidth usage (in bps)  
- Outputs data in Prometheus `textfile` format  
- Compatible with `node_exporter`'s `textfile` collector

## 📦 Script File  
- `panabit_flow_export.php`

## ⚙ Usage

### 1. Edit Configuration  
Open the script and modify the following 5 parameters at the top:

```php
$ip = "panabitipmgt";         // IP address of the Panabit management interface  
$username = "user";           // Login username  
$password = "pwd";            // Login password  
$file = "path for metrics";   // Output file path for Prometheus scraping  
$int = "interface";           // Name of the interface to monitor  
```

### 2. Run the Script  
Ensure PHP is installed (with curl extension enabled), then run:

```bash
php panabit_flow_export.php
```

The script runs continuously and updates data every 5 seconds.

## 🔗 Recommended Prometheus Configuration  

Use with `node_exporter`'s `textfile` module. Example:

**Start node_exporter with:**
```bash
--collector.textfile.directory=/tmp
```

**Prometheus job configuration:**
```yaml
- job_name: 'panabit-metrics'
  static_configs:
    - targets: ['your_node_exporter_host:9100']
```

For more information, see: https://github.com/prometheus

## 📝 Output Format  
The output file contains metrics in standard Prometheus format:

```
panabit_out 123456  
panabit_in 234567
```

## 🚧 Notes  
- Interface name must match the actual device configuration  
- Ensure the API user has sufficient permissions  
- For background execution, consider using `systemd`, `supervisord`, etc.  
- If the interface is invalid or not found, values may be empty

## 📣 Contribution & Feedback  
Feel free to use, modify, or extend this script. Issues and suggestions are welcome!  
More Panabit API examples will be released—stay tuned!

