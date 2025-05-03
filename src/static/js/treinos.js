// let cronometro;
// let segundos = 0;
// let minutos = 0;
// let horas = 0;
// let horaInicio;
// let cronometroIniciado;
// let mensagemAlerta = "Treino concluído automaticamente.";


// Função para formatar o tempo
// function formatarTempo(tempo) {
//     return tempo < 10 ? `0${tempo}` : tempo.toString();
// }

// Função para atualizar o display do tempo
// function atualizarTempoDisplay() {
//     document.getElementById('tempo-cronometro').textContent = `${formatarTempo(horas)}:${formatarTempo(minutos)}:${formatarTempo(segundos)}`;
// }

// Inicia o treino
// function iniciarTreino() {

//     // Obtém a hora de início do localStorage ou usa o tempo atual se não houver
//     let horaInicio = parseInt(localStorage.getItem('horaInicio')) || new Date().getTime();

//     // Calcula o tempo decorrido desde o início do treino
//     let tempoDecorrido = new Date().getTime() - horaInicio;

//     // Calcula horas, minutos e segundos a partir do tempo decorrido
//     horas = Math.floor(tempoDecorrido / 3600000);
//     minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
//     segundos = Math.floor((tempoDecorrido % 60000) / 1000);


//     // Atualiza o display do tempo
//     atualizarTempoDisplay();

//     // Inicia o cronômetro que atualiza o tempo a cada segundo
//     cronometro = setInterval(() => {
//         horas = Math.floor(tempoDecorrido / 3600000);
//         minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
//         segundos = Math.floor((tempoDecorrido % 60000) / 1000);

//         // Atualiza o display do tempo a cada segundo
//         atualizarTempoDisplay();

//         // Incrementa o tempo decorrido em 1 segundo
//         tempoDecorrido += 1000;

//         // Atualiza o localStorage a cada segundo com o estado do cronômetro
//         if (cronometroIniciado) {
//             localStorage.setItem('tempoEstado', JSON.stringify({
//                 horas: horas,
//                 minutos: minutos,
//                 segundos: segundos,
//                 treinoAtivo: true,
//                 horaInicio: horaInicio
//             }));
//         }
//     }, 1000);

//     // Desabilita o botão de iniciar treino
//     document.getElementById('btnIniciarTreino').disabled = true;

//     // Marca o cronômetro como iniciado no localStorage
//     cronometroIniciado = true;
//     localStorage.setItem('cronometroIniciado', 'true');
//     localStorage.setItem('horaInicio', horaInicio);
// }

// document.addEventListener('visibilitychange', function () {
//     if (document.hidden) {

//         // Verificar se há dados de cronômetro no localStorage

//     } else {
//         var dadosCronometro = localStorage.getItem('tempoEstado');

//         if (dadosCronometro) {
//             // Analisar os dados do cronômetro
//             var dadosObj = JSON.parse(dadosCronometro);

//             // Verificar se o cronômetro está ativo
//             if (dadosObj.treinoAtivo) {
//                 location.reload();
//             } else {
//                 // O cronômetro não está ativo, você pode adicionar lógica adicional aqui se necessário
//             }
//         } else {
//             // Não há dados de cronômetro no localStorage, você pode adicionar lógica adicional aqui se necessário
//         }
//     }
// });

// Função para concluir o treino
// function concluirTreino() {
//     clearInterval(cronometro);
//     document.getElementById('btnIniciarTreino').disabled = false;
//     let diaDaSemana = new Date().getDay();
//     let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

//     let elementoDia = document.getElementById(dias[diaDaSemana]);
//     if (elementoDia) {
//         elementoDia.textContent = '✅';
//         elementoDia.style.color = 'green';
//     }

//     let elementoTempo = document.getElementById('tempo-cronometro');
//     if (elementoTempo) {
//         let tempoAnterior = localStorage.getItem(`${dias[diaDaSemana]}Tempo`) || '00:00:00';
//         let partesAnteriores = tempoAnterior.split(':');
//         let totalSegundos = parseInt(partesAnteriores[2]) + segundos;
//         let totalMinutos = parseInt(partesAnteriores[1]) + minutos;
//         let totalHoras = parseInt(partesAnteriores[0]) + horas;

//         if (totalSegundos >= 60) {

