import sys
import os

# Adiciona o diretório da API ao path do sistema para que a importação funcione
sys.path.insert(0, os.path.dirname(__file__))

# Importa a instância do app Flask do seu arquivo classify.py
from api.classify import app

if __name__ == "__main__":
    app.run()
