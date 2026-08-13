/* =====================================================================
   KW Controle Financeiro — Alternância de Tema Escuro
   ---------------------------------------------------------------------
   A função `darkTheme` ativa/desativa o tema escuro no elemento raiz
   (<html>) alternando o atributo `data-theme="dark"`.

   - Persiste a preferência do usuário em localStorage (chave 'kw-theme').
   - Sem preferência salva, respeita `prefers-color-scheme` do sistema.
   - Reage a mudanças do sistema enquanto não houver preferência salva.
   - Expõe `darkTheme(force?)` e `toggleDarkTheme()` no escopo global.
   ===================================================================== */
(function () {
  'use strict';

  var STORAGE_KEY = 'kw-theme';
  var root = document.documentElement;

  function getSavedTheme() {
    try {
      var value = localStorage.getItem(STORAGE_KEY);
      return value === 'dark' || value === 'light' ? value : null;
    } catch (err) {
      return null;
    }
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (err) {
      /* Armazenamento indisponível: ignora silenciosamente. */
    }
  }

  function getSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }

  function applyTheme(theme) {
    var isDark = theme === 'dark';
    if (isDark) {
      root.setAttribute('data-theme', 'dark');
    } else {
      root.removeAttribute('data-theme');
    }

    // Sincroniza o botão de alternância, se presente.
    var toggle = document.querySelector('[data-theme-toggle]');
    if (toggle) {
      toggle.setAttribute('aria-pressed', String(isDark));
      toggle.setAttribute('aria-label', isDark ? 'Ativar tema claro' : 'Ativar tema escuro');
      var sun = toggle.querySelector('[data-theme-icon="sun"]');
      var moon = toggle.querySelector('[data-theme-icon="moon"]');
      // Exibe o ícone do próximo tema a ser ativado.
      if (sun) { sun.classList.toggle('d-none', !isDark); }
      if (moon) { moon.classList.toggle('d-none', isDark); }
    }
  }

  /**
   * Ativa ou desativa o tema escuro no elemento raiz.
   *
   * - `darkTheme()` ................. resolve a preferência (salva ou do sistema)
   * - `darkTheme('dark')` ........... força o tema escuro e salva
   * - `darkTheme('light')` .......... força o tema claro e salva
   */
  function darkTheme(force) {
    var theme;
    if (force === 'dark' || force === 'light') {
      theme = force;
      saveTheme(theme);
    } else {
      theme = getSavedTheme() || getSystemTheme();
    }
    applyTheme(theme);
    return theme;
  }

  /** Alterna entre claro e escuro, persistindo a escolha do usuário. */
  function toggleTheme() {
    var current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    var next = current === 'dark' ? 'light' : 'dark';
    saveTheme(next);
    applyTheme(next);
    return next;
  }

  // Aplica o tema antes do primeiro render para evitar "flash" de cor errada.
  darkTheme();

  // Reage a mudanças do sistema apenas enquanto não houver preferência salva.
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function onSystemChange(evt) {
    if (!getSavedTheme()) {
      applyTheme(evt.matches ? 'dark' : 'light');
    }
  }
  if (mq) {
    if (typeof mq.addEventListener === 'function') {
      mq.addEventListener('change', onSystemChange);
    } else if (typeof mq.addListener === 'function') {
      mq.addListener(onSystemChange);
    }
  }

  // Liga o botão de alternância e sincroniza o estado do ícone.
  function bindToggle() {
    var toggle = document.querySelector('[data-theme-toggle]');
    if (toggle) {
      toggle.addEventListener('click', toggleTheme);
    }
    applyTheme(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindToggle);
  } else {
    bindToggle();
  }

  // Expõe a API no escopo global.
  window.darkTheme = darkTheme;
  window.toggleDarkTheme = toggleTheme;
})();