//             totalSegundos -= 60;
//             totalMinutos++;
//         }
//         if (totalMinutos >= 60) {
//             totalMinutos -= 60;
//             totalHoras++;
//         }

//         let tempoTotal = `${formatarTempo(totalHoras)}:${formatarTempo(totalMinutos)}:${formatarTempo(totalSegundos)}`;
//         localStorage.setItem(`${dias[diaDaSemana]}Tempo`, tempoTotal);

//         let elementoResultadoDia = document.getElementById('resultadoDia');
//         if (elementoResultadoDia) {
//             elementoResultadoDia.textContent = `Hoje: ${tempoTotal}`;
//         }

//         calcularTempoSemana();
//     }

//     localStorage.setItem(dias[diaDaSemana], '✅');

//     horas = 0;
//     minutos = 0;
//     segundos = 0;
//     atualizarTempoDisplay();
//     cronometroIniciado = false;
//     localStorage.setItem('cronometroIniciado', 'false');
//     localStorage.removeItem('horaInicio');

//     // Limpa o estado do cronômetro no localStorage
//     localStorage.removeItem('tempoEstado');

//     // Reiniciar o progresso no final da semana (Domingo)
//     reiniciarProgresso();
// }

// Adicione essa linha antes do código do cronômetro para definir a função que atualiza o tempo da semana
// setInterval(calcularTempoSemana, 1000);

// Função para calcular o tempo total de treino na semana
// function calcularTempoSemana() {
//     let totalSegundos = 0;
//     let dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];
//     dias.forEach(dia => {
//         let tempo = localStorage.getItem(`${dia}Tempo`);
//         if (tempo) {
//             let partes = tempo.split(':');
//             totalSegundos += parseInt(partes[0]) * 3600 + parseInt(partes[1]) * 60 + parseInt(partes[2]);
//         }
//     });
//     let horas = Math.floor(totalSegundos / 3600);
//     totalSegundos %= 3600;
//     let minutos = Math.floor(totalSegundos / 60);
//     let segundos = totalSegundos % 60;

//     document.getElementById('resultadoSemana').textContent = `Na Semana: ${formatarTempo(horas)}:${formatarTempo(minutos)}:${formatarTempo(segundos)}`;
// }

// function marcarDiasNaoTreinados(dias) {
//     let hoje = new Date();
//     let diaAtual = hoje.getDay();

//     for (let i = 1; i < diaAtual; i++) {
//         let dia = dias[i];
//         let progresso = localStorage.getItem(dia);
//         let elementoDia = document.getElementById(dia);

//         if (elementoDia) {
//             if (!progresso || progresso !== '✅') {
//                 elementoDia.textContent = 'X';
//                 elementoDia.style.color = 'red';
//                 localStorage.setItem(dia, 'X');
//             }
//         }
//     }
// }

// function reiniciar() {
//     let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

//     dias.forEach(dia => {
//         let elementoDia = document.getElementById(dia);

//         if (elementoDia) {
//             localStorage.removeItem(dia);
//             localStorage.removeItem(`${dia}Tempo`);
//             elementoDia.textContent = '';
//         }
//     });

//     let elementoResultadoDia = document.getElementById('resultadoDia');
//     if (elementoResultadoDia) {
//         elementoResultadoDia.textContent = '';
//     }

//     let elementoResultadoSemana = document.getElementById('resultadoSemana');
//     if (elementoResultadoSemana) {
//         elementoResultadoSemana.textContent = '';
//     }
// }

// function reiniciarProgresso() {
//     let diaDaSemana = new Date().getDay();

//     // Verifica se o dia da semana é domingo (0)
//     if (diaDaSemana === 0) {
//         reiniciar();
//     }
// }

// Função para iniciar o cronômetro se estiver ativo
// function iniciarCronometroSeAtivo() {
//     let estadoArmazenado = localStorage.getItem('tempoEstado');

//     if (estadoArmazenado && estadoArmazenado !== 'null') {
//         let estado = JSON.parse(estadoArmazenado);
//         segundos = estado.segundos;
//         minutos = estado.minutos;
//         horas = estado.horas;

//         // Verifique se o cronômetro não está iniciado e se o treino estava ativo
//         if (!cronometroIniciado && estado.treinoAtivo) {
//             // Ajuste o tempo decorrido com base no tempo quando o treino foi iniciado
//             let tempoDecorrido = new Date().getTime() - estado.horaInicio;

