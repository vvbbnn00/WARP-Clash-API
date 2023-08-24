# WARP Clash API

[中文](README.md) | English

> **Warning**
>
> This project is entirely non-commercial and is intended solely for educational and communicative purposes. Please do
> not use it for illegal activities, as the consequences will be borne by the user.

## 🤔 What is This?

This project allows you to use `WARP+` through a subscription, supporting clients
like `Clash`, `Shadowrocket`, etc. The project includes a feature to replenish `WARP+` traffic,
enabling your `WARP+` traffic to be unrestricted (1GB of traffic every 18 seconds). Additionally, it comes with IP
optimization. It supports one-click deployment through `Docker compose`, so you can enjoy your private
high-speed `WARP+` node without extra hassle!

## 💡 Key Features

- 💻 Supports clients such as `Clash`, `Surge`, `Quantumult`, `Shadowrocket`, etc.
- 🌏 Supports IP optimization.
- 🐋 Supports one-click deployment using `Docker compose`.
- 📕 Automatically replenishes `WARP+` traffic, requests are proxied, preserving your IP from getting blocked.
- ❓ Randomly selects nodes each subscription update, adding a sense of randomness to your experience.

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

If you plan to deploy this project on the public internet, it's recommended to set up the `SECRET_KEY`. Create
a `.env.local` file in the project directory and add the following:

```bash
SECRET_KEY=your_secret_key
```

For more information on environment variables, refer to [Environment Variables](#-environment-variables).

### 4. Build and Run

```bash
docker-compose up -d
```

### 5. Obtain Subscription Link

Visit `http://your_IP:21001`, enter the `SECRET_KEY` (if configured), and you can get the subscription link.

**🎉 Congratulations, you're all set!**

## 🌏 Manual IP Optimization

The project includes a pre-optimized list of IPs, but due to the dynamic nature of `WARP` IPs, there might be cases
where IPs become unusable. If you wish to optimize manually, follow these steps:

If you deployed via `docker-compose`, you can manually execute IP optimization with the following command in the project
directory:

```bash
docker-compose exec warp-clash python3 app.py optimize
```

Otherwise, you can execute the following command in the project directory:

```bash
python3 app.py optimize
```

## 🔧 Environment Variables

Yes, you can configure this project using environment variables. Simply create a `.env.local` file and add the required
environment variables.

Here are the available environment variables:

| Variable Name      | Default | Description                                                                                                  |
|--------------------|---------|--------------------------------------------------------------------------------------------------------------|
| SECRET_KEY         | None    | Used to protect the subscription link. If not configured, no `SECRET_KEY` input is required to get the link. |
| DO_GET_WARP_DATA   | True    | Whether to get `WARP+` data. If set to `False`, the `WARP+` data will not be obtained.                       |
| REQUEST_RATE_LIMIT | 0       | Limits requests to once every X seconds. This feature is unstable; it's recommended not to enable it.        |
| RANDOM_COUNT       | 10      | Number of randomly selected nodes during each subscription update.                                           |
| LOSS_THRESHOLD     | 10      | Packet loss threshold; IPs exceeding this threshold will be removed.                                         |
| DELAY_THRESHOLD    | 500     | Delay threshold; IPs exceeding this threshold will be removed.                                               |

## 🗂️ Attribution

This project's development was influenced by the following projects. Thanks to the authors of these open-source
projects:

- [warp-script](https://gitlab.com/Misaka-blog/warp-script)
- [warp](https://replit.com/@aliilapro/warp)
- [wgcf](https://github.com/ViRb3/wgcf)