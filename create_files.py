import os

def create_project_files():
    # 创建项目文件夹
    os.makedirs('project', exist_ok=True)
    
    # 创建子文件夹
    os.makedirs('project/src', exist_ok=True)
    os.makedirs('project/tests', exist_ok=True)
    os.makedirs('project/docs', exist_ok=True)
    
    # 创建文件
    open('project/README.md', 'a').close()
    open('project/requirements.txt', 'a').close()
    open('project/src/main.py', 'a').close()
    open('project/tests/test_main.py', 'a').close()
    
    print("项目文件已创建完成。")

if __name__ == '__main__':
    create_project_files()
