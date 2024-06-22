## Tentei tirar o main do projeto e colocar direto no controler, mas aconteceu um erro por não conseguir rodar da outra forma mantive o arquivo. 

from fastapi import FastAPI
from app.controllers import task_controller

app = FastAPI()

app.include_router(task_controller.router)

