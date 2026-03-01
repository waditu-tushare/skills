#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理工具类
"""

from .logger import logger
import time


class ErrorHandler:
    """
    错误处理类
    """
    
    @staticmethod
    def handle_api_error(func):
        """
        API错误处理装饰器
        
        Args:
            func: 被装饰的函数
        
        Returns:
            function: 装饰后的函数
        """
        def wrapper(*args, **kwargs):
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retry_count += 1
                    logger.error(f"API调用失败 ({retry_count}/{max_retries}): {str(e)}")
                    
                    # 根据错误类型决定是否重试
                    if "网络" in str(e) or "timeout" in str(e).lower():
                        logger.info(f"正在重试... ({retry_count}/{max_retries})")
                        time.sleep(2 ** retry_count)  # 指数退避
                    else:
                        # 其他错误直接抛出
                        logger.error(f"无法重试的错误: {str(e)}")
                        raise
            
            # 达到最大重试次数
            logger.error(f"达到最大重试次数 ({max_retries})，API调用失败")
            return None
        
        return wrapper
    
    @staticmethod
    def validate_params(params, required_fields):
        """
        验证参数
        
        Args:
            params: 参数字典
            required_fields: 必填字段列表
        
        Returns:
            bool: 验证是否通过
        """
        for field in required_fields:
            if field not in params or params[field] is None:
                logger.error(f"缺少必填参数: {field}")
                return False
        return True
    
    @staticmethod
    def format_error_message(error):
        """
        格式化错误信息
        
        Args:
            error: 错误对象
        
        Returns:
            str: 格式化后的错误信息
        """
        return f"{type(error).__name__}: {str(error)}"
