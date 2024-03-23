#!/bin/bash
# This script is modified from https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/get_entrypoints.sh

archAffix() {
    case "$(uname -m)" in
        i386 | i686 ) echo '386' ;;
        x86_64 | amd64 ) echo 'amd64' ;;
        armv8 | arm64 | aarch64 ) echo 'arm64' ;;
        s390x ) echo 's390x' ;;
        * ) echo "不支持的CPU架构!" && exit 1 ;;
    esac
}

endpointyx() {
    # 判断 warp 文件是否存在，不存在则下载
    if ! [ -f warp ]; then
      # 下载优选工具软件，感谢某匿名网友的分享的优选工具
      wget https://gitlab.com/vvbbnn00/warp-script/-/raw/main/files/warp-yxip/warp-linux-"$(archAffix)" -O warp || { echo "下载优选工具失败"; exit 1; }
    fi

    # 取消 Linux 自带的线程限制，以便生成优选 Endpoint IP
    ulimit -n 102400

    # 启动 WARP Endpoint IP 优选工具
    chmod +x warp

    if [ "$suffix" == "_v6" ]; then
      ./warp -ipv6
    else
      ./warp
    fi

    # 将优选结果移动到指定目录
    if [ -n "$RUN_IN_DOCKER" ]; then
      mv -f result.csv "/app/config/result${suffix}.csv"
    else
      mv -f result.csv "./config/result${suffix}.csv"
    fi

    # 删除附属文件
    rm -f ips-v4.txt ips-v6.txt
}

init_ipv4() {
    echo "162.159.192.0/24
162.159.193.0/24
162.159.195.0/24
162.159.204.0/24
188.114.96.0/24
188.114.97.0/24
188.114.98.0/24
188.114.99.0/24" > ips-v4.txt
}

endpoint4() {
    init_ipv4
    endpointyx
}

init_ipv6() {
    echo "2606:4700:d0::/48
2606:4700:d1::/48" > ips-v6.txt
}

endpoint6() {
    init_ipv6
    endpointyx
}

suffix=

# 检查传入参数，若含有-4或-6则优选对应的IP段
while getopts "46" OPT; do
    case $OPT in
        6)
          suffix=_v6
          endpoint6
          ;;
        4)
          endpoint4
          ;; # 默认优选 IPv4
        *)
          echo "Usage: $0 [-4|-6]" && exit 1
          ;;
    esac
done

# 若未传入参数则优选 IPv4
[ -z "$1" ] && endpoint4
