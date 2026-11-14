#!/usr/bin/env python3
"""Workspace 2.0 router: task description -> model tier, model id, clean session name.

Usage:
  python route.py "task description"            # JSON
  python route.py --table "task one" "task two"  # Markdown table
  python route.py --idle "task"                 # idle session: one tier lower

Deterministic keyword scoring (English + Korean). No network, no dependencies.
"""
import json
import os
import re
import sys

TIERS = ["light", "standard", "deep", "frontier"]

# (tier, weight, keywords). Matching is case-insensitive substring.
RULES = [
    ("light", 3, ["status", "how far", "progress", "percent", "list ", "show me", "side chat", "chat",
                  "what is", "summar", "read the log", "look up", "lookup",
                  "몇퍼", "어디까지", "진행", "상태", "목록", "요약", "잡담", "보여줘", "찾아봐"]),
    ("standard", 3, ["rename", "translat", "upload", "run test", "run the test", "re-run", "rerun",
                     "re-shoot", "reshoot", "form", "fill", "commit", "format", "lint", "bump",
                     "copy", "move file", "export", "package", "screenshot", "localiz", "save",
                     "이름 바꾸", "번역", "올리", "업로드", "시험 돌", "테스트 돌", "다시 찍", "저장",
                     "커밋", "내보내", "패키징", "스크린샷", "옮기", "정리"]),
    ("deep", 3, ["debug", "bug", "fix", "why", "root cause", "design", "refactor", "architect",
                 "review", "pick the best", "choose", "trailer", "edit video", "visual", "look and feel",
                 "optimi", "investigat", "diagnos", "plan",
                 "버그", "고치", "원인", "왜", "설계", "구조", "리팩", "검토", "고르", "트레일러",
                 "편집", "겉모습", "최적화", "조사", "기획"]),
    ("frontier", 4, ["multi-system", "across systems", "failed twice", "keeps failing", "architecture decision",
                     "rewrite the engine", "large-scale", "concurren", "race condition", "deadlock",
                     "physics and ai", "ai and physics", "mass entity",
                     "여러 시스템", "두 번 실패", "계속 실패", "대규모", "동시성", "엔진 구조", "물리와 ai", "ai와 물리"]),
]

CATEGORIES = [
    ("[Bug]", ["bug", "fix", "broken", "crash", "glitch", "rolling over", "버그", "고치", "깨짐", "튕김", "안 됨", "안됨"]),
    ("[Test]", ["test", "verify", "measure", "qa", "benchmark", "시험", "확인", "측정", "검사"]),
    ("[Store]", ["store", "steam", "trailer", "release", "capsule", "스팀", "상점", "트레일러", "출시"]),
    ("[Content]", ["model", "sound", "sfx", "texture", "image", "text", "translat", "rename",
                   "모델", "소리", "텍스처", "그림", "번역", "이름"]),
    ("[Research]", ["research", "investigat", "find out", "compare", "조사", "리서치", "비교", "찾아"]),
    ("[Ops]", ["build", "ci", "package", "deploy", "cleanup", "archive", "빌드", "패키징", "배포", "정리"]),
    ("[Feature]", ["add", "new", "implement", "support", "만들", "추가", "새 ", "넣"]),
]

FILLER = re.compile(r"^(please|can you|could you|i want you to|let's|go ahead and)\s+", re.I)


def load_models():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {k: v for k, v in data.items() if k in TIERS}
    except (OSError, ValueError):
        return {t: t for t in TIERS}


def score(text):
    low = text.lower()
    scores = {t: 0 for t in TIERS}
    hits = {t: [] for t in TIERS}
    for tier, weight, words in RULES:
        for w in words:
            if w in low:
                scores[tier] += weight
                hits[tier].append(w.strip())
    return scores, hits


def pick_tier(text, idle=False):
    scores, hits = score(text)
    if scores["frontier"] >= 4:
        tier = "frontier"
    elif scores["light"] > 0 and len(text) <= 80:
        tier = "light"  # a short status question stays light even if it names a heavy topic
    elif scores["deep"] >= max(scores["standard"], scores["light"]) and scores["deep"] > 0:
        tier = "deep"
    elif scores["standard"] >= scores["light"] and scores["standard"] > 0:
        tier = "standard"
    elif scores["light"] > 0:
        tier = "light"
    else:
        tier = "standard"  # unknown work: safe middle
    # Long, multi-step briefs rarely fit the light tier.
    if tier == "light" and len(text) > 160:
        tier = "standard"
    if idle:
        tier = TIERS[max(0, TIERS.index(tier) - 1)]
    base = TIERS[min(len(TIERS) - 1, TIERS.index(tier) + 1)] if idle else tier
    reason = ", ".join(hits[base][:4]) or "no strong signal: default"
    if idle:
        reason = f"idle, one tier below {base} ({reason})"
    return tier, reason


def make_name(text, limit=45):
    low = text.lower()
    category = "[Task]"
    for cat, words in CATEGORIES:
        if any(w in low for w in words):
            category = cat
            break
    body = FILLER.sub("", text.strip())
    body = re.split(r"(?<=[.!?。])\s|\n|,\s*and\s| and verify| and then|그리고|하고 나서", body)[0]
    body = re.sub(r"\s+", " ", body).strip(" .")
    if body[:1].islower():
        body = body[0].upper() + body[1:]
    room = limit - len(category) - 1
    if len(body) > room:
        cut = body[:room].rsplit(" ", 1)[0]
        body = (cut if len(cut) > room * 0.6 else body[:room]).rstrip(" ,·-") + "…"
    return f"{category} {body}"


def route(text, idle=False):
    models = load_models()
    tier, reason = pick_tier(text, idle)
    return {"tier": tier, "model": models.get(tier, tier), "name": make_name(text), "reason": reason}


def main(argv):
    idle = "--idle" in argv
    table = "--table" in argv
    tasks = [a for a in argv if not a.startswith("--")]
    if not tasks:
        print(__doc__)
        return 1
    results = [route(t, idle) for t in tasks]
    if table:
        print("| Session name | Tier | Model | Why |")
        print("| --- | --- | --- | --- |")
        for r in results:
            print(f"| {r['name']} | {r['tier']} | `{r['model']}` | {r['reason']} |")
    else:
        out = results[0] if len(results) == 1 else results
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
