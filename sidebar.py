
import os

def has_markdown_files(directory):
    """检查目录中是否存在Markdown文件，包括子目录"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                return True
    return False

def list_markdown_files(startpath):
    lines = []  # 用于保存结果的列表
    for root, dirs, files in os.walk(startpath, topdown=True):
        # 移除没有Markdown文件的目录
        dirs[:] = [d for d in dirs if has_markdown_files(os.path.join(root, d))]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '  ' * level
        if root != startpath:  # 避免将起始目录也列出
            subdir = os.path.basename(root)
            lines.append(f"{indent}- {subdir}")
        subindent = '  ' * (level + 1)
        for f in files:
            if f.endswith(".md"):
                file_without_md = f[:-3]  # 去掉文件名中的 ".md"
                relative_path = os.path.join(root, f).replace(startpath + '/', '').replace(' ', '%20')
                # 在Windows中，路径分隔符为`\`，但在Markdown链接中应使用`/`
                relative_path = relative_path.replace('\\', '/')
                lines.append(f"{subindent}- [{file_without_md}]({relative_path})")
    return lines

# 要遍历的目录路径
docs_path = 'docs'
# 获取Markdown文件和符合条件的目录列表
markdown_lines = list_markdown_files(docs_path)
# 输出文件路径
output_file = '_sidebar.md'

# 将结果写入到a.md文件
with open(output_file, 'w', encoding='utf-8') as f:
    for line in markdown_lines:
        f.write(line + '\n')

print(f"Markdown list has been written to {output_file}")
