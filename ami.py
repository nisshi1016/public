import subprocess

# スナップショット情報をファイルから読み込む
with open('snapshots.txt', 'r') as file:
    snapshot_info = [line.strip().split() for line in file.readlines()]

# AMI IDのリストを取得
ami_ids = subprocess.check_output(
    ["aws", "ec2", "describe-images", "--owners", "<アカウントID>", "--query", "Images[*].ImageId", "--output", "text"]
).decode().split()

# 削除済みのAMIを特定
deleted_ami = []
for account, snapshot_id, ami_id in snapshot_info:
    if ami_id not in ami_ids:
        deleted_ami.append((account, snapshot_id, ami_id))

# 結果を表示
if deleted_ami:
    print("Deleted AMIs found:")
    for account, snapshot_id, ami_id in deleted_ami:
        print(f"Account: {account}, Snapshot ID: {snapshot_id}, AMI ID: {ami_id}")
else:
    print("No deleted AMIs found.")
