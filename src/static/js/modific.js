     // Escopo local para evitar variáveis globais desnecessárias
    var exercicios = [];


    function atualizarData() {
        // Obter a data atual no formato desejado (dia/mês/ano)
        var dataAtual = new Date().toLocaleDateString('pt-BR');
        
        // Atualizar o valor da input com a data atual
        document.getElementById('dia').value = dataAtual;
    }

    function atualizarCamposExercicio() {
        var opcaoExercicio = document.getElementById('opcaoExercicio').value;
        var cadastroTreinoForm = document.getElementById('cadastroTreinoForm');
     
        // Mostra ou oculta os elementos com base na escolha do administrador
        cadastroTreinoForm.style.display = opcaoExercicio === 'adicionarNovo' ? 'block' : 'none';
        cadastroTreinoForm.style.display = opcaoExercicio === 'Busca' ? 'block' : 'none';
        if (opcaoExercicio === 'Busca') {
            // Chama a função para buscar exercícios pelo nome do aluno
            utilizarExerciciosExistentes();
        }
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
            // Verifica se o exercício já está na lista
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

    function adicionarExercicioManualmente() {
        var tipoTreino = document.getElementById('tipoTreino').value;
        var exercicio = document.getElementById('exercicio').value;
        var serie = document.getElementById('serie').value;
        var repeticao = document.getElementById('repeticao').value;
        var descanso = document.getElementById('descanso').value;
        var carga = document.getElementById('carga').value;

        // Verifica se todos os campos estão preenchidos
        if (!tipoTreino || !exercicio || !serie || !repeticao || !descanso || !carga) {
            alert('Por favor, preencha todos os campos do exercício.');
            return;
        }

        // Adiciona ou edita um exercício à lista
        var exercicioInfo = {
            'tipoTreino': tipoTreino,
            'exercicio': exercicio,
            'serie': serie,
            'repeticao': repeticao,
            'descanso': descanso,
            'carga': carga,
        };

        exercicios.push(exercicioInfo);
        
        adicionarExercicios(exercicios);
        
        // Limpa os campos de treino
        limparCamposTreino();
    }

    function atualizarListaExercicios() {
    
    var listaExercicios = document.getElementById('exerciciosAdicionados');
    listaExercicios.innerHTML = '';
    
    exercicios.forEach(function (exercicio, index) {
        var itemLista = document.createElement('li');
        itemLista.textContent = `Dia: ${exercicio.tipoTreino}, Exercício: ${exercicio.exercicio}, Série: ${exercicio.serie}, Repetição: ${exercicio.repeticao}, Descanso: ${exercicio.descanso}, Carga: ${exercicio.carga}`;
        listaExercicios.appendChild(itemLista);
    });
    return exercicios;
    }
    
    function limparCamposTreino() {
    
    document.getElementById('exercicio').value = '';
    document.getElementById('serie').value = '';
    document.getElementById('repeticao').value = '';
    document.getElementById('descanso').value = '';
    document.getElementById('carga').value = '';
    }
    
    function enviarExerciciosParaServidor() {
        // Obtenha os dados dos exercícios
        var exercicios = atualizarListaExercicios();
    
        var opcaoExercicio = document.getElementById('opcaoExercicio').value;

        if (opcaoExercicio === 'manterCadastrado') {
            enviarMedidasParaServidor();
            // Redireciona para a outra página após o cadastro
            window.location.href = '/alunos';
            return false; // Impede o envio do formulário
            
            
        }
        else {
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
                window.location.href = '/alunos';
            })
            .catch(error => {
                // Lida com erros
                console.error(error);
            });
    
        return false; // Impede o envio do formulário
        }
        
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
                window.location.href = '/alunos';
            })
            .catch(error => {
                // Lida com erros
                console.error(error);
            });
    }