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
      wget https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-"$(archAffix)" -O warp || { echo "下载优选工具失败"; exit 1; }
    fi

    # 取消 Linux 自带的线程限制，以便生成优选 Endpoint IP
    ulimit -n 102400

    # 启动 WARP Endpoint IP 优选工具
    chmod +x warp && ./warp >/dev/null 2>&1

    # 读取 WARP Endpoint IP 优选工具生成的 Endpoint IP 段列表
    process_result_csv() {
        awk -F, '$3!="timeout ms" {print}' |
        sort -t, -nk2 -nk3 |
        uniq |
        head -11
    }

    # 优选结果处理
    process_result_csv < result.csv

    # 将优选结果移动到指定目录
    if [ -n "$RUN_IN_DOCKER" ]; then
      mv -f result.csv "/app/config/result${suffix}.csv"
    else
      mv -f result.csv "./config/result${suffix}.csv"
    fi

    # 删除附属文件
    rm -f ip.txt
}

generate_random_ips() {
    local iplist=100
    local count=0
    local ip_base=("162.159.192." "162.159.193." "162.159.195." "162.159.204." "188.114.96." "188.114.97." "188.114.98." "188.114.99.")

    while [ $count -lt $iplist ]; do
        for base in "${ip_base[@]}"; do
            temp[$count]="${base}$(($RANDOM % 256))"
            ((count++))
            [ $count -ge $iplist ] && break
        done
    done

    # 确保列表中的 IP 地址是唯一的
    printf '%s\n' "${temp[@]}" | sort -u > ip.txt
}

endpoint4() {
    generate_random_ips
    endpointyx
}

generate_random_ipv6s() {
    local iplist=100
    local n=0
    local temp

    while [ $n -lt $iplist ]; do
        local hex1 hex2 hex3 hex4
        hex1=$(printf '%x\n' $((RANDOM * 2 + RANDOM % 2)))
        hex2=$(printf '%x\n' $((RANDOM * 2 + RANDOM % 2)))
        hex3=$(printf '%x\n' $((RANDOM * 2 + RANDOM % 2)))
        hex4=$(printf '%x\n' $((RANDOM * 2 + RANDOM % 2)))
        temp[$n]="[2606:4700:d0::$hex1:$hex2:$hex3:$hex4]"
        ((n++))
        [ $n -ge $iplist ] && break

        temp[$n]="[2606:4700:d1::$hex1:$hex2:$hex3:$hex4]"
        ((n++))
    done

    # 确保列表中的 IP 地址是唯一的
    printf '%s\n' "${temp[@]}" | sort -u > ip.txt
}

endpoint6() {
    generate_random_ipv6s
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
