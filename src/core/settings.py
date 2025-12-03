import os
import json

class Settings ():
    _default_path = 'src/data/settings/config.json'
    _data: dict = {}

    @classmethod
    def _load_data (cls) -> None:
        """ Carrega os dados do arquivo JSON """
        if cls._data: return

        try: 
            file_path = os.path.abspath(cls._default_path)

            with open(file_path, "r") as f:
                cls._data = json.load(f)

        except FileNotFoundError:
            print(f"[ERRO]: O arquivo de configuração '{cls._default_path}' não foi encontrado.")
            cls._data = {}
            
        except json.JSONDecodeError:
            print(f"[ERRO]: Falha ao decodificar o JSON do arquivo '{cls._default_path}'. Verifique o formato.")
            cls._data = {}

    @classmethod
    def get (cls, config_name: str, default=None):
        """ Retorna uma configuração específica. """
        cls._load_data()
        return cls._data.get(config_name, default)
    
    @classmethod
    def set_config_path (cls, new_path: str) -> None:
        """ Altera o caminho padrão do arquivo de configuração antes do primeiro carregamento. """
        if not cls._data:
            cls._default_path = new_path
        else:
            print("[AVISO]: O caminho do arquivo de configuração não pode ser alterado após o carregamento inicial.")