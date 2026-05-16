
AI Image Upscaler & Detail Enhancer(เว็บแอปพลิเคชันเพิ่มความละเอียดและรายละเอียดรูปภาพด้วย AI)
/
Claude finished the response
Act as an Expert Full-Stack Developer. I am building a "Universal AI Image Upscaler" application. 
CRITICAL REQUIREMENT: I want this to act as a Mobile App that can be installed on a phone. Therefore, you MUST build the frontend as a Progressive Web App (PWA) with a Mobile-First UI design.
Please generate the complete, ready-to-run code. I want to write zero code manually, so provide everything completely.
### Tech Stack:
- Backend: FastAPI (Python) - Designed to be deployed on a cloud service (e.g., Render).
- Frontend: HTML5, CSS, Vanilla JavaScript. Must include a manifest.json and a basic service-worker.js to make it an installable PWA.
- UI Framework: Use Tailwind CSS (via CDN) for rapid, modern, mobile-responsive styling. Include Cropper.js for image cropping.
### Key Features Required:
1. **PWA Setup:** Include manifest.json (with app name, icons setup placeholder, display: standalone) and a basic service-worker.js for caching so the user gets an "Install App" prompt on mobile.
2. **Mobile-First UI:** The interface should look and feel like a native mobile app. Use large, touch-friendly buttons, bottom navigation or clean floating action buttons, and a responsive layout.
3. **Upload & Crop:** A button to select an image from the phone's gallery. Once selected, open a mobile-friendly Cropper.js view.
4. **Processing (Backend):** 
   - A FastAPI endpoint /enhance that receives the cropped image.
   - For now, use cv2.resize (OpenCV) with INTER_CUBIC as a placeholder to simulate a 4x AI upscale. Ensure the backend handles CORS properly so the frontend can call it from a different domain.
5. **Result Viewer:** An interactive "Before & After" slider optimized for touch screens.
6. **Export:** A prominent "Save to Gallery" button (downloads the result image).
### Project Structure:
/mobile_image_enhancer
├── /backend
│   ├── main.py (FastAPI with CORS enabled)
│   ├── requirements.txt
├── /frontend
│   ├── index.html (Mobile-first UI)
│   ├── manifest.json (PWA configuration)
│   ├── service-worker.js (PWA service worker)
│   ├── app.js (Logic for UI, camera/gallery upload, cropping, and API call)
Please provide the exact code for ALL files. Keep the logic modular but simple enough that I can just deploy the frontend to Vercel and the backend to Render without changing much code.
Show more
00:50

Architecting refined dark theme with vibrant accent aesthetics
Architecting refined dark theme with vibrant accent aesthetics
I'll build this complete PWA image upscaler project for you. Let me first check the design guidelines, then create all the files.

Architecting polished mobile interface with dark electric lime aesthetic
Architecting polished mobile interface with dark electric lime aesthetic
I have a clear picture now. I'll build this as a sleek dark-mode imaging app with a distinctive aesthetic — premium-feeling like Halide or Darkroom, with a custom-built touch-friendly before/after slider. Let me create all the files.

Architecting JavaScript functionality for image processing workflow
Architecting JavaScript functionality for image processing workflow
Now the main UI — I'll write the HTML with the design system inline, then the JS logic separately.

Crafting deployment documentation and verifying code consistency
Crafting deployment documentation and verifying code consistency
I need to fix the before/after slider CSS — the inset: 0 was conflicting with width. Let me correct that:

Fix the before/after slider CSS so the inner div stays at the container's pixel width
Fix the before/after slider CSS so the inner div stays at the container's pixel width
Now the application logic:

Verified code consistency and architected comprehensive deployment documentation
Verified code consistency and architected comprehensive deployment documentation
Now a deployment README so they can ship this without questions:

Orchestrated comprehensive file inventory and quality assurance verification
Orchestrated comprehensive file inventory and quality assurance verification
Let me verify everything is in place:

