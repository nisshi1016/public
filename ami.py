import boto3

# AWS クライアント作成
ec2 = boto3.client('ec2')

# 入力ファイル名
input_filename = "snap_ami_list.txt"
output_deleted_ami_filename = "deleted_snapshots.txt"
output_visualized_filename = "visualized_snapshots.txt"

# ファイルからスナップショットと AMI のリストを読み込む
snap_ami_map = []
with open(input_filename, "r") as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) == 2:
            snap_ami_map.append((parts[0], parts[1]))

# AMI の存在をチェック
deleted_snapshots = []
visualized_data = []

for snap_id, ami_id in snap_ami_map:
    try:
        response = ec2.describe_images(ImageIds=[ami_id])
        # AMI が存在する場合、そのままリストに追加
        if response.get("Images"):
            visualized_data.append(f"{snap_id} {ami_id}")
        else:
            deleted_snapshots.append(snap_id)
            visualized_data.append(f"{snap_id}")  # AMI 削除済みは snap_id のみ表示
    except ec2.exceptions.ClientError as e:
        # AMI が見つからないエラーなら削除リストに追加
        if "InvalidAMIID.NotFound" in str(e):
            deleted_snapshots.append(snap_id)
            visualized_data.append(f"{snap_id}")  # AMI 削除済み
        else:
            print(f"Error checking AMI {ami_id}: {e}")

# 結果をファイルに出力
with open(output_deleted_ami_filename, "w") as file:
    file.write("\n".join(deleted_snapshots) + "\n")

with open(output_visualized_filename, "w") as file:
    file.write("\n".join(visualized_data) + "\n")

print("処理完了: 削除対象スナップショットを", output_deleted_ami_filename, "に保存")
print("処理完了: 可視化結果を", output_visualized_filename, "に保存")
