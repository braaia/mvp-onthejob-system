
# On The Job — Employee Activity Management System

<p align="center">
  <a href="#português">🇧🇷 Português</a> |
  <a href="#english">🇺🇸 English</a>
</p>

<p align="center">
  Sistema de gerenciamento de colaboradores e atividades desenvolvido para simplificar registros internos e reduzir o uso de documentos físicos.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flet-02569B?style=for-the-badge&logo=flutter&logoColor=white" alt="Flet">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase">
</p>

---
<a id="português"></a>
## 🇧🇷 Português

### Sobre o projeto

O **On The Job** é um sistema de gerenciamento de colaboradores e atividades desenvolvido para solucionar um problema relacionado ao uso excessivo de papel e documentos físicos no registro de informações de funcionários.

A aplicação digitaliza o processo de cadastro de colaboradores e acompanhamento de suas atividades, permitindo que administradores gerenciem informações e que colaboradores acompanhem seus próprios registros.

O projeto foi desenvolvido individualmente como um MVP funcional, com foco na integração entre uma interface desktop, uma API REST e um banco de dados relacional.

### Funcionalidades

- **Autenticação de usuários:** cadastro, login e recuperação de senha utilizando Firebase Authentication.
- **Autenticação da API:** geração e validação de tokens JWT pela API FastAPI.
- **Controle de acesso:** diferenciação entre administradores e colaboradores.
- **Cadastro de colaboradores:** registro de informações pessoais e profissionais.
- **Gerenciamento de atividades:** criação, consulta, edição e exclusão de atividades.
- **Acompanhamento de atividades:** visualização de status, comentários e informações relacionadas às atividades.
- **Assinaturas:** campos para registro das assinaturas do colaborador e do gestor.
- **Exportação de relatórios PDF:**
  - Geração de PDF com todas as atividades de um colaborador.
  - Geração de PDF com atividades selecionadas.
  - Exportação de uma atividade individual.
- **Interface adaptável:** suporte a temas claro e escuro.

### Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flet | Construção da interface desktop |
| FastAPI | Desenvolvimento da API REST |
| SQLite | Persistência dos dados |
| Firebase Authentication | Autenticação de usuários |
| JWT | Autorização das requisições à API |
| HTTPX | Comunicação HTTP entre frontend e backend |
| ReportLab | Geração de documentos PDF |

### Arquitetura

O sistema utiliza uma arquitetura separada em frontend e backend.

```text
┌──────────────────────────────┐
│        Frontend              │
│                              │
│          Flet                │
│                              │
│  Interface e navegação       │
│  Autenticação Firebase       │
└──────────────┬───────────────┘
               │
               │ HTTP / HTTPX
               │ JWT
               ▼
┌──────────────────────────────┐
│          Backend             │
│                              │
│          FastAPI             │
│                              │
│  Autenticação JWT            │
│  Regras de negócio           │
│  Gerenciamento de dados      │
│  Geração de PDFs             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Database            │
│                              │
│           SQLite             │
│                              │
│  Usuários                    │
│  Colaboradores               │
│  Atividades                  │
└──────────────────────────────┘
```

O Firebase Authentication é utilizado para operações de autenticação, enquanto a API possui seu próprio mecanismo de autenticação e emissão de tokens JWT para autorizar as requisições.

### Estrutura do projeto

```text
mvp-onthejob-system/
│
├── app.py
├── requirements.txt
├── render.yaml
│
└── src/
    ├── backend/
    │   ├── api.py
    │   ├── auth.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── schemas.py
    │
    └── views/
        ├── adminpage.py
        ├── detalhes_atv.py
        ├── detalhes_cola.py
        ├── home.py
        ├── lista_cola.py
        │
        ├── loginpage/
        │   ├── login.py
        │   ├── register.py
        │   └── forgot.py
        │
        └── ...
```

### Executando o projeto

**Pré-requisitos**

- Python 3.10 ou superior.
- Conta e projeto configurados no Firebase.
- Firebase Authentication habilitado.
- Configuração do Firebase disponível para a aplicação.

**1. Clone o repositório**

```bash
git clone https://github.com/braaia/mvp-onthejob-system.git

cd mvp-onthejob-system
```

**2. Crie um ambiente virtual**

```bash
python -m venv venv
```

Ative o ambiente virtual:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Configure o Firebase**

Configure as credenciais do Firebase Authentication conforme a configuração esperada pela aplicação.

**5. Inicie o backend**

Na raiz do projeto:

```bash
uvicorn src.backend.main:app --reload
```

A API estará disponível em:

```text
http://localhost:8000
```

Documentação interativa da API:

```text
http://localhost:8000/docs
```

**6. Inicie o frontend**