Viewed a file, read a file
Viewed a file, read a file
All nine files are ready. Here's the quick map of what you got and the only line you need to touch before deploying:
Backend (backend/) — FastAPI service with CORS open to any origin, a POST /enhance?scale=4 endpoint that returns a PNG stream, safe input/output size caps, and a clearly-marked single line where you'd swap cv2.INTER_CUBIC for Real-ESRGAN or similar.
Frontend (frontend/) — Installable PWA with four screens (idle → crop → processing → result). Custom-built touch-friendly before/after slider using pointer events, Cropper.js with aspect-ratio chips, save-to-gallery via download, native share sheet via Web Share API on mobile. Dark theme with Bricolage Grotesque + Geist + JetBrains Mono typography, electric-lime accent, subtle film grain. Standalone display mode, service worker with stale-while-revalidate caching, and a header Install button that appears when Chrome offers the install prompt.
The one change you need to make before deploying: open frontend/app.js line 13 and replace "http://localhost:8000" with your Render URL. That's it.
Deployment, in order:
backend/ → Render as a Web Service, root directory backend, start command uvicorn main:app --host 0.0.0.0 --port $PORT.
Copy the Render URL into frontend/app.js.
frontend/ → Vercel as a static project, root directory frontend, no build command.
Open the Vercel URL on your phone → "Add to Home Screen" → it launches like a native app.
Full step-by-step (including the model-swap pointer and CORS tightening for production) is in the README.

Readme
Document · MD 

Main
PY 

Requirements
TXT 

Index
Code · HTML 

App
JS 

Manifest
Code · JSON 

Service worker
JS 

Icon
Image · SVG 

Icon maskable
Image · SVG 
ก่อนจะไปถึงขั้น Dead Point อ่ะให้ฉันลองเทสต์ฟังก์ชันก่อนได้ไหมว่ามันใช้งานได้จริงหรือเปล่า
01:39
ได้แน่นอนครับ มาเทสต์ก่อนค่อยไป deploy นั่นแหละแนวทางที่ถูก จะได้รู้ว่าใช้งานได้จริงทั้ง flow ก่อนเสียเวลา push ขึ้น cloud
วิธีเทสต์บนเครื่องตัวเอง ทำตามนี้เลย:
1. เปิด Backend ก่อน (terminal หน้าแรก)
bash
cd mobile_image_enhancer/backend
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
เช็คว่าทำงาน: เปิด browser ไปที่ http://localhost:8000/health ต้องเห็น {"status":"healthy"}
2. เปิด Frontend (terminal อีกหน้านึง อย่าปิดอันแรก)
bash
cd mobile_image_enhancer/frontend
python -m http.server 5173
แล้วเปิด http://localhost:5173 ใน Chrome หรือ Safari บนคอม ลองเทสต์ flow: เลือกรูป → crop → กด Enhance 4× → ดู before/after slider → กด Save
3. ถ้าอยากเทสต์บนมือถือจริงๆ ด้วย (อันนี้สำคัญเพราะเป็น mobile-first)
มี 2 วิธี:
วิธี A — เร็วสุด ใช้ ngrok หรือ cloudflared สร้าง HTTPS tunnel:
bash
# ติดตั้ง cloudflared ก่อน แล้วรัน 2 tunnel
cloudflared tunnel --url http://localhost:8000   # ได้ URL backend
cloudflared tunnel --url http://localhost:5173   # ได้ URL frontend
เอา backend URL ที่ได้ไปใส่ใน frontend/app.js บรรทัด API_BASE_URL แล้วเปิด frontend URL บนมือถือ — PWA install prompt จะโผล่ด้วยเพราะเป็น HTTPS
วิธี B — เทสต์ผ่าน LAN (PWA install ใช้ไม่ได้ แต่ฟังก์ชันหลักใช้ได้):
หา IP เครื่องตัวเอง (ipconfig บน Windows, ifconfig บน Mac/Linux) เช่น 192.168.1.50
รัน backend: uvicorn main:app --host 0.0.0.0 --port 8000
รัน frontend: python -m http.server 5173 --bind 0.0.0.0
ใน app.js แก้เป็น const API_BASE_URL = "http://192.168.1.50:8000"
บนมือถือเปิด http://192.168.1.50:5173 (ต้องอยู่ Wi-Fi เดียวกัน)
ลองเทสต์ดูก่อน ถ้าตรงไหนพัง — error ขึ้นใน console, รูปไม่ขึ้น, slider ไม่ลื่น, API call fail — copy error มาเลย เดี๋ยวช่วยแก้ให้
ถ้าฉันอยากจะให้มันมีเลือกระดับความคมชัดที่ตอนนี้เราใช้ได้เพียงแค่คูณสี่อ่ะฉันอยากให้มันมากกว่านี้อ่ะสามารถทำได้ไหมเอาให้มันแบบมากที่สุดเท่าที่มันจะทำไหวเลยนะไม่รู้ว่ามันจะคูณได้สูงสุดเท่าไหร่ช่วยพยายามให้ฉันหน่อยนะฉันอยากจะทำให้เขาสามารถเห็นความแตกต่างว่าเออภาพชัดชัดขึ้นมาจริงๆขนาดนั้นได้เลยอ่ะ
20:01
ทำได้ครับ แต่ขอเล่าตามตรงก่อนเรื่องนึง เพราะมันสำคัญกับผลลัพธ์ที่คุณอยากเห็น
ตอนนี้ backend ใช้ cv2.INTER_CUBIC ซึ่งไม่ใช่ AI จริง มันคือการ interpolation แบบคณิตศาสตร์ — มันแค่ "เดา" สีของพิกเซลใหม่จากพิกเซลข้างเคียง ปัญหาคือ ยิ่งคูณสูง (8x, 16x) ภาพจะไม่ได้ "ชัดขึ้น" แต่จะ เบลอและนิ่มลง เพราะมันไม่มีรายละเอียดใหม่ให้เติม มันแค่ขยายความเบลอเดิมให้ใหญ่ขึ้น
ดังนั้นถ้าเป้าหมายคือ "ให้คนเห็นความแตกต่างชัดๆ" — การเพิ่มตัวเลขคูณเฉยๆ จะให้ผลตรงข้าม ภาพ 16x จะดูแย่กว่า 4x ด้วยซ้ำ
แต่ผมจะทำให้คุณทั้งสองอย่าง เพื่อให้เทสต์ได้จริง:
เพิ่มตัวเลือกระดับ 2x / 4x / 6x / 8x ตามที่ขอ
เพิ่มการ sharpen หลัง upscale — ใส่ unsharp mask เข้าไป ทำให้ภาพ "ดูคม" ขึ้นจริงๆ ไม่ใช่แค่ใหญ่ขึ้น อันนี้แหละที่จะทำให้ before/after เห็นความต่างชัด
ก่อนแก้ ขอถามนิดนึงให้ตรงกับที่คุณต้องการ:

