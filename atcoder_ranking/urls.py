from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
# import ranks.views as ranks_view
import ranking.views as ranking_view

urlpatterns = [
    # admin
    url(r'^admin/?', admin.site.urls),

    url(r'^$', ranking_view.TopView.as_view()),
    url(r'^top/', ranking_view.TopView.as_view()),

    # ranking
    url(r'^ranking/?$', ranking_view.IndexView.as_view()),
    url(r'^ranking/mypage/$', ranking_view.MyPageView.as_view()),
    url(r'^ranking/create/$', ranking_view.CreateUserView.as_view()),
    url(r'^ranking/users/$', ranking_view.UsersView.as_view()),
    url(r'^ranking/problems/$', ranking_view.ProblemsView.as_view()),
    url(r'^ranking/posts/$', ranking_view.PostsView.as_view()),
    url(r'^ranking/posts/(?P<posts_id>[0-9]+)/$',
        ranking_view.PostsDetailView.as_view()),
    url(r'^ranking/create_posts/$', ranking_view.CreatePostsView.as_view()),
    url(r'^ranking/info/$', TemplateView.as_view(template_name='user_info.html')),
    url(r'^ranking/login/$', ranking_view.login, name='login'),
    url(r'^ranking/logout/$', ranking_view.logout, name='logout')
]
