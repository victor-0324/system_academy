    let cronometro;
    let segundos = 0;
    let minutos = 0;
    let horas = 0;
    let horaInicio;
    let cronometroIniciado;

    // Função para formatar o tempo
    function formatarTempo(tempo) {
        return tempo < 10 ? `0${tempo}` : tempo.toString();
    }

    // Função para atualizar o display do tempo
    function atualizarTempoDisplay() {
        document.getElementById('tempo-cronometro').textContent = `${formatarTempo(horas)}:${formatarTempo(minutos)}:${formatarTempo(segundos)}`;
    }

    // Inicia o treino
    function iniciarTreino() {
       
        // Obtém a hora de início do localStorage ou usa o tempo atual se não houver
        let horaInicio = parseInt(localStorage.getItem('horaInicio')) || new Date().getTime();

        // Calcula o tempo decorrido desde o início do treino
        let tempoDecorrido = new Date().getTime() - horaInicio;
        
        // Calcula horas, minutos e segundos a partir do tempo decorrido
        horas = Math.floor(tempoDecorrido / 3600000);
        minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
        segundos = Math.floor((tempoDecorrido % 60000) / 1000);
        
        // Atualiza o display do tempo
        atualizarTempoDisplay();

        // Inicia o cronômetro que atualiza o tempo a cada segundo
        cronometro = setInterval(() => {
            horas = Math.floor(tempoDecorrido / 3600000);
            minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
            segundos = Math.floor((tempoDecorrido % 60000) / 1000);
            
            // Atualiza o display do tempo a cada segundo
            atualizarTempoDisplay();
            
            // Incrementa o tempo decorrido em 1 segundo
            tempoDecorrido += 1000;

            // Atualiza o localStorage a cada segundo com o estado do cronômetro
            if (cronometroIniciado) {
                localStorage.setItem('tempoEstado', JSON.stringify({
                    horas: horas,
                    minutos: minutos,
                    segundos: segundos,
                    treinoAtivo: true,
                    horaInicio: horaInicio
                }));
            }
        }, 1000);

        // Desabilita o botão de iniciar treino
        document.getElementById('btnIniciarTreino').disabled = true;

        // Marca o cronômetro como iniciado no localStorage
        cronometroIniciado = true;
        localStorage.setItem('cronometroIniciado', 'true');
        localStorage.setItem('horaInicio', horaInicio);
    }

    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            
            // Verificar se há dados de cronômetro no localStorage
            
        } else {
            var dadosCronometro = localStorage.getItem('tempoEstado');
            
            if (dadosCronometro) {
                // Analisar os dados do cronômetro
                var dadosObj = JSON.parse(dadosCronometro);
                
                // Verificar se o cronômetro está ativo
                if (dadosObj.treinoAtivo) {
                    location.reload();
                } else {
                    // O cronômetro não está ativo, você pode adicionar lógica adicional aqui se necessário
                }
            } else {
                // Não há dados de cronômetro no localStorage, você pode adicionar lógica adicional aqui se necessário
            }
        }
    });

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
        
        // Limpa o estado do cronômetro no localStorage
        localStorage.removeItem('tempoEstado');

        // Reiniciar o progresso no final da semana (sábado)
        reiniciarProgresso();
    }

    // Adicione essa linha antes do código do cronômetro para definir a função que atualiza o tempo da semana
    setInterval(calcularTempoSemana, 1000);

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

    function marcarDiasNaoTreinados(dias) {
        let hoje = new Date();
        let diaAtual = hoje.getDay();
    
        for (let i = 1; i < diaAtual; i++) {
            let dia = dias[i];
            let progresso = localStorage.getItem(dia);
            let elementoDia = document.getElementById(dia);
    
            if (elementoDia) {
                if (!progresso || progresso !== '✅') {
                    elementoDia.textContent = 'X';
                    elementoDia.style.color = 'red';
                    localStorage.setItem(dia, 'X');
                }
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

    // Função para iniciar o cronômetro se estiver ativo
    function iniciarCronometroSeAtivo() {
        let estadoArmazenado = localStorage.getItem('tempoEstado');
    
        if (estadoArmazenado && estadoArmazenado !== 'null') {
            let estado = JSON.parse(estadoArmazenado);
            segundos = estado.segundos;
            minutos = estado.minutos;
            horas = estado.horas;
    
            // Verifique se o cronômetro não está iniciado e se o treino estava ativo
            if (!cronometroIniciado && estado.treinoAtivo) {
                // Ajuste o tempo decorrido com base no tempo quando o treino foi iniciado
                let tempoDecorrido = new Date().getTime() - estado.horaInicio;
    
                horas = Math.floor(tempoDecorrido / 3600000);
                minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
                segundos = Math.floor((tempoDecorrido % 60000) / 1000);
    
                // Atualize o tempo da semana ao iniciar o cronômetro
                calcularTempoSemana();
    
                atualizarTempoDisplay();
    
                // Inicie o cronômetro novamente
                cronometro = setInterval(() => {
                    horas = Math.floor(tempoDecorrido / 3600000);
                    minutos = Math.floor((tempoDecorrido % 3600000) / 60000);
                    segundos = Math.floor((tempoDecorrido % 60000) / 1000);
                    atualizarTempoDisplay();
    
                    // Atualiza o localStorage a cada segundo
                    localStorage.setItem('tempoEstado', JSON.stringify({
                        horas: horas,
                        minutos: minutos,
                        segundos: segundos,
                        treinoAtivo: true,
                        horaInicio: estado.horaInicio
                    }));
    
                    tempoDecorrido += 1000;
                }, 1000);
    
                cronometroIniciado = true;
                localStorage.setItem('cronometroIniciado', 'true');
            }
        } else {
            // Se não houver estado salvo, reinicie o progresso
            reiniciarProgresso();
        }
    }
    
    function carregarProgresso() {
        let dias = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'];

        dias.forEach(dia => {
            let progresso = localStorage.getItem(dia);
            let elementoDia = document.getElementById(dia);
    
            if (elementoDia) {
                if (progresso) {
                    elementoDia.textContent = progresso;
                    if (progresso === '✅') {
                        elementoDia.style.color = 'green';
                    } else if (progresso === 'X') {
                        elementoDia.style.color = 'red';
                    }
                } else {
                    elementoDia.textContent = '';
                }
            }
        });
        marcarDiasNaoTreinados(dias);
        iniciarCronometroSeAtivo();
    }
   
    // Carregar progresso do LocalStorage ao recarregar a página
    window.onload = function () {
        carregarProgresso();
    };

    function marcarConcluido(botao) {
        botao.innerHTML = 'Concluído';
        botao.style.backgroundColor = '#008000';  // Cor verde após clicar
        botao.style.color = '#ffffff';  // Texto branco após clicar
        botao.disabled = true;  // Desativa o botão após ser concluído
    };