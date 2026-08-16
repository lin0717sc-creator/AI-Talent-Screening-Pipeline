import logging
import os
from config.settings import STORAGE_REGISTRY

# ==========================================
# 📝 V5.0 工业级合规审计日志总控塔 (Audit Trail)
# ==========================================

def setup_system_logger():
    """
    配置并启动全局监控雷达：同时向终端和物理硬盘 (logs/) 输出合规日志
    """
    log_dir = STORAGE_REGISTRY.get('log_dir', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, 'system_audit.log')

    # 创建一个全局 logger
    logger = logging.getLogger("Talent-Alpha-Engine")
    
    # 避免重复绑定句柄导致日志打印两次
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # 制定大厂标准的雷达时间戳格式: [时间] [级别] [执行模块] - 物理事件
        formatter = logging.Formatter(
            fmt='[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 通道一：物理落盘 (FileHandler) - 满足 PDPA 合规，永久留痕
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # 通道二：终端轰鸣 (StreamHandler) - 满足指挥官肉眼监控
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

    return logger

# 启动单例雷达，全系统共享此探针
SYSTEM_LOGGER = setup_system_logger()