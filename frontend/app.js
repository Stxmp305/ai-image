/* =========================================================================
 * Universal AI Image Upscaler — Frontend Logic
 *
 *   IMPORTANT: After deploying the backend to Render (or any host), set
 *   API_BASE_URL below to your backend URL. Example:
 *       const API_BASE_URL = "https://upscale-api.onrender.com";
 *
 *   For local development with `uvicorn main:app --reload --port 8000`,
 *   leave it as "http://localhost:8000".
 * ========================================================================= */
const API_BASE_URL = "http://localhost:8000";

// Enhancement settings (user-adjustable on the crop screen)
let selectedScale = 4;        // 2 | 4 | 8 | 16
let selectedSharpen = 0.8;    // 0.0 .. 2.0 (strength)
let sharpenEnabled = true;    // master on/off for sharpening

// ---------------------------------------------------------------------------
// DOM
// ---------------------------------------------------------------------------
const $ = (id) => document.getElementById(id);

const screens = {
  idle:    $("screenIdle"),
  crop:    $("screenCrop"),
  loading: $("screenLoading"),
  result:  $("screenResult"),
};

const uploadBtn    = $("uploadBtn");
const fileInput    = $("fileInput");
const cropperImage = $("cropperImage");
const cropCancelBtn= $("cropCancelBtn");
const enhanceBtn   = $("enhanceBtn");
const rotateBtn    = $("rotateBtn");
const resetBtn     = $("resetBtn");
const enhanceLabel = $("enhanceLabel");
const scaleHint    = $("scaleHint");
const sharpenSlider= $("sharpenSlider");
const sharpenVal   = $("sharpenVal");
const sharpenToggle= $("sharpenToggle");
const sharpenCtrls = $("sharpenControls");
const baAfterLabel = $("baAfterLabel");
const saveBtn      = $("saveBtn");
const shareBtn     = $("shareBtn");
const restartBtn   = $("restartBtn");
const installBtn   = $("installBtn");
const toastEl      = $("toast");
const dimsLabel    = $("dimsLabel");

// Before/After slider DOM
const baSlider = $("baSlider");
const baAfter  = $("baAfter");
const baHandle = $("baHandle");
const origImg  = $("origImg");
const enhImg   = $("enhImg");

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
let cropper = null;
let originalDataUrl = null;       // pre-upscale (after crop)
let enhancedBlobUrl = null;       // upscaled result
let enhancedBlob    = null;
let deferredInstallPrompt = null;

// ---------------------------------------------------------------------------
// Screen switching
// ---------------------------------------------------------------------------
function showScreen(name) {
  Object.values(screens).forEach(s => s.classList.remove("active"));
  screens[name].classList.add("active");
  window.scrollTo(0, 0);
}

// ---------------------------------------------------------------------------
// Toast
// ---------------------------------------------------------------------------
let toastTimer = null;
function toast(message, isError = false) {
  toastEl.textContent = message;
  toastEl.classList.toggle("error", !!isError);
  toastEl.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove("show"), 2600);
}

// ---------------------------------------------------------------------------
// Step 1 — Upload
// ---------------------------------------------------------------------------
uploadBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
  const file = e.target.files?.[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    toast("That doesn't look like an image.", true);
    return;
  }
  if (file.size > 15 * 1024 * 1024) {
    toast("Image too large (max 15MB).", true);
    return;
  }

  const reader = new FileReader();
  reader.onload = (ev) => {
    initCropper(ev.target.result);
  };
  reader.onerror = () => toast("Could not read that file.", true);
  reader.readAsDataURL(file);

  // Allow re-selecting the same file later
  fileInput.value = "";
});

// ---------------------------------------------------------------------------
// Step 2 — Crop
// ---------------------------------------------------------------------------
function initCropper(dataUrl) {
  cropperImage.src = dataUrl;
  showScreen("crop");
  setScale(selectedScale);                 // reflect current scale in the UI
  sharpenToggle.checked = sharpenEnabled;
  sharpenSlider.value = selectedSharpen;
  sharpenVal.textContent = selectedSharpen.toFixed(2);
  applySharpenEnabled();

  // Destroy any previous instance
  if (cropper) { cropper.destroy(); cropper = null; }

  // Cropper.js may not have loaded yet (defer); wait if needed
  const start = () => {
    cropper = new Cropper(cropperImage, {
      viewMode: 1,
      dragMode: "move",
      autoCropArea: 0.9,
      background: false,
      responsive: true,
      restore: false,
      guides: true,
      center: true,
      highlight: false,
      cropBoxResizable: true,
      cropBoxMovable: true,
      toggleDragModeOnDblclick: false,
      // Free aspect ratio by default
      aspectRatio: NaN,
    });
  };
  if (typeof Cropper !== "undefined") start();
  else window.addEventListener("load", start, { once: true });
}

