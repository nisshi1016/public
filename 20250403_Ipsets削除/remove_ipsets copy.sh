#!/bin/bash

# ====== 設定 ======
SCOPE="REGIONAL"          # or CLOUDFRONT
REGION="ap-northeast-1"
TARGET_IP_FILE="target_ips.txt"
TARGET_IPSETS_FILE="target_ipsets.txt"
# ===================

# ファイル存在チェック
if [ ! -f "$TARGET_IP_FILE" ] || [ ! -f "$TARGET_IPSETS_FILE" ]; then
  echo "必要なファイルが見つかりません: $TARGET_IP_FILE または $TARGET_IPSETS_FILE"
  exit 1
fi

# 対象IP・IPSet名を配列に読み込み
mapfile -t TARGET_IPS < "$TARGET_IP_FILE"
mapfile -t TARGET_IPSET_NAMES < "$TARGET_IPSETS_FILE"

# 全IPSet一覧取得
IPSETS_JSON=$(aws wafv2 list-ip-sets --scope $SCOPE --region $REGION --output json)

for TARGET_NAME in "${TARGET_IPSET_NAMES[@]}"; do
  # IDを取得
  ID=$(echo "$IPSETS_JSON" | jq -r --arg NAME "$TARGET_NAME" '.IPSets[] | select(.Name == $NAME) | .Id')

  if [ -z "$ID" ]; then
    echo "[SKIP] IPSet '$TARGET_NAME' は見つかりません（削除済み？）"
    continue
  fi

  # IPSet詳細取得
  IPSET_DETAIL=$(aws wafv2 get-ip-set \
    --id "$ID" \
    --name "$TARGET_NAME" \
    --scope "$SCOPE" \
    --region "$REGION" \
    --output json 2>/dev/null)

  if [ -z "$IPSET_DETAIL" ]; then
    echo "[SKIP] IPSet '$TARGET_NAME' の詳細取得に失敗"
    continue
  fi

  LOCK_TOKEN=$(echo "$IPSET_DETAIL" | jq -r '.LockToken')
  CURRENT_IPS=($(echo "$IPSET_DETAIL" | jq -r '.IPSet.Addresses[]'))

  # 削除対象を除いたIP一覧を作成
  NEW_IPS=()
  CHANGED=false

  for ip in "${CURRENT_IPS[@]}"; do
    should_remove=false
    for target_ip in "${TARGET_IPS[@]}"; do
      if [[ "$ip" == "$target_ip" ]]; then
        should_remove=true
        CHANGED=true
        echo "[REMOVE] $ip を '$TARGET_NAME' から削除します"
        break
      fi
    done

    if [ "$should_remove" = false ]; then
      NEW_IPS+=("$ip")
    fi
  done

  if [ "$CHANGED" = true ]; then
    # 更新を実行
    aws wafv2 update-ip-set \
      --name "$TARGET_NAME" \
      --id "$ID" \
      --scope "$SCOPE" \
      --lock-token "$LOCK_TOKEN" \
      --addresses "${NEW_IPS[@]}" \
      --region "$REGION"
  else
    echo "[SKIP] '$TARGET_NAME' に削除対象のIPは含まれていません"
  fi
done
