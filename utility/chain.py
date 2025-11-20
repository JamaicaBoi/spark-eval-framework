from langchain_openai import ChatOpenAI
from langsmith import Client
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from functools import lru_cache
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langfuse import Langfuse

client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))

class ChainLoader:
    def __init__(self,prompt_name=None,local_prompt=None, prompt_provider="langsmith",partial_variables={}, parser=None,**kwargs):
        """
        Initialize the ChainLoader class.
        """
        if prompt_name is None and local_prompt is None:
            raise ValueError("Either prompt_name or local_prompt must be provided.")
        
        self.json_schema =None
        if prompt_provider=="local":
            if local_prompt:
                if isinstance(local_prompt, ChatPromptTemplate):
                    self.prompt = local_prompt
                else:
                    raise ValueError("local_prompt must be an instance of ChatPromptTemplate")
            else:
                raise ValueError("local_prompt must be provided if prompt_provider is 'local'")
        elif prompt_provider == "langsmith":
            self.prompt = self.langsmith_pull_prompt(prompt_name)
        elif prompt_provider == "langfuse":
            self.prompt,self.json_schema  = self.langfuse_pull_prompt(prompt_name)

        self._set_partial_variables(partial_variables)

        self.configurable_models = self.create_model()
        if self.json_schema:
            self.configurable_models = self.configurable_models.with_structured_output(self.json_schema)

    @staticmethod
    @lru_cache(maxsize=100)
    def langsmith_pull_prompt(prompt_name: str):

        return client.pull_prompt(prompt_name)
    
    @staticmethod
    @lru_cache(maxsize=100)
    def langfuse_pull_prompt(prompt_name: str):

        langfuse = Langfuse()
        langfuse_prompt = langfuse.get_prompt(prompt_name)
        langchain_prompt = ChatPromptTemplate.from_messages(langfuse_prompt.get_langchain_prompt())
        langchain_prompt.metadata = {"langfuse_prompt": langfuse_prompt}

        json_schema = None
        if "json_schema" in langfuse_prompt.config:
            json_schema = langfuse_prompt.config["json_schema"]

        if "placeholder" in langfuse_prompt.config:
            langchain_prompt.append(MessagesPlaceholder(langfuse_prompt.config["placeholder"]))

        return langchain_prompt, json_schema

    def _set_partial_variables(self, partial_variables):
        """
        Sets partial variables for the prompt and validates them.
        
        Args:
            partial_variables (dict): Dictionary of partial variables to set.
        
        Raises:
            ValueError: If a partial variable key is not in the prompt's input variables.
        """
        if partial_variables:
            for key in partial_variables:
                if key in self.prompt.input_variables:
                    self.prompt.input_variables.remove(key)
            self.prompt.partial_variables = partial_variables
            
    @staticmethod
    @lru_cache(maxsize=2)
    def create_model(ollama_url = None):
        """
        Creates and returns a language model (LLM) based on the provided or default configuration.

        Args:
            **kwargs: Override parameters such as model_provider and model_name.

        Returns:
            ChatOpenAI: An instance of the language model.

        Raises:
            ValueError: If an unsupported model provider is specified.
        """
        openai_models = ChatOpenAI(model="gpt-5-mini", temperature=0).configurable_fields(
            model_name=ConfigurableField(
                id="openai_model_name",
                name="Model Name",
                description="The name of the model to use",
            ),
            temperature=ConfigurableField(
                id="openai_temperature",
                name="LLM Temperature",
                description="The temperature of the LLM",
            )
        )

        anthropic_models = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0).configurable_fields(
            model=ConfigurableField(
                id="anthropic_model_name",
                name="Model Name",
                description="The name of the model to use",
            ),
            temperature=ConfigurableField(
                id="anthropic_temperature",
                name="LLM Temperature",
                description="The temperature of the LLM",
            )
        )
        ollama_url = ollama_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        ollama_models = ChatOllama(base_url=ollama_url,model="deepseek-r1:1.5b", temperature=0).configurable_fields(
            model=ConfigurableField(
                id="ollama_model_name",
                name="Model Name",
                description="The name of the model to use",
            ),
            temperature=ConfigurableField(
                id="ollama_temperature",
                name="LLM Temperature",
                description="The temperature of the LLM",
            )
        )

        configurable_models = openai_models.configurable_alternatives(
            ConfigurableField(id="llm_provider"),
            default_key="openai",
            anthropic=anthropic_models,
            ollama=ollama_models
        )
        

        return configurable_models

    @classmethod
    def load_chain(cls, prompt_name=None,local_prompt=None, prompt_provider="langsmith",partial_variables={}, parser=None, config={},**kwargs):
        """
        Class method to create a full processing chain with a prompt, model, and optional parser.

        Args:
            prompt_name (str): Name of the prompt to pull from LangSmith.
            partial_variables (dict): Dictionary of partial variables to set in the prompt.
            parser (callable, optional): An optional parser to process model outputs.
            **kwargs: Additional arguments for model creation.

        Returns:
            chain: The processing chain (prompt → model → parser, if provided).
        """
        # Create an instance of the class
        

        if config:
            prompt_provider = config["configurable"].get("prompt_provider", prompt_provider)
            instance = cls(prompt_name, local_prompt,prompt_provider, partial_variables, parser, **kwargs)

            llm_provider = config["configurable"].get("llm_provider", "openai")
            default_model_name = {"openai":"gpt-5-mini","anthropic":"claude-3-haiku-20240307","ollama":"deepseek-r1:1.5b"}
            model_name = config["configurable"].get("model_name", default_model_name[llm_provider])
            temperature = config["configurable"].get("temperature", 0)
            instance.configurable_models = instance.configurable_models.with_config(configurable={
                "llm_provider": llm_provider, 
                f"{llm_provider}_model_name": model_name, 
                f"{llm_provider}_temperature": temperature
            })
        else:
            instance = cls(prompt_name, local_prompt,prompt_provider, partial_variables, parser, **kwargs)
        if parser:
            chain = instance.prompt | instance.configurable_models | parser
        else:
            chain = instance.prompt | instance.configurable_models
        
        return chain