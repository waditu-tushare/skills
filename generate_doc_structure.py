#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
import re
import codecs

# 读取CSV文件
def read_csv(file_path):
    data = []
    with codecs.open(file_path, 'r', 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 去除ID和PARENT_ID的引号
            row['ID'] = row['ID'].strip('"')
            row['PARENT_ID'] = row['PARENT_ID'].strip('"')
            row['TITLE'] = row['TITLE'].strip('"')
            row['SRC_CONTENT'] = row['SRC_CONTENT'].strip('"') if row['SRC_CONTENT'] else ''
            data.append(row)
    return data

# 构建树结构
def build_tree(data):
    # 创建ID到节点的映射
    node_map = {}
    for item in data:
        node_map[item['ID']] = {
            'id': item['ID'],
            'parent_id': item['PARENT_ID'],
            'title': item['TITLE'],
            'content': item['SRC_CONTENT'],
            'children': []
        }
    
    # 构建树
    root_nodes = []
    for item in data:
        node = node_map[item['ID']]
        parent_id = item['PARENT_ID']
        if parent_id == '2':  # 顶级节点
            root_nodes.append(node)
        elif parent_id in node_map:
            node_map[parent_id]['children'].append(node)
    
    return root_nodes, node_map

# 清理文件名，移除不合法字符
def clean_filename(name):
    # 移除不合法的文件名字符
    return re.sub(r'[<>:"/\\|?*]', '', name)

# 生成目录结构
def generate_structure(root_nodes, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 递归生成结构
    def _generate(node, path):
        # 创建当前节点的目录
        dir_name = clean_filename(node['title'])
        current_path = os.path.join(path, dir_name)
        
        # 检查是否有子节点
        if node['children']:
            # 非叶子节点，只创建目录
            os.makedirs(current_path, exist_ok=True)
            for child in node['children']:
                _generate(child, current_path)
        else:
            # 叶子节点，创建.md文件
            with codecs.open(current_path, 'w', 'utf-8') as f:
                f.write(node['content'])
    
    # 处理所有根节点
    for node in root_nodes:
        _generate(node, output_dir)

if __name__ == "__main__":
    # 读取CSV文件
    csv_file = 'data/api-doc.csv-1772824286286.csv'
    output_dir = 'tushare/references'
    
    data = read_csv(csv_file)
    root_nodes, node_map = build_tree(data)
    generate_structure(root_nodes, output_dir)
    
    print("文档结构已生成到 {} 目录".format(output_dir))