ออกแบบระบบปรับระดับการขยายภาพและเพิ่มความคมชัด
ออกแบบระบบปรับระดับการขยายภาพและเพิ่มความคมชัด
เข้าใจแล้วครับ — คุณอยากให้ดันสุดและให้ภาพชัดขึ้นแบบเห็นชัด ผมจะจัดให้แบบนี้:
เพิ่มตัวเลือก 2x / 4x / 6x / 8x บนหน้า crop — 8x คือเพดานที่เหมาะสมที่สุด เกินนั้นภาพจะเริ่มเบลอแทนที่จะชัด (เพราะ cubic ไม่ใช่ AI จริง)
ใส่ระบบ sharpen (unsharp mask) เปิดอยู่เป็นค่าตั้งต้น — อันนี้แหละที่ทำให้ before/after เห็นความต่างจริงๆ
มี slider ปรับความคม ให้ผู้ใช้เร่ง/ลดเองได้
มาเริ่มแก้ backend ก่อน:

Created 2 files, ran a command
Created 2 files, ran a command
Now the frontend. I'll add a scale selector and sharpen slider to the crop screen. First let me view the relevant section:

Ran a command, viewed a file
Ran a command, viewed a file
Now I'll insert the scale selector and sharpen slider between the tool row and bottom actions:

