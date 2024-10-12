"""
認証関連のBlueprintを定義するモジュール。
"""

from flask import Blueprint

bp = Blueprint("auth", __name__)

# 循環インポートを避けるために、この行を下に移動します。
from app.auth import routes
