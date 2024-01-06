var exercicios = [];


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
    // Atualiza a lista de exercícios na página
    // atualizarListaExercicios();

    // Limpa os campos de treino
    limparCamposTreino();
}

// function atualizarListaExercicios() {
//     var listaExercicios = document.getElementById('exerciciosAdicionados');
//     listaExercicios.innerHTML = '';

//     var ulExercicios = document.createElement('ul');

//     exercicios.forEach(function (exercicio, index) {
//         var itemLista = document.createElement('li');
//         itemLista.textContent = `Dia: ${exercicio.tipoTreino}, Exercício: ${exercicio.exercicio}, Série: ${exercicio.serie}, Repetição: ${exercicio.repeticao}, Descanso: ${exercicio.descanso}, Carga: ${exercicio.carga}`;
//         ulExercicios.appendChild(itemLista);
//     });

//     listaExercicios.appendChild(ulExercicios);
// }

function limparCamposTreino() {
    document.getElementById('tipoTreino').value = '';
    document.getElementById('exercicio').value = '';
    document.getElementById('serie').value = '';
    document.getElementById('repeticao').value = '';
    document.getElementById('descanso').value = '';
    document.getElementById('carga').value = '';
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
        console.log('Resposta do servidor:', data);
        // Verifique se a busca foi bem-sucedida
        if (data && data.aluno) {
            console.log('Dados do aluno:', data.aluno);
            // Adicione os exercícios à lista
            adicionarExercicios(data.aluno);
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
function adicionarExercicios(exercicios) {
    // Limpar a lista de exercícios antes de preenchê-la
    const exerciciosAdicionados = document.getElementById('exerciciosAdicionados');
    exerciciosAdicionados.innerHTML = '';

    // Iterar sobre os exercícios e adicionar campos de edição à lista
    exercicios.forEach(exercicio => {
        const divExercicio = document.createElement('div');
        divExercicio.className = 'exercicio-editavel';

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

    // Adiciona a lista de exercícios à lista global
    exercicios = exercicios.slice(); // Cria uma cópia para evitar referências diretas
    exercicios.push(...exercicios);
}



// // Função para preencher automaticamente os campos com exercícios
// function preencherCamposComExercicios(exercicios) {
//     // Limpar a lista de exercícios antes de preenchê-la
//     const exerciciosAdicionados = document.getElementById('exerciciosAdicionados');
//     exerciciosAdicionados.innerHTML = '';

//     // Iterar sobre os exercícios e adicionar à lista
//     exercicios.forEach(exercicio => {
//         const itemLista = document.createElement('li');
//         itemLista.textContent = `Dia: ${exercicio.tipoTreino}, Exercício: ${exercicio.exercicio}, Série: ${exercicio.serie}, Repetição: ${exercicio.repeticao}, Descanso: ${exercicio.descanso}, Carga: ${exercicio.carga}`;
//         exerciciosAdicionados.appendChild(itemLista);
//     });
// }

// Função para atualizar exercício editado
// function atualizarExercicioEditado(exercicio, divExercicio) {
//     // Obter os novos valores editados
//     const novosValores = {};
//     const inputs = divExercicio.querySelectorAll('input');
//     inputs.forEach((input, index) => {
//         novosValores[input.getAttribute('data-campo')] = input.value;
//     });

//     // Atualizar os valores do exercício com os novos valores
//     Object.assign(exercicio, novosValores);

//     // Chamar a função para preencher automaticamente os campos com exercícios atualizados
//     preencherCamposComExercicios([exercicio]);
// }


// Função para obter exercícios da lista de exercícios adicionados
function obterExerciciosAdicionados() {
    const exerciciosAdicionados = document.getElementById('exerciciosAdicionados');
    const exercicios = [];

    for (let i = 0; i < exerciciosAdicionados.children.length; i++) {
        const divExercicio = exerciciosAdicionados.children[i];
        const exercicio = {};

        divExercicio.querySelectorAll('input').forEach(function (input) {
            exercicio[input.getAttribute('data-campo')] = input.value;
        });

        exercicios.push(exercicio);
    }

    return exercicios;
}

function enviarExerciciosParaServidor() {
    // Obtenha os dados dos exercícios
    var exercicios = obterExerciciosAdicionados();

    // Verifique se há exercícios antes de enviar
    if (exercicios.length === 0) {
        alert('Adicione pelo menos um exercício antes de cadastrar.');
        return false; // Impede o envio do formulário
    }

    // Adicione os exercícios ao formData
    var formData = new FormData(document.querySelector('form'));
    formData.append('exercicios', JSON.stringify(exercicios));

    var alunoId = window.location.pathname.split('/').pop();
    var url = '' + alunoId;

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
            // atualizarListaExercicios();
            // Redireciona para a outra página após o cadastro
            window.location.href = '/alunos';
        })
        .catch(error => {
            // Lida com erros
            console.error(error);
        });

    return false; // Impede o envio do formulário
}


$(document).ready(function () {
    // Ocultar o aviso quando a página é carregada
    $('#aviso-admin').hide();

    // Exibir ou ocultar o aviso com base na escolha do usuário
    $('#permissao').change(function () {
        if ($(this).val() === 'admin') {
            $('#aviso-admin').show();
        } else {
            $('#aviso-admin').hide();
        }
    });
});