//             horas = Math.floor(tempoDecorrido / 3600000);
//             minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
//             segundos = Math.floor((tempoDecorrido % 60000) / 1000);

//             // Atualize o tempo da semana ao iniciar o cronômetro
//             calcularTempoSemana();

//             atualizarTempoDisplay();

//             // Inicie o cronômetro novamente
//             cronometro = setInterval(() => {
//                 horas = Math.floor(tempoDecorrido / 3600000);
//                 minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
//                 segundos = Math.floor((tempoDecorrido % 60000) / 1000);
//                 atualizarTempoDisplay();

//                 // Atualiza o localStorage a cada segundo
//                 localStorage.setItem('tempoEstado', JSON.stringify({
//                     horas: horas,
//                     minutos: minutos,
//                     segundos: segundos,
//                     treinoAtivo: true,
//                     horaInicio: estado.horaInicio
//                 }));

//                 tempoDecorrido += 1000;
//             }, 1000);

//             cronometroIniciado = true;
//             localStorage.setItem('cronometroIniciado', 'true');
//         }
//     } else {
//         // Se não houver estado salvo, reinicie o progresso
//         reiniciarProgresso();
//     }
// }

// function calcularTempoDecorrido() {
//     // Obtém a hora de início do treino do localStorage
//     let horaInicio = parseInt(localStorage.getItem('horaInicio')) || new Date().getTime();

//     // Calcula o tempo decorrido desde o início do treino
//     let tempoDecorrido = new Date().getTime() - horaInicio;

//     return tempoDecorrido;
// }

// function carregarProgresso() {
//     // Verifica se o cronômetro está ativo no localStorage
//     let cronometroAtivo = localStorage.getItem('cronometroIniciado') === 'true';

//     // Se o cronômetro estiver ativo, desabilite o botão de iniciar treino
//     if (cronometroAtivo) {
//         document.getElementById('btnIniciarTreino').disabled = true;

//         // Verifica se o tempo decorrido excedeu o tempo específico (por exemplo, 30 minutos)
//         let tempoDecorrido = calcularTempoDecorrido();
//         if (tempoDecorrido >= 150 * 60 * 1000) { // 30 minutos em milissegundos
//             // Se o tempo decorrido exceder o tempo específico, chama a função para concluir o treino
//             concluirTreino();

//             // Exibe a mensagem de alerta armazenada na variável mensagemAlerta
//             document.getElementById('mensagemAlerta').textContent = mensagemAlerta;

//         }
//     }



//     let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

//     dias.forEach(dia => {
//         let progresso = localStorage.getItem(dia);
//         let elementoDia = document.getElementById(dia);

//         if (elementoDia) {
//             if (progresso) {
//                 elementoDia.textContent = progresso;
//                 if (progresso === '✅') {
//                     elementoDia.style.color = 'green';
//                 } else if (progresso === 'X') {
//                     elementoDia.style.color = 'red';
//                 }
//             } else {
//                 elementoDia.textContent = '';
//             }
//         }
//     });
//     marcarDiasNaoTreinados(dias);
//     iniciarCronometroSeAtivo();
// }

// function confirmarReinicio() {
//     // Adiciona uma janela de confirmação
//     let confirmacao = confirm("Tem certeza de que deseja reiniciar o progresso? Isso não pode ser desfeito.");

//     // Se o usuário confirmar, então reinicia o progresso
//     if (confirmacao) {
//         reiniciar();
//     }
// }


// Carregar progresso do LocalStorage ao recarregar a página
// window.onload = function () {
//     carregarProgresso();
//     reiniciarProgresso();
// };


// let startTime;

// function iniciarTreino() {
//     const alunoId = document.querySelector('.botoes').getAttribute('data-aluno-id');

//     fetch('/treino/cronometro/iniciar', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ aluno_id: alunoId })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             startTime = Date.now();  // Registrar o tempo de início
//             document.getElementById("btnIniciarTreino").disabled = true;
//             iniciarCronometro();  // Iniciar a exibição do cronômetro
//         } else {
//             alert("Erro ao iniciar o cronômetro.");
//         }
//     });
// }

// function iniciarCronometro() {
//     const cronometroDisplay = document.getElementById("tempo-cronometro");

