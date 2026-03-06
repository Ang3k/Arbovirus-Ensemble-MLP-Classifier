import sys
from pathlib import Path

# Add src to path so imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

from models_classes.models_orchestrator import ModelsOrchestrator

app = FastAPI(title='Classificador de Arboviroses')

# Serve static files (HTML, CSS, JS)
app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

# Load models on startup
models = {}

MODELS_DIR = Path(__file__).resolve().parent.parent / 'models_saved'


@app.on_event('startup')
def load_models():
    for disease in ['dengue', 'chikungunya']:
        disease_dir = MODELS_DIR / disease
        if disease_dir.exists() and (disease_dir / 'artifacts.json').exists():
            orch, mlp, lgbm, xgb = ModelsOrchestrator.load_for_inference(disease_dir)
            models[disease] = {'orch': orch, 'mlp': mlp, 'lgbm': lgbm, 'xgb': xgb}
            print(f'Loaded {disease} models')
        else:
            print(f'Warning: {disease} models not found at {disease_dir}')


class PatientInput(BaseModel):
    disease_type: str

    # Demographics
    age: int
    sex: str
    pregnancy_status: str = 'Não se aplica'
    race: str = 'Ignorado'
    education_level: str = 'Ignorado'
    occupation_code: str = ''
    residence_state: str = 'São Paulo'

    # Dates
    symptom_onset_date: str
    notification_date: Optional[str] = None

    # Symptoms
    fever: int = 0
    myalgia: int = 0
    headache: int = 0
    rash: int = 0
    vomiting: int = 0
    nausea: int = 0
    back_pain: int = 0
    conjunctivitis: int = 0
    arthritis: int = 0
    joint_pain: int = 0
    petechiae: int = 0
    retro_orbital_pain: int = 0

    # Comorbidities
    diabetes: int = 0
    blood_disorder: int = 0
    liver_disease: int = 0
    kidney_disease: int = 0
    hypertension: int = 0
    peptic_ulcer: int = 0
    autoimmune_disease: int = 0

    # Hemorrhagic
    nosebleed: int = 0
    gum_bleeding: int = 0
    metrorrhagia: int = 0
    petechiae_hemorrh: int = 0
    hematuria: int = 0
    other_bleeding: int = 0


@app.get('/', response_class=HTMLResponse)
def index():
    html_path = Path(__file__).parent / 'static' / 'index.html'
    return html_path.read_text(encoding='utf-8')


@app.post('/predict')
def predict(patient: PatientInput):
    disease = patient.disease_type
    if disease not in models:
        return {'error': f'Modelos para "{disease}" não encontrados. Rode o notebook para gerar os artefatos.'}

    m = models[disease]
    patient_dict = patient.model_dump(exclude={'disease_type'})

    result = m['orch'].predict(patient_dict, m['mlp'], m['lgbm'], m['xgb'])
    return result


@app.get('/available_diseases')
def available_diseases():
    return list(models.keys())
