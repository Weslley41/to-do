function ordenarTarefas(tipo, crescente=true) {
	/* 
		Ao receber um clique em uma label da tabela, ordena as tarefas.
	*/

	let label = document.getElementById('label-' + tipo);

	if (crescente) {
		label.setAttribute('onclick', `ordenarTarefas('${tipo}', false)`);
	} else {
		label.setAttribute('onclick', `ordenarTarefas('${tipo}')`);
	}

	let request = new XMLHttpRequest();
	request.open('GET', '/tarefas_ordenadas/' + tipo + '/' + Number(crescente));
	request.send();

	let tbody = document.querySelector('tbody')
	let body = document.querySelector('body')
	request.onreadystatechange = function() {
		if (request.readyState == request.DONE) {
			document.getElementById('aviso').remove();
			if (request.status == 200) {
				tbody.innerHTML = '';
				let tarefas = JSON.parse(request.responseText).tarefas;
				tarefas.forEach(tarefa => {
					let tr = document.createElement('tr');
					tr.tittle = tarefa.titulo;
					let tdTitulo = document.createElement('td');
					tdTitulo.innerHTML = `<button onclick="atualizarModal(${tarefa.id})" class="btn btn-link text-decoration-none text-black" data-bs-toggle="modal" data-bs-target="#task-details">${tarefa.titulo}</button>`;
					tr.appendChild(tdTitulo);
					let tdCriado = document.createElement('td');
					tdCriado.innerText = formatarData(tarefa.data_criacao);
					tr.appendChild(tdCriado);
					let tdData = document.createElement('td');
					let tdConcluido = document.createElement('td');
					if (tarefa.concluida) {
						tdData.innerText = formatarData(tarefa.data_conclusao);
						tdConcluido.innerHTML = '<span class="badge bg-success">Sim</span>';
					} else {
						tdData.innerText = formatarData(tarefa.data_prevista);
						tdConcluido.innerHTML = '<span class="badge bg-danger">Não</span>';
					}
					tr.appendChild(tdData);
					tr.appendChild(tdConcluido);
					let tdPrioridade = document.createElement('td');
					if (tarefa.prioridade == 0) {
						tdPrioridade.innerHTML = '<span class="badge bg-secondary">Indefinida</span>';
					} else if (tarefa.prioridade == 1) {
						tdPrioridade.innerHTML = '<span class="badge bg-primary">Baixa</span>';
					} else if (tarefa.prioridade == 2) {
						tdPrioridade.innerHTML = '<span class="badge bg-warning text-dark">Média</span>';
					} else {
						tdPrioridade.innerHTML = '<span class="badge bg-danger">Alta</span>';
					}
					tr.appendChild(tdPrioridade);
					tbody.appendChild(tr);
				});
			} else {
				// Mensagem de erro
				tbody.innerHTML = '';
				let aviso = document.createElement('div');
				aviso.id = 'aviso';
				aviso.setAttribute('class', 'alert alert-danger container');
				aviso.innerHTML = 'Erro ao ordenar tarefas';
				body.appendChild(aviso);
			}
		} else {
			// Mensagem de carregamento
			if (document.getElementById('aviso')) {
				document.getElementById('aviso').remove();
			}
			tbody.innerHTML = '';
			let aviso = document.createElement('div');
			aviso.id = 'aviso';
			aviso.setAttribute('class', 'alert alert-info container');
			aviso.innerHTML = 'Carregando...';
			body.appendChild(aviso);
		}
	}
}

function formatarData(data) {
	/*
		Formata uma data para: dd de mm(string) de yyyy às hh:mm
		ex: "01 de janeiro de 2020 às 21:30"
	*/

	let listaMeses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
	data = new Date(data);
	let dia = data.getDate();
	let mes = listaMeses[data.getMonth()];
	let ano = data.getFullYear();

	return `${dia} de ${mes} de ${ano} às ` + data.toLocaleTimeString().substring(0, 5);
}
