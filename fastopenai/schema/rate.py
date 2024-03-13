from dataclasses import dataclass
from typing import Dict, List


@dataclass
class RateLimit:
    # -1 means can't use this model
    # 0 means unlimited
    rpm: int
    rpd: int
    tpm: int

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            rpm=d['rpm'],
            rpd=d['rpd'],
            tpm=d['tpm'],
        )


@dataclass
class ModelLimit:
    model_name: str
    free: RateLimit
    tier_1: RateLimit
    tier_2: RateLimit
    tier_3: RateLimit
    tier_4: RateLimit
    tier_5: RateLimit

    @classmethod
    def from_list(cls, model_name: str, lst: List[Dict]):
        return cls(
            model_name=model_name,
            free=RateLimit.from_dict(lst[0]),
            tier_1=RateLimit.from_dict(lst[1]),
            tier_2=RateLimit.from_dict(lst[2]),
            tier_3=RateLimit.from_dict(lst[3]),
            tier_4=RateLimit.from_dict(lst[4]),
            tier_5=RateLimit.from_dict(lst[5]),
        )

    @classmethod
    def from_rate_limits(cls, model_name: str, lst: List[RateLimit]):
        return cls(
            model_name=model_name,
            free=lst[0],
            tier_1=lst[1],
            tier_2=lst[2],
            tier_3=lst[3],
            tier_4=lst[4],
            tier_5=lst[5],
        )
