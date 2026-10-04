from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.app.core.platform_version import resolve_version


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Enal AI OS"
    # Bound to ECP_VERSION only. A bare VERSION key in .env / the container env
    # must not shadow the resolved value: generic VERSION vars are set by base
    # images and previously pinned the API to 3.0.0 on a 3.1.0-rc1 checkout.
    VERSION: str = Field(
        default_factory=resolve_version,
        validation_alias=AliasChoices("ECP_VERSION"),
    )
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = "enal"
    MINIO_SECURE: bool = False

    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    STT_PROVIDER: str = "whisper"
    STT_MODEL_PATH: str = ""
    STT_API_KEY: str = ""
    STT_LANGUAGE: str = "id"
    STT_WHISPER_HOST: str = "http://localhost:8082"

    TTS_PROVIDER: str = "pyttsx3"
    TTS_VOICE: str = "en"
    TTS_VOICE_NAME: str = ""
    TTS_VOICE_GENDER: str = "female"
    TTS_VOICE_TONE: str = "sexy"
    TTS_VOICE_ATTITUDE: str = "bratty"
    TTS_SPEED: float = 1.0
    TTS_API_KEY: str = ""
    TTS_ELEVENLABS_VOICE_ID: str = ""
    TTS_PITCH: float = 1.25
    TTS_EMPHASIS: float = 1.4
    TTS_PAUSE_SCALE: float = 1.2
    TTS_STYLE_EXAGGERATION: float = 0.85
    TTS_STABILITY: float = 0.35
    TTS_SIMILARITY_BOOST: float = 0.85
    LOCAL_TTS_URL: str = "http://localhost:8083"

    JENNY_VOICE_PROFILE: str = "jenny"
    JENNY_TTS_VOICE_ID: str = "2E0E83F1-1B49-4C73-9D92-A6C6E9A9A9A5"
    JENNY_LANGUAGE: str = "id"

    DEFAULT_MODEL: str = "ollama/llama3:8b"
    DEFAULT_REASONING_MODEL: str = "ollama/llama3:8b"
    DEFAULT_EMBEDDING_MODEL: str = "ollama/nomic-embed-text"
    FALLBACK_MODEL: str = "ollama/qwen2.5:0.5b"
    FALLBACK_REASONING_MODEL: str = "ollama/qwen2.5:0.5b"
    OLLAMA_FALLBACK_ENABLED: bool = True

    GPU_INFERENCE_ENABLED: bool = False
    GPU_MODEL_PATH: str = "E:/Enal-AI-OS/models/qwen2.5-3b"
    GPU_FALLBACK_ENABLED: bool = True

    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    TESTING: bool = False

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "enal-ai-os"

    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "http://localhost:3000"

    LITELLM_MASTER_KEY: str = ""
    DEBUG: bool = False
    ENABLE_BENCHMARK_RUNTIME: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOGGING_PROVIDER: str = "console"

    @model_validator(mode="after")
    def validate_secret_key(self):
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is required. Set it via environment variable or .env file."
            )
        return self

    def require_database_url(self) -> str:
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL is required. Set it via environment variable or .env file."
            )
        return self.DATABASE_URL


settings = Settings()
