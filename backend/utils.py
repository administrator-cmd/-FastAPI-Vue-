import markdown
import bleach

# 允许的 HTML 标签和属性（根据需求调整）
ALLOWED_TAGS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
    'ul', 'ol', 'li',
    'strong', 'em', 'b', 'i', 'u', 'strike',
    'a', 'img', 'code', 'pre', 'blockquote',
    'table', 'thead', 'tbody', 'tr', 'th', 'td'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt', 'title'],
    'code': ['class'],
    'pre': ['class'],
    '*': ['class']   # 允许 class 属性（用于代码高亮等）
}

def render_markdown(text: str) -> str:
    """将 Markdown 转为安全的 HTML"""
    # 1. 转换为 HTML
    html = markdown.markdown(
        text,
        extensions=[
            'extra',          # 表格、脚注等
            'codehilite',     # 代码高亮（需配合 CSS）
            'toc',            # 目录
            'nl2br',          # 换行转 <br>
        ]
    )
    # 2. 清洗 HTML，移除危险标签和属性
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True          # 移除不允许的标签而不是转义
    )
    return clean_html