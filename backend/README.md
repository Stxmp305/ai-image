# Universal AI Image Upscaler

A mobile-first **Progressive Web App** that upscales images by 4×. Drop-in installable on Android & iOS, with a touch-friendly before/after slider.

```
mobile_image_enhancer/
├── backend/            FastAPI service (deploy to Render / Railway / Fly.io)
│   ├── main.py
│   └── requirements.txt
└── frontend/           Static PWA (deploy to Vercel / Netlify / Cloudflare Pages)
    ├── index.html
    ├── app.js
    ├── service-worker.js
    ├── manifest.json
    ├── icon.svg
    └── icon-maskable.svg
```

The backend currently uses `cv2.resize(..., INTER_CUBIC)` as a placeholder for AI upscaling. Swap it for Real-ESRGAN / SwinIR / your model of choice — the single line is flagged with a comment in `main.py`.

---

## 1. Run locally

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Test it: `curl http://localhost:8000/health` → `{"status":"healthy"}`

### Frontend

The frontend is fully static. Serve it with anything that speaks HTTP. The simplest:

```bash
cd frontend
python -m http.server 5173
```

Open <http://localhost:5173> on your laptop, or on your phone (same Wi-Fi) at `http://<your-laptop-ip>:5173`.

> **Service workers and PWA install require HTTPS** (or `localhost`). For phone testing over LAN, use a tunnel like `ngrok http 5173` or `cloudflared tunnel`.

`app.js` defaults to `API_BASE_URL = "http://localhost:8000"`. Leave it for local dev.

---

## 2. Deploy the backend to Render

1. Push this repo to GitHub.
2. On <https://render.com> → **New** → **Web Service** → connect the repo.
3. Settings:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy. You'll get a URL like `https://upscale-api.onrender.com`.
5. Smoke test: visit `https://upscale-api.onrender.com/health` in a browser.

> Render's free tier sleeps after inactivity — the first request may take ~30s to wake up.

---

## 3. Deploy the frontend to Vercel

1. Edit **`frontend/app.js`** and set:
   ```js
   const API_BASE_URL = "https://upscale-api.onrender.com"; // your Render URL
   ```
2. Commit & push.
3. On <https://vercel.com> → **Add New Project** → import the repo.
4. Settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Other (it's static)
   - No build command needed; the output is the directory itself.
5. Deploy. Vercel gives you `https://your-project.vercel.app`.

Open it on your phone → tap the browser's "Add to Home Screen" / "Install" → you've got a native-feeling app icon. Chrome on Android will also show the in-app **Install** button in the header.

---

## 4. Replacing the placeholder upscaler with a real model

Open `backend/main.py` and look for:

```python
# === Placeholder for real AI upscaler =====================
upscaled = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
# ==========================================================
```

Replace that single line with a call into Real-ESRGAN, SwinIR, BSRGAN, or any other super-resolution model. The surrounding code already handles input limits, output capping, encoding, and CORS — you only need to swap the algorithm.

If your model is heavy (a GPU model), consider running it on Replicate / Modal / Runpod and calling that from this endpoint, instead of doing inference inside the Render service itself.

---

## 5. Tweaks you might want

- **Tighter CORS**: in `main.py`, replace `allow_origins=["*"]` with `["https://your-project.vercel.app"]`.
- **Smaller payloads**: change PNG encoding to JPEG (`.jpg`, with `cv2.IMWRITE_JPEG_QUALITY = 92`) for ~5× smaller output.
- **Higher input cap**: bump `MAX_INPUT_DIM` env var on Render (memory permitting).
- **Custom icon**: replace `icon.svg` / `icon-maskable.svg`. For best iOS rendering, also generate PNGs at 180, 192, 512 px and add them to `manifest.json`.
