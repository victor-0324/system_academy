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

// Adicione logs para verificar o que está sendo adicionado
console.log('Exercício adicionado:', exercicioInfo);
console.log('Lista de exercícios atualizada:', exercicios);
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