// Aspect ratio chips
document.querySelectorAll(".ratio-chip").forEach(chip => {
  chip.addEventListener("click", () => {
    if (!cropper) return;
    const v = parseFloat(chip.dataset.ratio);
    cropper.setAspectRatio(v && v > 0 ? v : NaN);
    document.querySelectorAll(".ratio-chip").forEach(c => {
      c.style.borderColor = "";
      c.style.color = "";
    });
    chip.style.borderColor = "var(--accent)";
    chip.style.color = "var(--accent)";
  });
});

rotateBtn.addEventListener("click", () => cropper?.rotate(90));
resetBtn.addEventListener("click",  () => cropper?.reset());

// --- Scale selector ---
function setScale(scale) {
  selectedScale = scale;
  document.querySelectorAll(".scale-chip").forEach(c => {
    const active = parseInt(c.dataset.scale, 10) === scale;
    c.style.background    = active ? "var(--accent)" : "";
    c.style.color         = active ? "#0a0a0b" : "";
    c.style.borderColor   = active ? "var(--accent)" : "";
  });
  enhanceLabel.textContent = `Enhance ${scale}×`;
  // Honest hint about what high scales do
  const hints = {
    2:  "Crisp · safe",
    4:  "Recommended",
    8:  "Large · slight softening",
    16: "Extreme · slow & blurry",
  };
  scaleHint.textContent = hints[scale] || "";
}

document.querySelectorAll(".scale-chip").forEach(chip => {
  chip.addEventListener("click", () => setScale(parseInt(chip.dataset.scale, 10)));
});

// --- Sharpen on/off toggle ---
function applySharpenEnabled() {
  sharpenCtrls.classList.toggle("disabled", !sharpenEnabled);
  sharpenSlider.disabled = !sharpenEnabled;
}

sharpenToggle.addEventListener("change", () => {
  sharpenEnabled = sharpenToggle.checked;
  applySharpenEnabled();
});

// --- Sharpen strength slider ---
sharpenSlider.addEventListener("input", () => {
  selectedSharpen = parseFloat(sharpenSlider.value);
  sharpenVal.textContent = selectedSharpen.toFixed(2);
});

cropCancelBtn.addEventListener("click", () => {
  cropper?.destroy(); cropper = null;
  showScreen("idle");
});

// ---------------------------------------------------------------------------
// Step 3 — Enhance (call backend)
// ---------------------------------------------------------------------------
enhanceBtn.addEventListener("click", async () => {
  if (!cropper) return;

  // Get cropped image as a blob
  const canvas = cropper.getCroppedCanvas({
    maxWidth: 2048,
    maxHeight: 2048,
    imageSmoothingEnabled: true,
    imageSmoothingQuality: "high",
  });
  if (!canvas) {
    toast("Could not crop that image.", true);
    return;
  }

  // Keep the pre-upscale version for the "before" comparison
  originalDataUrl = canvas.toDataURL("image/png");

  showScreen("loading");

  const blob = await new Promise(res => canvas.toBlob(res, "image/png", 0.95));
  if (!blob) {
    toast("Could not encode image.", true);
    showScreen("crop");
    return;
  }

  const form = new FormData();
  form.append("file", blob, "input.png");

  try {
    // When the sharpen toggle is off, send 0 so the backend skips it entirely.
    const sharpenParam = sharpenEnabled ? selectedSharpen : 0;
    const res = await fetch(`https://ai-image-e6li.onrender.com/enhance?scale=${selectedScale}&sharpen=${sharpenParam}`,
      { method: "POST", body: form }
    );

    if (!res.ok) {
      let msg = `Server error (${res.status})`;
      try { const j = await res.json(); if (j?.error) msg = j.error; } catch (_) {}
      throw new Error(msg);
    }

    const outW = res.headers.get("X-Output-Width");
    const outH = res.headers.get("X-Output-Height");
    const appliedScale = res.headers.get("X-Applied-Scale");
    const wasCapped = res.headers.get("X-Capped") === "1";
    enhancedBlob = await res.blob();

    if (enhancedBlobUrl) URL.revokeObjectURL(enhancedBlobUrl);
    enhancedBlobUrl = URL.createObjectURL(enhancedBlob);

    showResult(originalDataUrl, enhancedBlobUrl, outW, outH, appliedScale);

    if (wasCapped) {
      toast(`Output capped to server max — applied ${appliedScale}× instead of ${selectedScale}×.`);
    }
  } catch (err) {
    console.error(err);
    const isNetwork = err instanceof TypeError;
    toast(
      isNetwork
        ? "Cannot reach the backend. Check API_BASE_URL in app.js."
        : err.message || "Something went wrong.",
      true
    );
    showScreen("crop");
  }
});