Add scale selector and sharpen slider to the crop screen
Add scale selector and sharpen slider to the crop screen
Now update the result screen label to show the actual scale used (it's hardcoded "AFTER · 4×"):

Make the after-label scale dynamic
Make the after-label scale dynamic
Now update app.js to wire up the new controls. Let me update the relevant sections:

Edited 2 files
Edited 2 files
Now add the control logic. I'll insert it after the rotate/reset handlers:

Add scale-chip and sharpen-slider handlers
Add scale-chip and sharpen-slider handlers
Now I need to set the default scale state when the cropper initializes, and update the API call. First, set defaults in initCropper:

Initialize default scale selection when crop screen opens
Initialize default scale selection when crop screen opens
Now update the API call to use the selected scale and sharpen, and pass the scale to showResult:

Edited 2 files
Edited 2 files
Let me verify the changes are consistent — check there are no lingering references to the old SCALE constant:

Verify no stale SCALE refs and app.js is syntactically valid
Verify no stale SCALE refs and app.js is syntactically valid
Let me also verify the Python backend compiles:

Check backend Python syntax
Check backend Python syntax
Both files check out. Let me present the updated files:

Presented 3 files
Presented 3 files
เรียบร้อยครับ ปรับ 3 ไฟล์ (main.py, index.html, app.js) — ส่วน manifest.json, service-worker.js, icons ไม่ต้องแตะ
สิ่งที่ได้เพิ่ม:
บนหน้า crop จะมีกล่อง "Enhancement settings" ใหม่:
ปุ่มเลือก 2× / 4× / 6× / 8× — กดเลือกได้ ปุ่ม Enhance จะเปลี่ยนข้อความตาม
Slider ปรับ Sharpness 0.0–2.0 (ค่าตั้งต้น 0.80) — อันนี้แหละตัวเด็ด ทำให้ขอบภาพคมเด้งขึ้น before/after เห็นต่างชัด
มีคำอธิบายสั้นๆ บอกผู้ใช้ตรงๆ ว่า 8× ภาพจะเริ่มนิ่ม
Backend รับ ?scale=2..8&sharpen=0..2 มี unsharp mask ทำงานหลัง upscale และส่ง header X-Applied-Scale / X-Capped กลับมา ถ้าภาพใหญ่จน 8× เกินเพดาน 8192px ระบบจะลดให้อัตโนมัติแล้วเด้ง toast บอก
ขอย้ำเรื่องที่ตรงไปตรงมา เพราะคุณบอกว่าอยากให้คนเห็นว่า "ภาพชัดขึ้นจริง":
ตัวเลขคูณสูง (8×) จะไม่ได้ทำให้ชัดขึ้น มันแค่ทำให้ภาพใหญ่ขึ้น ส่วนที่ทำให้ดู "คมขึ้นจริง" ในตาคนดูคือ slider Sharpness ต่างหาก ลองเทสต์เทียบดูจะเห็นเอง — เปิดรูปเดียวกัน ลอง 4× sharpen 0 เทียบกับ 4× sharpen 1.5 ความต่างจะชัดกว่าการเทียบ 4× กับ 8× ด้วยซ้ำ
ถ้าอยากได้ความชัดแบบ "เติมรายละเอียดที่หายไปกลับมา" จริงๆ — ต้องใช้ AI model จริง (Real-ESRGAN) แทนบรรทัด cv2.resize ในไฟล์ main.py ที่ผมคอมเมนต์ === Placeholder === ไว้ให้ บอกได้ถ้าอยากให้ช่วยต่อจุดนั้น
ตอนนี้ลองเทสต์ flow ใหม่ดูก่อน: เลือกรูป → เลือก 8× → ลาก sharpness ไปสุด → กด Enhance → ดู slider ถ้าตรงไหนพังบอกได้เลยครับ

Main
PY 

Index
Code · HTML 

App
JS 
Q: เพดานสูงสุดที่อยากให้เลือกได้ควรเป็นเท่าไหร่?
A: สูงสุด 16x (เสี่ยงเบลอ + ช้า)
Q: อยากให้ใส่ตัวปรับความคมชัด (sharpen) หลังขยายภาพไหม?
A: ใส่ แต่ให้ผู้ใช้เปิด/ปิดเองได้
20:07

Orchestrated 16× scaling with toggleable sharpening feature implementation
Orchestrated 16× scaling with toggleable sharpening feature implementation
ได้ตามที่เลือกครับ — เพดาน 16× และ sharpen แบบ เปิด/ปิดเองได้ มาแก้ทั้ง backend และ frontend
Backend — ขยายเพดานเป็น 16×:

Edited 2 files
Edited 2 files
The sigma formula 1.0 + scale/8.0 gives 3.0 at 16× which is fine. Now the frontend. First add the toggle switch CSS:

Add toggle switch styles for the sharpen on/off control
Add toggle switch styles for the sharpen on/off control
Now update the scale chips to 2/4/8/16 and rebuild the sharpen section with a toggle:

Change scale options to 2/4/8/16 and add sharpen on/off toggle
Change scale options to 2/4/8/16 and add sharpen on/off toggle
Now wire up the toggle in app.js. Add the state and DOM ref:

Edited 2 files
Edited 2 files
Now update the scale hints for the new values and add the toggle handler:

Update scale hints for 2/4/8/16 and add sharpen toggle handler
Update scale hints for 2/4/8/16 and add sharpen toggle handler
Now sync the toggle UI state when the crop screen opens:

Sync toggle and slider state when crop screen opens
Sync toggle and slider state when crop screen opens
Now update the API call so sharpen=0 is sent when the toggle is off:

Send sharpen=0 when toggle is off
Send sharpen=0 when toggle is off
Let me verify both files:

Validate both files and confirm new controls wired up
Validate both files and confirm new controls wired up
Everything checks out. Let me update the README to reflect the new 16× ceiling and RAM consideration:

Edited a file, read a file
Edited a file, read a file
เรียบร้อยครับ ปรับ 4 ไฟล์ตามที่เลือก
สิ่งที่เปลี่ยน:
ปุ่มเลือกระดับเป็น 2× / 4× / 8× / 16× — เปลี่ยนจาก 6× เป็น 16× ฝั่ง backend ขยายเพดานเป็น MAX_SCALE = 16
Sharpen ตอนนี้มี toggle เปิด/ปิด อยู่เหนือ slider — ปิดเมื่อไหร่ slider จะจางลงและกดไม่ได้ พอปิดแล้วระบบจะส่ง sharpen=0 ไป backend ข้ามขั้นตอน sharpen ทั้งหมด เปิดกลับมาก็ปรับ strength ต่อได้ตามเดิม
2 เรื่องที่ต้องบอกตรงๆ ก่อนเทสต์:
16× ช้าและเบลอจริงตามที่เตือนไว้ — ปุ่ม 16× จะขึ้น hint ว่า "Extreme · slow & blurry" มันไม่ได้ทำให้ชัดขึ้น แค่ทำให้ไฟล์ใหญ่ขึ้น ตัวที่ทำให้ "ดูคม" คือ toggle Sharpen ต่างหาก เวลาเทสต์ลองเทียบ 4× sharpen-on กับ 16× sharpen-off จะเห็นว่า 4× ดูดีกว่าด้วยซ้ำ
เรื่อง RAM ตอน deploy — ภาพ output 16× ขนาดใหญ่กินหน่วยความจำเยอะมาก (12000×12000 ≈ 432MB ในแรม และ OpenCV สร้าง copy ชั่วคราว พีคได้ 2-3 เท่า) Render free tier (512MB) จะ crash ถ้าเจอ job 16× ใหญ่ๆ — ต้องใช้ instance 2GB ขึ้นไป ผมใส่ระบบ cap ไว้แล้ว (MAX_OUTPUT_DIM = 12000) ถ้าภาพเกินเพดาน ระบบจะลดขนาดให้อัตโนมัติแล้วเด้ง toast บอก ไม่ crash แต่ภาพจะเล็กกว่าที่ขอ
ตอนเทสต์บนเครื่อง (เครื่องคุณแรมเยอะกว่า free tier) น่าจะรัน 16× ได้ ลองดูว่านานแค่ไหน ถ้าช้าเกินรับได้บอกได้ เดี๋ยวปรับ MAX_OUTPUT_DIM ให้ หรือถ้าอยากได้ความชัดจริงๆ ค่อยคุยเรื่องต่อ Real-ESRGAN เข้าไปแทน placeholder

Main
PY 

Index
Code · HTML 

App
JS 

Readme
Document · MD 





Claude is AI and can make mistakes. Please double-check responses.
Main · PY
Copy

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
MAX_INPUT_DIM = int(os.getenv("MAX_INPUT_DIM", "2048"))     # downscale very large inputs first
# Output cap (memory safety). A 12000x12000 RGB image is ~432MB in memory, and
# OpenCV operations create temporary copies — peak usage can be 2-3x that.
# Render free tier (512MB) cannot handle large 16x jobs; use a 2GB+ instance,
# or lower this value. The frontend handles capping gracefully with a notice.
MAX_OUTPUT_DIM = int(os.getenv("MAX_OUTPUT_DIM", "12000"))
MIN_SCALE = 2
MAX_SCALE = 16                                              # hard ceiling — see note in /enhance
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upscaler")
 
# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Universal AI Image Upscaler",
    description="A FastAPI service that upscales images. Currently uses cv2.INTER_CUBIC "
                "plus an unsharp-mask sharpening pass as a placeholder for AI upscaling.",
    version="2.0.0",
)
 
