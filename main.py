import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from department import router as department_router
import create_table  # ✅ Calls table creation
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (change this in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run table creation before app starts
@app.on_event("startup")
async def startup_event():
    await create_table.create_tables()  # ✅ Calls table creation before running API

app.include_router(department_router)

# Ensure the "templates" folder exists for Jinja2
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"

os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Set up Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Serve static files (for CSS, JS, images)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include the department router
app.include_router(department_router)

@app.get("/", response_class=HTMLResponse)
async def serve_homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
