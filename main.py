from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import os

app = FastAPI()

# 🔹 CORS (OBRIGATÓRIO PARA SURVEY123)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 BANCO VIA VARIÁVEL DE AMBIENTE (RENDER)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não configurada")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 🔹 MODELO
class Survey_Visitas(BaseModel):
    model_config = ConfigDict(extra="ignore")

    globalid: str
    tipo_registro: Optional[str] = None
    data_hora_visita: Optional[datetime] = None
    fiscal_campo: Optional[str] = None
    municipio: Optional[str] = None
    corpo_hidrico: Optional[str] = None
    tipo_frente: Optional[str] = None
    status_andamento: Optional[str] = None
    trecho_adicional: Optional[str] = None
    status_geral_frente: Optional[str] = None
    encarregado: Optional[int] = None
    ajudantes: Optional[int] = None
    agentes_socioambientais: Optional[int] = None
    retroescavadeira: Optional[int] = None
    escavadeira_long_reach: Optional[int] = None
    escavadeira_17_ton: Optional[int] = None
    escavadeira_23_ton: Optional[int] = None
    escavadeira_anfibia: Optional[int] = None
    dragline_clamshell: Optional[int] = None
    caminhao_basculante_7m3: Optional[int] = None
    caminhao_basculante_12m3: Optional[int] = None
    caminhao_hidro_vacuo: Optional[int] = None
    status_avanco_esperado: Optional[str] = None
    extensao_avanco_m2: Optional[float] = None
    extensao_avanco_m3: Optional[float] = None
    coord_x: Optional[float] = None
    coord_y: Optional[float] = None
    desvio: Optional[str] = None
    observacoes_gerais: Optional[str] = None

# 🔹 OPTIONS (preflight do Survey123)
@app.options("/survey123")
async def survey123_options():
    return JSONResponse(status_code=200, content={"status": "ok"})

# 🔹 POST
@app.post("/survey123")
def receber_survey(dados: Survey_Visitas):
    parametros = dados.model_dump()

    try:
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT IGNORE INTO survey_visitas (
                        globalid, tipo_registro, data_hora_visita, fiscal_campo,
                        municipio, corpo_hidrico, tipo_frente, status_andamento,
                        trecho_adicional, status_geral_frente, encarregado,
                        ajudantes, agentes_socioambientais, retroescavadeira,
                        escavadeira_long_reach, escavadeira_17_ton,
                        escavadeira_23_ton, escavadeira_anfibia,
                        dragline_clamshell, caminhao_basculante_7m3,
                        caminhao_basculante_12m3, caminhao_hidro_vacuo,
                        status_avanco_esperado, extensao_avanco_m2,
                        extensao_avanco_m3, coord_x, coord_y, desvio,
                        observacoes_gerais
                    ) VALUES (
                        :globalid, :tipo_registro, :data_hora_visita, :fiscal_campo,
                        :municipio, :corpo_hidrico, :tipo_frente, :status_andamento,
                        :trecho_adicional, :status_geral_frente, :encarregado,
                        :ajudantes, :agentes_socioambientais, :retroescavadeira,
                        :escavadeira_long_reach, :escavadeira_17_ton,
                        :escavadeira_23_ton, :escavadeira_anfibia,
                        :dragline_clamshell, :caminhao_basculante_7m3,
                        :caminhao_basculante_12m3, :caminhao_hidro_vacuo,
                        :status_avanco_esperado, :extensao_avanco_m2,
                        :extensao_avanco_m3, :coord_x, :coord_y, :desvio,
                        :observacoes_gerais
                    )
                """),
                parametros
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "ok", "globalid": dados.globalid}
