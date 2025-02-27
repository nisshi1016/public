#!/bin/bash

# 引数で指定されたファイル名を取得
instance_ids_file="$1"

# ファイル内の各インスタンスIDを停止
while IFS= read -r instance_id; do
    echo "インスタンス $instance_id を停止中..."
    aws ec2 stop-instances --instance-ids "$instance_id"
    echo "インスタンス $instance_id の停止処理が完了しました。"
done < "$instance_ids_file"

echo "すべてのインスタンス停止処理が完了しました。"
