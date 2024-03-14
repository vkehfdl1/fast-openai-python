from openaiexpress import fast_chat_completion


def test_fast_chat_completion():
    prompts = [
        [{"role": "user", "content": "Say this is a test"}],
        [{"role": "user", "content": "Another test prompt"}],
    ]
    model = "gpt-3.5-turbo"
    tier = "tier_4"
    results = fast_chat_completion(prompts, model, tier)

    assert len(results) == 2
