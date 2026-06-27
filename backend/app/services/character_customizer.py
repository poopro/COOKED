from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .oasis_profile_generator import OasisAgentProfile

PLATFORM_ENTITY_TYPES = {
    "x", "twitter", "tweet", "tweets", "reddit", "subreddit", "threads",
    "tiktok", "youtube", "instagram", "facebook", "linkedin", "producthunt",
    "product_hunt", "hackernews", "hacker_news", "hn", "discord", "telegram",
    "social", "socialmedia", "social_media", "social platform", "platform",
}

DEFAULT_PLATFORM_TAGS = ["Reddit", "X/Twitter", "Threads", "Product Hunt"]


def _clamp_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(minimum, min(maximum, number))


def _clean_tag(value: Any) -> str:
    return str(value or "").strip()[:40]


def normalize_platform_tags(raw: Any) -> List[str]:
    if isinstance(raw, str):
        items = [part.strip() for part in raw.split(",")]
    elif isinstance(raw, Sequence):
        items = [_clean_tag(item) for item in raw]
    else:
        items = []

    seen = set()
    tags: List[str] = []
    for item in items:
        if not item:
            continue
        key = item.lower()
        if key not in seen:
            seen.add(key)
            tags.append(item)
    return tags or list(DEFAULT_PLATFORM_TAGS)


