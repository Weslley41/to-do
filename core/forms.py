from django import forms
from django.core.mail.message import EmailMessage
from .models import Tarefa


class contatoForm(forms.Form):
	""" Formulário de contato """

	nome = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='E-mail')
	assunto = forms.CharField(label='Assunto', max_length=100)
	mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

	def enviar_email(self):
		""" Envia o e-mail para o administrador do sistema """

		nome = self.cleaned_data['nome']
		email = self.cleaned_data['email']
		assunto = self.cleaned_data['assunto']
		mensagem = self.cleaned_data['mensagem']

		conteudo = f"{mensagem}\n\n Enviado por: {nome} ({email})"
		email = EmailMessage(
			from_email='contato@dominio.com',
			to=['contato@dominio.com'],
			headers={'Reply-To': email},
			subject=assunto,
			body=conteudo,
		)

		email.send()


class tarefaForm(forms.ModelForm):
	""" Formulário para criação de nova tarefa """

	class Meta:
		model = Tarefa
		fields = ['titulo', 'descricao', 'imagem', 'data_prevista', 'prioridade']

		labels = {
			'titulo': 'Título',
			'descricao': 'Descrição (opcional)',
			'imagem': 'Imagem (opcional)',
			'data_prevista': 'Data prevista',
			'prioridade': 'Prioridade',
		}

		widgets = {
			'descricao': forms.Textarea(attrs={'rows': 4}),
			# datetime picker
			'data_prevista': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
			'prioridade': forms.Select(attrs={'class': 'form-control'}, choices={
				(0, 'Indefinida'),
				(1, 'Baixa'),
				(2, 'Média'),
				(3, 'Alta'),
			}),
		}
