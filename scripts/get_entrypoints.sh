#!/bin/bash
# This script is modified from https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/get_entrypoints.sh


archAffix(){
    case "$(uname -m)" in
        i386 | i686 ) echo '386' ;;
        x86_64 | amd64 ) echo 'amd64' ;;
        armv8 | arm64 | aarch64 ) echo 'arm64' ;;
        s390x ) echo 's390x' ;;
        * ) echo "不支持的CPU架构!" && exit 1 ;;
    esac
}

endpointyx(){
    # 下载优选工具软件，感谢某匿名网友的分享的优选工具
    wget https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-"$(archAffix)" -O warp

    # 取消 Linux 自带的线程限制，以便生成优选 Endpoint IP
    ulimit -n 102400

    # 启动 WARP Endpoint IP 优选工具
    chmod +x warp && ./warp >/dev/null 2>&1

    # 读取 WARP Endpoint IP 优选工具生成的 Endpoint IP 段列表
    process_result_csv() {
        awk -F, '$3!="timeout ms" {print}' | 
        sort -t, -nk2 -nk3 | 
        uniq | 
        head -11 |
        awk -F, '{print "端点 "$1" 丢包率 "$2" 平均延迟 "$3}'
    }

    if [ -d /app/config ]; then
        process_result_csv < /app/config/result.csv
    else
        process_result_csv < ./config/result.csv  
    fi

    # 删除 WARP Endpoint IP 优选工具及其附属文件
    rm -f warp ip.txt
}

endpoint4(){
    # 生成优选 WARP IPv4 Endpoint IP 段列表
    n=0
    iplist=100
    while true; do
        temp[$n]=$(echo 162.159.192.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 162.159.193.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 162.159.195.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 162.159.204.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 188.114.96.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 188.114.97.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 188.114.98.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
        temp[$n]=$(echo 188.114.99.$(($RANDOM % 256)))
        n=$(($n + 1))
        if [ $n -ge $iplist ]; then
            break
        fi
    done
    while true; do
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 162.159.192.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 162.159.193.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 162.159.195.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 162.159.204.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 188.114.96.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 188.114.97.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 188.114.98.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
        if [ "$(echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u | wc -l)" -ge $iplist ]; then
            break
        else
            temp[$n]=$(echo 188.114.99.$(($RANDOM % 256)))
            n=$(($n + 1))
        fi
    done

    # 将生成的 IP 段列表放到 ip.txt 里，待程序优选
    echo "${temp[@]}" | sed -e 's/ /\n/g' | sort -u > ip.txt

    # 启动优选程序
    endpointyx
}

endpoint4
