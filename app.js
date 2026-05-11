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
  document.getElementById("mode").addEventListener("change", (e) => {
    const isTxt = e.target.value === "txt";
    document.getElementById("title").placeholder = isTxt ? "Describe your design..." : "Main headline...";
  });
});

async function generate() {
  const btn = document.getElementById("generate-btn");
  const loading = document.getElementById("loading");
  const preview = document.getElementById("preview");
  const placeholder = document.getElementById("placeholder");
  const downloadBtn = document.getElementById("download-btn");

  btn.disabled = true;
  loading.classList.remove("hidden");
  placeholder.classList.add("hidden");
  preview.classList.add("hidden");
  downloadBtn.classList.add("hidden");

  const mode = document.getElementById("mode").value;
  const template = document.getElementById("template").value;
  const palette = document.getElementById("palette").value;
  const platform = document.getElementById("platform").value;
  const title = document.getElementById("title").value;
  const subtitle = document.getElementById("subtitle").value;

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode, template, palette, platform, title, subtitle }),
    });
    const data = await res.json();
    preview.src = "data:image/png;base64," + data.image;
    preview.classList.remove("hidden");
    downloadBtn.href = preview.src;
    downloadBtn.classList.remove("hidden");
  } catch (err) {
    placeholder.textContent = "Error: " + err.message;
    placeholder.classList.remove("hidden");
  } finally {
    btn.disabled = false;
    loading.classList.add("hidden");
  }
}
