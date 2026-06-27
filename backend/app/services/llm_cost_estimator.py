"""LLM cost estimation for OpenRouter-compatible simulation runs.

Prices are stored as USD per 1M tokens. Live OpenRouter prices are preferred;
static prices are only fallbacks and are intentionally conservative.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger("mirofish.cost.estimator")

KNOWN_MODELS: Dict[str, Dict[str, Any]] = {
    # Free / rate-limited OpenRouter options. Best for demos and rough tests.
    "qwen/qwen3-next-80b-a3b-instruct:free": {"name": "Qwen3 Next 80B A3B Instruct (free)", "input": 0.0, "output": 0.0, "tier": "free"},
    "meta-llama/llama-3.3-70b-instruct:free": {"name": "Llama 3.3 70B Instruct (free)", "input": 0.0, "output": 0.0, "tier": "free"},
    "openai/gpt-oss-120b:free": {"name": "OpenAI gpt-oss-120b (free)", "input": 0.0, "output": 0.0, "tier": "free"},
    "openai/gpt-oss-20b:free": {"name": "OpenAI gpt-oss-20b (free)", "input": 0.0, "output": 0.0, "tier": "free"},
    "nousresearch/hermes-3-llama-3.1-405b:free": {"name": "Nous Hermes 3 405B (free)", "input": 0.0, "output": 0.0, "tier": "free"},
    "nvidia/nemotron-3-super-120b-a12b:free": {"name": "NVIDIA Nemotron 3 Super (free)", "input": 0.0, "output": 0.0, "tier": "free"},

    # Ultra-cheap current OpenRouter options. More reliable than free, still cheap.
    "inclusionai/ling-2.6-flash": {"name": "Ling 2.6 Flash", "input": 0.01, "output": 0.03, "tier": "ultra_cheap"},
    "deepseek/deepseek-v4-flash": {"name": "DeepSeek V4 Flash", "input": 0.089, "output": 0.224, "tier": "ultra_cheap"},
    "qwen/qwen3.5-9b": {"name": "Qwen3.5 9B", "input": 0.10, "output": 0.15, "tier": "ultra_cheap"},
    "poolside/laguna-xs.2": {"name": "Poolside Laguna XS.2", "input": 0.10, "output": 0.20, "tier": "ultra_cheap"},
    "google/gemma-4-26b-a4b-it": {"name": "Gemma 4 26B A4B", "input": 0.06, "output": 0.33, "tier": "ultra_cheap"},

    # Cheap stable options.
    "google/gemini-3.1-flash-lite": {"name": "Gemini 3.1 Flash Lite", "input": 0.25, "output": 1.50, "tier": "cheap"},
    "qwen/qwen3.6-flash": {"name": "Qwen3.6 Flash", "input": 0.1875, "output": 1.125, "tier": "cheap"},
    "nex-agi/nex-n2-pro": {"name": "Nex-N2-Pro", "input": 0.25, "output": 1.00, "tier": "cheap"},
    "google/gemini-2.5-flash-lite": {"name": "Gemini 2.5 Flash Lite", "input": 0.10, "output": 0.40, "tier": "cheap"},
    "openai/gpt-4o-mini": {"name": "GPT-4o mini", "input": 0.15, "output": 0.60, "tier": "cheap"},
    "deepseek/deepseek-chat": {"name": "DeepSeek Chat", "input": 0.27, "output": 1.10, "tier": "cheap"},
    "mistralai/mistral-small-2603": {"name": "Mistral Small 4", "input": 0.15, "output": 0.60, "tier": "cheap"},

    # Balanced options for better quality.
    "google/gemini-2.5-flash": {"name": "Gemini 2.5 Flash", "input": 0.30, "output": 2.50, "tier": "balanced"},
    "qwen/qwen-2.5-72b-instruct": {"name": "Qwen 2.5 72B Instruct", "input": 0.35, "output": 0.40, "tier": "balanced"},
    "meta-llama/llama-3.3-70b-instruct": {"name": "Llama 3.3 70B Instruct", "input": 0.59, "output": 0.79, "tier": "balanced"},
    "openai/gpt-5.4-nano": {"name": "GPT-5.4 Nano", "input": 0.20, "output": 1.25, "tier": "balanced"},

    # Premium synthesis options.
    "z-ai/glm-5.2": {"name": "GLM 5.2", "input": 0.95, "output": 3.00, "tier": "premium"},
    "moonshotai/kimi-k2.7-code": {"name": "Kimi K2.7 Code", "input": 0.74, "output": 3.50, "tier": "premium"},
    "openai/gpt-4.1": {"name": "GPT-4.1", "input": 2.00, "output": 8.00, "tier": "premium"},
    "anthropic/claude-fable-5": {"name": "Claude Fable 5", "input": 10.00, "output": 50.00, "tier": "premium"},
}

ALIASES: Dict[str, str] = {
    "free-qwen": "qwen/qwen3-next-80b-a3b-instruct:free",
    "free-llama": "meta-llama/llama-3.3-70b-instruct:free",
    "free-gpt-oss": "openai/gpt-oss-120b:free",
    "free-nous": "nousresearch/hermes-3-llama-3.1-405b:free",
    "ling-flash": "inclusionai/ling-2.6-flash",
    "deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "qwen3.5-9b": "qwen/qwen3.5-9b",
    "gemini-3.1-flash-lite": "google/gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite": "google/gemini-2.5-flash-lite",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "deepseek-chat": "deepseek/deepseek-chat",
    "gpt-4.1": "openai/gpt-4.1",
}

PER_CALL_TOKENS = {
    "input_low": 1200,
    "input_mid": 2200,
    "input_high": 3500,
    "output_low": 80,
    "output_mid": 200,
    "output_high": 400,
}

TOOL_CALL_FACTOR_LOW = 1.0
TOOL_CALL_FACTOR_MID = 1.3
TOOL_CALL_FACTOR_HIGH = 1.6
GRAPH_MEMORY_INPUT_BUMP = 0.20
GRAPH_MEMORY_OUTPUT_BUMP = 0.10
_OPENROUTER_TTL_SEC = 30 * 60
_OPENROUTER_CACHE: Dict[str, Any] = {"fetched_at": 0.0, "by_id": {}}


@dataclass
class RoundsEstimate:
    total_rounds_config: int
    effective_rounds: int
    total_decisions_one_platform: float


def _fetch_openrouter_models() -> Dict[str, Dict[str, float]]:
    now = time.time()
    if _OPENROUTER_CACHE["by_id"] and now - _OPENROUTER_CACHE["fetched_at"] < _OPENROUTER_TTL_SEC:
        return _OPENROUTER_CACHE["by_id"]

    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get("https://openrouter.ai/api/v1/models")
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("OpenRouter pricing fetch failed; using static fallback: %s", exc)
        return {}

    by_id: Dict[str, Dict[str, float]] = {}
    for item in data.get("data", []):
        model_id = item.get("id")
        pricing = item.get("pricing") or {}
        try:
            prompt_per_token = float(pricing.get("prompt", 0) or 0)
            completion_per_token = float(pricing.get("completion", 0) or 0)
        except (TypeError, ValueError):
            continue
        if model_id:
            by_id[model_id] = {
                "input": prompt_per_token * 1_000_000,
                "output": completion_per_token * 1_000_000,
            }

    _OPENROUTER_CACHE["by_id"] = by_id
    _OPENROUTER_CACHE["fetched_at"] = now
    logger.info("OpenRouter pricing cache updated: %s models", len(by_id))
    return by_id


def _normalize_model_id(raw: str) -> str:
    if not raw:
        return ""
    raw = raw.strip()
    if raw in KNOWN_MODELS:
        return raw
    if raw in ALIASES:
        return ALIASES[raw]
    if "/" not in raw and f"openai/{raw}" in KNOWN_MODELS:
        return f"openai/{raw}"
    return raw


def _resolve_pricing(model_id: str) -> Tuple[float, float, str]:
    normalized = _normalize_model_id(model_id)
    live = _fetch_openrouter_models()
    if normalized in live:
        prc = live[normalized]
        return float(prc["input"]), float(prc["output"]), "openrouter"
    if normalized in KNOWN_MODELS:
        prc = KNOWN_MODELS[normalized]
        return float(prc["input"]), float(prc["output"]), "fallback_static"
    return 0.0, 0.0, "unknown"


def _avg_activity_filter(agent_configs: List[Dict[str, Any]]) -> float:
    if not agent_configs:
        return 0.5
    levels: List[float] = []
    for cfg in agent_configs:
        try:
            levels.append(max(0.0, min(1.0, float(cfg.get("activity_level", 0.5)))))
        except (TypeError, ValueError):
            continue
    return sum(levels) / len(levels) if levels else 0.5


def _estimate_decisions_per_platform(config: Dict[str, Any], max_rounds: Optional[int]) -> RoundsEstimate:
    time_config = config.get("time_config", {})
    agent_configs = config.get("agent_configs", [])

    total_hours = int(time_config.get("total_simulation_hours", 72) or 72)
    minutes_per_round = max(int(time_config.get("minutes_per_round", 60) or 60), 1)
    config_total_rounds = max((total_hours * 60) // minutes_per_round, 0)
    effective_rounds = min(config_total_rounds, max_rounds) if max_rounds and max_rounds > 0 else config_total_rounds

    base_min = float(time_config.get("agents_per_hour_min", 5) or 5)
    base_max = float(time_config.get("agents_per_hour_max", 20) or 20)
    avg_target = (base_min + base_max) / 2.0

    peak_hours = set(time_config.get("peak_hours") or [19, 20, 21, 22])
    off_peak_hours = set(time_config.get("off_peak_hours") or [0, 1, 2, 3, 4, 5])
    peak_mult = float(time_config.get("peak_activity_multiplier", 1.5) or 1.5)
    off_peak_mult = float(time_config.get("off_peak_activity_multiplier", 0.3) or 0.3)

    activity_pass_rate = _avg_activity_filter(agent_configs)
    candidate_count = len(agent_configs)
    total_decisions = 0.0

    for round_idx in range(effective_rounds):
        simulated_hour = ((round_idx * minutes_per_round) // 60) % 24
        if simulated_hour in peak_hours:
            mult = peak_mult
        elif simulated_hour in off_peak_hours:
            mult = off_peak_mult
        else:
            mult = 1.0
        expected_candidates = candidate_count * activity_pass_rate
        total_decisions += max(min(expected_candidates, avg_target * mult), 0.0)

    return RoundsEstimate(config_total_rounds, effective_rounds, total_decisions)


def _compute_usd_for_pricing(
    decisions_total: float,
    input_per_mtok: float,
    output_per_mtok: float,
    graph_memory: bool,
) -> Tuple[float, float, float, Dict[str, Any]]:
    in_bump = 1 + GRAPH_MEMORY_INPUT_BUMP if graph_memory else 1.0
    out_bump = 1 + GRAPH_MEMORY_OUTPUT_BUMP if graph_memory else 1.0

    calls_low = decisions_total * TOOL_CALL_FACTOR_LOW
    calls_mid = decisions_total * TOOL_CALL_FACTOR_MID
    calls_high = decisions_total * TOOL_CALL_FACTOR_HIGH

    in_low = calls_low * PER_CALL_TOKENS["input_low"] * in_bump
    in_mid = calls_mid * PER_CALL_TOKENS["input_mid"] * in_bump
    in_high = calls_high * PER_CALL_TOKENS["input_high"] * in_bump
    out_low = calls_low * PER_CALL_TOKENS["output_low"] * out_bump
    out_mid = calls_mid * PER_CALL_TOKENS["output_mid"] * out_bump
    out_high = calls_high * PER_CALL_TOKENS["output_high"] * out_bump

    usd_low = (in_low / 1_000_000) * input_per_mtok + (out_low / 1_000_000) * output_per_mtok
    usd_mid = (in_mid / 1_000_000) * input_per_mtok + (out_mid / 1_000_000) * output_per_mtok
    usd_high = (in_high / 1_000_000) * input_per_mtok + (out_high / 1_000_000) * output_per_mtok

    return usd_low, usd_mid, usd_high, {
        "input_tokens_low": int(in_low),
        "input_tokens_mid": int(in_mid),
        "input_tokens_high": int(in_high),
        "output_tokens_low": int(out_low),
        "output_tokens_mid": int(out_mid),
        "output_tokens_high": int(out_high),
        "estimated_llm_calls_low": int(calls_low),
        "estimated_llm_calls": int(calls_mid),
        "estimated_llm_calls_high": int(calls_high),
    }


def load_simulation_config_from_disk(simulation_id: str) -> Dict[str, Any]:
    sim_dir = os.path.join(Config.OASIS_SIMULATION_DATA_DIR, simulation_id)
    config_path = os.path.join(sim_dir, "simulation_config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"simulation_config.json not found for {simulation_id}; prepare simulation first")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _platforms_count(platform: str) -> int:
    return 2 if platform == "parallel" else 1


def _build_recommendations(
    selected_id: str,
    decisions_per_platform: float,
    platforms_count: int,
    graph_memory: bool,
    live_pricing: Dict[str, Dict[str, float]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    decisions_total = decisions_per_platform * platforms_count
    rows: List[Dict[str, Any]] = []

    for model_id, info in KNOWN_MODELS.items():
        if model_id == selected_id:
            continue
        input_p = float(info["input"])
        output_p = float(info["output"])
        pricing_src = "fallback_static"
        if model_id in live_pricing:
            input_p = float(live_pricing[model_id]["input"])
            output_p = float(live_pricing[model_id]["output"])
            pricing_src = "openrouter"
        _, usd_mid, _, _ = _compute_usd_for_pricing(decisions_total, input_p, output_p, graph_memory)
        rows.append({
            "id": model_id,
            "name": info["name"],
            "tier": info["tier"],
            "pricing_source": pricing_src,
            "input_per_mtok": round(input_p, 4),
            "output_per_mtok": round(output_p, 4),
            "estimated_usd_mid": round(usd_mid, 3),
        })

    cheaper = [r for r in rows if r["tier"] in ("free", "ultra_cheap", "cheap")]
    cheaper.sort(key=lambda r: (0 if r["tier"] == "free" else 1, r["estimated_usd_mid"], r["output_per_mtok"]))

    premium = [r for r in rows if r["tier"] in ("balanced", "premium")]
    premium.sort(key=lambda r: (r["estimated_usd_mid"], r["output_per_mtok"]))
    return cheaper[:10], premium[:8]


def build_cost_estimate_payload(
    config: Dict[str, Any],
    resolved_model_id: str,
    platform: str,
    max_rounds: Optional[int],
    graph_memory: bool,
) -> Dict[str, Any]:
    rounds_est = _estimate_decisions_per_platform(config, max_rounds)
    plats = _platforms_count(platform)
    decisions_total = rounds_est.total_decisions_one_platform * plats

    in_p, out_p, pricing_source = _resolve_pricing(resolved_model_id)
    if pricing_source == "unknown":
        usd_low = usd_mid = usd_high = 0.0
        breakdown = {
            "estimated_llm_calls_low": int(decisions_total * TOOL_CALL_FACTOR_LOW),
            "estimated_llm_calls": int(decisions_total * TOOL_CALL_FACTOR_MID),
            "estimated_llm_calls_high": int(decisions_total * TOOL_CALL_FACTOR_HIGH),
        }
        disclaimer = "模型不在內建清單，也無法從 OpenRouter 即時取得報價；只顯示決策次數估算。"
    else:
        usd_low, usd_mid, usd_high, breakdown = _compute_usd_for_pricing(decisions_total, in_p, out_p, graph_memory)
        src_note = "OpenRouter 即時報價" if pricing_source == "openrouter" else "內建參考單價"
        gm_note = "，已加上圖譜記憶額外 token" if graph_memory else ""
        disclaimer = (
            f"粗估使用 {src_note}{gm_note}。免費模型通常有速率限制或排隊；正式長跑建議用 ultra-cheap/cheap 模型，"
            "並把 max_rounds 先壓到 5-20 輪做探路。"
        )

    live_pricing = _fetch_openrouter_models() if pricing_source != "unknown" else {}
    cheaper, premium = _build_recommendations(_normalize_model_id(resolved_model_id), rounds_est.total_decisions_one_platform, plats, graph_memory, live_pricing)

    return {
        "resolved_model_id": _normalize_model_id(resolved_model_id) or resolved_model_id,
        "input_per_mtok": round(in_p, 4),
        "output_per_mtok": round(out_p, 4),
        "pricing_source": pricing_source,
        "platform": platform,
        "platforms_count": plats,
        "graph_memory": graph_memory,
        "usd_low": round(usd_low, 3),
        "usd_mid": round(usd_mid, 3),
        "usd_high": round(usd_high, 3),
        "token_estimate": {
            "total_rounds_config": rounds_est.total_rounds_config,
            "effective_rounds": rounds_est.effective_rounds,
            "decisions_per_platform": int(rounds_est.total_decisions_one_platform),
            "platforms_count": plats,
            **breakdown,
        },
        "recommend_cheaper": cheaper,
        "recommend_premium": premium,
        "openrouter_models_url": "https://openrouter.ai/models?max_price=0",
        "disclaimer_zh": disclaimer,
    }
