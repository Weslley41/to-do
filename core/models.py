from django.db import models
from stdimage.models import StdImageField


class Tarefa(models.Model):
	""" Modelo de tarefa """
	# Campos a serem preenchidos ao criar uma nova tarefa
	titulo = models.CharField(max_length=100)
	descricao = models.TextField(null=True, blank=True)
	imagem = StdImageField(upload_to='tarefas', null=True, blank=True)
	data_prevista = models.DateTimeField()
	prioridade = models.IntegerField(default=0)
	# Campos preenchidos automaticamente ou posteriormente
	data_criacao = models.DateTimeField(auto_now_add=True)
	data_conclusao = models.DateTimeField(null=True, blank=True)
	concluida = models.BooleanField(default=False)

	def __str__(self):
		return self.titulo + ' - concluída' if self.concluida else self.titulo


	def get_infos(self):
		""" Retorna informações da tarefa """

		infos = {
			'id': self.id,
			'titulo': self.titulo,
			'descricao': self.descricao,
			'imagem': self.imagem.url if self.imagem else None,
			'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M'),
			'data_prevista': self.data_prevista.strftime('%d/%m/%Y %H:%M'),
			'prioridade': self.prioridade,
			'concluida': self.concluida,
		}

		return infos


	def concluir(self):
		""" Marca a tarefa como concluída """

		from datetime import datetime

		self.concluida = True
		self.data_conclusao = datetime.now()
		self.save()


	def desfazer_concluir(self):
		""" Marca a tarefa como não concluída """

		self.concluida = False
		self.data_conclusao = None
		self.save()
