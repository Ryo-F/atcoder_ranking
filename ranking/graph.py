rom django.core.urlresolvers import reverse
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, CreateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.utils import timezone


from atcoder_ranking.commons import *
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .forms import RegisterForm, CreatePostsForm, LoginForm
from .models import *
###
from django.shortcuts import render
import urllib
import json
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import datetime as dt
import pdb


def plotResults(users, results):
    users_list = []
    python_len_list = np.array([])
    cpp_len_list = np.array([])
    others_len_list = np.array([])
    for user in users.all():
        users_list.append(str(user))
        python_len_list = np.append(python_len_list,
                                    len(results.filter(user=user, result_language='Python')))
        cpp_len_list = np.append(cpp_len_list,
                                 len(results.filter(user=user, result_language='C++')))
        others_len_list = np.append(others_len_list,
                                    len(results.filter(user=user, result_language='Others')))
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    left = np.arange(len(users_list))

    p1 = ax.barh(left, others_len_list, color="blue")
    p2 = ax.barh(left, cpp_len_list,
                 left=others_len_list, color="skyblue")
    p3 = ax.barh(left, python_len_list, left=cpp_len_list +
                 others_len_list, color="lightblue")
    ax.legend((p1[0], p2[0], p3[0]), ("Others", "C++", "Python"))
    ax.set_xlabel('Score')
    ax.set_ylabel('Users')
    ax.set_yticklabels(users_list, fontdict=None, minor=False)
    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)

    return response
