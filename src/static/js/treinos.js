document.addEventListener('DOMContentLoaded', async () => {
    let treinoAtivo = false, tempoInicial, intervaloCronometro;
    const btnStart = document.getElementById('btnIniciarTreino');
    const btnStop = document.getElementById('btnConcluirTreino');

    function formatarSegundos(sec) {
        const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
        return [h, m, s].map(v => String(v).padStart(2, '0')).join(':');
    }

    function atualizarBotoes() {
        btnStart.disabled = treinoAtivo;
        btnStop.disabled = !treinoAtivo;
        mostrarCronometro(treinoAtivo);
    }
    function mostrarCronometro(ativo) {
        document.getElementById("cronometroContainer").classList.toggle("hidden", !ativo);
    }
    // function autoFinalizarTreino() {
    //     clearInterval(intervaloCronometro);
    //     treinoAtivo = false;
    //     localStorage.removeItem('treinoAtivo');
    //     localStorage.removeItem('tempoInicial');
    //     const msgDiv = document.getElementById("mensagemAlerta");
    //     msgDiv.textContent = 'Tempo finalizado automaticamente ';
    //     msgDiv.style.display = 'block';
    //     carregarProgressoSemanal();
    //     atualizarBotoes();
    // }
    async function autoFinalizarTreino() {
        clearInterval(intervaloCronometro);
        treinoAtivo = false;
        localStorage.removeItem('treinoAtivo');
        localStorage.removeItem('tempoInicial');

        // ① Pega o ID do aluno (mesma lógica que você já usa)
        const alunoId = document.querySelector('.botoes').dataset.alunoId;

        // ② Penaliza no backend
        if (alunoId) {
            fetch('/treino/penalizar_auto_finalizacao', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ aluno_id: alunoId })
            })
                .then(res => {
                    if (!res.ok) console.warn('Falha ao penalizar auto finalização');
                    return res.json();
                })
                .then(json => console.log('Penalização:', json))
                .catch(err => console.error(err));
        }

        // ③ Exibe alerta e atualiza interface
        const msgDiv = document.getElementById("mensagemAlerta");
        msgDiv.textContent = 'Tempo finalizado automaticamente. Penalidade aplicada!';
        msgDiv.style.display = 'block';


        await carregarProgressoSemanal(); // recarrega pontos, conquistas, nível
        atualizarBotoes();
    }

    function iniciarCronometro() {
        clearInterval(intervaloCronometro);
        intervaloCronometro = setInterval(() => {
            const dec = Date.now() - tempoInicial;
            document.getElementById('tempo-cronometro').textContent = formatarSegundos(Math.floor(dec / 1000));
            if (dec >= 7020000) {
                autoFinalizarTreino();
            }
        }, 1000);

    }

    async function carregarProgressoSemanal() {
        const alunoId = document.querySelector('.botoes').dataset.alunoId;
        if (!alunoId) return;

        const resp = await fetch(`/treino/verificar_progresso_semanal?aluno_id=${alunoId}`);
        if (!resp.ok) return console.warn("Sem progresso");


        // Extrai também nivel e conquistas
        const { progresso, total_pontos, nivel, conquista } = await resp.json();

        // mapeia e pinta o progresso na tabela (como você já tem)
        const mapIds = {
            "segunda-feira": "segunda",
            "terça-feira": "terca",
            "quarta-feira": "quarta",
            "quinta-feira": "quinta",
            "sexta-feira": "sexta",
            "sábado": "sabado",
        };
        Object.values(mapIds).forEach(id => document.getElementById(id).textContent = "");
        progresso.forEach(item => {
            const tdId = mapIds[item.dia_nome];
            if (tdId) document.getElementById(tdId).textContent = item.status;
        });

        // formata e mostra o cronômetro e pontos (como você já tem)
        function formatarSegundos(segundos) {
            if (!segundos) return '';
            const h = Math.floor(segundos / 3600);
            const m = Math.floor((segundos % 3600) / 60);
            const s = segundos % 60;
            return [h > 0 && `${h}h`, m > 0 && `${m}m`, s > 0 && `${s}s`].filter(Boolean).join(' ');
        }
        const hojeNome = new Date().toLocaleDateString('pt-BR', { weekday: 'long' });
        const progHoje = progresso.find(p => p.dia_nome === hojeNome);
        document.getElementById('resultadoDia').textContent =
            progHoje ? `Hoje: ${formatarSegundos(progHoje.tempo_treino)}` : '';
        document.getElementById('ponTos').textContent = `Pontos: ${total_pontos}`;

        // —— NOVO —— mostrar nível e conquistas
        document.getElementById('nivel').textContent = `${nivel} 🏅`;

        document.getElementById('conquista').textContent =
            conquista || "😴 Sem Treino";
    }

    // e não esqueça de chamar
    document.addEventListener('DOMContentLoaded', carregarProgressoSemanal);

    async function iniciarTreino() {
        if (treinoAtivo) return;
        const alunoId = document.querySelector('.botoes').dataset.alunoId;
        if (!alunoId) return alert('Aluno não identificado');
        const resp = await fetch('/treino/iniciar_treino', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ aluno_id: alunoId }) });
        if (resp.ok) {
            treinoAtivo = true;
            tempoInicial = Date.now();
            localStorage.setItem('treinoAtivo', 'true');
            localStorage.setItem('tempoInicial', String(tempoInicial));
            iniciarCronometro();
            atualizarBotoes();
            mostrarCronometro(true);
        } else {
            const e = await resp.json(); alert(e.error);
        }
    }

    async function finalizarTreino() {
        if (!treinoAtivo) return;
        const alunoId = document.querySelector('.botoes').dataset.alunoId;
        const tIni = localStorage.getItem('tempoInicial');
        if (!alunoId || !tIni) return alert('Sessão inválida');
        const resp = await fetch('/treino/finalizar_treino', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ aluno_id: alunoId, tempo_inicial: tIni }) });
        if (resp.ok) {
            const data = await resp.json();
            clearInterval(intervaloCronometro);
            document.getElementById('tempo-cronometro').textContent = '00:00:00';
            treinoAtivo = false;
            localStorage.removeItem('treinoAtivo');
            localStorage.removeItem('tempoInicial');

            await carregarProgressoSemanal();
            atualizarBotoes();
            mostrarCronometro(false);
        } else {
            const e = await resp.json(); alert(e.error);
        }
    }

    if (localStorage.getItem('treinoAtivo') === 'true') {
        const t = parseInt(localStorage.getItem('tempoInicial'), 10);
        if (!isNaN(t)) { treinoAtivo = true; tempoInicial = t; iniciarCronometro(); }
    }
    atualizarBotoes();
    btnStart.addEventListener('click', iniciarTreino);
    btnStop.addEventListener('click', finalizarTreino);
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
