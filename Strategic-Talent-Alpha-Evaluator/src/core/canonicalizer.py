import re
import unicodedata
import hashlib
import base64
from pydantic import BaseModel, Field

# 定义洗消后的“纯净数据体”标准 (Schema)
class CanonicalDocument(BaseModel):
    raw_text_hash: str
    canonical_text_hash: str
    source_format: str = "text"
    normalization_version: str = "v1.0"
    canonical_text: str
    risk_flags: list[str] = Field(default_factory=list)

class ResumeCanonicalizer:
    """简历标准化与洗消引擎 (防御 Prompt Injection 的第一道物理门)"""
    
    def __init__(self):
        self.version = "v1.0"
        # 匹配常见的 Zero-width characters (零宽字符)
        self.zero_width_pattern = re.compile(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]')
        # 匹配基础的 HTML 标签
        self.html_pattern = re.compile(r'<[^>]+>')
        # 匹配可能是 Base64 编码的长字符串 (简单探针)
        self.base64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

    def _generate_hash(self, text: str) -> str:
        """生成绝对一致的 MD5 指纹"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _detect_base64_injection(self, text: str) -> bool:
        """探针：检测是否隐藏了 Base64 密文"""
        matches = self.base64_pattern.findall(text)
        for match in matches:
            try:
                # 尝试解码，如果解码出来是可读的指令词汇，就是实锤注入
                decoded = base64.b64decode(match).decode('utf-8').lower()
                if "ignore" in decoded or "instruction" in decoded:
                    return True
            except:
                continue
        return False

    def normalize(self, raw_text: str) -> CanonicalDocument:
        risk_flags = []
        
        # 1. 记录原始罪证 (Raw Hash)
        raw_hash = self._generate_hash(raw_text)

        # 2. 物理洗消：剥离 HTML / Markdown 隐藏文本
        text = self.html_pattern.sub(' ', raw_text)

        # 3. 物理洗消：剔除零宽字符 (防止 Pyth\u200Bon 骗过正则)
        if self.zero_width_pattern.search(text):
            risk_flags.append("DETECTED_ZERO_WIDTH_CHARS")
            text = self.zero_width_pattern.sub('', text)

        # 4. 物理洗消：Unicode 统一化 (将同形字如 admin 强行转为标准字母)
        # NFKC: 兼容分解并重新组合，最严格的标准化
        text = unicodedata.normalize('NFKC', text)

        # 5. 探针扫描：Base64 恶意指令探测
        if self._detect_base64_injection(text):
            risk_flags.append("DETECTED_BASE64_INJECTION")

        # 6. 规整空白字符
        text = re.sub(r'\s+', ' ', text).strip()

        # 7. 记录洗消后的纯净指纹 (Canonical Hash)
        canonical_hash = self._generate_hash(text)

        return CanonicalDocument(
            raw_text_hash=raw_hash,
            canonical_text_hash=canonical_hash,
            normalization_version=self.version,
            canonical_text=text,
            risk_flags=risk_flags
        )