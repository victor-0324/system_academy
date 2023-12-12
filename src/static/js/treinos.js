
   // Variáveis do cronômetro
    let cronometro;
    let segundos = 0;
    let minutos = 0;
    let horas = 0;
    let cronometroIniciado = localStorage.getItem('cronometroIniciado') === 'true';
    let horaInicio;

    // Função para formatar o tempo
    function formatarTempo(tempo) {
        return tempo < 10 ? `0${tempo}` : tempo.toString();
    }

    // Função para atualizar o display do tempo
    function atualizarTempoDisplay() {
        document.getElementById('tempo-cronometro').textContent = `${formatarTempo(horas)}:${formatarTempo(minutos)}:${formatarTempo(segundos)}`;
    }

    // Função para iniciar o treino
    function iniciarTreino() {
        horaInicio = parseInt(localStorage.getItem('horaInicio')) || new Date().getTime();
        let tempoDecorrido = new Date().getTime() - horaInicio;
        horas = Math.floor(tempoDecorrido / 3600000);
        minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
        segundos = Math.floor((tempoDecorrido % 60000) / 1000);
        atualizarTempoDisplay();

        cronometro = setInterval(() => {
            horas = Math.floor(tempoDecorrido / 3600000);
            minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
            segundos = Math.floor((tempoDecorrido % 60000) / 1000);
            atualizarTempoDisplay();
            tempoDecorrido += 1000;
        }, 1000);

        document.getElementById('btnIniciarTreino').disabled = true;

        cronometroIniciado = true;
        localStorage.setItem('cronometroIniciado', 'true');
        localStorage.setItem('horaInicio', horaInicio);
    }

    // Função para concluir o treino
    function concluirTreino() {
        clearInterval(cronometro);
        document.getElementById('btnIniciarTreino').disabled = false;
        let diaDaSemana = new Date().getDay();
        let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

        let elementoDia = document.getElementById(dias[diaDaSemana]);
        if (elementoDia) {
            elementoDia.textContent = '✅';
            elementoDia.style.color = 'green';
        }

        let elementoTempo = document.getElementById('tempo-cronometro');
        if (elementoTempo) {
            let tempoAnterior = localStorage.getItem(`${dias[diaDaSemana]}Tempo`) || '00:00:00';
            let partesAnteriores = tempoAnterior.split(':');
            let totalSegundos = parseInt(partesAnteriores[2]) + segundos;
            let totalMinutos = parseInt(partesAnteriores[1]) + minutos;
            let totalHoras = parseInt(partesAnteriores[0]) + horas;

            if (totalSegundos >= 60) {
                totalSegundos -= 60;
                totalMinutos++;
            }
            if (totalMinutos >= 60) {
                totalMinutos -= 60;
                totalHoras++;
            }

            let tempoTotal = `${formatarTempo(totalHoras)}:${formatarTempo(totalMinutos)}:${formatarTempo(totalSegundos)}`;
            localStorage.setItem(`${dias[diaDaSemana]}Tempo`, tempoTotal);

            let elementoResultadoDia = document.getElementById('resultadoDia');
            if (elementoResultadoDia) {
                elementoResultadoDia.textContent = `Treino Hoje: ${tempoTotal}`;
            }

            calcularTempoSemana();
        }

        localStorage.setItem(dias[diaDaSemana], '✅');

        horas = 0;
        minutos = 0;
        segundos = 0;
        atualizarTempoDisplay();
        cronometroIniciado = false;
        localStorage.setItem('cronometroIniciado', 'false');
        localStorage.removeItem('horaInicio');

        // Reiniciar o progresso no final da semana (sábado)
        reiniciarProgresso();
    }

    // Função para calcular o tempo total de treino na semana
    function calcularTempoSemana() {
        let totalSegundos = 0;
        let dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta'];
        dias.forEach(dia => {
            let tempo = localStorage.getItem(`${dia}Tempo`);
            if (tempo) {
                let partes = tempo.split(':');
                totalSegundos += parseInt(partes[0]) * 3600 + parseInt(partes[1]) * 60 + parseInt(partes[2]);
            }
        });
        let horas = Math.floor(totalSegundos / 3600);
        totalSegundos %= 3600;
        let minutos = Math.floor(totalSegundos / 60);
        let segundos = totalSegundos % 60;
        document.getElementById('resultadoSemana').textContent = `Tempo da Semana: ${formatarTempo(horas)}:${formatarTempo(minutos)}:${formatarTempo(segundos)}`;
    }

    function marcarDiasNaoTreinados() {
        let diaDaSemana = new Date().getDay();
        let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

        // Verificar se não é domingo (dia 0) e se não é segunda-feira (dia 1)
        if (diaDaSemana !== 0 && diaDaSemana !== 1) {
            // Pegar o dia anterior
            let diaAnterior = dias[diaDaSemana - 1];
            let progresso = localStorage.getItem(diaAnterior);
            let elementoDia = document.getElementById(diaAnterior);

            // Verificar se o dia anterior não foi marcado como treinado
            if (elementoDia && (!progresso || progresso !== '✅')) {
                // Marcar como não treinado (X)
                elementoDia.textContent = 'X';
                elementoDia.style.color = 'red';
                localStorage.setItem(diaAnterior, 'X');
            }
        }
    }

    function reiniciar() {
        let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

        dias.forEach(dia => {
            let elementoDia = document.getElementById(dia);

            if (elementoDia) {
                localStorage.removeItem(dia);
                localStorage.removeItem(`${dia}Tempo`);
                elementoDia.textContent = '';
            }
        });

        let elementoResultadoDia = document.getElementById('resultadoDia');
        if (elementoResultadoDia) {
            elementoResultadoDia.textContent = '';
        }

        let elementoResultadoSemana = document.getElementById('resultadoSemana');
        if (elementoResultadoSemana) {
            elementoResultadoSemana.textContent = '';
        }
    }

    function confirmarReinicio() {
        // Adiciona uma janela de confirmação
        let confirmacao = confirm("Tem certeza de que deseja reiniciar o progresso? Isso não pode ser desfeito.");

        // Se o usuário confirmar, então reinicia o progresso
        if (confirmacao) {
            reiniciar();
        }
    }


    function reiniciarProgresso() {
        let diaDaSemana = new Date().getDay();

        // Verifica se o dia da semana é sábado (6) ou domingo (0)
        if (diaDaSemana === 0 ) {
            let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

            dias.forEach(dia => {
                let elementoDia = document.getElementById(dia);

                // Verifica se o elemento está presente antes de tentar acessá-lo
                if (elementoDia) {
                    localStorage.removeItem(dia);
                    localStorage.removeItem(`${dia}Tempo`);
                    elementoDia.textContent = '';
                }
            });

            let elementoResultadoDia = document.getElementById('resultadoDia');
            if (elementoResultadoDia) {
                elementoResultadoDia.textContent = '';
            }

            let elementoResultadoSemana = document.getElementById('resultadoSemana');
            if (elementoResultadoSemana) {
                elementoResultadoSemana.textContent = '';
            }
        }
    }

    // Carregar progresso do LocalStorage ao recarregar a página
    window.onload = function () {
        let dias = [ 'domingo','segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

        dias.forEach(dia => {
            let progresso = localStorage.getItem(dia);
            if (progresso) {
                document.getElementById(dia).textContent = progresso;
                if (progresso === '✅') {
                    document.getElementById(dia).style.color = 'green';
                } else if (progresso === 'X') {
                    document.getElementById(dia).style.color = 'red';
                }
            }
        });

        iniciarCronometroSeAtivo();

        marcarDiasNaoTreinados();
    };

    // Função para iniciar o cronômetro se estiver ativo
    function iniciarCronometroSeAtivo() {
        let estadoArmazenado = localStorage.getItem('tempoEstado');
        if (estadoArmazenado && estadoArmazenado !== 'null' && !cronometroIniciado) {
            let estado = JSON.parse(estadoArmazenado);
            segundos = estado.segundos;
            minutos = estado.minutos;
            horas = estado.horas;
            atualizarTempoDisplay();
            iniciarTreino();
            cronometroIniciado = true;
            localStorage.setItem('cronometroIniciado', 'true');
        }
    }

    function marcarConcluido(botao) {
        botao.innerHTML = 'Concluído';
        botao.style.backgroundColor = '#008000';  // Cor verde após clicar
        botao.style.color = '#ffffff';  // Texto branco após clicar
        botao.disabled = true;  // Desativa o botão após ser concluído
        }