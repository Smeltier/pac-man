import os
import json

class Settings ():

    def __init__ (self, path: str) -> None:
        self._path = path
        self._data = self._load_data()

    def _load_data (self) -> dict:
        try:
            path = os.path.abspath(self._path)
            with open(path, "r") as file:
                return json.load(file)
            
        except FileNotFoundError: 
            print(f"[ERRO]: O arquivo de configuração '{self._path}' não foi encontrado.") 
            return {} 
        
        except json.JSONDecodeError: 
            print(f"[ERRO]: Falha ao decodificar o JSON do arquivo '{self._path}'. Verifique o formato.")
            return {}
        
    def get (self, key: str, default = None) -> dict:
        return self._data.get(key, default)