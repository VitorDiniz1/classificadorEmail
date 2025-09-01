Classificador e Gerador de Resposta de E-mail com IA
Este é um projeto simples de uma aplicação web que classifica o conteúdo de e-mails em categorias Produtivo e Improdutivo e, em seguida, gera uma resposta sugerida usando a API do Google Gemini.

Funcionalidades
Classificação de E-mail: Analisa o conteúdo de um e-mail para determinar se ele é uma solicitação que requer ação (Produtivo) ou uma comunicação sem ação necessária, como um agradecimento (Improdutivo).

Geração de Resposta: Cria uma resposta de e-mail personalizada e profissional com base na classificação.

Interface Intuitiva: Um frontend simples e limpo para que o usuário possa interagir facilmente com a aplicação.

Tecnologias Utilizadas
Backend:

Python

Flask para o servidor web.

Requests para fazer requisições à API do Gemini.

python-dotenv para gerenciar variáveis de ambiente.

Inteligência Artificial:

Google Gemini API para classificação e geração de texto.

Frontend:

HTML, CSS e JavaScript puro.

Como Executar o Projeto Localmente
Siga estas instruções para configurar e rodar a aplicação em sua máquina.

Pré-requisitos
Python 3.8 ou superior

Pip (gerenciador de pacotes do Python)

1. Clonar o Repositório
git clone [https://github.com/](https://github.com/)[seu_usuario]/[nome_do_repositorio].git
cd [nome_do_repositorio]

2. Configurar o Ambiente
Crie um ambiente virtual para o projeto.

python -m venv venv

Ative o ambiente virtual:

No Windows:

venv\Scripts\activate

No macOS e Linux:

source venv/bin/activate

3. Instalar as Dependências
Instale todas as bibliotecas Python necessárias a partir do arquivo requirements.txt. Crie este arquivo com o seguinte conteúdo:

Flask==2.3.2
python-dotenv==1.0.0
requests==2.31.0

E instale-o com o comando:

pip install -r requirements.txt

4. Configurar a Chave da API
Para usar a API do Google Gemini, você precisa de uma chave.

Obtenha sua chave em Google AI Studio.

Crie um arquivo chamado .env na raiz do projeto e adicione sua chave nele:

GEMINI_API_KEY="SUA_CHAVE_AQUI"

5. Executar a Aplicação
Navegue até a pasta api e execute o script Flask:

cd api
python classify.py