# CORS — allow any origin so the PWA frontend (on Vercel, etc.) can call this API.
# Tighten this to your real frontend domain(s) when going to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "X-Output-Width", "X-Output-Height",
                    "X-Applied-Scale", "X-Capped"],
)
 
 
# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------
def unsharp_mask(img: np.ndarray, sigma: float, strength: float) -> np.ndarray:
    """
    Sharpen an image using the unsharp-mask technique:
    subtract a blurred copy from the original to boost edge contrast.
 
    sigma    — blur radius. Larger = sharpens broader features.
    strength — how strongly to apply it. 0 = none, 1.5+ = aggressive.
    """
    if strength <= 0:
        return img
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, 1.0 + strength, blurred, -strength, 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)
 
 
# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Universal AI Image Upscaler",
        "version": "2.0.0",
        "endpoints": {
            "POST /enhance": "Multipart upload (field: file). "
                             f"Query: scale={MIN_SCALE}..{MAX_SCALE} (default 4), "
                             "sharpen=0..2 (default 0.8).",
            "GET /health": "Health check.",
        },
        "limits": {"max_input_dim": MAX_INPUT_DIM, "max_output_dim": MAX_OUTPUT_DIM},
    }
 
 
@app.get("/health")
def health():
    return {"status": "healthy"}
 
 
