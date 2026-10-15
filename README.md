# 📦 Sistema de Gestão de Empréstimos de Equipamentos (IFCE)

Aplicação desenvolvida em **Flask (Python)** com **SQLAlchemy** e banco de dados **SQLite** (com suporte e compatibilidade para migração rápida para **PostgreSQL**). 

Implementa observabilidade com **Sentry** e automação **ChatOps** integrando **GitHub e Discord**, conforme os requisitos da **Prática 02 - PWII (IFCE)**.


---

## 📸 Validação da Atividade (Prints Obrigatórios)

> Conforme solicitado no enunciado da Prática 02, abaixo estão os 4 prints comprobatórios da execução da atividade:

### 1. Print 1 – Código-Fonte (`Sentry.init` e Gatilho/Endpoint)
*Exibição no editor do código com a inicialização do SDK do Sentry e o endpoint de teste `/debug-sentry`.*

![Print 1 - Codigo Fonte](docs/print1_codigo_sentry.png)

---

### 2. Print 2 – Painel do Sentry (Aba *Issues*)
*Painel web do Sentry capturando o erro proativo disparado com o respectivo stack trace detalhado.*

![Print 2 - Painel Sentry](docs/print2_painel_sentry.png)

---

### 3. Print 3 – Configuração do Webhook no GitHub
*Tela de Settings > Webhooks do repositório no GitHub com a URL do Discord terminada em `/github` e tipo `application/json`.*

![Print 3 - Webhook GitHub](docs/print3_webhook_github.png)

---

### 4. Print 4 – Canal de Texto no Discord (Notificação ChatOps)
*Notificação automática enviada pelo bot do Discord após a realização de um `git push` no repositório.*

![Print 4 - Notificacao Discord](docs/print4_notificacao_discord.png)

---

---

## 🚀 Funcionalidades
- **Cadastrar Equipamentos:** Adição de notebooks, monitores, teclados, mouses e periféricos com código de patrimônio único.
- **Listar Equipamentos:** Filtros visuais por status (*Disponíveis*, *Emprestados*, *Em Manutenção*).
- **Registrar Empréstimos e Devoluções:** Controle do responsável, contato, prazos de devolução e encerramento com 1 clique.
- **Consultar Estado do Equipamento:** Tela de detalhes com histórico completo de empréstimos e opções de manutenção.
- **Observabilidade (Sentry):** Rastreamento de erros em tempo real via SDK oficial e rota de teste `/debug-sentry`.

---


## 🛠️ Como Executar o Projeto Localmente

### 1. Clonar o repositório e acessar a pasta
```bash
git clone <URL_DO_REPOSITORIO>
cd emprestados
```

### 2. Criar e ativar o ambiente virtual (Opcional, mas recomendado)
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente
Copie o arquivo `.env.example` para `.env`:
```bash
copy .env.example .env
```
Edite o arquivo `.env` para inserir sua DSN do Sentry:
```env
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta

# Banco SQLite padrão:
DATABASE_URL=sqlite:///emprestados.db

# Para migrar para PostgreSQL, basta alterar a DATABASE_URL:
# DATABASE_URL=postgresql://usuario:senha@localhost:5432/emprestados_db

# Sua DSN obtida no Sentry.io:
SENTRY_DSN=https://xxxxxxxx@xxxx.ingest.sentry.io/xxxx
```

### 5. Executar a aplicação
```bash
python app.py
```
Acesse no navegador: `http://localhost:5000`

---


