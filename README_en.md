# WARP Clash API

![GitHub License](https://img.shields.io/github/license/vvbbnn00/WARP-Clash-API)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/67ca8d105fb947eca6204230ba3ac09b)](https://app.codacy.com/gh/vvbbnn00/WARP-Clash-API/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![GitHub Repo stars](https://img.shields.io/github/stars/vvbbnn00/WARP-Clash-API?style=flat)

[中文](README.md) | English

> **Warning**
>
> This project is entirely non-commercial and is intended solely for educational
> and communicative purposes. Please do not use it for illegal activities, as
> the consequences will be borne by the user.

## 🤔 What is This?

This project allows you to use `WARP+` through a subscription, supporting
clients like `Clash`, `Shadowrocket`, etc. The project includes a feature to
replenish `WARP+` traffic, enabling your `WARP+` traffic to be unrestricted
(1GB of traffic every 18 seconds). Additionally, it comes with IP optimization.

It supports one-click deployment through `Docker compose`, so you can enjoy
your private high-speed `WARP+` node without extra hassle!

## 💡 Key Features

- 💻 Supports clients such as `Clash`, `Surge`, `Shadowrocket`, etc.
- 
- 🔑 Supports setting your own `LicenseKey`.
- 🌏 Supports IP optimization.
- 🐋 Supports one-click deployment using `Docker compose`.
- 📕 Automatically replenishes `WARP+` traffic, requests are proxied, 
preserving your IP from getting blocked.
- ❓ Randomly selects nodes each subscription update, adding a sense of
randomness to your experience.

## 🚀 Quick Start

### 1. Install `Docker` and `Docker compose`

- Docker Installation Guide: [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)
- Docker Compose Installation
  Guide: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### 2. Download the Project

```bash
git clone https://github.com/vvbbnn00/WARP-Clash-API.git
```

### 3. [Optional] Configure `SECRET_KEY`

If you plan to deploy this project on the public internet, it's recommended to
set up the `SECRET_KEY`. Create a `.env.local` file in the project directory
and add the following:

```bash
SECRET_KEY=your_secret_key
```

For more information on environment variables, refer to
[Environment Variables](#-environment-variables).

### 4. Build and Run

```bash
docker-compose up -d
```

### 5. Obtain Subscription Link

Visit `http://your_IP:21001`, enter the `SECRET_KEY` and `PUBLIC_URL` (if
configured), and you can get the subscription link.

**🎉 Congratulations, you're all set!**

## 🌏 Manual IP Optimization

The project includes a pre-optimized list of IPs, but due to the dynamic
nature of `WARP` IPs, there might be cases where IPs become unusable. If you
wish to optimize manually, follow these steps:

If you deployed via `docker-compose`, you can manually execute IP optimization
with the following command in the project directory:

```bash
docker-compose exec warp-clash python3 app.py optimize
```

Otherwise, you can execute the following command in the project directory:

```bash
python3 app.py optimize
```

## 🔧 Environment Variables

Yes, you can configure this project using environment variables. Simply create
a `.env.local` file and add the required environment variables.

Here are the available environment variables:

| Variable Name          | Default                           | Description                                                                                                                                                                                                                                                                                                                |
|------------------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DELAY_THRESHOLD        | `500`                             | Delay threshold; IPs exceeding this threshold will be removed.                                                                                                                                                                                                                                                             |
| DO_GET_WARP_DATA       | `True`                            | Whether to get `WARP+` data. If set to `False`, the `WARP+` data will not be obtained.                                                                                                                                                                                                                                     |
| GET_WARP_DATA_INTERVAL | `18`                              | Time interval for obtaining `WARP+` data, in seconds. `WARP+` data will be obtained every this interval, it is not recommended to set the interval too short.                                                                                                                                                              |
| LOSS_THRESHOLD         | `10`                              | Packet loss threshold; IPs exceeding this threshold will be removed.                                                                                                                                                                                                                                                       |
| PROXY_POOL_URL         | `https://getproxy.bzpl.tech/get/` | IP proxy pool address, used to get `WARP+` traffic. You can build it yourself, check [proxy_pool](https://github.com/jhao104/proxy_pool) for more information.                                                                                                                                                             |
| PUBLIC_URL             | `None`                            | When deployed on the public network, fill in the public IP or domain name to generate subscription links. for example `https://subs.zeabur.app`                                                                                                                                                                            |
| RANDOM_COUNT           | `10`                              | Number of randomly selected nodes during each subscription update.                                                                                                                                                                                                                                                         |
| REOPTIMIZE_INTERVAL    | `-1`                              | Re-optimization interval in seconds, if less than or equal to 0, re-optimization will not occur, otherwise it will re-optimize every this interval, it is not recommended to set the interval too short.                                                                                                                   |
| REQUEST_RATE_LIMIT     | `0`                               | Limits requests to once every X seconds. This feature is unstable; it's recommended not to enable it.                                                                                                                                                                                                                      |
| SECRET_KEY             | `None`                            | Used to protect the subscription link. If not configured, no `SECRET_KEY` input is required to get the link.                                                                                                                                                                                                               |
| SHARE_SUBSCRIPTION     | `False`                           | If you want to share subscriptions with the community but doesn't want your account information to be publicly accessible or modified, you can set this to `True`. In this case, accessing the subscription link does not require entering the `SECRET_KEY`, but for other operations, the `SECRET_KEY` is still required. |

### 📝 Configuration Example

If you set `SECRET_KEY` to `123456` and plan to share the subscription with
the community, your `.env.local` file should look like this:

```env
SECRET_KEY=123456
SHARE_SUBSCRIPTION=True
```

## 🧰 Advanced Operations

**Please note that if you set `SECRET_KEY`, you need to add the `key`
parameter at the end of the URL**, for example:

```text
http://your_IP:21001/some/api/actions?key=your_secret_key
```

### Resetting the `PublicKey` and `PrivateKey` of an Account

The project supports resetting the `PublicKey` and `PrivateKey` by requesting
the following interface:

```bash
curl -X POST http://host:port/api/account/reset_key
```

After resetting, it is necessary to re-acquire the subscription content;
otherwise, it may not be usable.

### Setting Your Own `LicenseKey`

If you already have a `WARP+` `LicenseKey`, you can set it through the
following interface:

```bash
curl -X POST http://host:port/api/account/update_license -H "Content-Type: application/json" -d "{\"license_key\": \"your_license_key\"}"
```

Please note that when you set the `LicenseKey`, your `PublicKey` and
`PrivateKey` will be reset, and you will need to re-acquire the subscription
content.

## 🗂️ Attribution

This project's development was influenced by the following projects.
Thanks to the authors of these open-source projects:

- [warp-script](https://gitlab.com/Misaka-blog/warp-script)
- [warp](https://replit.com/@aliilapro/warp)
- [wgcf](https://github.com/ViRb3/wgcf)
- [proxy_pool](https://github.com/jhao104/proxy_pool)
- [geolite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
