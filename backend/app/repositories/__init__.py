"""
数据访问层（Repository/DAO）
包含所有数据库操作
"""
from app.repositories.user import (
    get_user_by_id, get_user_by_username, get_user_by_email,
    get_user_count, get_all_users, create_user, authenticate_user
)
from app.repositories.post import (
    get_post_by_id, get_posts_by_user, get_posts, get_post_count,
    create_post, update_post, delete_post
)
from app.repositories.comment import (
    create_comment, get_comments, get_comment_by_id, delete_comment
)

__all__ = [
    "get_user_by_id", "get_user_by_username", "get_user_by_email",
    "get_user_count", "get_all_users", "create_user", "authenticate_user",
    "get_post_by_id", "get_posts_by_user", "get_posts", "get_post_count",
    "create_post", "update_post", "delete_post",
    "create_comment", "get_comments", "get_comment_by_id", "delete_comment"
]
