from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import contatoForm, tarefaForm
from .models import Tarefa

def index(request):
	"""
		Página inicial.
		...
		Exibe a lista de tarefas, ordenadas por prioridade/data prevista.
		Tarefas não concluídas ficam no topo eventualmente.
	"""

	tarefas = Tarefa.objects.all().order_by('concluida', '-prioridade', 'data_prevista')

	context = {
		'tarefas': tarefas.values('id', 'titulo', 'data_criacao','data_prevista', 'data_conclusao', 'prioridade', 'concluida')
	}

	return render(request, 'index.html', context)


def nova_tarefa(request):
	"""
		Página de criação de nova tarefa.
		- Restrita a usuários autenticados!
		...
		Exibe o formulário de criação de nova tarefa.
		Cadastra uma nova tarefa no banco de dados.
	"""

	if (request.method == 'POST'):
		form = tarefaForm(request.POST, request.FILES)
		if (form.is_valid()):
			form.save()
			messages.success(request, 'Tarefa cadastrada com sucesso!')
		else:
			messages.error(request, 'Erro ao cadastrar tarefa!')

	context = {
		'form': tarefaForm()
	}

	if (request.user.is_authenticated):
		return render(request, 'nova_tarefa.html', context)
	else:
		return render(request, 'acesso_negado.html')


def contato(request):
	"""
		Página de contato.
		...
		Exibe o formulário de contato.
		Envia um e-mail para o administrador do sistema.
	"""
	if (request.method == 'POST'):
		form = contatoForm(request.POST)
		if (form.is_valid()):
			form.enviar_email()
			messages.success(request, 'Mensagem enviada com sucesso!')
		else:
			messages.error(request, 'Erro ao enviar mensagem!')

	context = {
		'form': contatoForm()
	}

	return render(request, 'contato.html', context)


# ações
def get_tarefa(request, id):
	"""
		Retorna informações de uma tarefa específica(JSON).
	"""
	tarefa = get_object_or_404(Tarefa, id=id)

	return JsonResponse(tarefa.get_infos())


def marcar_tarefa_concluida(request, id):
	"""
		Marca uma tarefa como concluída.
		- Restrito a usuários autenticados!
	"""
	tarefa = get_object_or_404(Tarefa, id=id)

	if (request.user.is_authenticated):
		tarefa.concluir()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=403)


def marcar_tarefa_nao_concluida(request, id):
	"""
		Marca uma tarefa como não concluída.
		- Restrito a usuários autenticados!
	"""
	tarefa = get_object_or_404(Tarefa, id=id)

	if (request.user.is_authenticated):
		tarefa.desfazer_concluir()
		return HttpResponse(status=200)
	else:
		return HttpResponse(status=403)


def ordenar_tarefas(request, ordem, crescente):
	"""
		Params:
			(string) ordem: campo a ser ordenado
			(int) crescente: 1 para crescente, 0 para decrescente

		Retorna a lista de tarefas ordenadas(JSON).
	"""

	lista_ordenacao = {
		'nome': ('titulo', 'data_prevista'),
		'criacao': ('data_criacao', 'data_prevista'),
		'previsao': ('concluida', 'data_prevista'),
		'concluida': ('concluida', 'data_conclusao'),
		'prioridade': ('prioridade', 'data_prevista'),
	}
	if (ordem == 'previsao' and not crescente):
		ordem = ('concluida', '-data_prevista')
	else:
		ordem = lista_ordenacao[ordem] if crescente else ('-' + lista_ordenacao[ordem][0], lista_ordenacao[ordem][1])

	tarefas = Tarefa.objects.all().order_by(ordem[0], ordem[1])

	context = {
		'tarefas': list(tarefas.values('id', 'titulo', 'data_criacao','data_prevista', 'data_conclusao', 'prioridade', 'concluida'))
	}

	return JsonResponse(context)
