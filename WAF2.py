import boto3
import json

region = "ap-northeast-1"
target_web_acl_name = "test"  # 取得したい WebACL の名前
client = boto3.client("waf", region_name=region)

# WebACL の一覧を取得（ID のみ取得される）
web_acls = client.list_web_acls()["WebACLs"]

# 名前でフィルタリングするために、各 WebACL の詳細を取得
target_web_acl = None
for web_acl in web_acls:
    web_acl_details = client.get_web_acl(WebACLId=web_acl["WebACLId"])
    if web_acl_details["WebACL"]["Name"] == target_web_acl_name:
        target_web_acl = web_acl_details["WebACL"]
        break

if not target_web_acl:
    print(f"'{target_web_acl_name}' という名前の WebACL は見つかりませんでした。")
    exit()

web_acl_id = target_web_acl["WebACLId"]

# ルールの取得
rule_ids = [rule["RuleId"] for rule in target_web_acl["Rules"]]
rules = []
for rule_id in rule_ids:
    rule_details = client.get_rule(RuleId=rule_id)
    rules.append(rule_details["Rule"])

# WebACL の情報にルールを追加
target_web_acl["Rules"] = rules

# JSON に保存
output_file = f"classic_waf_{target_web_acl_name}_export.json"
with open(output_file, "w") as f:
    json.dump(target_web_acl, f, indent=4)

print(f"Classic WAF '{target_web_acl_name}' の設定を {output_file} に保存しました。")
