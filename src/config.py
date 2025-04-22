# src/config.py
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.VERSION: str = os.getenv("VERSION", "Version not set!")
        self.DATE: str = os.getenv("DATE", datetime.now().isoformat())
        self.BENTO_BACKEND_GRAPHQL_URI: Optional[str] = os.getenv(
            "BENTO_BACKEND_GRAPHQL_URI", "https://caninecommons.cancer.gov/v1/graphql"
        )
        if not self.BENTO_BACKEND_GRAPHQL_URI:
            raise ValueError("BENTO_BACKEND_GRAPHQL_URI must be set")
        print(self.BENTO_BACKEND_GRAPHQL_URI)

    def validate_config(self):
        unset_vars = []
        for key, value in vars(self).items():
            if key not in ["VERSION", "DATE"] and value is None:
                unset_vars.append(key)

        if unset_vars:
            raise ValueError(
                f"The following environment variables are not set: {', '.join(unset_vars)}"
            )


config = Config()
config.validate_config()
