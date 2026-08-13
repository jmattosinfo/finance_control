# 🛠️ Workflow de Desenvolvimento — KW Controle Financeiro

Este documento auxilia o desenvolvedor a trabalhar de forma consistente com o projeto, com foco no **sistema de temas** (paleta de tons de verde com tema claro/escuro) e nos fluxos padrão do Django.

---

## Índice

- [🛠️ Workflow de Desenvolvimento — KW Controle Financeiro](#️-workflow-de-desenvolvimento--kw-controle-financeiro)
  - [Índice](#índice)
  - [🏗️ Visão geral e estrutura](#️-visão-geral-e-estrutura)
    - [Pontos importantes](#pontos-importantes)
  - [⚙️ Setup do ambiente](#️-setup-do-ambiente)
  - [⌨️ Comandos úteis](#️-comandos-úteis)
  - [🎨 Sistema de temas](#-sistema-de-temas)
    - [Arquivos do sistema](#arquivos-do-sistema)
    - [Como funciona a alternância](#como-funciona-a-alternância)
    - [Como carregar o tema em uma nova página](#como-carregar-o-tema-em-uma-nova-página)
    - [Como adicionar o botão de alternância](#como-adicionar-o-botão-de-alternância)
  - [🧩 Como adicionar novas cores e componentes](#-como-adicionar-novas-cores-e-componentes)
    - [Paleta de verdes (design system)](#paleta-de-verdes-design-system)
    - [Variáveis semânticas (use estas nos componentes)](#variáveis-semânticas-use-estas-nos-componentes)
    - [Regras de ouro para novos componentes](#regras-de-ouro-para-novos-componentes)
  - [🧭 Workflow: criar ou alterar uma página](#-workflow-criar-ou-alterar-uma-página)
  - [🧭 Workflow: adicionar rota, view e formulário](#-workflow-adicionar-rota-view-e-formulário)
  - [✅ Checklist de acessibilidade e contraste](#-checklist-de-acessibilidade-e-contraste)
  - [🔁 Ciclo de desenvolvimento recomendado](#-ciclo-de-desenvolvimento-recomendado)

---

## 🏗️ Visão geral e estrutura

Projeto **Django 5** com **MVT**, **Bootstrap 5.3** (via CDN), **Font Awesome**, **Chart.js** e **Django REST Framework**.

```
FINANCE_CONTROL/
├── core/                       # Kernel do sistema (settings, URLs globais)
│   ├── settings.py             # Configurações (templates, estáticos, apps)
│   ├── urls.py                 # Roteamento global
│   └── context_processors_mes.py
├── finance/                    # App principal (models, views, forms)
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── serializers.py
│   ├── static/
│   │   └── finance/
│   │       ├── css/theme.css   # ⭐ Sistema de temas (CSS custom properties)
│   │       └── js/theme.js     # ⭐ Função darkTheme (alternância do tema)
│   └── templates/
│       ├── finance/            # Páginas do app
│       └── registration/       # Fluxo de senha (estendem base.html)
├── manage.py
└── requirements.txt
```

### Pontos importantes

- **Não há CSS próprio por página.** O tema é centralizado em [`finance/static/finance/css/theme.css`](finance/static/finance/css/theme.css:1) e carregado por **todas** as páginas.
- A maioria das páginas estende [`finance/templates/finance/base.html`](finance/templates/finance/base.html:1) (navbar + tema). Algumas páginas são **standalone**: [`mes_atual.html`](finance/templates/finance/mes_atual.html:1), [`grafico_mes.html`](finance/templates/finance/grafico_mes.html:1), [`sobre.html`](finance/templates/finance/sobre.html:1) e [`teste_context.html`](finance/templates/finance/teste_context.html:1).
- O Bootstrap é carregado via CDN; o tema sobrescreve as variáveis `--bs-*` para manter a consistência visual.

---

## ⚙️ Setup do ambiente

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate      # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar migrações (SQLite)
python manage.py migrate

# 4. Iniciar o servidor
python manage.py runserver 127.0.0.1:8000
```

> ⚠️ **Importante:** após alterar templates ou arquivos estáticos, reinicie o servidor caso ele tenha sido iniciado com `--noreload` (o autoreload não recompila o estado em memória).

---

## ⌨️ Comandos úteis

```bash
# Servidor de desenvolvimento (com autoreload)
python manage.py runserver

# Criar migrações após alterar models.py
python manage.py makemigrations finance
python manage.py migrate

# Testes
python manage.py test

# Coletar estáticos para produção
python manage.py collectstatic --noinput

# Shell interativo (útil para depurar/renderizar templates)
python manage.py shell
```

Exemplo de verificação rápida de renderização de template (independente do servidor):

```python
from django.template.loader import render_to_string
html = render_to_string('finance/login.html')
print('theme.css' in html, 'data-theme-toggle' in html)
```

---

## 🎨 Sistema de temas

O projeto usa **CSS custom properties** para centralizar as cores. Há dois temas:

| Tema | Seletor | Descrição |
|------|---------|-----------|
| Claro (padrão) | `:root` | Superfícies claras, texto escuro, acentos em verde escuro |
| Escuro | `[data-theme="dark"]` | Fundos verdes profundos, texto claro, acentos em verde claro |

### Arquivos do sistema

- [`theme.css`](finance/static/finance/css/theme.css:1) — define a paleta `--verde-*`, as variáveis semânticas (fundo, superfície, texto, borda, hover/ativo) e as sobrescritas do Bootstrap (`--bs-*`) para os dois temas.
- [`theme.js`](finance/static/finance/js/theme.js:1) — implementa a função **`darkTheme`**:

```js
// Resolve a preferência (localStorage ou prefers-color-scheme) e aplica
darkTheme();

// Força e salva o tema
darkTheme('dark');
darkTheme('light');

// Alterna e salva
toggleDarkTheme();
```

### Como funciona a alternância

1. `darkTheme()` é executado **no `<head>`** de todas as páginas, antes do primeiro render (evita "flash" de cor errada).
2. A preferência do usuário fica salva no `localStorage` (chave `kw-theme`).
3. Sem preferência salva, respeita `prefers-color-scheme` do sistema e reage a mudanças do SO.
4. O botão de alternância (`.btn[data-theme-toggle]`) alterna entre os temas e salva a escolha.

### Como carregar o tema em uma nova página

Se a página **estende** [`base.html`](finance/templates/finance/base.html:1), nada precisa ser feito (o tema já é carregado).

Se a página for **standalone**, adicione no `<head>`:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'finance/css/theme.css' %}" />
<script src="{% static 'finance/js/theme.js' %}"></script>
```

### Como adicionar o botão de alternância

Em qualquer página com navbar:

```html
<button type="button" class="btn btn-sm btn-outline-light border-0" data-theme-toggle title="Alternar tema" aria-label="Alternar tema" aria-pressed="false">
  <i class="fa-solid fa-moon" data-theme-icon="moon"></i>
  <i class="fa-solid fa-sun d-none" data-theme-icon="sun"></i>
</button>
```

O `theme.js` sincroniza automaticamente o ícone e o `aria-pressed`.

---

## 🧩 Como adicionar novas cores e componentes

### Paleta de verdes (design system)

```css
:root {
  --verde-50:  #e8f7ef;
  --verde-100: #d1fae5;
  --verde-200: #a7f3d0;
  --verde-300: #6ee7b7;
  --verde-400: #34d399;
  --verde-500: #10b981;
  --verde-600: #059669;
  --verde-700: #047857;
  --verde-800: #065f46;
  --verde-900: #064e2e;
  --verde-950: #052e16;
}
```

### Variáveis semânticas (use estas nos componentes)

| Variável | Tema claro | Tema escuro | Uso |
|----------|-----------|-------------|-----|
| `--bg-body` | `#f2f7f4` | `#06100a` | Fundo da página |
| `--bg-surface` | `#ffffff` | `#0c1c12` | Cards, modais, superfícies |
| `--bg-surface-2` | `#eaf3ee` | `#132a1c` | Headers, destaques |
| `--bg-input` | `#ffffff` | `#09150d` | Campos de formulário |
| `--bg-hover` / `--bg-active` | verde translúcido | verde translúcido | Estados hover/ativo |
| `--text-body` | `#212529` | `#e7f3ec` | Texto principal |
| `--text-secondary` | `#495057` | `#c0d6c9` | Texto secundário |
| `--text-muted` | `#67786f` | `#9db8aa` | Texto suave |
| `--border-color` / `--border-strong` | verde-acinzentado | verde escuro | Bordas |
| `--border-focus` | `#198754` | `#34d399` | Borda de foco |
| `--focus-ring` | verde suave | verde suave | Sombra de foco |
| `--navbar-bg` | `#064e2e` | `#04210f` | Barra de navegação |
| `--shadow-sm/-shadow/-shadow-lg` | suave | escura | Sombras |
| `--primary` / `--primary-hover` / `--primary-active` | verde escuro | verde claro | Acentos |

### Regras de ouro para novos componentes

1. **Nunca** use cores hex hardcoded dentro dos templates. Use as custom properties ou a paleta `--verde-*`.
2. Defina o componente no `theme.css` usando as variáveis semânticas — assim ele funciona em **ambos os temas** automaticamente.
3. Quando uma classe for específica do tema escuro, use o prefixo `[data-theme="dark"]`:

```css
[data-theme="dark"] .meu-componente {
  background-color: var(--bg-surface-2);
  color: var(--text-body);
  border-color: var(--border-color);
}
```

4. Sobrescreva componentes do Bootstrap via variáveis (`--bs-*`) sempre que possível, em vez de regras CSS pontuais.

---

## 🧭 Workflow: criar ou alterar uma página

1. **Defina se a página estende `base.html`** (recomendado) ou é standalone.
   - Estende: `{% extends 'finance/base.html' %}` e use `{% block content %}`.
   - Standalone: `<!DOCTYPE html>` completo + `{% load static %}` + os links do tema (ver seção anterior).
2. **Use os componentes Bootstrap existentes** (`.card`, `.btn`, `.table`, `.modal`, `.form-control`) — eles já são tratados pelo tema.
3. **Não adicione CSS inline** para cores. Se precisar de estilo específico, adicione a regra no `theme.css` usando variáveis semânticas.
4. **Adicione o botão de alternância** na navbar se for uma página standalone.
5. **Teste nos dois temas**: alterne pelo botão (lua/sol) e confira contraste e legibilidade.
6. **Gráficos Chart.js**: use `getAttribute('data-theme')` para ajustar a cor de textos/bordas, como em [`mes_atual.html`](finance/templates/finance/mes_atual.html:248) e [`grafico_mes.html`](finance/templates/finance/grafico_mes.html:57):

```js
const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
const chartText = isDark ? '#c0d6c9' : '#495057';
const chartBorder = isDark ? '#0c1c12' : '#ffffff';
```

---

## 🧭 Workflow: adicionar rota, view e formulário

1. **Model** em [`finance/models.py`](finance/models.py:1) → `python manage.py makemigrations finance` → `migrate`.
2. **Form** em [`finance/forms.py`](finance/forms.py:1) (validações e integridade dos dados).
3. **View** em [`finance/views.py`](finance/views.py:1):
   - Páginas autenticadas usam `@login_required`.
   - Contexto inclui o que o template precisar (saldos, listas, etc.).
4. **Rota** em [`finance/urls.py`](finance/urls.py:1) (ou [`core/urls.py`](core/urls.py:1) para rotas globais).
5. **Template** conforme o workflow anterior.
6. **Teste** os fluxos principais (CRUD, permissões, redirecionamentos).

---

## ✅ Checklist de acessibilidade e contraste

- [ ] Texto principal sobre fundo: razão de contraste **≥ 4.5:1** (AA) para texto normal e **≥ 3:1** para texto grande/bold.
- [ ] Botões sólidos usam verde escuro (`--primary-solid`) com texto branco legível no tema escuro.
- [ ] Texto de destaque (`text-success`, `text-danger`, `text-info`) usa tons claros no tema escuro.
- [ ] Campos de formulário têm borda de foco visível (`--border-focus` + `--focus-ring`).
- [ ] Botão de tema tem `aria-pressed` e `aria-label` (já gerenciados pelo `theme.js`).
- [ ] Nenhuma cor hardcoded dentro dos templates — tudo via custom properties.
- [ ] Testado nos dois temas (claro e escuro) e em modo de alto contraste quando aplicável.

---

## 🔁 Ciclo de desenvolvimento recomendado

```text
1. Identificar a tarefa (nova feature / correção / ajuste de tema)
2. Alterar model → form → view → url → template
3. Atualizar theme.css apenas quando houver mudança visual
4. Rodar migrate / test
5. Reiniciar o servidor (se --noreload)
6. Validar nos dois temas e em diferentes resoluções
```
