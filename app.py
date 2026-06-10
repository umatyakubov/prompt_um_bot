from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
import sqlite3

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = BASE_DIR / "images"

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/static", StaticFiles(directory="static"), name="static")


def db():
    conn = sqlite3.connect("gallery.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            image TEXT,
            link TEXT
        )
    """)
    return conn


@app.get("/", response_class=HTMLResponse)
def gallery():
    conn = db()
    items = conn.execute("SELECT id, title, image, link FROM prompts ORDER BY id DESC").fetchall()
    conn.close()

    cards = ""
    for item in items:
        cards += f"""
        <div class="item" onclick="openModal('{item[1]}','{item[2]}','{item[3]}')">
            <img src="{item[2]}">
        </div>
        """

    return f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <header>
            <h1>📸 Promptlar Galereyasi</h1>
            <input id="search" placeholder="Prompt qidirish...">
        </header>

        <div class="gallery" id="gallery">{cards}</div>

        <div class="modal" id="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">&times;</span>
                <img id="modalImg">
                <h2 id="modalTitle"></h2>
                <a id="promptBtn" target="_blank">📥 Promtni olish</a>
            </div>
        </div>

        <script>
        function openModal(title, img, link){{
            document.getElementById("modal").style.display="flex";
            document.getElementById("modalTitle").innerText=title;
            document.getElementById("modalImg").src=img;
            document.getElementById("promptBtn").href=link;
        }}
        function closeModal(){{
            document.getElementById("modal").style.display="none";
        }}
        </script>
    </body>
    </html>
    """


@app.get("/admin", response_class=HTMLResponse)
def admin():
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body{font-family:Arial;background:#111;color:white;padding:20px}
            input,button{width:100%;padding:14px;margin:8px 0;border-radius:12px;border:0}
            button{background:#2ea6ff;color:white;font-weight:bold}
        </style>
    </head>
    <body>
        <h2>Admin panel</h2>
        <form action="/add" method="post" enctype="multipart/form-data">
            <input name="title" placeholder="Prompt nomi" required>
            <input name="link" placeholder="Telegram post link" required>
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Saqlash</button>
        </form>
    </body>
    </html>
    """


@app.post("/add")
def add_prompt(title: str = Form(...), link: str = Form(...), image: UploadFile = File(...)):
    IMAGES_DIR.mkdir(exist_ok=True)

    file_path = IMAGES_DIR / image.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/images/{image.filename}"

    conn = db()
    conn.execute(
        "INSERT INTO prompts (title, image, link) VALUES (?, ?, ?)",
        (title, image_url, link)
    )
    conn.commit()
    conn.close()

    return RedirectResponse("/admin", status_code=303)