"""
根据文档列表，csv文件，自动生成tushare的skill文档库，并更新接口列表
"""
import re
import os

import pandas as pd


class Node:
    id: int
    parent_id: int
    is_doc: bool
    key: str
    title: str
    desc: str = ''
    name: str
    dir_path: str
    file_path: str
    content: str
    children: list['Node']
    categories: list[str]

def parse_df_recursive(df: pd.DataFrame, parent_id: int, parent_titles: list[str], docs: list[dict] = None, path='') -> list['Node']:
    nodes = []
    for _, row in df[df['PARENT_ID'] == parent_id].iterrows():
        # title 转为 name， 作为文件路径和文件名
        name = re.sub(r'[<>:"/\\|?*]', '', row.TITLE)
        name = name.replace('（', '(')
        name = name.replace('）', ')')

        # 实例化Node对象
        node = Node()
        node.id = row['ID']
        node.parent_id = parent_id
        node.is_doc = row['IS_DOC']
        node.title = row['TITLE']
        node.name = name
        node.dir_path = os.path.join(path, node.name)
        node.file_path = os.path.join(path, node.name+'.md')
        node.content = row['SRC_CONTENT']
        node.categories = parent_titles
        if isinstance(node.content, str):
            # 解析接口key
            mm = (re.search(r'接口[:： ]+(?P<key>[a-zA-Z0-9_]+)', node.content) or
                  re.search(r'\*\*接口名称\*\*[:： ]+(?P<key>[a-zA-Z0-9_]+)', node.content) or
                  re.search(r'\*\*接口\*\*[:： ]+(?P<key>[a-zA-Z0-9_]+)', node.content))
            if mm:
                node.key = mm.group('key').strip()
            # 解析接口描述
            mm = re.search(r'描述[:： ]+(?P<desc>.+)\n', node.content)
            if mm:
                node.desc = mm.group('desc').strip()
        nodes.append(node)
        if node.is_doc and isinstance(docs, list):
            docs.append({
                'id': node.id,
                'key': node.key,
                'title': f'[{node.title}]({node.file_path})',
                'categories': ','.join(node.categories),
                'desc': node.desc,
            })
        node.children = parse_df_recursive(df, node.id, parent_titles + [node.name], docs, node.dir_path)
    return nodes


def create_dir_file_recursive(children: list[Node], path: str):
    for child in children:
        if child.is_doc:
            with open(os.path.join(path, child.file_path), 'w', encoding='utf-8') as f:
                f.write(child.content)
        else:
            os.makedirs(os.path.join(path, child.dir_path), exist_ok=True)
            create_dir_file_recursive(child.children, path)


def main():
    # 读取csv文件，头信息为：ID, PARENT_ID, TITLE, SRC_CONTENT(markdown格式)
    df = pd.read_csv('data/api-doc.csv.csv')
    df = df.drop(df[df["TITLE"] == "历史Tick行情"].index)
    docids = set[int](df['PARENT_ID'].tolist())
    df['IS_DOC'] = ~df['ID'].isin(docids)
    print(df)
    docs = []
    node = parse_df_recursive(df, 2, [], docs, 'references')

    # 生成文件
    create_dir_file_recursive(node, 'tushare')

    # 生成markdown
    df_md = pd.DataFrame(docs)
    df_md.sort_values(by=['categories'], inplace=True)
    df_md.rename(columns={
        'id': 'ID',
        'title': '标题(详细文档)',
        'key': '接口名',
        'categories': '分类',
        'desc': '描述'
    }, inplace=True)
    df_md.to_markdown('data/docs.md', index=False)


if __name__ == "__main__":
    main()