def normalize_character_settings(raw: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    raw = raw or {}
    customer_count = _clamp_int(raw.get("customer_count"), 24, 0, 200)
    vendor_count = _clamp_int(raw.get("vendor_count"), 4, 0, 80)
    other_count = _clamp_int(raw.get("other_count"), 8, 0, 120)
    custom_archetypes = raw.get("custom_archetypes") or []
    if isinstance(custom_archetypes, str):
        custom_archetypes = [custom_archetypes]
    custom_archetypes = [_clean_tag(item) for item in custom_archetypes if _clean_tag(item)][:24]
    platform_tags = normalize_platform_tags(raw.get("platform_tags"))
    target = raw.get("target_profile_count")
    if target is None:
        target_count = customer_count + vendor_count + other_count + len(custom_archetypes)
    else:
        target_count = _clamp_int(target, customer_count + vendor_count + other_count + len(custom_archetypes), 1, 240)
    if target_count < 1:
        target_count = 1
    return {
        "customer_count": customer_count,
        "vendor_count": vendor_count,
        "other_count": other_count,
        "custom_archetypes": custom_archetypes,
        "platform_tags": platform_tags,
        "target_profile_count": target_count,
    }


def filter_platform_entity_types(entity_types: Optional[Sequence[str]]) -> Optional[List[str]]:
    if entity_types is None:
        return None
    filtered: List[str] = []
    seen = set()
    for item in entity_types:
        label = str(item or "").strip()
        if not label:
            continue
        normalized = re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")
        compact = normalized.replace("_", "")
        if normalized in PLATFORM_ENTITY_TYPES or compact in PLATFORM_ENTITY_TYPES:
            continue
        if label.lower() not in seen:
            seen.add(label.lower())
            filtered.append(label)
    return filtered


def desired_total(settings: Dict[str, Any]) -> int:
    return _clamp_int(settings.get("target_profile_count"), 36, 1, 240)


def _profile_role(index: int, settings: Dict[str, Any]) -> Tuple[str, str, str]:
    customer_count = settings.get("customer_count", 0)
    vendor_count = settings.get("vendor_count", 0)
    other_count = settings.get("other_count", 0)
    custom_archetypes = settings.get("custom_archetypes") or []

    if index < customer_count:
        role = "Customer"
        profession = "潛在客戶"
        persona = "像真實公眾使用者一樣反應，關心痛點、信任、定價與是否會推薦給朋友。"
    elif index < customer_count + vendor_count:
        role = "Vendor"
        profession = "競品 / Vendor"
        persona = "競品視角：專挑定位、護城河、可複製性與 GTM 破口。"
    elif index < customer_count + vendor_count + other_count:
        role = "Public"
        profession = ["VC 觀察員", "運營者", "創作者", "重度使用者", "懷疑論者"][index % 5]
        persona = "一個有明確偏見的公共市場觀察者，會依選定平台標籤發言。"
    else:
        custom_index = index - customer_count - vendor_count - other_count
        label = custom_archetypes[custom_index % len(custom_archetypes)] if custom_archetypes else "自訂公共角色"
        role = "Custom"
        profession = label
        persona = f"自訂角色：{label}。以狀態鮮明的公共聲音發言，不是社群平台實體。"
    return role, profession, persona


def _make_profile(index: int, settings: Dict[str, Any]) -> OasisAgentProfile:
    role, profession, persona = _profile_role(index, settings)
    tags = settings.get("platform_tags") or DEFAULT_PLATFORM_TAGS
    username = f"{role.lower()}_{index + 1:03d}"
    return OasisAgentProfile(
        user_id=index + 1,
        user_name=username,
        name=f"{role} #{index + 1}",
        bio=f"COOKED? 市場推演的 {role} 聲音。發言平台：{', '.join(tags[:5])}?",
        persona=persona,
        karma=800 + (index * 137) % 9000,
        friend_count=80 + (index * 17) % 900,
        follower_count=120 + (index * 41) % 12000,
        statuses_count=200 + (index * 29) % 5000,
        age=18 + (index * 7) % 38,
        gender=None,
        mbti=["INTJ", "ENTP", "ISFJ", "ENFP", "ISTP", "ENTJ"][index % 6],
        country=["Taiwan", "US", "Japan", "Singapore", "UK", "Canada"][index % 6],
        profession=profession,
        interested_topics=[profession, role, *tags[:6]],
        source_entity_uuid=f"custom_{role.lower()}_{index + 1}",
        source_entity_type=role,
    )


def apply_character_mix(profiles: List[OasisAgentProfile], settings: Dict[str, Any]) -> List[OasisAgentProfile]:
    target = desired_total(settings)
    mixed = list(profiles[:target])
    tags = settings.get("platform_tags") or DEFAULT_PLATFORM_TAGS

    for index, profile in enumerate(mixed):
        role, profession, persona = _profile_role(index, settings)
        profile.source_entity_type = role
        if not profile.profession:
            profile.profession = profession
        if profile.interested_topics:
            merged = list(dict.fromkeys([*profile.interested_topics, *tags[:6]]))
            profile.interested_topics = merged
        else:
            profile.interested_topics = [profession, role, *tags[:6]]
        if not profile.persona:
            profile.persona = persona

    while len(mixed) < target:
        mixed.append(_make_profile(len(mixed), settings))

    for index, profile in enumerate(mixed):
        profile.user_id = index + 1
        if not profile.user_name:
            profile.user_name = f"agent_{index + 1:03d}"
    return mixed


def build_initial_cooked_meter(settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    settings = settings or {}
    vendors = int(settings.get("vendor_count") or 0)
    customers = int(settings.get("customer_count") or 0)
    total = max(1, int(settings.get("target_profile_count") or customers + vendors or 1))
    score = 45 + round((vendors / total) * 25)
    return _meter(score, "heuristic", "依角色組成估算的初始壓力")


def _meter(score: int, source: str, reason: str) -> Dict[str, Any]:
    score = max(0, min(100, int(score)))
    if score >= 75:
        label = "COOKED"
    elif score >= 45:
        label = "PARTIALLY COOKED"
    else:
        label = "NOT COOKED YET"
    return {"score": score, "label": label, "reason": reason, "source": source}


def estimate_cooked_meter(simulation: Dict[str, Any], config: Optional[Dict[str, Any]] = None, report_text: str = "") -> Dict[str, Any]:
    config = config or {}
    report_text = report_text or ""
    existing = config.get("cooked_meter") if isinstance(config, dict) else None
    score = int((existing or {}).get("score", 50))
    source = "heuristic"
    reason = "依推演狀態與可用報告估算"

    match = re.search(r"risk[_\s-]*score[^0-9]{0,12}(\d{1,3})", report_text, re.I)
    if match:
        score = int(match.group(1))
        source = "report"
        reason = "從報告偵測到風險分數"
    else:
        lowered = report_text.lower()
        if any(word in lowered for word in ["cooked", "failure", "fail", "risk", "weak", "negative", "reject"]):
            score += 18
            source = "report" if report_text else source
        if any(word in lowered for word in ["safe", "viable", "opportunity", "strong", "positive", "traction"]):
            score -= 12
            source = "report" if report_text else source
        status = str(simulation.get("runner_status") or simulation.get("status") or "").lower()
        if status == "failed":
            score += 25
        elif status == "completed":
            score -= 4
        total = int(simulation.get("total_rounds") or 0)
        current = int(simulation.get("current_round") or 0)
        if total and current < total:
            score += 6

    return _meter(score, source, reason)
