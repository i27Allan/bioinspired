"""nqueens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import nqueens.views
import ackley.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', nqueens.views.index, name='index'),
    url(r'^nqueens/$', nqueens.views.IndexView.as_view(), name='index_queens'),
    url(r'^nqueens/solve$', nqueens.views.IndexView.as_view(), name='solve_queens'),
    url(r'^ackley/$', ackley.views.IndexView.as_view(), name='index_ackley'),
    url(r'^ackley/solve/$', ackley.views.IndexView.as_view(), name='solve_ackley'),
    url(r'^ackley/docs/pt/$', ackley.views.docs, name='docs_ackley')
]

