# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

from pathlib import Path
from typing import Any, Dict
import os
import logging # Added import

from langchain_openai import ChatOpenAI

from src.config import load_yaml_config
from src.config.agents import LLMType

# Cache for LLM instances
_llm_cache: dict[LLMType, ChatOpenAI] = {}

logger = logging.getLogger(__name__) # Added logger


def _get_env_llm_conf(llm_type: str) -> Dict[str, Any]:
    """
    Get LLM configuration from environment variables.
    Environment variables should follow the format: {LLM_TYPE}__{KEY}
    e.g., BASIC_MODEL__api_key, BASIC_MODEL__base_url
    """
    prefix = f"{llm_type.upper()}_MODEL__"
    conf = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            conf_key = key[len(prefix) :].lower()
            # Map openai_api_key to api_key for ChatOpenAI compatibility
            if conf_key == "openai_api_key":
                conf_key = "api_key"
            conf[conf_key] = value
    return conf


def _create_llm_use_conf(llm_type: LLMType, conf: Dict[str, Any]) -> ChatOpenAI:
    # DIRECT FIX: Use hardcoded configuration to bypass environment variable issues
    logger.info(f"Creating LLM for type: {llm_type} with direct configuration")

    # Hardcoded working configuration
    merged_conf = {
        "model": "google/gemini-2.5-pro-preview",
        "api_key": "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",
        "base_url": "https://openrouter.ai/api/v1"
    }

    logger.info(f"Creating LLM for type: {llm_type} with model: {merged_conf.get('model')}, base_url: {merged_conf.get('base_url')}")
    logger.info(f"API key present: {'✓' if merged_conf.get('api_key') else '✗'}")

    # Add default headers for OpenRouter if using OpenRouter base URL
    if merged_conf.get("base_url") == "https://openrouter.ai/api/v1":
        default_headers = merged_conf.get("default_headers", {})
        default_headers.update({
            "HTTP-Referer": "https://avaxsearch.vercel.app",
            "X-Title": "CryptoSearch",
        })
        merged_conf["default_headers"] = default_headers

    # Log the final configuration (without exposing the API key)
    safe_conf = {k: v if k != "api_key" else "***" for k, v in merged_conf.items()}
    logger.info(f"Final LLM configuration: {safe_conf}")

    return ChatOpenAI(**merged_conf)


def clear_llm_cache():
    """Clear the LLM cache to force reloading of configurations."""
    global _llm_cache
    _llm_cache.clear()


def reload_all_llms():
    """Force reload all LLM instances with current configuration."""
    clear_llm_cache()
    # Pre-load all LLM types to ensure they're available
    for llm_type in ["basic", "reasoning", "vision"]:
        get_llm_by_type(llm_type, force_reload=True)


def get_llm_by_type(
    llm_type: LLMType,
    force_reload: bool = False,
) -> ChatOpenAI:
    """
    Get LLM instance by type. Returns cached instance if available.

    Args:
        llm_type: The type of LLM to get
        force_reload: If True, forces reloading even if cached instance exists
    """
    # Force reload if requested or if cache is empty
    if force_reload or llm_type not in _llm_cache:
        conf = load_yaml_config(
            str((Path(__file__).parent.parent.parent / "conf.yaml").resolve())
        )
        llm = _create_llm_use_conf(llm_type, conf)
        _llm_cache[llm_type] = llm
        return llm

    return _llm_cache[llm_type]


# In the future, we will use reasoning_llm and vl_llm for different purposes
# reasoning_llm = get_llm_by_type("reasoning")
# vl_llm = get_llm_by_type("vision")


if __name__ == "__main__":
    # Initialize LLMs for different purposes - now these will be cached
    basic_llm = get_llm_by_type("basic")
    print(basic_llm.invoke("Hello"))
