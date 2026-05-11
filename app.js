let palettesData = {};

async function init() {
  const palettesRes = await fetch("/api/generate");
  let palettesInfo = {};
  try { palettesInfo = await palettesRes.json(); } catch(e) { console.error(e) }
  if (palettesInfo.palettes) {
    palettesData = palettesInfo.palettes;
    const sel = document.getElementById("palette");
    Object.keys(palettesData).forEach((name) => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name.charAt(0).toUpperCase() + name.slice(1);
      sel.appendChild(opt);
    });
    updatePalettePreview();
  }
}

function updatePalettePreview() {
  const sel = document.getElementById("palette");
  const colors = palettesData[sel.value] || [];
  const preview = document.getElementById("palette-preview");
  preview.innerHTML = colors
    .map((c) => `<span class="swatch" style="background:${c}"></span>`)
    .join("");
}

document.addEventListener("DOMContentLoaded", () => {
  init();
  document.getElementById("palette").addEventListener("change", updatePalettePreview);
});

async function generate() {
  const btn = document.getElementById("generate-btn");
  const loading = document.getElementById("loading");
  const preview = document.getElementById("preview");
  const placeholder = document.getElementById("placeholder");
  const downloadBtn = document.getElementById("download-btn");
  const resultActions = document.getElementById("result-actions");

  btn.disabled = true;
  loading.classList.remove("hidden");
  placeholder.classList.add("hidden");
  preview.classList.add("hidden");
  resultActions.classList.add("hidden");

  const template = document.getElementById("template").value;
  const palette = document.getElementById("palette").value;
  const title = document.getElementById("title").value;
  const subtitle = document.getElementById("subtitle").value;
  const body = document.getElementById("body").value;
  const author = document.getElementById("author").value;
  const cta = document.getElementById("cta").value;

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mode: "fill",
        template,
        palette,
        platform: template,
        title,
        subtitle,
        body,
        author,
        cta,
      }),
    });
    const data = await res.json();
    if (!data.image) throw new Error(data.error || "Generation failed");
    preview.src = "data:image/png;base64," + data.image;
    preview.classList.remove("hidden");
    downloadBtn.href = preview.src;
    downloadBtn.download = `${template}-${Date.now()}.png`;
    resultActions.classList.remove("hidden");
  } catch (err) {
    placeholder.classList.remove("hidden");
    placeholder.querySelector("span").textContent = "Error: " + err.message;
  } finally {
    btn.disabled = false;
    loading.classList.add("hidden");
  }
}
