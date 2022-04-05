from django.contrib import admin
from django.urls import path

from .views import (index, nova_tarefa, contato, get_tarefa, marcar_tarefa_concluida,
										marcar_tarefa_nao_concluida, ordenar_tarefas)

urlpatterns = [
	path('', index, name='index'),
	path('nova_tarefa/', nova_tarefa, name='nova_tarefa'),
	path('contato/', contato, name='contato'),
	path('get_tarefa/<int:id>/', get_tarefa, name='get_tarefa'),
	path('marcar_concluida/<int:id>/', marcar_tarefa_concluida, name='marcar_tarefa_concluida'),
	path('marcar_nao_concluida/<int:id>/', marcar_tarefa_nao_concluida, name='marcar_tarefa_nao_concluida'),
	path('tarefas_ordenadas/<str:ordem>/<int:crescente>', ordenar_tarefas, name='ordenar_tarefas'),
]
