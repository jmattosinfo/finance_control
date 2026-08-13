# 🤖 AI_GUIDELINES.md — Diretrizes para IA

> **Documentação permanente para qualquer IA que trabalhar neste projeto.**
> Sempre que o usuário solicitar alterações, **este arquivo é a fonte de orientação** de design, código, identidade e regras de trabalho.

---

## Índice

- [🤖 AI\_GUIDELINES.md — Diretrizes para IA](#-ai_guidelinesmd--diretrizes-para-ia)
  - [Índice](#índice)
  - [🎯 Objetivo do projeto](#-objetivo-do-projeto)
  - [🛠️ Stack](#️-stack)
  - [🎨 Identidade visual](#-identidade-visual)
  - [🎨 Paleta](#-paleta)
    - [Verde (design system)](#verde-design-system)
    - [Semânticas (tema claro)](#semânticas-tema-claro)
    - [Semânticas (tema escuro)](#semânticas-tema-escuro)
  - [🔤 Tipografia](#-tipografia)
  - [⚠️ Regra de uso do amarelo](#️-regra-de-uso-do-amarelo)
  - [🧑‍💻 Princípios de UX](#-princípios-de-ux)
  - [♿ Princípios de acessibilidade](#-princípios-de-acessibilidade)
  - [⚡ Princípios de performance](#-princípios-de-performance)
  - [🏗️ Estrutura prevista](#️-estrutura-prevista)
  - [📐 Regras de código](#-regras-de-código)
  - [📦 Dependências permitidas](#-dependências-permitidas)
  - [🚫 Regra: não inventar conteúdo profissional](#-regra-não-inventar-conteúdo-profissional)
  - [🧩 Regra: não criar complexidade sem necessidade](#-regra-não-criar-complexidade-sem-necessidade)

---

## 🎯 Objetivo do projeto

O **KW Controle Financeiro** é um sistema web de gestão financeira pessoal. Seu objetivo é permitir ao usuário:

- Registrar e organizar **transações** (entradas e saídas) e previsões mensais;
- Acompanhar **saldos** por mês (realizado vs. previsto);
- Visualizar **gráficos** (Chart.js) do comparativo mensal;
- Gerenciar membros/responsáveis e conta do próprio usuário.

É um projeto Django (MVT) com foco em simplicidade, usabilidade e clareza visual. **Manter o código simples e legível é prioridade.**

---

## 🛠️ Stack

| Camada | Tecnologia | Observação |
|--------|-----------|------------|
| Backend | Python 3.x / Django 5 | Arquitetura MVT, Server-Side Rendering |
| API | Django REST Framework (DRF) | Endpoint `/api/transacoes/` |
| Banco | SQLite3 (dev) | Preparado para PostgreSQL |
| Frontend | Bootstrap 5.3.3 | Carregado via CDN |
| Ícones | Font Awesome 6 | Via CDN |
| Gráficos | Chart.js | Via CDN |
| Templates | Jinja/Django Templates | Herança via `base.html` |

---

## 🎨 Identidade visual

- Linguagem visual **limpa, leve e confiável**, com predomínio de **verdes**.
- Navbar em **verde escuro** (`--navbar-bg`) com texto branco.
- Cards com bordas arredondadas (`rounded-4`) e sombras suaves.
- Botões principais (ações positivas) em verde; botões destrutivos em vermelho.
- **Tema claro (padrão) e tema escuro** via atributo `data-theme="dark"` no `<html>`, controlados pela função `darkTheme` ([`theme.js`](finance/static/finance/js/theme.js:1)).
- **Toda cor deve vir de CSS custom properties** centralizadas no [`theme.css`](finance/static/finance/css/theme.css:1). Proibido cores hardcoded em templates.

---

## 🎨 Paleta

Todas as cores são definidas como custom properties em [`finance/static/finance/css/theme.css`](finance/static/finance/css/theme.css:1).

### Verde (design system)

| Token | Valor | Uso típico |
|-------|-------|-----------|
| `--verde-50` | `#e8f7ef` | Fundos muito claros |
| `--verde-100` | `#d1fae5` | Subtle (badges) |
| `--verde-200` | `#a7f3d0` | Bordas subtle |
| `--verde-300` | `#6ee7b7` | Hover claro |
| `--verde-400` | `#34d399` | Acento escuro/primary claro |
| `--verde-500` | `#10b981` | Acento |
| `--verde-600` | `#059669` | Botões (tema escuro) |
| `--verde-700` | `#047857` | Primary / botões |
| `--verde-800` | `#065f46` | Hover escuro |
| `--verde-900` | `#064e2e` | Navbar (tema claro) |
| `--verde-950` | `#052e16` | Navbar (tema escuro) |

### Semânticas (tema claro)

| Token | Valor |
|-------|-------|
| `--bg-body` | `#f2f7f4` |
| `--bg-surface` | `#ffffff` |
| `--bg-surface-2` | `#eaf3ee` |
| `--text-body` | `#212529` |
| `--text-muted` | `#67786f` |
| `--border-color` | `#d8e2db` |
| `--primary` | `#047857` |
| `--danger` | `#c0392b` |
| `--warning` | `#f39c12` |
| `--info` | `#2980b9` |
| `--navbar-bg` | `#064e2e` |

### Semânticas (tema escuro)

| Token | Valor |
|-------|-------|
| `--bg-body` | `#06100a` |
| `--bg-surface` | `#0c1c12` |
| `--bg-surface-2` | `#132a1c` |
| `--text-body` | `#e7f3ec` |
| `--text-muted` | `#9db8aa` |
| `--border-color` | `#1d3b2a` |
| `--primary` | `#34d399` |
| `--danger` | `#f87171` |
| `--warning` | `#fbbf24` |
| `--info` | `#38bdf8` |
| `--navbar-bg` | `#04210f` |

---

## 🔤 Tipografia

- Família principal: **`'Segoe UI', sans-serif`** (definida no `body` do [`theme.css`](finance/static/finance/css/theme.css:1)).
- Títulos usam pesos **bold** (`fw-bold`) para hierarquia clara.
- Textos auxiliares/legendas usam as classes de tamanho do Bootstrap (`small`, `x-small`).
- Valores monetários em destaque: `fs-3 fw-bold` (texto grande).
- **Não adicionar novas fontes externas** sem necessidade (performance).

---

## ⚠️ Regra de uso do amarelo

O **amarelo** é reservado exclusivamente para **estado de alerta/pendência**:

- Badge **"Pendente"** (transação não paga): `bg-warning-subtle text-warning-emphasis border border-warning`.
- **Não** usar amarelo como cor primária, de destaque de marca ou em botões principais.
- Verde = positivo/salvável; Vermelho = negativo/destrutivo; **Amarelo = atenção/pendente**.

---

## 🧑‍💻 Princípios de UX

1. **Clareza sobre criatividade** — layout previsível, hierarquia visual evidente.
2. **Feedback imediato** — ações salvam/excluem com mensagens (`messages`) e modais de confirmação para exclusões.
3. **SSR (Server-Side Rendering)** — o backend entrega o HTML processado (saldos, filtros) ao cliente.
4. **Modais dinâmicos** — edição/criação de transações em modais no dashboard.
5. **Navegação consistente** — todas as páginas usam a navbar do `base.html`; páginas standalone mantêm o mesmo padrão visual.
6. **Tema claro/escuro** — o usuário alterna e a preferência é persistida (localStorage).
7. **Menos é mais** — evitar elementos decorativos que não agregam informação.

---

## ♿ Princípios de acessibilidade

1. **Contraste WCAG AA** — texto normal ≥ 4.5:1; texto grande/bold ≥ 3:1, nos dois temas.
2. **Foco visível** — campos de formulário têm borda de foco (`--border-focus`) + anel de foco (`--focus-ring`).
3. **Botões de tema** com `aria-pressed` e `aria-label` (gerenciados pelo `theme.js`).
4. **Texto descritivo em ícones** sempre que não houver rótulo visível (atributo `title`/`aria-label`).
5. **Respeito ao sistema** — sem preferência salva, o tema segue `prefers-color-scheme`.
6. **Linguagem** do documento `pt-BR` e formato de moeda BRL (`pt-BR`).

---

## ⚡ Princípios de performance

1. **Evitar FOUC** — `theme.js` é carregado no `<head>` e aplica o tema antes do primeiro render.
2. **Centralizar estilos** — CSS em [`theme.css`](finance/static/finance/css/theme.css:1); **não duplicar CSS inline por página**.
3. **CDN para bibliotecas** — Bootstrap, Font Awesome e Chart.js via CDN (sem empacotar).
4. **Estáticos via `{% static %}`** — usar `django.contrib.staticfiles` (`finance/static/`).
5. **Charts sob demanda** — o gráfico do dashboard só é criado ao abrir o modal (`shown.bs.modal`), evitando trabalho desnecessário no carregamento.
6. **Evitar consultas N+1** — usar `select_related`/`prefetch_related` quando necessário.
7. **Minimizar reflows** — transições de tema limitadas a `background-color`/`color`/`box-shadow`.

---

## 🏗️ Estrutura prevista

```
FINANCE_CONTROL/
├── core/                       # Kernel (settings, URLs globais, context processors)
├── finance/                    # App principal (models, views, forms, serializers)
│   ├── migrations/
│   ├── static/finance/
│   │   ├── css/theme.css       # Sistema de temas (custom properties)
│   │   └── js/theme.js         # Função darkTheme
│   └── templates/
│       ├── finance/            # Páginas do app
│       └── registration/       # Fluxo de senha
├── assets/                     # Mídias de documentação
├── AI_GUIDELINES.md            # ⭐ Este arquivo (fonte de orientação)
├── workflow.md                 # Workflow operacional do desenvolvedor
├── manage.py
└── requirements.txt
```

**Roadmap do projeto (README):** autenticação Token/JWT, containerização Docker, backend em Java Spring Boot, frontend React Native (integração via DRF).

---

## 📐 Regras de código

1. **Seguir o padrão MVT do Django** — lógica no backend (views), nunca no template.
2. **Usar Django Forms para validação e integridade** (proteção CSRF ativa).
3. **Herança de templates** — páginas estendem [`base.html`](finance/templates/finance/base.html:1); standalone é exceção justificada (dashboard, gráfico).
4. **Cores sempre via custom properties** — proibido hex/rgb hardcoded nos templates.
5. **Nomes de classes consistentes** — Bootstrap + utilitários; classes custom apenas quando necessário.
6. **URLs com `{% url %}`** — nunca hardcodar caminhos.
7. **Código em pt-BR nos templates/textos de UI** (mensagens, labels).
8. **Comentários em código** apenas quando agregam contexto (ex.: intenção de uma regra).
9. **Sempre documentar** mudanças de tema/design no [`theme.css`](finance/static/finance/css/theme.css:1) ou no [`workflow.md`](workflow.md:1) quando relevante.
10. **Testar nos dois temas** antes de considerar uma alteração visual concluída.

---

## 📦 Dependências permitidas

**Backend (requirements.txt):**
- `Django`
- `djangorestframework`
- `django-cors-headers`

**Frontend (via CDN, não empacotadas):**
- Bootstrap 5.3.3 (CSS + JS bundle)
- Font Awesome 6
- Bootstrap Icons
- Chart.js

**Regras de dependências:**
- Adicionar nova biblioteca **apenas** com justificativa clara de necessidade.
- Preferir soluções nativas do Django/Bootstrap ao invés de pacotes extras.
- Não substituir o padrão de temas (custom properties) por frameworks de terceiros.

---

## 🚫 Regra: não inventar conteúdo profissional

1. **Não inventar** nomes de pessoas, e-mails, cargos, empresas, depoimentos, dados de contato ou informações profissionais fictícias.
2. **Não fabricar** números, saldos, métricas de performance ou resultados de negócio.
3. **Não criar** conteúdo que atribua autoria, experiência ou conquistas a terceiros sem base real.
4. O único autor divulgado no projeto é o que consta no [`README.md`](README.md:1) (autor real). Não adicionar outros nomes/atribuições.
5. Dados de exemplo (transações, valores) podem ser usados apenas em **dados de teste/mock** claramente identificados, nunca como conteúdo profissional/real.

---

## 🧩 Regra: não criar complexidade sem necessidade

1. **Princípio YAGNI** — implementar apenas o que foi pedido; não antecipar funcionalidades futuras.
2. **Princípio KISS** — preferir a solução mais simples que funcione; código legível > código "esperto".
3. **Não adicionar** camadas, abstrações, configurações ou arquivos que não sejam necessários para a tarefa atual.
4. **Não duplicar** infraestrutura já existente (ex.: criar um segundo CSS de tema, outra camada de estilo).
5. Ao propor algo mais complexo, **explicar o porquê** e buscar a alternativa mais simples primeiro.
6. Manter o escopo da alteração focado na solicitação do usuário.

---

> 📌 **Lembrete final:** consulte sempre este arquivo antes de propor ou implementar alterações. Em caso de conflito entre este documento e outra instrução, **este documento prevalece** como fonte de orientação do projeto.
