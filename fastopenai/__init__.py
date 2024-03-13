tier_list = [
    "free",
    "tier_1",
    "tier_2",
    "tier_3",
    "tier_4",
    "tier_5",
]

gpt_3_5_limits = {
    'tpm': [40_000, 60_000, 80_000, 160_000, 1_000_000, 2_000_000],
    'rpm': [3, 3_500, 3_500, 3_500, 10_000, 10_000],
    'rpd': [200, 10_000, 0, 0, 0, 0],
}

gpt_4_limits = {
    'tpm': [-1, 10_000, 40_000],  # -1 means can't use this model
    'rpm': [-1, 500, 5_000],
    'rpd': [-1, 10_000, 0],  # 0 means unlimited
}

rate_limits = {
    "gpt-3.5-turbo": gpt_3_5_limits,
    "gpt-3.5-turbo-0125": gpt_3_5_limits,
    "gpt-3.5-turbo-0301": gpt_3_5_limits,
    "gpt-3.5-turbo-0613": gpt_3_5_limits,
    "gpt-3.5-turbo-1106": gpt_3_5_limits,
    "gpt-3.5-turbo-16k": gpt_3_5_limits,
    "gpt-3.5-turbo-16k-0125": gpt_3_5_limits,
}
