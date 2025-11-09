from abc import abstractmethod, ABC
from typing import List, Any

class api_client(ABC):
    """
    Abstract class to provide shared interface for making api calls
    """
    model_name: str

    def __init__(self, model_name) -> None:
        self.model_name = model_name
    
    @abstractmethod
    async def call(self, prompt: str, **kwargs):
        """
        send a single response to the API

        return type should be whatever response object (or raw output) the API gives, so that errors can be
        handled elegantly later in the pipeline
        """
        raise NotImplementedError
    
    async def batch_call(self, prompts=List[str], **kwargs):
        """
        optional method if we decide to batch multiple prompts?
        can use for specific APIs that may allow this
        """
    
    async def retry_call(self, prompt: str, max_retries: int, **kwargs):
        """
        retry the API call a certain amount of times in case the first one failed / raised an error
        If the call exceeds max_retries the error should be logged somewhere
        """
        raise NotImplementedError

    # --------------------- rate limiting / token counting maybe ?----------------------------------

    def estimate_tokens(self, prompt: str, response: Any):
        """
        Estimate the amount of tokens the prompt and response will cost
        Varies a lot depending on model

        This should act as a helper function for rate limiting our calls
        """
        raise NotImplementedError