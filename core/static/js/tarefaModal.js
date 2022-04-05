function atualizarModal(tarefaId) {
	/*
		Busca a tarefa no banco de dados e atualiza o modal com os dados da tarefa.
	*/

	let request = new XMLHttpRequest();
	request.open('GET', '/get_tarefa/' + tarefaId, true);
	request.send();

	request.onreadystatechange = function() {
		if (request.readyState == request.DONE) {
			let response = JSON.parse(request.responseText);
			let titulo = document.getElementById('modal-title');
			let body = document.getElementById('modal-body');
			let btnSalvar = document.getElementById('btn-salvar');
			let labelPrioridades = ['Indefinida', 'Baixa', 'Média', 'Alta'][response.prioridade];
			let classPrioridades = ['bg-secondary', 'bg-primary', 'bg-warning text-dark', 'bg-danger'][response.prioridade];

			titulo.innerText = response.titulo;
			body.innerHTML = '';
			if (response.concluida) {
				btnSalvar.innerText = 'Marcar como não concluída';
				btnSalvar.setAttribute('onclick', 'salvarTarefa(' + response.id + ', false)');
			} else {
				btnSalvar.innerText = 'Marcar como concluída';
				btnSalvar.setAttribute('onclick', 'salvarTarefa(' + response.id + ', true)');
			}

			if (response.imagem) {
				let imagem = document.createElement('img');
				imagem.src = response.imagem;
				imagem.setAttribute('class', 'img-fluid');
				body.appendChild(imagem);
			}
			let descricao = document.createElement('p');
			descricao.innerHTML = `
			Criado em: ${response.data_criacao}<br>
			Prazo para conclusão: ${response.data_prevista}<br>
			Prioridade: <span class="badge ${classPrioridades}">${labelPrioridades}</span><br><br>
			${response.descricao}`;
			body.appendChild(descricao);
		}
	}
}

function salvarTarefa(tarefaId, concluida) {
	/* Marca uma tarefa como concluída ou não concluída */

	let request = new XMLHttpRequest();
	let url = concluida ? '/marcar_concluida/' : '/marcar_nao_concluida/';
	request.open('GET', url + tarefaId, true);
	request.send();

	request.onreadystatechange = function() {
		if (request.readyState == request.DONE) {
			if (request.status == 200) {
				window.location.reload();
			} else if (request.status == 403) {
				let modalBody = document.getElementById('modal-body');
				modalBody.innerHTML += "<p class='alert alert-warning'>Você não tem permissão para realizar esta ação.</p>";
			} else {
				let modalBody = document.getElementById('modal-body');
				modalBody.innerHTML += "<p class='alert alert-danger'>Ocorreu um erro inesperado e não foi possivel realizar esta ação.</p>";
			}
		}
	}
}
