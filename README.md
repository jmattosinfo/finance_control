Agora faça o processo de commit# 💰 KW Controle Financeiro - Gestão Financeira Inteligente

Sistema web de alta performance para gerenciamento financeiro pessoal, desenvolvido com **Django**. O projeto soluciona a organização de fluxos de caixa através de uma arquitetura robusta e interface orientada à experiência do usuário (UX).

---

## 🎬 Demonstração em Tempo Real

Aqui você pode observar o fluxo de funcionamento do sistema, incluindo a abertura de modais dinâmicos e a renderização de gráficos:

![Demonstração do Sistema](assets/gifs/cadastroTransacao.gif)

---

## 🚀 Diferenciais e Autoridade Técnica

Diferente de sistemas básicos, este projeto implementa:
- **Arquitetura MVT (Model-View-Template):** Separação rigorosa de responsabilidades, garantindo facilidade na manutenção e escalabilidade.
- **Django REST Framework (DRF):** Implementação de API para interoperabilidade, permitindo a futura integração com ecossistema **Java + Spring Boot** e **React Native**.
- **Server-Side Rendering (SSR):** Processamento lógico de saldos e filtragem temporal realizado integralmente no backend, entregando um HTML otimizado e seguro ao cliente.
- **Data Visualization:** Integração estratégica de **JavaScript (Chart.js)** para transformar dados brutos em insights visuais (Entradas vs. Saídas).
- **Sistema de Temas (Design System Verde):** Paleta baseada em tons de verde, centralizada em CSS custom properties e alternada entre **tema claro/escuro** via `data-theme="dark"`, com persistência da preferência no `localStorage` e respeito à preferência do sistema (`prefers-color-scheme`).
- **Segurança de Dados:** Implementação de proteção contra ataques CSRF e validação de integridade via Django Forms e ORM.

---

## 📸 Interface e visualização

| Dashboard Mensal | Análise com Gráficos |
| :---: | :---: |
| ![Dashboard](assets/images/dash.png) | ![Gráficos](assets/images/grafico.png) |

| Gestão de Lançamentos | Edição e Exclusão |
| :---: | :---: |
| ![Cadastro](assets/images/novaTransacao.png) | ![Edição](assets/images/editarItem.png) |

---

## 🛠️ Stack Tecnológica

- **Core:** Python 3.x / Django (Framework Full-stack) / Django REST Framework
- **Frontend:** Bootstrap 5 (UI/UX Responsivo), FontAwesome (Iconografia), CSS customizado com Design System de tons de verde
- **Theming:** Tema claro/escuro gerenciado por `finance/static/finance/js/theme.js` + `finance/static/finance/css/theme.css`
- **Database:** SQLite3 (Desenvolvimento) / Preparado para PostgreSQL
- **Analytics:** Chart.js (Visualização de dados dinâmica)

---

## 🏗️ Estrutura Arquitetural

O projeto segue um padrão de organização modular, facilitando a portabilidade e manutenção:

```text
FINANCE_CONTROL/
├── core/           # Kernel do sistema (Settings, URLs globais)
├── finance/        # Business Logic (Models, Views, Serializers, Forms)
│   ├── migrations/ # Histórico de versões do banco de dados
│   ├── static/     # Assets estáticos (Custom CSS, JS)
│   └── templates/  # Camada de apresentação com Herança de Templates (DRY)
├── assets/         # Mídias de documentação (Imagens e GIFs)
├── manage.py       # Utilitário de linha de comando do Django
└── requirements.txt # Gerenciamento de dependências

```

---

## ⚙️ Engenharia de Execução (Instruções)

**Siga os passos abaixo para configurar o ambiente de desenvolvimento localmente:**

**1. Clonagem e Ambiente**
```text
git clone [https://github.com/jmattosinfo/finance-control.git](https://github.com/jmattosinfo/finance-control.git)
cd FINANCE_CONTROL
python -m venv venv
```
### Ativação Windows:
```text
venv\Scripts\activate
```
### Ativação Linux/Mac:
```text
source venv/bin/activate
```
**2. Instalação e Setup**

### Instala as dependências (Django, DRF, CORS-headers)
```text
pip install -r requirements.txt
```
### Executa as migrações do banco de dados
```text
python manage.py migrate
```
### Inicia o servidor (com auto-recarregamento)
```text
python manage.py runserver 127.0.0.1:8000
```
O sistema estará disponível em: http://127.0.0.1:8000/

A API REST estará disponível em: http://127.0.0.1:8000/api/transacoes/

---

## 🛠️ Solução de Problemas (Troubleshooting)

### ❗ Alterações no CSS/templates não renderizam
Sintomas: o tema (verde/escuro) ou outras alterações recentes não aparecem mesmo após salvar os arquivos.

Causas mais comuns e soluções:

1. **Servidor iniciado com `--noreload`** — esse modo **nunca recarrega o código**. Se o servidor foi iniciado antes das alterações, ele continuará servindo a versão antiga indefinidamente.
   - **Solução:** encerre o processo e inicie novamente **sem** a flag `--noreload`:
     ```text
     python manage.py runserver 127.0.0.1:8000
     ```

2. **Múltiplos servidores disputando a mesma porta (8000)** — iniciar `runserver` várias vezes em terminais diferentes deixa vários processos ativos; o navegador pode ser atendido por um servidor "velho".
   - **Solução:** encerre **todos** os processos `runserver` antes de iniciar um novo:
     ```text
     tasklist | findstr python.exe      # identifica os PIDs
     taskkill /PID <PID> /F /T          # encerra cada processo (e filhos)
     ```
   - Depois, inicie **apenas um** servidor.

3. **Cache do navegador** — mesmo com o servidor correto, o navegador pode exibir o CSS antigo em cache.
   - **Solução:** faça um **hard refresh** com **Ctrl+Shift+R** (Windows/Linux) ou **Cmd+Shift+R** (Mac). Se necessário, limpe o cache do navegador.

4. **Cache de static files do Django (produção)** — em ambiente de produção, use `python manage.py collectstatic` após alterar `finance/static/` e aplique um versionamento de cache (ex.: `ManifestStaticFilesStorage`) para forçar a atualização dos assets.

### ❗ Porta 8000 já em uso
Outros processos (Docker, WSL, ou outro projeto) podem estar ocupando a porta `8000`.
- **Solução:** identifique com `netstat -ano | findstr :8000` e, se o processo não for essencial, encerre-o — ou rode o servidor em outra porta:
  ```text
  python manage.py runserver 127.0.0.1:8001
  ```

---

## 📈 Roadmap de Evolução

- [x] Dashboard dinâmico com integração de Gráficos (Chart.js).

- [x] Implementação de API REST com Django REST Framework (DRF).

- [ ] Implementação de autenticação via Token/JWT.

- [ ] Containerização com Docker.

- [ ] Migração planejada para backend em Java Spring Boot.

### 👨‍💻 Autor
Julio César de Mattos Vieira

Desenvolvedor de Software | Especialista em Suporte e Infraestrutura

 [LinkedIn](https://linkedin.com/in/juliomattos-dev) | [GitHub](https://github.com/jmattosinfo)