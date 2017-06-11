from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
# import ranks.views as ranks_view
import ranking.views as ranking_view

urlpatterns = [
    url(r'^admin/?', admin.site.urls),

    # ranking
    url(r'^$', ranking_view.TopView.as_view()),
    url(r'^top/', ranking_view.TopView.as_view()),
    url(r'^ranking/?$', ranking_view.IndexView.as_view()),
    url(r'^ranking/mypage/$', ranking_view.MyPageView.as_view()),
    url(r'^ranking/create/$', ranking_view.CreateUserView.as_view()),
    url(r'^ranking/login/$', ranking_view.login, name='login'),
    url(r'^ranking/logout/$', ranking_view.logout, name='logout')
]
