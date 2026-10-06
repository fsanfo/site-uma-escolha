// Configure aqui os canais reais da fundação.
const CONFIG = {
  email: "contato@umaescolha.org", // TODO: substituir pelo e-mail oficial
  instagram: "https://www.instagram.com/", // TODO: colocar o perfil da fundação
};

// Menu mobile
const burger = document.getElementById("burger");
const nav = document.getElementById("nav");
const setMenu = (open) => {
  nav.classList.toggle("open", open);
  burger.setAttribute("aria-expanded", String(open));
  burger.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
};
burger.addEventListener("click", () => setMenu(!nav.classList.contains("open")));
nav.addEventListener("click", (e) => { if (e.target.closest("a")) setMenu(false); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

// Links externos e ano
document.querySelectorAll("[data-instagram]").forEach((a) => {
  a.href = CONFIG.instagram;
  a.target = "_blank";
  a.rel = "noopener";
});
document.getElementById("ano").textContent = new Date().getFullYear();

// Atalho "Propor parceria" pré-seleciona o tipo no formulário
document.querySelectorAll("[data-tipo]").forEach((a) => {
  a.addEventListener("click", () => {
    const r = document.querySelector('input[name="tipo"][value="Propor parceria"]');
    if (r) r.checked = true;
  });
});

// Formulário: abre o e-mail do usuário com a mensagem preenchida
const form = document.getElementById("form");
const erro = document.getElementById("erro");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const d = new FormData(form);
  const nome = (d.get("nome") || "").trim();
  const contato = (d.get("contato") || "").trim();
  if (!nome || !contato) {
    erro.hidden = false;
    (nome ? form.contato : form.nome).focus();
    return;
  }
  erro.hidden = true;
  const corpo = [
    `Interesse: ${d.get("tipo")}`,
    `Nome: ${nome}`,
    `Contato: ${contato}`,
    d.get("org") ? `Organização: ${d.get("org").trim()}` : "",
    "",
    (d.get("msg") || "").trim(),
  ].filter((l, i) => l || i > 3).join("\n");
  const url = `mailto:${CONFIG.email}?subject=${encodeURIComponent("Site: " + d.get("tipo"))}&body=${encodeURIComponent(corpo)}`;
  form.innerHTML = `<div class="form__ok" role="status"><h3>Quase lá, ${nome.split(" ")[0]}.</h3><p>Abrimos o seu aplicativo de e-mail com a mensagem pronta. Basta enviar. Se nada abriu, escreva para ${CONFIG.email}.</p></div>`;
  window.location.href = url;
});
