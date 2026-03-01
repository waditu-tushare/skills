#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志工具类
"""

import logging
import os
import datetime


class Logger:
    """
    日志类
    """
    
    def __init__(self, name='tushare', log_dir='./logs', level=logging.INFO):
        """
        初始化日志
        
        Args:
            name: 日志名称
            log_dir: 日志目录
            level: 日志级别
        """
        self.name = name
        self.log_dir = log_dir
        self.level = level
        
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 生成日志文件名
        log_file = os.path.join(self.log_dir, f"{name}_{datetime.datetime.now().strftime('%Y%m%d')}.log")
        
        # 创建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 创建file handler
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            
            # 创建console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            
            # 定义日志格式
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加handler
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """
        记录debug级别的日志
        
        Args:
            message: 日志信息
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        记录info级别的日志
        
        Args:
            message: 日志信息
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        记录warning级别的日志
        
        Args:
            message: 日志信息
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        记录error级别的日志
        
        Args:
            message: 日志信息
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        记录critical级别的日志
        
        Args:
            message: 日志信息
        """
        self.logger.critical(message)
    
    def exception(self, message):
        """
        记录异常信息
        
        Args:
            message: 日志信息
        """
        self.logger.exception(message)


# 创建全局logger实例
logger = Logger()
