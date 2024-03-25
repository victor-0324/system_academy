     // Escopo local para evitar variáveis globais desnecessárias
    var exercicios = [];

    // Detalhes
    function atualizarData() {
        // Obter a data atual no formato desejado (dia/mês/ano)
        var dataAtual = new Date().toLocaleDateString('pt-BR');
        
        // Atualizar o valor da input com a data atual
        document.getElementById('dia').value = dataAtual;
    }

    function utilizarExerciciosExistentes() {
        // Obtenha o nome do aluno a ser pesquisado (você pode modificar isso conforme necessário)
        var nomeAluno = prompt("Digite o nome do aluno:");

        // Faça uma solicitação ao servidor Flask para buscar os exercícios do aluno pelo nome
        fetch('/cadastro/busca_pornome', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }, 
            body: JSON.stringify({ nome_aluno: nomeAluno }), 
        })
        .then(response => response.json())
        .then(data => {
            // Verifique se a busca foi bem-sucedida
            if (data && data.aluno.exercicios) {
                // Adicione os exercícios à lista
                adicionarExercicios(Object.values(data.aluno.exercicios));
            } else {
                alert('Aluno não encontrado ou sem exercícios');
            }
        })
        .catch(error => {
            console.error(error);
            alert('Erro ao buscar aluno');
        });
    }

    // Função para adicionar exercícios à lista
    function adicionarExercicios(novosExercicios) {
        // Adiciona cada novo exercício à lista global
        novosExercicios.forEach(novoExercicio => {
            // Adiciona a propriedade 'id' ao novo exercício
            novoExercicio.id = Date.now();
            const exercicioExistente = exercicios.find(exercicio => (
                exercicio.tipoTreino === novoExercicio.tipoTreino &&
                exercicio.exercicio === novoExercicio.exercicio &&
                exercicio.serie === novoExercicio.serie &&
                exercicio.repeticao === novoExercicio.repeticao &&
                exercicio.descanso === novoExercicio.descanso &&
                exercicio.carga === novoExercicio.carga
            ));
    
            // Adiciona o novo exercício apenas se não estiver na lista
            if (!exercicioExistente) {
                exercicios.push(novoExercicio);
            }
        });
    
        // Limpa a lista de exercícios antes de preenchê-la
        const exerciciosAdicionados = document.getElementById('exerciciosAdicionados');
        exerciciosAdicionados.innerHTML = '';
    
        // Itera sobre os exercícios e adiciona campos de edição à lista
        exercicios.forEach(exercicio => {
            const divExercicio = document.createElement('div');
            divExercicio.className = 'exercicio-editavel';
            
            // Adiciona uma margem inferior para criar espaço entre as divs
            divExercicio.style.marginBottom = '10px'; // Ajuste conforme necessário
            
            const camposEdicao = ['tipoTreino', 'exercicio', 'serie', 'repeticao', 'descanso', 'carga'];
    
            camposEdicao.forEach(campo => {
                const input = document.createElement('input');
                input.type = 'text';
                input.value = exercicio[campo];
                input.setAttribute('data-campo', campo);
                divExercicio.appendChild(input);
            });
    
            exerciciosAdicionados.appendChild(divExercicio);
        });
    }


    // Modific
    // Função para adicionar exercício à lista de visualização
    function adicionarExercicioAListaDeVisualizacao(exercicio) {
        var listaExercicios = document.getElementById('listaExercicios');
    
        var divColMd12Mb6 = document.createElement('div');
        divColMd12Mb6.className = 'col-md-12 mb-6';
    
        var tipoTreino = document.createElement('h5');
        tipoTreino.className = 'mb-3 text-center dia-treino';
        tipoTreino.innerHTML = '<strong>' + exercicio.tipoTreino.replace('&', '&amp;') + '</strong>';
    
        var listaExerciciosItem = document.createElement('ul');
        listaExerciciosItem.className = 'list-group text-left';
    
        var form = document.createElement('form');
        form.onsubmit = function () { return false; };
    
        var camposExercicio = ['exercicio', 'serie', 'repeticao', 'descanso', 'carga'];
    
        camposExercicio.forEach(function (campo) {
            var itemLista = document.createElement('li');
           
            var divCampo = document.createElement('div');
            divCampo.className = 'mb-1';
    
            var strong = document.createElement('strong');
            strong.textContent = campo.charAt(0).toUpperCase() + campo.slice(1) + ': ';
    
            var input = document.createElement('input');
            input.type = 'text';
            input.name = campo;
            input.value = exercicio[campo];
            input.readOnly = true;
    
            divCampo.appendChild(strong);
            divCampo.appendChild(input);
    
            itemLista.appendChild(divCampo);
            form.appendChild(itemLista);
        });
    
        var botaoExcluir = document.createElement('button');
        botaoExcluir.type = 'button';
        botaoExcluir.textContent = 'Excluir';
        botaoExcluir.onclick = function () { excluirExercicioDaLista(exercicio); };
    
        form.appendChild(botaoExcluir);
        listaExerciciosItem.appendChild(form);
        divColMd12Mb6.appendChild(tipoTreino);
        divColMd12Mb6.appendChild(listaExerciciosItem);
    
        listaExercicios.appendChild(divColMd12Mb6);
    }
    
    // Função auxiliar para encontrar o elemento do exercício na lista
    function encontrarElementoExercicioNaLista(exercicio) {
        var listaExercicios = document.getElementById('listaExercicios');
        var elementos = listaExercicios.getElementsByClassName('col-md-12 mb-6');

        for (var i = 0; i < elementos.length; i++) {
            var tipoTreino = elementos[i].querySelector('.dia-treino strong').textContent;
            if (tipoTreino === exercicio.tipoTreino) {
                return elementos[i];
            }
        }

        return null;
    }

    function adicionarExercicioAoDiaTreino(diaTreino, exercicio) {
        // Adiciona um identificador único ao exercício
        exercicio.id = Date.now();
    
        // Cria um novo elemento li para o exercício
        var novoExercicioElemento = document.createElement("li");
        novoExercicioElemento.id = "exercicio-" + exercicio.id;
    
        // Cria uma string com o HTML do exercício
        var exercicioHTML = "<strong>Exercício:</strong> " + exercicio.exercicio + "<br>" +
            "<strong>Série:</strong> " + exercicio.serie + "<br>" +
            "<strong>Repetição:</strong> " + exercicio.repeticao + "<br>" +
            "<strong>Descanso:</strong> " + exercicio.descanso + "<br>" +
            "<strong>Carga:</strong> " + exercicio.carga + "<br>" +
            "<button type='button' onclick='excluirExercicio(\"" + exercicio.id + "\")'>Excluir</button>";
    
        // Define o HTML do exercício no elemento li
        novoExercicioElemento.innerHTML = exercicioHTML;
    
        // Encontra o container do dia de treino correspondente
        var containerDiaTreino = document.querySelector(".dia-treino-" + escapedDiaTreino);
    
        if (containerDiaTreino) {
            // Adiciona o novo exercício ao container do dia de treino
            containerDiaTreino.appendChild(novoExercicioElemento);
        } else {
            console.error("Container do dia de treino não encontrado:", diaTreino);
        }
    }

    function adicionarExercicioAoLista(exercicio) {
        exercicios.push(exercicio);
        adicionarExercicioAListaDeVisualizacao(exercicio);
    }

    // Função para adicionar exercícios do backend à lista
    function adicionarExerciciosDoBackend(exerciciosBackend) {
        exerciciosBackend.forEach(function (exercicio) {
            adicionarExercicioAListaDeVisualizacao(exercicio);
        });
    }

    // Chamada à função ao carregar a página
    document.addEventListener("DOMContentLoaded", function () {
        adicionarExerciciosDoBackend(exerciciosDoBackend);
    });
   

    // Função para excluir exercício da lista
    function excluirExercicioDaLista(exercicio) {
        // Lógica para excluir o exercício da lista
        // Pode ser algo como:
        var listaExercicios = document.getElementById('listaExercicios');
        var elementoExercicio = encontrarElementoExercicioNaLista(exercicio);
    
        if (elementoExercicio) {
            listaExercicios.removeChild(elementoExercicio);
        } else {
            console.error('Exercício não encontrado na lista.');
        }
    }

    // Função para editar exercício na lista
    function editarExercicio(index) {
        var exercicioParaEditar = exercicios[index];
        // Implemente a lógica para editar o exercício conforme necessário
        // Você pode abrir um modal, preencher um formulário, etc.
        console.log('Editar exercício:', exercicioParaEditar);
    }

    // Função chamada ao adicionar exercício manualmente
    function adicionarExercicioManualmente() {
        var diaTreino = document.getElementById('tipoTreino').value;
        var exercicio = document.getElementById('exercicio').value;
        var serie = document.getElementById('serie').value;
        var repeticao = document.getElementById('repeticao').value;
        var descanso = document.getElementById('descanso').value;
        var carga = document.getElementById('carga').value;

        var novoExercicio = {
            tipoTreino: diaTreino,
            exercicio: exercicio,
            serie: serie,
            repeticao: repeticao,
            descanso: descanso,
            carga: carga
        };

        adicionarExercicioAoLista(novoExercicio);
        limparCamposTreino(); // Limpar campos após adicionar exercício
    }

    // Função para atualizar a lista de exercícios na interface
    function atualizarListaExercicios() {
        var listaExercicios = document.getElementById('listaExercicios');
        listaExercicios.innerHTML = ''; // Limpa a lista antes de atualizar

        exercicios.forEach(function (exercicio, index) {
            var itemLista = document.createElement('li');
            itemLista.textContent = `Dia: ${exercicio.tipoTreino}, Exercício: ${exercicio.exercicio}, Série: ${exercicio.serie}, Repetição: ${exercicio.repeticao}, Descanso: ${exercicio.descanso}, Carga: ${exercicio.carga}`;
            

            var excluirBotao = document.createElement('button');
            excluirBotao.textContent = 'Excluir';
            excluirBotao.addEventListener('click', function () {
                excluirExercicio(index);
            });

           
            itemLista.appendChild(excluirBotao);

            listaExercicios.appendChild(itemLista);
        });
    }

    // Função para limpar campos do treino
    function limparCamposTreino() {
        document.getElementById('exercicio').value = '';
        document.getElementById('serie').value = '';
        document.getElementById('repeticao').value = '';
        document.getElementById('descanso').value = '';
        document.getElementById('carga').value = '';
    }
    
    function enviarExerciciosParaServidor() {
    
    // Adicione os exercícios ao formData
    var formData = new FormData(document.querySelector('form'));
    formData.append('exercicios', JSON.stringify(exercicios));

    // Obtenha o ID do aluno da URL
    var alunoId = window.location.pathname.split('/').pop();
    var url = '/alunos/atualizar/' + alunoId;

    // Faça a solicitação POST para o servidor
    fetch(url, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Lida com a resposta do servidor
            // Limpa os exercícios após o envio
            exercicios = [];
            atualizarListaExercicios();
            // Redireciona para a outra página após o cadastro
            window.location.href = '/';
        })
        .catch(error => {
            // Lida com erros
            console.error(error);
        });

    return false; // Impede o envio do formulário
    }
    
    function enviarMedidasParaServidor() {
        // Obtenha os dados das medidas, excluindo os exercícios
        var formData = new FormData(document.querySelector('form'));
        formData.delete('exercicios');
    
    
        // Obtenha o ID do aluno da URL
        var alunoId = window.location.pathname.split('/').pop();
        var url = '/alunos/atualizar/' + alunoId;
    
        // Faça a solicitação POST para o servidor
        fetch(url, {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
       
                // Redireciona para a outra página após o cadastro
                window.location.href = '/';
            })
            .catch(error => {
                // Lida com erros
                console.error(error);
            });
    }