@app.post("/enhance")
async def enhance(
    file: UploadFile = File(...),
    scale: int = Query(4, ge=MIN_SCALE, le=MAX_SCALE,
                       description=f"Upscale factor ({MIN_SCALE}-{MAX_SCALE})"),
    sharpen: float = Query(0.8, ge=0.0, le=2.0,
                           description="Sharpening strength (0 = off, ~0.8 default, 2 = max)"),
):
    """
    Receive an image, upscale it by `scale`x, then apply an unsharp-mask
    sharpening pass so the result looks visibly crisper.
 
    NOTE ON HIGH SCALES:
    cv2.INTER_CUBIC is interpolation, NOT AI super-resolution. It cannot invent
    detail that isn't there. Past ~8x the image gets soft rather than sharp, and
    16x is noticeably blurry + slow — those high settings exist because the user
    asked for them, not because they look good. The sharpening pass compensates
    by boosting edge contrast, which is what makes the before/after difference
    pop. For genuine detail reconstruction, swap the resize line below for a
    real model (Real-ESRGAN, SwinIR, etc.).
    """
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
    logger.info("Received image %dx%d, scale=%d, sharpen=%.2f", w, h, scale, sharpen)
 
    # Pre-shrink very large inputs to keep memory + latency reasonable
    if max(h, w) > MAX_INPUT_DIM:
        ratio = MAX_INPUT_DIM / max(h, w)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        h, w = img.shape[:2]
        logger.info("Pre-shrunk input to %dx%d", w, h)
 
    # Compute target size
    out_w, out_h = w * scale, h * scale
    capped = False
 
    # Cap output to a safe ceiling (prevents out-of-memory on big inputs * big scale)
    if max(out_w, out_h) > MAX_OUTPUT_DIM:
        cap = MAX_OUTPUT_DIM / max(out_w, out_h)
        out_w, out_h = max(1, int(out_w * cap)), max(1, int(out_h * cap))
        capped = True
        logger.info("Capped output to %dx%d", out_w, out_h)
 
    effective_scale = round(out_w / w, 2)
 
    # === Placeholder for real AI upscaler ===================================
    # Replace this single line with a call into Real-ESRGAN / SwinIR / etc.
    upscaled = cv2.resize(img, (out_w, out_h), interpolation=cv2.INTER_CUBIC)
    # =======================================================================
 
    # Sharpening pass — this is what makes the result look genuinely crisper.
    # We scale the blur radius slightly with the upscale factor so the effect
    # stays proportional on larger images.
    if sharpen > 0:
        sigma = 1.0 + (scale / 8.0)        # ~1.25 at 2x, ~2.0 at 8x
        upscaled = unsharp_mask(upscaled, sigma=sigma, strength=sharpen)
 
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
            "X-Applied-Scale": str(effective_scale),
            "X-Capped": "1" if capped else "0",
            "Cache-Control": "no-store",
        },
    )
 
 
# Friendly error JSON
@app.exception_handler(HTTPException)
async def http_exc_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
 
