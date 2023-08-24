# WARP Clash API

中文 | [English](./README_en.md)

> **Warning**
>
> 本项目是完全非商业项目，仅供学习交流使用，请勿用于非法用途，否则后果自负。

## 🤔 这是什么？

该项目可以让你通过订阅的方式使用`WARP+`，支持`Clash`、`Shadowrocket`等客户端。项目内置了刷取`WARP+`
流量的功能，可以让你的`WARP+`流量不再受限制（每`18`秒可获得`1GB`流量），同时，配备了`IP`选优功能。支持`Docker compose`
一键部署，无需额外操作，即可享受你自己的`WARP+`私有高速节点！

## 💡 特色功能

- 💻 支持`Clash`、`Surge`、`Quantumult`、`Shadowrocket`等客户端
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

若您需要在公网上部署该项目，建议您配置`SECRET_KEY`。在项目目录下创建`.env.local`文件，写入如下内容：

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

项目本身包含了一个选优过的`IP`列表，但是由于`WARP`的`IP`是动态的，所以可能会出现`IP`不可用的情况。若您需要手动选优，可以遵循以下步骤：

若您通过`docker-compose`部署，可以在项目目录下通过以下命令手动执行`IP`选优：

```bash
docker-compose exec warp-clash python3 app.py optimize
```

否则，可以在项目目录下执行以下命令：

```bash
python3 app.py optimize
```

## 🔧 环境变量

没错，您可以通过环境变量来配置该项目，在配置时，只需新建一个`.env.local`文件，写入您需要的环境变量即可。

以下是可用的环境变量：

| 变量名                | 默认值  | 说明                                       |
|--------------------|------|------------------------------------------|
| SECRET_KEY         | 无    | 用于保护订阅链接，若不配置，则不需要输入`SECRET_KEY`即可获取订阅链接 |
| DO_GET_WARP_DATA   | True | 是否刷取`WARP+`流量，若不需要刷取流量，则设置为`False`即可     |
| REQUEST_RATE_LIMIT | 0    | 限制X秒一次请求，该功能不太稳定，建议不要开启                  |
| RANDOM_COUNT       | 10   | 每次更新订阅随机节点的数量                            |
| LOSS_THRESHOLD     | 10   | 丢包率阈值，超过该阈值的`IP`将被剔除                     |
| DELAY_THRESHOLD    | 500  | 延迟阈值，超过该阈值的`IP`将被剔除                      |

## 🗂️ 引用项目

本项目的开发参照了以下项目，感谢这些开源项目的作者：

- [warp-script](https://gitlab.com/Misaka-blog/warp-script)
- [warp](https://replit.com/@aliilapro/warp)
- [wgcf](https://github.com/ViRb3/wgcf)

