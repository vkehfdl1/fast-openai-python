import os
import asyncio
import time
from typing import Dict, List

from openai import AsyncOpenAI
from tqdm import tqdm
import tiktoken
import logging

from fastopenai.constant_limits import MODEL_LIMITS

# Initialize the AsyncOpenAI client
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


logger = logging.getLogger("fast-openai")


# Function to count tokens in a prompt
def count_tokens(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        # print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return count_tokens(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return count_tokens(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


# Function to make batches with RPM and TPM limits
def make_batches(messages, rpm_limit: int, tpm_limit: int, context_len: int):
    batches = []
    current_batch = []
    current_tokens = 0

    for message in tqdm(messages):
        prompt_tokens = count_tokens(message)
        if prompt_tokens > context_len:
            logger.warning(f"Message with {prompt_tokens} tokens exceeds context length {context_len}. Skipping."
                           f"The message : \n{message}")
            current_batch.append(None)  # skip this message

        if len(current_batch) >= rpm_limit or current_tokens + prompt_tokens > tpm_limit:
            batches.append(current_batch)
            current_batch = [message]
            current_tokens = prompt_tokens
        else:
            current_batch.append(message)
            current_tokens += prompt_tokens
    if current_batch:
        batches.append(current_batch)

    return batches


# Async function to process a single batch of prompts
async def process_batch(messages, model, **kwargs):
    responses = []
    for message in messages:
        if message is None:
            responses.append(None)
        else:
            response = await client.chat.completions.create(
                messages=message,
                model=model,
                **kwargs
            )
            responses.append(response)
    return responses


# Main async function to process all prompts with rate limiting
async def process_prompts_with_rate_limiting(messages: List[List[Dict]], model, tpm_limit, rpm_limit, context_len,
                                             **kwargs):
    batches = make_batches(messages, rpm_limit, tpm_limit, context_len)
    all_responses = []

    for i, batch in enumerate(tqdm(batches)):
        start_time = time.time()
        responses = await process_batch(batch, model, **kwargs)
        all_responses.extend(responses)
        elapsed_time = time.time() - start_time

        if elapsed_time < 62 and i + 1 < len(batches):
            await asyncio.sleep(62 - elapsed_time)  # Wait until a minute has passed

    return all_responses


def fast_chat_completion(messages, model: str, tier: str, **kwargs):
    # find limits
    model_limits = list(filter(lambda x: x.model_name == model, MODEL_LIMITS))
    if len(model_limits) <= 0:
        raise ValueError(f"Model {model} not found in MODEL_LIMITS")
    model_limit = model_limits[0]
    rate_limit = getattr(model_limit, tier)
    results = asyncio.run(process_prompts_with_rate_limiting(messages, model, rate_limit.tpm, rate_limit.rpm,
                                                             model_limit.context_len, **kwargs))
    return results
