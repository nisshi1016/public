import boto3
import json

region = "ap-northeast-1"
client = boto3.client("waf", region_name=region)

# WebACL の一覧を取得
web_acls = client.list_web_acls()["WebACLs"]

# 取得したデータを保存するリスト
waf_data = []

for web_acl in web_acls:
    web_acl_id = web_acl["WebACLId"]
    
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
    waf_data.append(web_acl_details)

# JSON に保存
with open("classic_waf_export.json", "w") as f:
    json.dump(waf_data, f, indent=4)

print("Classic WAF 設定を classic_waf_export.json に保存しました。")
