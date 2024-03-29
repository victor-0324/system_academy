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
        
        // Limpa os campos de treino
        limparCamposTreino();
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
    
    function limparCamposTreino() {
            document.getElementById('exercicio').value = '0';
            document.getElementById('serie').value = '0';
            document.getElementById('repeticao').value = '0';
            document.getElementById('descanso').value = '0';
            document.getElementById('carga').value = 'Constante';
    }

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
    
   
    document.addEventListener('DOMContentLoaded', function() {
        // Adicione um ouvinte de evento ao formulário
        var formulario = document.querySelector('form');
        formulario.addEventListener('submit', function(event) {
            // Previne o envio padrão do formulário
            event.preventDefault();
    
            // Obtenha os dados dos exercícios
            var exercicios = obterExerciciosAdicionados();
    
            // Verifique se há exercícios antes de enviar
            if (exercicios.length === 0) {
                alert('Adicione pelo menos um exercício antes de cadastrar.');
                return;
            }
    
            // Adicione os exercícios ao formData
            var formData = new FormData(formulario);
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
                // Limpa os exercícios após o envio
                exercicios = [];
                // Redireciona para a outra página após o cadastro
                window.location.href = '/';
            })
            .catch(error => {
                // Lida com erros
                console.error(error);
            });
        });
    });

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