//     intervalo = setInterval(function () {
//         const now = Date.now();
//         const tempoDecorrido = now - startTime;

//         let segundos = Math.floor((tempoDecorrido / 1000) % 60);
//         let minutos = Math.floor((tempoDecorrido / (1000 * 60)) % 60);
//         let horas = Math.floor((tempoDecorrido / (1000 * 60 * 60)) % 24);

//         cronometroDisplay.innerText = `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;
//     }, 1000);

//     document.getElementById("btnPararTreino").addEventListener("click", function() {
//         clearInterval(intervalo);
//         concluirTreino();
//     });
// }

// function concluirTreino() {
//     const alunoId = document.querySelector('.botoes').getAttribute('data-aluno-id');

//     fetch('/treino/cronometro/concluir', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ aluno_id: alunoId })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.error) {
//             alert(data.error);
//         } else {
//             clearInterval(intervalo);
//             document.getElementById('tempo-cronometro').innerText = data.tempo_treino;
//             document.getElementById('resultadoDia').innerText = `Tempo de treino hoje: ${data.tempo_treino}`;
//             document.getElementById('resultadoSemana').innerText = `Tempo total da semana: ${data.tempo_total_semana}`;
//             document.getElementById("btnIniciarTreino").disabled = false;
//         }
//     })
//     .catch(error => console.error('Erro:', error));
// }

document.addEventListener("DOMContentLoaded", async function () {
    let treinoAtivo = false;
    let tempoInicial;
    let intervaloCronometro;

    async function iniciarTreino() {
        const alunoId = document.querySelector(".botoes").dataset.alunoId;
        if (!alunoId) {
            alert("Erro: Aluno não identificado.");
            return;
        }

        const response = await fetch("/treino/iniciar_treino", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ aluno_id: alunoId })
        });

        const data = await response.json();
        if (response.ok) {
            treinoAtivo = true;
            tempoInicial = Date.now();
            localStorage.setItem("treinoAtivo", "true");
            localStorage.setItem("tempoInicial", tempoInicial);
            iniciarCronometro();
            alert("Treino iniciado!");
        } else {
            alert("Erro ao iniciar treino: " + data.error);
        }
    }

    async function finalizarTreino() {
        const alunoId = document.querySelector(".botoes").dataset.alunoId;
        const tempoInicial = localStorage.getItem("tempoInicial"); // Recupera o tempo de início

        if (!alunoId) return alert("Erro: Aluno não identificado.");
        if (!tempoInicial) return alert("Erro: Nenhuma sessão de treino encontrada.");

        const response = await fetch("/treino/finalizar_treino", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                aluno_id: alunoId,
                tempo_inicial: tempoInicial // Enviando tempo inicial 
            })
        });

        const data = await response.json();
        if (response.ok) {
            clearInterval(intervaloCronometro);
            document.getElementById("tempo-cronometro").textContent = "00:00:00";
            treinoAtivo = false;
            localStorage.removeItem("treinoAtivo");
            localStorage.removeItem("tempoInicial");
            alert(`Treino finalizado! Pontuação: ${data.pontos}`);
        } else {
            alert("Erro ao finalizar treino: " + data.error);
        }
    }

    function iniciarCronometro() {
        clearInterval(intervaloCronometro);
        intervaloCronometro = setInterval(() => {
            const tempoAtual = Date.now();
            const tempoDecorrido = tempoAtual - tempoInicial;

            const horas = Math.floor(tempoDecorrido / 3600000);
            const minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
            const segundos = Math.floor((tempoDecorrido % 60000) / 1000);

            document.getElementById("tempo-cronometro").textContent =
                `${String(horas).padStart(2, "0")}:${String(minutos).padStart(2, "0")}:${String(segundos).padStart(2, "0")}`;

        }, 1000);
    }

    async function carregarProgressoSemanal() {
        const alunoId = document.querySelector(".botoes").dataset.alunoId;
        if (!alunoId) return;

        const response = await fetch(`/treino/verificar_progresso_semanal?aluno_id=${alunoId}`);
        const data = await response.json();
        console.log(data);
        if (response.ok) {
            document.getElementById("resultadoSemana").textContent = `Total de Pontos: ${data.total_pontos}`;
        }
    }

    // Se o cronômetro estava ativo, reiniciar ao recarregar a página
    if (localStorage.getItem("treinoAtivo") === "true") {
        tempoInicial = parseInt(localStorage.getItem("tempoInicial"), 10);
        if (!isNaN(tempoInicial)) {
            treinoAtivo = true;
            iniciarCronometro();
        }
    }
    document.getElementById("btnIniciarTreino").addEventListener("click", iniciarTreino);
    document.getElementById("btnConcluirTreino").addEventListener("click", finalizarTreino);

    await carregarProgressoSemanal();
});

