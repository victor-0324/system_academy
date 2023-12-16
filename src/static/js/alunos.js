
    var pesquisaInput = document.getElementById('pesquisa');
    var listaPesquisa = document.getElementById('listaPesquisa');
    var tabelaAlunosBody = document.getElementById('tabelaAlunosBody');

    pesquisaInput.addEventListener('input', function () {
        var termoPesquisa = pesquisaInput.value.trim().toLowerCase();
    
        if (termoPesquisa === '') {
            listaPesquisa.innerHTML = '';
            atualizarTabela(alunos);
            return;
        }
    
        var resultados = alunos.filter(function (aluno) {
            return aluno.nome.toLowerCase().includes(termoPesquisa);
        });
    
        listaPesquisa.innerHTML = '';
        resultados.forEach(function (resultado) {
            var listItem = document.createElement('li');
            listItem.textContent = resultado.nome;
            listItem.onclick = function () {
                window.open('detalhes/' + resultado.id);
            };
            listaPesquisa.appendChild(listItem);
        });
    
        // Atualiza a tabela de alunos
        atualizarTabela(resultados);
    });

    function atualizarTabela(resultados) {
        tabelaAlunosBody.innerHTML = '';
    
        resultados.forEach(function (resultado) {
            var newRow = tabelaAlunosBody.insertRow(tabelaAlunosBody.rows.length);
            var cellNome = newRow.insertCell(0);
            var cellStatus = newRow.insertCell(1);
            var cellAcoes = newRow.insertCell(2);
    
            cellNome.innerHTML = resultado.nome;
    
            cellStatus.innerHTML = resultado.inadimplente
                ? '<span class="text-danger">Inadimplente</span><br>'
                : '<span class="text-success">Pago</span>';
    
            var detalhesButton = document.createElement('button');
            detalhesButton.textContent = 'Detalhes';
            detalhesButton.onclick = function () {
                window.open('detalhes/' + resultado.id);
            };
    
            cellAcoes.appendChild(detalhesButton);
    
            var deletarButton = document.createElement('button');
            deletarButton.textContent = 'Deletar';
            deletarButton.className = 'registro-formulario';
            deletarButton.onclick = function () {
                var confirmacao = confirm("Tem certeza de que deseja excluir este aluno?");
                if (confirmacao) {
                    window.location.href = "/alunos/deletar/" + resultado.id;
                }
            };
    
            cellAcoes.appendChild(deletarButton);
        });
    }