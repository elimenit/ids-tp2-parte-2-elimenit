from fastapi import APIRouter
from routers.movimientos import move_router
from routers.pokemon import router_pokemon
from routers.equipos import team_router
routers = APIRouter(prefix="/api")

routers.include_router(move_router)
routers.include_router(router_pokemon)
routers.include_router(team_router)