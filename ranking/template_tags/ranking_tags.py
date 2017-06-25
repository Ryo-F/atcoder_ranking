from django import template

from ranking.views import *
from ranking.models import *

register = template.Library()

# 使ってないなら消そう！
# これを使うには、パッケージ名はtemplatetagsにして、モジュールに__init__.py
# を追加しよう〜
