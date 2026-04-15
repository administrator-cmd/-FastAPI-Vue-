"""
Markdown 渲染工具
"""
import markdown
import bleach


# 允许的 HTML 标签和属性
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
    '*': ['class']
}


def render_markdown(text: str) -> str:
    """将 Markdown 转为安全的 HTML"""
    # 转换为 HTML
    html = markdown.markdown(
        text,
        extensions=[
            'extra',
            'codehilite',
            'toc',
            'nl2br',
        ]
    )
    
    # 清洗 HTML，移除危险标签和属性
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return clean_html
