from openai import OpenAI
from . import GEMENI_KEY
from src.abs.client import api_client
import asyncio
from openai import OpenAIError, APIError, RateLimitError, APIConnectionError, Timeout
from src.abs.prompt import Prompt