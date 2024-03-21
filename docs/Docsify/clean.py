import os
import re

# 设定当前工作目录
current_dir = os.getcwd()

# Markdown 文件所在的目录
markdown_dir = current_dir

# 图片所在的目录
images_dir = os.path.join(current_dir, 'images')

# 收集所有图片文件名
image_files = {f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))}

# 收集所有 Markdown 文件名
markdown_files = [f for f in os.listdir(markdown_dir) if f.endswith('.md')]

# 用于查找图片引用的正则表达式
pattern = r'!\[.*?\]\((.*?)\)'

# 遍历所有 Markdown 文件，检查图片引用
for md_file in markdown_files:
    with open(os.path.join(markdown_dir, md_file), 'r', encoding='utf-8') as file:
        content = file.read()
        # 查找所有的图片引用
        referenced_images = re.findall(pattern, content)
        for img in referenced_images:
            # 处理相对路径引用的图片
            img_path = os.path.normpath(os.path.join(markdown_dir, img))
            img_name = os.path.basename(img_path)
            image_files.discard(img_name)

# 删除未被引用的图片
for img in image_files:
    os.remove(os.path.join(images_dir, img))
    print(f'Deleted {img}')

print('Cleanup complete.')