Em outro terminal, com o ambiente virtual ativado:

```bash
python app.py
```

> **Observação:** o endereço da API está configurado em `src/backend/api.py`. Para execução local, frontend e backend devem estar configurados para utilizar o mesmo endereço. A configuração do Firebase também precisa estar disponível no ponto de inicialização da aplicação.

### Status do projeto

O On The Job está em estágio de MVP funcional. A aplicação possui os principais fluxos de cadastro, gerenciamento de atividades, autenticação e geração de documentos PDF.

O projeto ainda pode receber melhorias de arquitetura, segurança, tratamento de erros, configuração de ambiente e experiência do usuário.

### Autor

**Desenvolvido individualmente por [Braia](https://github.com/braaia).**

- GitHub: [github.com/braaia](https://github.com/braaia)
- LinkedIn: [linkedin.com/in/wesleynog](https://www.linkedin.com/in/wesleynog/)

---
<a id="english"></a>
## 🇺🇸 English

### About the project

**On The Job** is an employee and activity management system developed to address excessive paper usage and physical documentation in employee record management.

The application digitizes employee registration and activity tracking, allowing administrators to manage employee information while employees can access and follow their own records.

The project was independently developed as a functional MVP, focusing on integration between a desktop interface, a REST API, and a relational database.

### Features

- **User authentication:** registration, login, and password recovery using Firebase Authentication.
- **API authentication:** JWT generation and validation through the FastAPI backend.
- **Access control:** separate roles for administrators and employees.
- **Employee registration:** management of personal and professional information.
- **Activity management:** create, retrieve, update, and delete activities.
- **Activity tracking:** status updates, comments, and activity information.
- **Signatures:** fields for employee and manager signatures.
- **PDF report generation:**
  - Export all activities associated with an employee.
  - Export selected activities.
  - Export individual activity records.
- **Adaptive interface:** light and dark theme support.

### Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flet | Desktop user interface |
| FastAPI | REST API development |
| SQLite | Data persistence |
| Firebase Authentication | User authentication |
| JWT | API request authorization |
| HTTPX | HTTP communication between frontend and backend |
| ReportLab | PDF document generation |

### Architecture

The application follows a separated frontend and backend architecture.

```text
┌──────────────────────────────┐
│          Frontend            │
│                              │
│            Flet              │
│                              │
│  Interface and navigation    │
│  Firebase authentication     │
└──────────────┬───────────────┘
               │
               │ HTTP / HTTPX
               │ JWT
               ▼
┌──────────────────────────────┐
│           Backend            │
│                              │
│           FastAPI            │
│                              │
│  JWT authentication          │
│  Business logic              │
│  Data management             │
│  PDF generation              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Database           │
│                              │
│            SQLite            │
│                              │
│  Users                       │
│  Employees                   │
│  Activities                  │
└──────────────────────────────┘
```

Firebase Authentication handles user authentication operations, while the API maintains its own authentication mechanism and JWT issuance to authorize requests.

### Project structure

```text
mvp-onthejob-system/
│
├── app.py
├── requirements.txt
├── render.yaml
│
└── src/
    ├── backend/
    │   ├── api.py
    │   ├── auth.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   └── schemas.py
    │
    └── views/
        ├── adminpage.py
        ├── detalhes_atv.py
        ├── detalhes_cola.py
        ├── home.py
        ├── lista_cola.py
        │
        ├── loginpage/
        │   ├── login.py
        │   ├── register.py
        │   └── forgot.py
        │
        └── ...
```

### Running the project

**Prerequisites**

- Python 3.10 or higher.
- A configured Firebase project.
- Firebase Authentication enabled.
- Firebase configuration available to the application.

**1. Clone the repository**

```bash
git clone https://github.com/braaia/mvp-onthejob-system.git

cd mvp-onthejob-system
```

**2. Create a virtual environment**

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure Firebase**

Set up Firebase Authentication credentials according to the configuration expected by the application.

**5. Start the backend**

From the project root:

```bash
uvicorn src.backend.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

**6. Start the frontend**

In another terminal, with the virtual environment activated:

```bash
python app.py
```

> **Note:** the API address is configured in `src/backend/api.py`. For local execution, the frontend and backend must use the same address. Firebase configuration must also be available when the application starts.

### Project status

On The Job is currently a functional MVP. It includes the main workflows for employee registration, activity management, authentication, and PDF generation.

Further improvements can be made to the architecture, security, error handling, environment configuration, and user experience.

### Author

**Independently developed by [Braia](https://github.com/braaia).**

- GitHub: [github.com/braaia](https://github.com/braaia)
- LinkedIn: [linkedin.com/in/wesleynog](https://www.linkedin.com/in/wesleynog/)
