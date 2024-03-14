# openai-express
Max speed of openai call in tpm &amp; rpm limitation.

One hundred gpt-3.5-turbo requests only take 5 seconds.

One thousand gpt-3.5-turbo requests takes 5 minutes.

**This is a super early version of this project. Needs to optimize more.**


### AutoRAG
Want to optimize your RAG pipeline? Check out [AutoRAG](https://github.com/Marker-Inc-Korea/AutoRAG)!


## Install

```bash
pip install openai-express
```

## Usage
First, find your openai limit tier at [here](https://platform.openai.com/account/limits).
There are 'free', 'tier_1', 'tier_2', 'tier_3', 'tier_4' and 'tier_5' tiers.


```python
from openaiexpress import fast_chat_completion

messages = [
        [{"role": "user", "content": "Say this is a test"}],
        [{"role": "user", "content": "Another test prompt"}],
    ]
results = fast_chat_completion(messages, model='gpt-3.5-turbo', tier="tier_3")

```

That's it!


## Acknowledgements
This can lead you to pay api call fee more than you expected. Please be aware of the pricing of openai api call.
