# Smart Vending Machine System with AI

This project implements a backend system for an intelligent vending machine, leveraging FastAPI for the API, SQLModel for database management (SQLite), and `instructor` to interact with OpenAI's Large Language Models (LLMs) for natural language processing.

The main objective is to simulate user interaction with a vending machine through text commands, where the artificial intelligence interprets the purchase intent, and the application manages stock and records transactions.

## Table of Contents

* [Features](#features)
* [Technologies Used](#technologies-used)
* [Prerequisites](#prerequisites)
* [Environment Setup](#environment-setup)
* [Running the Application](#running-the-application)
    * [Locally (Python Virtual Env)](#locally-python-virtual-env)
    * [With Docker Compose](#with-docker-compose)
* [API Endpoints](#api-endpoints)
* [Challenges and Solutions](#challenges-and-solutions)
* [Future Improvements](#future-improvements)
* [Author](#author)

## Features

* Stock Management: Maintain a record of the stock for different soda types.
* AI Command Processing: Utilize the OpenAI API to interpret user purchase intent from natural language commands (e.g., "I want 2 Pepsis").
* Purchase Fulfillment: Process transactions, update stock, and record purchases.
* Data Persistence: Store soda and transaction information in an SQLite database.
* RESTful API: Provides HTTP endpoints for system interaction.
* Robust Error Handling: Manages internal errors and OpenAI API errors, returning clear messages.

## Technologies Used

* **Python 3.11+**
* **FastAPI:** A modern, fast (high-performance) web framework for building APIs.
* **SQLModel:** A library for interacting with databases, combining SQLAlchemy and Pydantic.
* **OpenAI API:** For access to language models like GPT-3.5 Turbo.
* **`instructor`:** A library that facilitates structured data extraction from LLMs using Pydantic.
* **`python-dotenv`:** For loading environment variables from a `.env` file.
* **Uvicorn:** An ASGI server for running FastAPI applications.
* **Docker / Docker Compose:** For containerization and service orchestration.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

* [Python 3.11+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
* [Git](https://git-scm.com/downloads)
* **OpenAI API Key:** You will need a valid OpenAI API key. This key must be configured in a `.env` file at the root of your project. Visit [platform.openai.com](https://platform.openai.com/) to obtain one. **Please note: sufficient credit on your OpenAI account is required for the AI integration to function.**
* [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/) (optional, for running via containers)

## Environment Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/jl-07/soda_machine](https://github.com/jl-07/soda_machine) # Example, replace with your project repository URL
    cd soda_machine
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create the `.env` file:**
    In the project root (`soda_machine/`), create a file named `.env` and add your OpenAI key:
    ```
    OPENAI_API_KEY="your_secret_key_here"
    ```
    (Replace `"your_secret_key_here"` with your actual OpenAI key, which starts with `sk-...`).

## Running the Application

### Locally (Python Virtual Env)

After setting up the environment (steps 1 to 4 above):

1.  **Remove `soda.db` (optional, to reset stock):**
    If you wish to have the database recreated from scratch and the initial stock populated, delete the `soda.db` file from the project root before starting.
    ```bash
    del soda.db  # On Windows
    rm soda.db   # On macOS/Linux
    ```
2.  **Start the Uvicorn server:**
    ```bash
    uvicorn app.main:app --reload --log-level debug
    ```
    The server will be running at `http://127.0.0.1:8000`. You will see logs in the terminal indicating table creation and stock initialization.

### With Docker Compose

Ensure Docker and Docker Compose are installed and your `.env` file is configured.

1.  **Build and start the services:**
    ```bash
    docker compose up --build -d
    ```
    The `-d` runs the service in detached mode (in the background).
2.  **Check logs (optional):**
    ```bash
    docker compose logs -f soda_api
    ```
3.  **To stop the services:**
    ```bash
    docker compose down
    ```

## API Endpoints

The interactive API documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs`.

### 1. `GET /parse`

* **Description:** Interprets a text message using AI to extract purchase intent, soda type, and quantity.
* **Method:** `GET`
* **Query Parameters:**
    * `message` (string, **required**): The user's message to be processed.
* **Example Usage (in browser):**
    ```
    [http://127.0.0.1:8000/parse?message=buy%201%20fanta](http://127.0.0.1:8000/parse?message=buy%201%20fanta)
    ```
* **Example Response (Success):**
    ```json
    {
        "intent": "comprar", # Intent is still 'comprar' as per your ParsedCommand model
        "soda_type": "fanta",
        "quantity": 1
    }
    ```
* **Example Response (OpenAI Error - Quota Exceeded):**
    ```json
    {
        "detail": "Erro da OpenAI: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: [https://platform.openai.com/docs/guides/error-codes/api-errors](https://platform.openai.com/docs/guides/error-codes/api-errors)."
    }
    ```

### 2. `POST /buy`

* **Description:** Processes the purchase of sodas based on a user's message. AI is used to interpret the message, stock is updated, and the transaction is recorded.
* **Method:** `POST`
* **Request Body (JSON):**
    ```json
    {
        "message": "I'd like 2 Pepsis please."
    }
    ```
* **Example Response (Success):**
    ```json
    {
        "status": "success",
        "message": "Purchase of 2 pepsi completed. Remaining stock: 8." # Message from your handle_purchase
    }
    ```
* **Example Response (Error - Insufficient Stock):**
    ```json
    {
        "status": "error",
        "message": "Soda 'coke' unavailable or insufficient stock. We only have 5." # Message from your handle_purchase
    }
    ```
* **Example Response (OpenAI Error - Quota Exceeded):**
    ```json
    {
        "detail": "Erro da OpenAI: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: [https://platform.openai.com/docs/guides/error-codes/api-errors](https://platform.openai.com/docs/guides/error-codes/api-errors)."
    }
    ```

## Challenges and Solutions

One of the main challenges during development was the robust integration with the OpenAI API. Initially, errors related to API quota (`insufficient_quota`) resulted in generic `500 Internal Server Errors`. The solution involved:

* **Importing `OpenAIError`:** To specifically catch exceptions from the OpenAI library.
* **Detailed Error Handling:** Implementing `try-except OpenAIError` blocks in routes that interact with the OpenAI API to extract and return the detailed error message from OpenAI to the API client, improving debugging and user experience. This ensures that, even without credits, the user receives a clear message about the issue.

## Future Improvements

* Authentication and Authorization: Implement security mechanisms for the API.
* Enhanced Input Validation: More robust validation for user messages before sending them to the AI.
* Integration with Other LLMs: Allow easy integration with different language models or providers.
* AI Response Caching: To optimize costs and latency for repeated requests.
* User Interface (Frontend): Develop a graphical interface to interact with the vending machine.
* Monitoring and Logging: Implement a more advanced monitoring system for the application.

## Author

**Júnior Lira**
* [LinkedIn](https://www.linkedin.com/in/juniorlirati/)
* [GitHub](https://github.com/jl-07)



 In portuguese language
# Sistema de Máquina de Refrigerantes com IA

Este projeto implementa um sistema de backend para uma máquina de refrigerantes inteligente, utilizando FastAPI para a API, SQLModel para gerenciamento do banco de dados (SQLite) e `instructor` para interagir com modelos de Linguagem Grande (LLMs) da OpenAI para processamento de linguagem natural.

O objetivo principal é simular a interação de um usuário com uma máquina de refrigerantes através de comandos de texto, onde a inteligência artificial interpreta a intenção de compra e a aplicação gerencia o estoque e registra as transações.

## Índice

* [Funcionalidades](#funcionalidades)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Pré-requisitos](#pré-requisitos)
* [Configuração do Ambiente](#configuração-do-ambiente)
* [Executando a Aplicação](#executando-a-aplicação)
    * [Localmente (Python Virtual Env)](#localmente-python-virtual-env)
    * [Com Docker Compose](#com-docker-compose)
* [Endpoints da API](#endpoints-da-api)
* [Desafios e Soluções](#desafios-e-soluções)
* [Próximos Passos (Melhorias Futuras)](#próximos-passos-melhorias-futuras)
* [Autor](#autor)

## Funcionalidades

* Gerenciamento de Estoque: Mantenha um registro do estoque de diferentes tipos de refrigerantes.
* Processamento de Comandos com IA: Utilize a API da OpenAI para interpretar a intenção de compra do usuário a partir de comandos em linguagem natural (ex: "Quero 2 Pepsis").
* Realização de Compras: Processa a transação, atualiza o estoque e registra a compra.
* Persistência de Dados: Armazena informações de refrigerantes e transações em um banco de dados SQLite.
* API RESTful: Oferece endpoints HTTP para interagir com o sistema.
* Tratamento de Erros Robusto: Lida com erros internos e erros da API da OpenAI, retornando mensagens claras.

## Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI:** Framework web moderno e rápido para construção de APIs.
* **SQLModel:** Biblioteca para interagir com bancos de dados, combinando SQLAlchemy e Pydantic.
* **OpenAI API:** Para acesso a modelos de linguagem como GPT-3.5 Turbo.
* **`instructor`:** Biblioteca que facilita a extração de dados estruturados de LLMs usando Pydantic.
* **`python-dotenv`:** Para carregar variáveis de ambiente de um arquivo `.env`.
* **Uvicorn:** Servidor ASGI para rodar aplicações FastAPI.
* **Docker / Docker Compose:** Para containerização e orquestração de serviços.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

* [Python 3.11+](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/) (gerenciador de pacotes do Python)
* [Git](https://git-scm.com/downloads)
* **Chave de API da OpenAI:** Você precisará de uma chave de API válida da OpenAI. Esta chave deve ser configurada em um arquivo `.env` na raiz do projeto. Acesse [platform.openai.com](https://platform.openai.com/) para obter uma. **É necessário ter créditos na conta da OpenAI para que a integração com a IA funcione.**
* [Docker](https://www.docker.com/products/docker-desktop) e [Docker Compose](https://docs.docker.com/compose/install/) (opcional, para rodar via containers)

## Configuração do Ambiente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/jl-07/soda_machine](https://github.com/jl-07/soda_machine) # Exemplo, substitua pelo URL do seu repositório do projeto
    cd soda_machine
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Crie o arquivo `.env`:**
    Na raiz do projeto (`soda_machine/`), crie um arquivo chamado `.env` e adicione sua chave da OpenAI:
    ```
    OPENAI_API_KEY="sua_chave_secreta_aqui"
    ```
    (Substitua `"sua_chave_secreta_aqui"` pela sua chave real da OpenAI, que começa com `sk-...`).

## Executando a Aplicação

### Localmente (Python Virtual Env)

Após configurar o ambiente (passos 1 a 4 acima):

1.  **Remova o arquivo `soda.db` (opcional, para resetar o estoque):**
    Se você deseja que o banco de dados seja recriado do zero e o estoque inicial seja populado, apague o arquivo `soda.db` na raiz do projeto antes de iniciar.
    ```bash
    del soda.db  # No Windows
    rm soda.db   # No macOS/Linux
    ```
2.  **Inicie o servidor Uvicorn:**
    ```bash
    uvicorn app.main:app --reload --log-level debug
    ```
    O servidor estará rodando em `http://127.0.0.1:8000`. Você verá logs no terminal indicando a criação das tabelas e a inicialização do estoque.

### Com Docker Compose

Certifique-se de ter o Docker e o Docker Compose instalados e o arquivo `.env` configurado.

1.  **Construa e inicie os serviços:**
    ```bash
    docker compose up --build -d
    ```
    O `-d` roda o serviço em modo detached (em segundo plano).
2.  **Verifique os logs (opcional):**
    ```bash
    docker compose logs -f soda_api
    ```
3.  **Para parar os serviços:**
    ```bash
    docker compose down
    ```

## Endpoints da API

A documentação interativa da API (Swagger UI) estará disponível em `http://127.0.0.1:8000/docs`.

### 1. `GET /parse`

* **Descrição:** Interpreta uma mensagem de texto usando IA para extrair a intenção, tipo de refrigerante e quantidade.
* **Método:** `GET`
* **Parâmetros de Query:**
    * `message` (string, **obrigatório**): A mensagem do usuário para ser processada.
* **Exemplo de Uso (no navegador):**
    ```
    [http://127.0.0.1:8000/parse?message=comprar%201%20fanta](http://127.0.0.1:8000/parse?message=comprar%201%20fanta)
    ```
* **Exemplo de Resposta (Sucesso):**
    ```json
    {
        "intent": "comprar",
        "soda_type": "fanta",
        "quantity": 1
    }
    ```
* **Exemplo de Resposta (Erro OpenAI - Cota Excedida):**
    ```json
    {
        "detail": "Erro da OpenAI: You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: [https://platform.openai.com/docs/guides/error-codes/api-errors](https://platform.openai.com/docs/guides/error-codes/api-errors)."
    }
    ```

### 2. `POST /buy`

* **Descrição:** Processa a compra de refrigerantes com base em uma mensagem do usuário. A IA é utilizada para interpretar a mensagem, o estoque é atualizado e a transação é registrada.
* **Método:** `POST`
* **Corpo da Requisição (JSON):**
    ```json
    {
        "message": "Eu quero 2 Pepsis por favor."
    }
    ```
* **Exemplo de Resposta (Sucesso):**
    ```json
    {
        "status": "success",
        "message": "Compra de 2 pepsi realizada. Estoque restante: 8."
    }
    ```
* **Exemplo de Resposta (Erro - Estoque Insuficiente):**
    ```json
    {
        "status": "error",
        "message": "Refrigerante 'coke' indisponível ou estoque insuficiente. Temos apenas 5."
    }
    ```
* **Exemplo de Resposta (Erro OpenAI - Cota Excedida):**
    ```json
    {
        "detail": "Erro da OpenAI: You exceeded your current quota, please please check your plan and billing details. For more information on this error, read the docs: [https://platform.openai.com/docs/guides/error-codes/api-errors](https://platform.openai.com/docs/guides/error-codes/api-errors)."
    }
    ```

## Desafios e Soluções

Um dos principais desafios durante o desenvolvimento foi a integração robusta com a API da OpenAI. Inicialmente, erros relacionados à quota da API (`insufficient_quota`) resultavam em `500 Internal Server Errors` genéricos. A solução envolveu:

* **Importar `OpenAIError`:** Para capturar especificamente exceções da biblioteca OpenAI.
* **Tratamento Detalhado:** Implementar blocos `try-except OpenAIError` nas rotas que interagem com a API da OpenAI para extrair e retornar a mensagem de erro detalhada da OpenAI ao cliente da API, melhorando a depuração e a experiência do usuário. Isso garante que, mesmo sem créditos, o usuário receba uma mensagem clara sobre o problema.

## Próximos Passos (Melhorias Futuras)

* Autenticação e Autorização: Implementar mecanismos de segurança para a API.
* Validação de Entrada Aprimorada: Mais validações para as mensagens do usuário antes de enviar para a IA.
* Integração com Outros LLMs: Permitir a fácil integração com diferentes modelos de linguagem ou provedores.
* Cache de Respostas da IA: Para otimizar custos e latência em requisições repetidas.
* Interface do Usuário (Frontend): Desenvolver uma interface gráfica para interagir com a máquina de refrigerantes.
* Monitoramento e Logs: Implementar um sistema de monitoramento mais avançado para a aplicação.

## Autor

**Júnior Lira**
* [LinkedIn](https://www.linkedin.com/in/juniorlirati/)
* [GitHub](https://github.com/jl-07)