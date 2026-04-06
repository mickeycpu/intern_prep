# 文件类型分类规则（后缀名 -> 文件夹名）
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac"],
    "Documents": [".doc", ".docx", ".pdf", ".txt", ".xlsx", ".pptx"],
    "Code": [".py", ".java", ".c", ".html", ".css", ".js"],
}

import os

def get_category(filename):
    """根据文件后缀名返回分类名称"""
    ext = os.path.splitext(filename)[1].lower()  # 获取后缀名并转小写
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Others"  # 不在规则里的归到 Others

def organize_folder(folder_path):
    """扫描文件夹，按类型整理文件"""
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print(f"路径不存在: {folder_path}")
        return

    moved_count = 0

    # 遍历文件夹里的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 跳过文件夹，只处理文件
        if os.path.isdir(file_path):
            continue

        # 判断分类
        category = get_category(filename)

        # 创建分类文件夹（如果不存在）
        category_folder = os.path.join(folder_path, category)
        os.makedirs(category_folder, exist_ok=True)

        # 移动文件
        new_path = os.path.join(category_folder, filename)
        os.rename(file_path, new_path)
        print(f"移动: {filename} -> {category}/")
        moved_count += 1

    print(f"\n整理完成！共移动了 {moved_count} 个文件")
    
if __name__ == "__main__":
    target_folder = r"C:\Users\Administrator\Desktop\test_folder"
    organize_folder(target_folder)