// ---------------------------------------------------------------------------
// Step 4 — Result + Before/After slider
// ---------------------------------------------------------------------------
function showResult(beforeUrl, afterUrl, outW, outH, appliedScale) {
  origImg.src = beforeUrl;
  enhImg.src  = afterUrl;

  dimsLabel.textContent = (outW && outH) ? `${outW} × ${outH}` : "";

  // Show the scale actually applied (may differ from requested if capped)
  const shown = appliedScale ? parseFloat(appliedScale) : selectedScale;
  baAfterLabel.textContent = `AFTER · ${Number.isInteger(shown) ? shown : shown.toFixed(1)}×`;

  // Cleanup cropper
  cropper?.destroy(); cropper = null;

  showScreen("result");

  // Wait for layout to settle, then size the inner clip container
  requestAnimationFrame(() => {
    updateBaWidth();
    setHandle(0.5);
  });
}

function updateBaWidth() {
  if (!baSlider) return;
  const w = baSlider.getBoundingClientRect().width;
  baSlider.style.setProperty("--ba-w", w + "px");
}

window.addEventListener("resize", updateBaWidth);

function setHandle(pct) {
  pct = Math.max(0, Math.min(1, pct));
  const x = pct * 100;
  baAfter.style.width = `${x}%`;
  baHandle.style.left = `${x}%`;
}

// Pointer-event-based drag (works for touch, mouse, pen)
(function attachSliderDrag() {
  let dragging = false;

  function pctFromEvent(e) {
    const r = baSlider.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    return x;
  }

  baSlider.addEventListener("pointerdown", (e) => {
    dragging = true;
    baSlider.setPointerCapture(e.pointerId);
    setHandle(pctFromEvent(e));
  });
  baSlider.addEventListener("pointermove", (e) => {
    if (!dragging) return;
    setHandle(pctFromEvent(e));
  });
  baSlider.addEventListener("pointerup",     () => dragging = false);
  baSlider.addEventListener("pointercancel", () => dragging = false);

  // Keyboard accessibility
  baSlider.tabIndex = 0;
  baSlider.addEventListener("keydown", (e) => {
    const step = e.shiftKey ? 0.1 : 0.02;
    const current = parseFloat(baAfter.style.width) / 100 || 0.5;
    if (e.key === "ArrowLeft")  { e.preventDefault(); setHandle(current - step); }
    if (e.key === "ArrowRight") { e.preventDefault(); setHandle(current + step); }
  });
})();

// ---------------------------------------------------------------------------
// Save to gallery
// ---------------------------------------------------------------------------
saveBtn.addEventListener("click", () => {
  if (!enhancedBlobUrl) return;
  const a = document.createElement("a");
  a.href = enhancedBlobUrl;
  a.download = `upscale-${Date.now()}.png`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  toast("Saved to your downloads / gallery.");
});

// ---------------------------------------------------------------------------
// Share (Web Share API if available — works great on mobile)
// ---------------------------------------------------------------------------
shareBtn.addEventListener("click", async () => {
  if (!enhancedBlob) return;

  const file = new File([enhancedBlob], `upscale-${Date.now()}.png`, { type: "image/png" });

  if (navigator.canShare && navigator.canShare({ files: [file] })) {
    try {
      await navigator.share({
        files: [file],
        title: "Upscaled image",
        text: "Enhanced with Upscale 4× AI",
      });
    } catch (err) {
      if (err.name !== "AbortError") toast("Could not open share sheet.", true);
    }
  } else if (navigator.clipboard && window.ClipboardItem) {
    try {
      await navigator.clipboard.write([new ClipboardItem({ "image/png": enhancedBlob })]);
      toast("Copied to clipboard.");
    } catch {
      toast("Sharing isn't supported on this browser.", true);
    }
  } else {
    toast("Sharing isn't supported on this browser.", true);
  }
});

// ---------------------------------------------------------------------------
// Restart
// ---------------------------------------------------------------------------
restartBtn.addEventListener("click", () => {
  if (enhancedBlobUrl) { URL.revokeObjectURL(enhancedBlobUrl); enhancedBlobUrl = null; enhancedBlob = null; }
  originalDataUrl = null;
  showScreen("idle");
});

// ---------------------------------------------------------------------------
// PWA: install prompt + service worker
// ---------------------------------------------------------------------------
window.addEventListener("beforeinstallprompt", (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  installBtn.classList.remove("hidden");
});

installBtn.addEventListener("click", async () => {
  if (!deferredInstallPrompt) return;
  deferredInstallPrompt.prompt();
  const choice = await deferredInstallPrompt.userChoice;
  if (choice.outcome === "accepted") installBtn.classList.add("hidden");
  deferredInstallPrompt = null;
});

window.addEventListener("appinstalled", () => {
  installBtn.classList.add("hidden");
  toast("Installed. Find Upscale on your home screen.");
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").catch((err) => {
      console.warn("Service worker registration failed:", err);
    });
  });
}
