Sistema de Gerenciamento de Academia com Flask
Este é um sistema de gerenciamento de academia desenvolvido em Python utilizando o framework Flask. Ele oferece funcionalidades essenciais para facilitar a administração de uma academia, incluindo o cadastro de alunos, controle de treinos, monitoramento de pagamentos e muito mais.

Instalação
Certifique-se de ter o Python e o pip instalados em sua máquina. Em seguida, siga os passos abaixo:

Clone este repositório:

bash
Copy code
git clone https://github.com/seu-usuario/sistema-academia-flask.git
Acesse o diretório do projeto:

bash
Copy code
cd sistema-academia-flask
Instale as dependências:

bash
Copy code
pip install -r requirements.txt
Configuração
Crie um arquivo .env na raiz do projeto e configure as variáveis necessárias. Você pode usar o arquivo .env.example como referência.

Configure o banco de dados executando as migrações:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Uso
Execute o aplicativo Flask:

bash
Copy code
flask run
O aplicativo estará disponível em http://localhost:5000.

Funcionalidades
Cadastro de Alunos: Registre informações detalhadas sobre os alunos, incluindo nome, idade, sexo, etc.

Controle de Treinos: Atribua planos de treino específicos para cada aluno, com a capacidade de atualizar e monitorar o progresso.

Gestão de Pagamentos: Registre os pagamentos dos alunos e visualize facilmente os status de pagamento.

Relatórios: Gere relatórios personalizados sobre a frequência dos alunos, pagamentos pendentes, entre outros.

Contribuições
Contribuições são bem-vindas! Se você encontrar problemas ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Licença
Este projeto é licenciado sob a MIT License.