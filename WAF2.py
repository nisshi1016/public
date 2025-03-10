import boto3
import json

region = "ap-northeast-1"
target_web_acl_name = "test"  # 取得したい WebACL の名前を指定
client = boto3.client("waf", region_name=region)

# WebACL の一覧を取得
web_acls = client.list_web_acls()["WebACLs"]

# 対象の WebACL を検索
target_web_acl = next((acl for acl in web_acls if acl["Name"] == target_web_acl_name), None)

if not target_web_acl:
    print(f"'{target_web_acl_name}' という名前の WebACL は見つかりませんでした。")
    exit()

web_acl_id = target_web_acl["WebACLId"]

# WebACL の詳細を取得
web_acl_details = client.get_web_acl(WebACLId=web_acl_id)

# ルールの取得
rule_ids = [rule["RuleId"] for rule in web_acl_details["WebACL"]["Rules"]]
rules = []
for rule_id in rule_ids:
    rule_details = client.get_rule(RuleId=rule_id)
    rules.append(rule_details["Rule"])

# WebACL の情報にルールを追加
web_acl_details["Rules"] = rules

# JSON に保存
output_file = f"classic_waf_{target_web_acl_name}_export.json"
with open(output_file, "w") as f:
    json.dump(web_acl_details, f, indent=4)

print(f"Classic WAF '{target_web_acl_name}' の設定を {output_file} に保存しました。")
