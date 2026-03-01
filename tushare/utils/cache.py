#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据缓存工具类
"""

import os
import json
import pickle
import datetime
import hashlib


class DataCache:
    """
    数据缓存类
    """
    
    def __init__(self, cache_dir='./cache', expire_hours=24):
        """
        初始化缓存
        
        Args:
            cache_dir: 缓存目录
            expire_hours: 缓存过期时间（小时）
        """
        self.cache_dir = cache_dir
        self.expire_hours = expire_hours
        
        # 创建缓存目录
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_key(self, func_name, **kwargs):
        """
        生成缓存键
        
        Args:
            func_name: 函数名
            **kwargs: 参数
        
        Returns:
            str: 缓存键
        """
        # 构建键字符串
        key_str = f"{func_name}:{json.dumps(kwargs, sort_keys=True)}"
        # 使用MD5生成唯一键
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache_file(self, key):
        """
        获取缓存文件路径
        
        Args:
            key: 缓存键
        
        Returns:
            str: 缓存文件路径
        """
        return os.path.join(self.cache_dir, f"{key}.pkl")
    
    def get(self, func_name, **kwargs):
        """
        获取缓存数据
        
        Args:
            func_name: 函数名
            **kwargs: 参数
        
        Returns:
            object: 缓存数据，如果不存在或已过期则返回None
        """
        key = self._get_cache_key(func_name, **kwargs)
        cache_file = self._get_cache_file(key)
        
        # 检查缓存文件是否存在
        if not os.path.exists(cache_file):
            return None
        
        # 检查缓存是否过期
        mtime = os.path.getmtime(cache_file)
        expire_time = mtime + self.expire_hours * 3600
        if datetime.datetime.now().timestamp() > expire_time:
            # 删除过期缓存
            os.remove(cache_file)
            return None
        
        # 读取缓存数据
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
            return data
        except Exception as e:
            print(f"读取缓存失败：{e}")
            return None
    
    def set(self, func_name, data, **kwargs):
        """
        设置缓存数据
        
        Args:
            func_name: 函数名
            data: 数据
            **kwargs: 参数
        """
        key = self._get_cache_key(func_name, **kwargs)
        cache_file = self._get_cache_file(key)
        
        # 写入缓存数据
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"写入缓存失败：{e}")
    
    def clear(self):
        """
        清空所有缓存
        """
        try:
            for file in os.listdir(self.cache_dir):
                if file.endswith('.pkl'):
                    os.remove(os.path.join(self.cache_dir, file))
            print("缓存已清空")
        except Exception as e:
            print(f"清空缓存失败：{e}")
    
    def clear_expired(self):
        """
        清理过期缓存
        """
        try:
            count = 0
            for file in os.listdir(self.cache_dir):
                if file.endswith('.pkl'):
                    cache_file = os.path.join(self.cache_dir, file)
                    mtime = os.path.getmtime(cache_file)
                    expire_time = mtime + self.expire_hours * 3600
                    if datetime.datetime.now().timestamp() > expire_time:
                        os.remove(cache_file)
                        count += 1
            print(f"清理了 {count} 个过期缓存")
        except Exception as e:
            print(f"清理过期缓存失败：{e}")
