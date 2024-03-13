from fastopenai.schema.rate import ModelLimit, RateLimit

gpt_3_5_limits = [
    RateLimit(rpm=3, rpd=200, tpm=40_000),
    RateLimit(rpm=3_500, rpd=10_000, tpm=60_000),
    RateLimit(rpm=3_500, rpd=0, tpm=80_000),
    RateLimit(rpm=3_500, rpd=0, tpm=160_000),
    RateLimit(rpm=10_000, rpd=0, tpm=1_000_000),
    RateLimit(rpm=10_000, rpd=0, tpm=2_000_000),
]

gpt_4_limits = [
    RateLimit(rpm=-1, rpd=-1, tpm=-1),
    RateLimit(rpm=500, rpd=10_000, tpm=10_000),
    RateLimit(rpm=5_000, rpd=0, tpm=40_000),
    RateLimit(rpm=5_000, rpd=0, tpm=80_000),
    RateLimit(rpm=10_000, rpd=0, tpm=300_000),
    RateLimit(rpm=10_000, rpd=0, tpm=300_000),
]

gpt_4_turbo_limits = [
    RateLimit(rpm=-1, rpd=-1, tpm=-1),
    RateLimit(rpm=500, rpd=0, tpm=300_000),
    RateLimit(rpm=5_000, rpd=0, tpm=450_000),
    RateLimit(rpm=5_000, rpd=0, tpm=600_000),
    RateLimit(rpm=10_000, rpd=0, tpm=800_000),
    RateLimit(rpm=10_000, rpd=0, tpm=1_500_000),
]


MODEL_LIMITS = [
    ModelLimit.from_rate_limits("gpt-3.5-turbo", 16_385, gpt_3_5_limits),
    ModelLimit.from_rate_limits("gpt-3.5-turbo-0125", 16_385, gpt_3_5_limits),
    ModelLimit.from_rate_limits("gpt-3.5-turbo-0613", 4_096, gpt_3_5_limits),
    ModelLimit.from_rate_limits("gpt-3.5-turbo-1106", 16_385, gpt_3_5_limits),
    ModelLimit.from_rate_limits("gpt-3.5-turbo-16k", 16_385, gpt_3_5_limits),
    ModelLimit.from_rate_limits("gpt-4", 8_192, gpt_4_limits),
    ModelLimit.from_rate_limits("gpt-4-0613", 8_192, gpt_4_limits),
    ModelLimit.from_rate_limits("gpt-4-turbo-preview", 128_000, gpt_4_turbo_limits),
    ModelLimit.from_rate_limits("gpt-4-0125-preview", 128_000, gpt_4_turbo_limits),
    ModelLimit.from_rate_limits("gpt-4-1106-preview", 128_000, gpt_4_turbo_limits),
]
