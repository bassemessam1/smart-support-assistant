from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from llm import run_model
from tools import ACTIONS
from database import get_all_tickets
from schemas import AIResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """
        <html>
        <body>
        <h2>Smart Support Assistant</h2>
        <form action="/ask" method="post">
            <textarea name="user_input" rows="5" cols="50"></textarea><br>
            <button type="submit">Ask</button>
            <link rel="icon" href="/static/favicon.ico" />
        </form>
        </body>
        </html>
    """

@app.get("/tickets", response_class=HTMLResponse)
def browse_tickets():
    tickets = get_all_tickets()
    html = "<h2>All Tickets</h2><ul>"
    for t in tickets:
        html += f"<li><strong>ID {t['id']}</strong>: {t['title']} — {t['status']}</li>"
    html += "</ul><br><a href='/'>Back</a>"
    return html

@app.post("/ask")
async def ask(request: Request):
    form = await request.form()
    user_input = form.get("user_input")

    ai: AIResponse = run_model(user_input)

    if ai.response_type=='action':
        action_fn = ACTIONS.get(ai.action_name)
        if action_fn:
            result = action_fn(**(ai.action_args or {}))
            print(f"Result:{result}")
            return {"final_answer": ai.final_answer, "action_output": result}
        
    app.mount("/static", StaticFiles(directory="static"), name="static")
    html = f"""
    <html>
    <body>
        <h2>Final Answer</h2>
        <p>{ai.final_answer}</p>
        <h2>Action</h2>
        <p>{ai.action_name}</p>
        <br><a href="/">Back</a>
    </body>
    </html>
    """

    return HTMLResponse(content=html)