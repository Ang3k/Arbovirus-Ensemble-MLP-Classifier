"""
SINAN (Sistema de Informação de Agravos de Notificação) field mappings.
Maps human-readable Portuguese labels to their corresponding SINAN numeric codes.

Sources:
- DIC_DADOS_NET - Notificação Individual (SINAN NET v5.0)
- Anexo A do Instrutivo - CBO 2002 (CEREST TOCANTINS)
"""


EDUCATION_MAP = {
    'Analfabeto': 0,
    '1ª a 4ª série incompleta': 1,
    '4ª série completa': 2,
    '5ª à 8ª série incompleta': 3,
    'Ensino fundamental completo': 4,
    'Ensino médio incompleto': 5,
    'Ensino médio completo': 6,
    'Educação superior incompleta': 7,
    'Educação superior completa': 8,
    'Ignorado': 9,
    'Não se aplica': 10,
}


RACE_MAP = {
    'Branca': 1,
    'Preta': 2,
    'Amarela': 3,
    'Parda': 4,
    'Indígena': 5,
    'Ignorado': 9,
}


PREGNANCY_MAP = {
    '1º Trimestre': 1,
    '2º Trimestre': 2,
    '3º Trimestre': 3,
    'Idade gestacional ignorada': 4,
    'Não': 5,
    'Não se aplica': 6,
    'Ignorado': 9,
}


SEX_MAP = {'Masculino': 'M', 'Feminino': 'F', 'Ignorado': 'I'}


UF_MAP = {
    'Rondônia': 11,
    'Acre': 12,
    'Amazonas': 13,
    'Roraima': 14,
    'Pará': 15,
    'Amapá': 16,
    'Tocantins': 17,
    'Maranhão': 21,
    'Piauí': 22,
    'Ceará': 23,
    'Rio Grande do Norte': 24,
    'Paraíba': 25,
    'Pernambuco': 26,
    'Alagoas': 27,
    'Sergipe': 28,
    'Bahia': 29,
    'Minas Gerais': 31,
    'Espírito Santo': 32,
    'Rio de Janeiro': 33,
    'São Paulo': 35,
    'Paraná': 41,
    'Santa Catarina': 42,
    'Rio Grande do Sul': 43,
    'Mato Grosso do Sul': 50,
    'Mato Grosso': 51,
    'Goiás': 52,
    'Distrito Federal': 53,
}


# CBO_MAP is loaded from cbo_map.py (auto-generated from Anexo-A-do-instrutivo.pdf)
# If cbo_map.py doesn't exist yet, CBO_MAP will be an empty dict
try:
    from data_processing.cbo_map import CBO_MAP
except ImportError:
    CBO_MAP = {}
