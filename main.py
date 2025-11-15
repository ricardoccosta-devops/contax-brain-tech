"""
Ponto de entrada principal da aplicação e-BrAIn.Tech
Execute: streamlit run main.py
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa a aplicação principal
from app.frontend.main_app import *

