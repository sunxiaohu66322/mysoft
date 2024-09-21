import os
import json
import time
import subprocess
from datetime import datetime
from shutil import copyfile

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def backup_file(src_file, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(backup_dir, f"{os.path.basename(src_file)}.{timestamp}.bak")
    copyfile(src_file, backup_file)
    print(f"已备份文件: {src_file} -> {backup_file}")

def monitor_changes():
    config = load_config()
    project_path = config['project_path']
    backup_dir = os.path.join(project_path, 'backups')
    important_files = ['config.json', 'create_files.py', 'monitor_changes.py']  # 重要文件列表
    
    while True:
        # 检查是否有文件变更
        changed_files = get_changed_files(project_path)
        
        if changed_files:
            # 备份重要文件
            for file in changed_files:
                if os.path.basename(file) in important_files:
                    backup_file(file, backup_dir)
            
            # 提交变更
            commit_changes(project_path, config['commit_message_format'])
            # 推送到远程仓库
            push_to_remote(config['github_repo'])
        
        time.sleep(5)  # 每5秒检查一次

def get_changed_files(path):
    # 获取发生变更的文件列表
    output = subprocess.check_output(["git", "diff", "--name-only"], cwd=path)
    return output.decode('utf-8').splitlines()

def has_changes(path):
    # 检查文件夹中是否有变更
    output = subprocess.check_output(["git", "status", "--porcelain"], cwd=path)
    return output != b''

def commit_changes(path, message_format):
    # 提交文件变更
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    message = message_format.replace('时间戳', timestamp)
    print(f"检测到文件变更,正在提交...{message}")
    subprocess.call(["git", "add", "."], cwd=path)
    subprocess.call(["git", "commit", "-m", message], cwd=path)
    print("文件变更已提交。")

def push_to_remote(repo_url):
    # 推送到远程仓库
    print("正在推送到远程仓库...")
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            subprocess.check_call(["git", "push", repo_url])
            print("已成功推送到远程仓库。")
            break
        except subprocess.CalledProcessError:
            retry_count += 1
            print(f"推送失败,正在重试({retry_count}/{max_retries})...")
            time.sleep(5)
    else:
        print("重试次数已用完,请手动处理推送问题。")

if __name__ == '__main__':
    monitor_changes()