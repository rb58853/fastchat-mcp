import os
import json
from fastauth import FastauthSettings


class AuthApiConfig:
    def __init__(self, config_file: str = "fastchat.config.json"):
        self.auth_settings: FastauthSettings = FastauthSettings()

        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                config: dict = json.load(file)
                auth_config: dict = config.get("auth_middleware", {})
                self.auth_settings = FastauthSettings(
                    database_api_path=auth_config.get("database_api_path"),
                    master_token=auth_config.get("master-token", None)
                    or os.getenv("MASTER_TOKEN", None),
                    headers=auth_config.get("headers", {}),
                )
                
    def new_override(self,_settings:dict):
        settings = self.auth_settings.dict()
        settings.update(_settings)
        return settings
        
                    
