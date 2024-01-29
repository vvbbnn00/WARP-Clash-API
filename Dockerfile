FROM python:3.11-alpine

WORKDIR /app
COPY . .

# Check if in Github Actions, if not, change Alpine source to Aliyun
ARG GITHUB_ACTIONS
RUN if [ "$GITHUB_ACTIONS" != "true" ]; then \
        sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories; \
    fi

# Install dependencies
RUN apk add --no-cache bash build-base libffi-dev openssl-dev

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple
RUN chmod +x ./scripts/*.sh

CMD ["/bin/sh", "./scripts/run.sh"]
