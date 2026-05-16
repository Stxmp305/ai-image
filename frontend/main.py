"""
Universal AI Image Upscaler — FastAPI Backend
Deployable to Render, Railway, Fly.io, or any container host.

Local run:
    uvicorn main:app --reload --port 8000

Render start command:
    uvicorn main:app --host 0.0.0.0 --port $PORT
"""
import io
import os
import logging

import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MAX_INPUT_DIM = int(os.getenv("MAX_INPUT_DIM", "2048"))   # downscale very large inputs first
MAX_OUTPUT_DIM = int(os.getenv("MAX_OUTPUT_DIM", "8192")) # safety cap on output
ALLOWED_SCALES = {2, 3, 4}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upscaler")

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Universal AI Image Upscaler",
    description="A FastAPI service that upscales images. Currently uses cv2.INTER_CUBIC as a placeholder for AI upscaling.",
    version="1.0.0",
)

# CORS — allow any origin so the PWA frontend (on Vercel, etc.) can call this API.
# Tighten this to your real frontend domain(s) when going to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Output-Width", "X-Output-Height"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Universal AI Image Upscaler",
        "version": "1.0.0",
        "endpoints": {
            "POST /enhance": "Multipart upload (field: file). Optional ?scale=2|3|4 (default 4).",
            "GET /health": "Health check.",
        },
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/enhance")
async def enhance(
    file: UploadFile = File(...),
    scale: int = Query(4, ge=2, le=4, description="Upscale factor (2, 3, or 4)"),
):
    """
    Receive an image, upscale it by `scale`x using cv2.INTER_CUBIC,
    and return the PNG result as a streamed response.

    NOTE: This is a placeholder. Swap `cv2.resize(..., INTER_CUBIC)` below
    for a real AI super-resolution model (Real-ESRGAN, SwinIR, etc.) when ready.
    """
    if scale not in ALLOWED_SCALES:
        raise HTTPException(status_code=400, detail=f"scale must be one of {sorted(ALLOWED_SCALES)}")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (image/*).")

    # Read bytes
    try:
        contents = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read upload: {e}")

    if not contents:
        raise HTTPException(status_code=400, detail="Empty upload.")

    # Decode
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Could not decode image. Is it a valid JPEG/PNG?")

    h, w = img.shape[:2]
    logger.info("Received image %dx%d, scale=%d", w, h, scale)

    # Pre-shrink very large inputs to keep memory + latency reasonable
    if max(h, w) > MAX_INPUT_DIM:
        ratio = MAX_INPUT_DIM / max(h, w)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        h, w = img.shape[:2]
        logger.info("Pre-shrunk input to %dx%d", w, h)

    # Compute target size
    out_w, out_h = w * scale, h * scale

    # Cap output to a safe ceiling
    if max(out_w, out_h) > MAX_OUTPUT_DIM:
        cap = MAX_OUTPUT_DIM / max(out_w, out_h)
        out_w, out_h = max(1, int(out_w * cap)), max(1, int(out_h * cap))
        logger.info("Capped output to %dx%d", out_w, out_h)

    # === Placeholder for real AI upscaler ===================================
    # Replace this single line with a call into Real-ESRGAN / SwinIR / etc.
    upscaled = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
    # =======================================================================

    # Encode as PNG (lossless). Use JPEG if you want smaller payloads.
    ok, buf = cv2.imencode(".png", upscaled, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to encode result image.")

    return StreamingResponse(
        io.BytesIO(buf.tobytes()),
        media_type="image/png",
        headers={
            "Content-Disposition": 'inline; filename="enhanced.png"',
            "X-Output-Width": str(out_w),
            "X-Output-Height": str(out_h),
            "Cache-Control": "no-store",
        },
    )


# Friendly 413 / general error JSON
@app.exception_handler(HTTPException)
async def http_exc_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
