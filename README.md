# Sistema de Mercado

Sistema de gerenciamento de mercado desenvolvido em Python, com interface gráfica em CustomTkinter e banco de dados MySQL.

O projeto tem como objetivo facilitar o gerenciamento das operações de um mercado, permitindo o cadastro e a consulta de informações por meio de uma interface gráfica organizada e intuitiva.

## Funcionalidades

- Cadastro e consulta de categorias.
- Cadastro e consulta de produtos.
- Gerenciamento de clientes.
- Gerenciamento de vendedores.
- Registro e consulta de vendas.
- Controle de estoque dos produtos.
- Dashboard com informações gerais do sistema.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento da aplicação.
- **CustomTkinter:** criação da interface gráfica.
- **MySQL:** armazenamento e gerenciamento dos dados.
- **mysql-connector-python:** conexão entre Python e MySQL.
- **Arquitetura MVC:** organização do projeto em Models, Views e Controllers.

## Estrutura do projeto

```text
sistema-mercado/
│
├── controllers/
├── database/
├── models/
├── views/
├── .env.example
├── .gitignore
├── main.py
└── requirements.txt
```

## Instalação e execução

1. Clone o repositório:

```bash
git clone https://github.com/biluzim2/sistema-mercado.git
```

2. Entre na pasta do projeto:

```bash
cd sistema-mercado
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados MySQL e crie seu arquivo `.env` com as credenciais locais, seguindo o modelo de `.env.example`.

5. Execute a aplicação:

```bash
python main.py
```

## Banco de dados

O sistema utiliza MySQL para armazenar as informações de categorias, produtos, clientes, vendedores e vendas.

As credenciais de conexão devem ser configuradas localmente no arquivo `.env`, que não deve ser enviado ao GitHub.

## Organização do código

O projeto utiliza o padrão arquitetural MVC:

- **Models:** responsáveis pela comunicação com o banco de dados e pelas operações com os dados.
- **Views:** responsáveis pela interface gráfica e apresentação das informações.
- **Controllers:** responsáveis por intermediar as ações entre as Views e os Models.

## Objetivo do projeto

Este projeto faz parte da minha jornada de aprendizado em Análise e Desenvolvimento de Sistemas e tem como objetivo aplicar na prática conceitos de programação, banco de dados, interface gráfica e organização de software.