document.addEventListener('DOMContentLoaded', () => {
    // Carrega o estado salvo dos exercícios
    const completedExercises = JSON.parse(localStorage.getItem('completedExercises')) || {};
    const lastActionTime = JSON.parse(localStorage.getItem('lastActionTime')) || null;

    // Função para verificar se 5 horas se passaram
    function checkTimeLimit() {
        if (lastActionTime) {
            const currentTime = new Date().getTime();
            const timeDifference = (currentTime - lastActionTime) / (1000 * 60 * 60); // Diferença em horas
            if (timeDifference >= 5) {
                // Se passaram 5 horas, reseta os botões para o estado inicial
                Object.keys(completedExercises).forEach(exerciseId => {
                    delete completedExercises[exerciseId]; // Remove o estado de concluído
                    const button = document.querySelector(`[data-exercise-id='${exerciseId}']`);
                    if (button) {
                        unmarkAsCompleted(button); // Restaura o botão para o estado inicial
                    }
                });

                // Atualiza a última ação como o reset
                const currentTime = new Date().getTime();
                localStorage.setItem('lastActionTime', JSON.stringify(currentTime));

                // Salva a alteração no localStorage
                localStorage.setItem('completedExercises', JSON.stringify(completedExercises));
                location.reload();
            }
        }
    }

    // Verifica se o tempo limite foi atingido assim que a página for carregada
    checkTimeLimit();

    // Atualiza a interface com base no estado
    document.querySelectorAll('.mark-complete').forEach(button => {
        const exerciseId = button.getAttribute('data-exercise-id');
        if (completedExercises[exerciseId]) {
            markAsCompleted(button);
        }

        // Adiciona evento de clique ao botão
        button.addEventListener('click', () => {
            // Verifica se o tempo limite de 5 horas foi atingido
            checkTimeLimit();

            if (completedExercises[exerciseId]) {
                // Marca como não concluído
                delete completedExercises[exerciseId];
                unmarkAsCompleted(button);
            } else {
                // Marca como concluído
                completedExercises[exerciseId] = true;
                markAsCompleted(button);
            }

            // Salva a data e hora da última ação
            const currentTime = new Date().getTime();
            localStorage.setItem('lastActionTime', JSON.stringify(currentTime));

            // Salva o estado dos exercícios
            localStorage.setItem('completedExercises', JSON.stringify(completedExercises));
        });
    });

    // Função para estilizar o botão como concluído
    function markAsCompleted(button) {
        button.textContent = "Feito 🏅💪";
        button.classList.add('completed'); // Classe para estilos
    }

    // Função para restaurar o botão ao estado original
    function unmarkAsCompleted(button) {
        button.textContent = "💤🕒💤";
        button.classList.remove('completed');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    // 1. Preenche do storage ao carregar
    document.querySelectorAll('td[data-exercise-id]').forEach(td => {
        const id = td.dataset.exerciseId;
        const saved = localStorage.getItem(`carga_${id}`);
        if (saved !== null) td.textContent = saved + ' kg';
    });

    // 2. Torna o campo editável ao clicar no texto
    document.querySelectorAll('td[data-exercise-id]').forEach(td => {
        td.addEventListener('click', () => {
            const id = td.dataset.exerciseId;
            const current = td.textContent.replace(' kg', '').trim();
            const input = document.createElement('input');
            input.type = 'number';
            input.value = current;
            input.style.width = '60px';
            td.textContent = '';
            td.appendChild(input);
            input.focus();

            // 3. Ao sair do input, salva no storage e volta para texto
            input.addEventListener('blur', () => {
                const val = input.value || current;
                localStorage.setItem(`carga_${id}`, val);
                td.textContent = val + ' kg';
            });
        });
    });
});