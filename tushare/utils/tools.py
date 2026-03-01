#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import pandas as pd
import numpy as np
import datetime
import os


def format_date(date_str):
    """
    格式化日期字符串
    
    Args:
        date_str: 日期字符串
    
    Returns:
        str: 格式化后的日期字符串 (YYYYMMDD)
    """
    if isinstance(date_str, datetime.datetime):
        return date_str.strftime('%Y%m%d')
    elif isinstance(date_str, str):
        # 处理不同格式的日期字符串
        for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d']:
            try:
                return datetime.datetime.strptime(date_str, fmt).strftime('%Y%m%d')
            except ValueError:
                pass
    return date_str


def format_dataframe(df):
    """
    格式化DataFrame
    
    Args:
        df: pandas DataFrame
    
    Returns:
        pandas DataFrame: 格式化后的DataFrame
    """
    if df is None:
        return None
    
    # 处理日期列
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass
    
    # 处理数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def export_to_csv(df, filename):
    """
    导出数据到CSV文件
    
    Args:
        df: pandas DataFrame
        filename: 文件名
    """
    if df is None:
        print("数据为空，无法导出")
        return
    
    # 创建导出目录
    export_dir = './export'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # 导出文件
    file_path = os.path.join(export_dir, filename)
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"数据已导出到：{file_path}")
    except Exception as e:
        print(f"导出失败：{e}")


def export_to_excel(df, filename):
    """
    导出数据到Excel文件
    
    Args:
        df: pandas DataFrame
        filename: 文件名
    """
    if df is None:
        print("数据为空，无法导出")
        return
    
    # 创建导出目录
    export_dir = './export'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    # 导出文件
    file_path = os.path.join(export_dir, filename)
    try:
        df.to_excel(file_path, index=False)
        print(f"数据已导出到：{file_path}")
    except Exception as e:
        print(f"导出失败：{e}")


def calculate_returns(price_series):
    """
    计算收益率
    
    Args:
        price_series: 价格序列
    
    Returns:
        pandas Series: 收益率序列
    """
    if price_series is None or len(price_series) < 2:
        return None
    
    returns = price_series.pct_change()
    return returns


def calculate_macd(price_series, fast_period=12, slow_period=26, signal_period=9):
    """
    计算MACD指标
    
    Args:
        price_series: 价格序列
        fast_period: 快速移动平均线周期
        slow_period: 慢速移动平均线周期
        signal_period: 信号线周期
    
    Returns:
        pandas DataFrame: MACD指标
    """
    if price_series is None or len(price_series) < slow_period:
        return None
    
    # 计算EMA
    ema_fast = price_series.ewm(span=fast_period, adjust=False).mean()
    ema_slow = price_series.ewm(span=slow_period, adjust=False).mean()
    
    # 计算MACD线
    macd_line = ema_fast - ema_slow
    
    # 计算信号线
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    
    # 计算柱状图
    histogram = macd_line - signal_line
    
    # 构建DataFrame
    macd_df = pd.DataFrame({
        'MACD': macd_line,
        'Signal': signal_line,
        'Histogram': histogram
    })
    
    return macd_df


def get_industry_stocks(industry):
    """
    获取指定行业的股票列表
    
    Args:
        industry: 行业名称
    
    Returns:
        list: 股票代码列表
    """
    import tushare as ts
    
    # 初始化pro接口
    pro = ts.pro_api()
    
    try:
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,industry')
        industry_stocks = data[data['industry'] == industry]['ts_code'].tolist()
        return industry_stocks
    except Exception as e:
        print(f"获取行业股票失败：{e}")
        return []
