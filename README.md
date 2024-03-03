# WARP Clash API

![GitHub License](https://img.shields.io/github/license/vvbbnn00/WARP-Clash-API)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/67ca8d105fb947eca6204230ba3ac09b)](https://app.codacy.com/gh/vvbbnn00/WARP-Clash-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![GitHub Repo stars](https://img.shields.io/github/stars/vvbbnn00/WARP-Clash-API?style=flat)

中文 | [English](./README_en.md)

> **Warning**
>
> 本项目是完全非商业项目，仅供学习交流使用，请勿用于非法用途，否则后果自负。

## 🤔 这是什么？

该项目可以让你通过订阅的方式使用`WARP+`，支持`Clash`、`Shadowrocket`等客户端。项目内置了
刷取`WARP+`流量的功能，可以让你的`WARP+`流量不再受限制（每`18`秒可获得`1GB`流量），同时，
配备了`IP`选优功能。支持`Docker compose`一键部署，无需额外操作，即可享受你自己的`WARP+`私
有高速节点！

## 💡 特色功能

- 💻 支持`Clash`、`Surge`、`Shadowrocket`等客户端
- 🔑 支持设置您自己的`LicenseKey`
- 🌏 支持`IP`选优
- 🐋 支持`Docker compose`一键部署
- 📕 全自动刷取`WARP+`流量，请求经过代理，防封`IP`
- ❓ 每次更新订阅随机节点，让你体验抽卡的乐趣

## 🚀 快速上手

### 1. 安装`Docker`和`Docker compose`

- `Docker`安装教程：[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
- `Docker compose`安装教程：[https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### 2. 下载项目

```bash
git clone https://github.com/vvbbnn00/WARP-Clash-API.git
```

### 3. [可选] 配置`SECRET_KEY`

若您需要在公网上部署该项目，建议您配置`SECRET_KEY`与`PUBLIC_URL`。在项目目录下创建
`.env.local`文件，写入如下内容：

```bash
SECRET_KEY=your_secret_key
```

关于环境变量的更多信息，请参考[环境变量](#-环境变量)。

### 4. 编译并运行

```bash
docker-compose up -d
```

### 5. 获取订阅链接

访问`http://你的IP:21001`，输入`SECRET_KEY`（若没有配置，则可以留空），即可获取订阅链接。

**🎉 大功告成**

## 🌏 手动IP选优

项目本身包含了一个选优过的`IP`列表，但是由于`WARP`的`IP`是动态的，所以可能会出现`IP`不可用的
情况。若您需要手动选优，可以遵循以下步骤：

若您通过`docker-compose`部署，可以在项目目录下通过以下命令手动执行`IP`选优：

```bash
docker-compose exec warp-clash python3 app.py optimize
```

否则，可以在项目目录下执行以下命令：

```bash
python3 app.py optimize
```

## 🔧 环境变量

没错，您可以通过环境变量来配置该项目，在配置时，只需新建一个`.env.local`文件，写入您需要的环境
变量即可。

以下是可用的环境变量：

| 变量名                    | 默认值                               | 说明                                                                                                         |
|------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------------|
| DELAY_THRESHOLD        | `500`                             | 延迟阈值，超过该阈值的`IP`将被剔除                                                                                        |
| DO_GET_WARP_DATA       | `True`                            | 是否刷取`WARP+`流量，若不需要刷取流量，则设置为`False`即可                                                                       |
| GET_WARP_DATA_INTERVAL | `18`                              | 刷取`WARP+`流量的时间间隔，单位为秒，每隔该时间间隔会刷取一次`WARP+`流量，不建议间隔设置过短。                                                     |
| LOSS_THRESHOLD         | `10`                              | 丢包率阈值，超过该阈值的`IP`将被剔除                                                                                       |
| PROXY_POOL_URL         | `https://getproxy.bzpl.tech/get/` | IP代理池地址，用于刷取`WARP+`流量，您可以自行搭建，参照[proxy_pool](https://github.com/jhao104/proxy_pool)                        |
| PUBLIC_URL             | `无`                               | 部署在公网上时，填写公网`IP`或域名，用于生成订阅链接，比如 `https://subs.zeabur.app`                                                  |
| RANDOM_COUNT           | `10`                              | 每次更新订阅随机节点的数量                                                                                              |
| REOPTIMIZE_INTERVAL    | `-1`                              | 重新选优的时间间隔，单位为秒，若小于等于0，则不会重新选优，否则每隔该时间间隔会重新选优一次，不建议间隔设置过短。                                                  |                     
| REQUEST_RATE_LIMIT     | `0`                               | 限制X秒一次请求，该功能不太稳定，建议不要开启                                                                                    |
| SECRET_KEY             | `无`                               | 用于保护订阅链接，若不配置，则不需要输入`SECRET_KEY`即可获取订阅链接                                                                   |
| SHARE_SUBSCRIPTION     | `False`                           | 若您的站点想要向社区分享订阅，但不想让自己的账户信息被公开或修改，可以设置为`True`，此时，访问订阅链接时，不需要输入`SECRET_KEY`即可获取，而对于其他的操作，仍然需要输入`SECRET_KEY`。 |

### 📝 配置示例

例如，您设置`SECRET_KEY`为`123456`，并打算将订阅分享给社区，那么您的`.env.local`文件应该
如下：

```env
SECRET_KEY=123456
SHARE_SUBSCRIPTION=True
```

## 🧰 进阶操作

**请注意，如果您设置了`SECRET_KEY`，需要在URL的末尾添加`key`参数**，例如：

```text
http://your_IP:21001/some/api/actions?key=your_secret_key
```

### 重置账户的`PublicKey`和`PrivateKey`

项目支持您通过请求以下接口来重置`PublicKey`和`PrivateKey`：

```bash
curl -X POST http://host:port/api/account/reset_key
```

重置过后，需要重新获取订阅内容，否则可能无法使用。

### 设置自己的`LicenseKey`

若您已经拥有了`WARP+`的`LicenseKey`，可以通过以下接口来设置：

```bash
curl -X POST http://host:port/api/account/update_license -H "Content-Type: application/json" -d "{\"license_key\": \"your_license_key\"}"
```

请注意，当您设置了`LicenseKey`后，其`PublicKey`和`PrivateKey`将会被重置，需要重新获取订阅
内容。

## 🗂️ 引用项目

本项目的开发参照了以下项目，感谢这些开源项目的作者：

- [warp-script](https://gitlab.com/Misaka-blog/warp-script)
- [warp](https://replit.com/@aliilapro/warp)
- [wgcf](https://github.com/ViRb3/wgcf)
- [proxy_pool](https://github.com/jhao104/proxy_pool)
- [geolite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
