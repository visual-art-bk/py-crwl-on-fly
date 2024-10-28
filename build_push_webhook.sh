#!/bin/bash

# Slack Webhook URL 설정
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/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"

current_datetime=$(date "+%Y-%m-%d_%H:%M:%S")

git add .
git commit -a -m ${current_datetime}
git push -u origin main

if [ $? -eq 0 ]; then
    # 성공 메시지
    echo  "\033[32mgit-push-success\033[0m" 
    curl -X POST -H 'Content-type: application/json' --data '{"text":"git-push-success"}' $SLACK_WEBHOOK_URL
else
    # 실패 메시지
    echo "\033[31mgit-push-fail\033[0m"
    curl -X POST -H 'Content-type: application/json' --data '{"text":"git-push-fail"}' $SLACK_WEBHOOK_URL
fi

/home/kbk/.fly/bin/flyctl deploy

# 빌드 및 푸시가 성공적으로 완료되었는지 확인
if [ $? -eq 0 ]; then
    # 성공 메시지
    curl -X POST -H 'Content-type: application/json' --data '{"text":"웹훅-Fly 배치 성공"}' $SLACK_WEBHOOK_URL
else
    # 실패 메시지
    curl -X POST -H 'Content-type: application/json' --data '{"text":"웹훅-Fly 배치 실패"}' $SLACK_WEBHOOK_URL
fi