#!/bin/bash

# 出力ファイル名
deleted_ami_filename="deleted_snapshots.txt"

# ファイル内の各スナップショットIDを削除
while IFS= read -r snap_id; do
    echo "スナップショット $snap_id を削除中..."
    aws ec2 delete-snapshot --snapshot-id "$snap_id"
    echo "スナップショット $snap_id の削除処理が完了しました。"
done < "$deleted_ami_filename"

echo "すべてのスナップショット削除処理が完了しました。"
