#!/bin/bash

# 1. すべての AMI ID を取得
aws ec2 describe-images --owners self --query "Images[*].ImageId" --output text > ami_list.txt

# 2. すべてのスナップショットを取得
aws ec2 describe-snapshots --owner-self --query "Snapshots[*].[SnapshotId,Description]" --output text > snapshot_list.txt

# 3. AMI 由来のスナップショットを抽出（"Created by CreateImage" を含むもの）
grep "Created by CreateImage" snapshot_list.txt | awk '{print $1, $(NF)}' | sed 's/.*ami-/ami-/' > snapshot_with_ami.txt

# 4. 削除された AMI に関連するスナップショットを抽出
grep -Fvf ami_list.txt snapshot_with_ami.txt > orphan_snapshots.txt

# 5. 結果を表示
if [ -s orphan_snapshots.txt ]; then
    echo "🔍 削除済み AMI に関連するスナップショット一覧:"
    cat orphan_snapshots.txt
else
    echo "✅ 削除済み AMI に関連するスナップショットはありません。"
fi
