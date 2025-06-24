README - Academia API
Visão Geral
Esta API gerencia alunos, checkins e prevê risco de cancelamento (churn) em academias. Desenvolvida com FastAPI, PostgreSQL e RabbitMQ, oferece endpoints RESTful e processamento assíncrono.

Pré-requisitos
Docker

Docker Compose

Instalação e Execução
1. Clonar o repositório:
bash
git clone https://github.com/Tihkuhh/academia-api.git
cd academia-api
2. Iniciar os containers:
bash
docker-compose up --build
3. Acessar a API:
Documentação interativa: http://localhost:8000/docs

Endpoint base: http://localhost:8000

Serviços em Execução
Serviço	Porta	Descrição
API FastAPI	8000	Serviço principal
PostgreSQL	5432	Banco de dados
RabbitMQ Management	15672	Interface de gerenciamento
RabbitMQ	5672	Sistema de filas
Endpoints Principais
Registrar Aluno
bash
curl -X POST "http://localhost:8000/aluno/registro" \
-H "Content-Type: application/json" \
-d '{"nome": "Maria Silva", "email": "maria@email.com", "plano_id": 1}'
Registrar Checkin
bash
curl -X POST "http://localhost:8000/aluno/checkin" \
-H "Content-Type: application/json" \
-d '{"aluno_id": 1}'
Verificar Frequência
bash
curl -X GET "http://localhost:8000/aluno/1/frequencia"
Obter Risco de Churn
bash
curl -X GET "http://localhost:8000/aluno/1/risco-churn"
Estrutura do Projeto
text
academia-api/
├── app/
│   ├── database/           # Conexão com banco de dados
│   ├── models/             # Modelos de dados
│   ├── routes/             # Endpoints da API
│   ├── schemas/            # Esquemas Pydantic
│   ├── workers/            # Processamento assíncrono
│   ├── initdb.py           # Inicialização do banco
│   └── main.py             # Aplicação principal
├── ml/                     # Modelos de machine learning
├── reports/                # Relatórios gerados (CSV)
├── docker-compose.yml      # Configuração Docker
├── Dockerfile              # Build da aplicação
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo
Workers (Processamento Assíncrono)
Checkin Worker: Processa registros de entrada na academia

Report Worker: Gera relatórios diários (CSV) em ./reports

Retrain Worker: Retreina o modelo de churn semanalmente

Modelo de Machine Learning
Prevê risco de cancelamento com base em:

Frequência semanal

Dias desde último checkin

Duração média das visitas

Tipo de plano

Notebook de treinamento: churn_model.ipynb

Retreinamento automático: Semanal

Testando a Aplicação
Registre um novo aluno

Faça alguns checkins

Verifique o histórico de frequência

Consulte o risco de churn

Acesse o RabbitMQ (http://localhost:15672) para monitorar filas

Solução de Problemas
Se encontrar erros na inicialização:

bash
docker-compose down --volumes
docker-compose up --build
Próximos Passos (Melhorias)
Implementar autenticação JWT

Adicionar testes automatizados

Configurar monitoramento

Implementar cache com Redis

Contato
Para suporte ou contribuições, entre em contato com Thiago - tico.lemesdarosa@gmail.com