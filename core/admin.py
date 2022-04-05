from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
	list_display = ('titulo', 'data_prevista', 'data_conclusao', 'concluida', 'prioridade')
