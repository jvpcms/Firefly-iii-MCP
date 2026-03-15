from dotenv import load_dotenv
import os

load_dotenv()


class EnvConfig:

    def _load_env(self, env_name: str) -> str:
        value = os.getenv(env_name)
        if not value:
            raise RuntimeError(f"Missing required environment variable: {env_name}")
        return value

    @property
    def firefly_iii_url(self) -> str:
        return self._load_env("FIREFLY_III_URL")

    @property
    def firefly_iii_access_token(self) -> str:
        return self._load_env("FIREFLY_III_ACCESS_TOKEN")

    @property
    def tool_data_path(self) -> str:
        return os.getenv("TOOL_DATA_PATH", "./tool_data")


env_config = EnvConfig()
