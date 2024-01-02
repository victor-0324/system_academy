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
    }

    // Escopo local para evitar variáveis globais desnecessárias
    var exercicios = [];
    
    function adicionarExercicio()  {
    
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
    
    var exercicioInfo = {
        'tipoTreino': tipoTreino,
        'exercicio': exercicio,
        'serie': serie,
        'repeticao': repeticao,
        'descanso': descanso,
        'carga': carga,
    };
    
    exercicios.push(exercicioInfo);
    

    // Atualiza a lista de exercícios na página
    atualizarListaExercicios();
    
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
                console.log(data);
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
    
        // Adicione qualquer lógica adicional necessária para enviar apenas as medidas
        // ...
    
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
                console.log(data);
                // Redireciona para a outra página após o cadastro
                window.location.href = '/alunos';
            })
            .catch(error => {
                // Lida com erros
                console.error(error);
            });
    }