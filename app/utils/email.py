from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, MessageType, FastMail
from jinja2 import Template
from starlette.responses import JSONResponse

from core.config import conf


async def send_in_background(
        background_tasks: BackgroundTasks,
        user, code
) -> JSONResponse:
    with open("templates/email_template.html", "r") as file:
        html_template = file.read()

    template = Template(html_template)
    html_content = template.render(username=user.username, code=code)

    message = MessageSchema(
        subject="FastAPI-Mail HTML Email",
        recipients=[user.email],
        body=html_content,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    # Send email as a background task
    background_tasks.add_task(fm.send_message, message, template_name=None)

    return JSONResponse(status_code=200, content={"message": "HTML Email sent successfully"})
