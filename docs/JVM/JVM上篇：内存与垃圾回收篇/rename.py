import os
import time
import re

def is_timestamp(filename):
    """
    判断文件名是否已经是时间戳格式。
    时间戳格式定义为 yyyyMMddHHmmssSSS，例如 20240406213535387。
    """
    return re.match(r'^\d{17}$', filename) is not None

def generate_timestamp_filename(extension):
    """
    生成基于当前时间的时间戳文件名。
    """
    timestamp = time.strftime('%Y%m%d%H%M%S') + str(int(round(time.time() * 1000)))[-3:]
    new_name = f"{timestamp}{extension}"
    return new_name, timestamp

def update_md_references(root_dir, old_name, new_name, timestamp):
    """
    更新Markdown文件中的图片引用。
    """
    md_img_pattern = re.compile(r'!\[(.*?)\]\((images\/' + re.escape(old_name) + r')\)')
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as md_file:
                    content = md_file.read()
                
                new_content, n = md_img_pattern.subn(lambda m: f"![{timestamp}](images/{new_name})", content)
                if n > 0:
                    with open(file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(new_content)
                    print(f"已更新文件 {file} 中的图片引用。")

def main():
    root_dir = os.getcwd()
    images_dir = os.path.join(root_dir, "images")

    for filename in os.listdir(images_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            base_name, extension = os.path.splitext(filename)
            if is_timestamp(base_name):
                print(f"文件名 {filename} 已是时间戳格式，跳过重命名。")
                continue
            
            new_filename, timestamp = generate_timestamp_filename(extension)
            new_path = os.path.join(images_dir, new_filename)
            original_path = os.path.join(images_dir, filename)
            os.rename(original_path, new_path)
            update_md_references(root_dir, filename, new_filename, timestamp)
            
            print(f"已将 {filename} 重命名为 {new_filename} 并更新了Markdown文件中的引用。")

if __name__ == "__main__":
    main()
