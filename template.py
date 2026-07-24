"""
K4 — Ngày 1: Khám Phá LLM API (14h00–18h00)
AICB-P1: AI Practical Competency Program, Phase 1

Hướng dẫn:
    1. Làm theo LAB_GUIDE.md — mỗi block có các bước chi tiết và checkpoint.
    2. Điền vào tất cả các chỗ đánh dấu TODO.
    3. KHÔNG đổi chữ ký hàm (tên hàm, tham số).
    4. Import OpenAI BÊN TRONG hàm (xem gợi ý) — nếu import ở đầu file,
       các bài test mock sẽ không hoạt động.
    5. Kiểm tra tiến độ:  pytest tests/test_part1.py -v  (từng phần)
       Chấm điểm tổng:    python grade.py
"""

import os
import time
from typing import Any, Callable

from dotenv import load_dotenv

# Nạp OPENAI_API_KEY từ file .env (copy .env.example thành .env và dán key vào)
load_dotenv()

# ---------------------------------------------------------------------------
# Bảng giá ước tính (USD / 1K token) — cập nhật nếu giá thay đổi
# ---------------------------------------------------------------------------
PRICING_PER_1K_TOKENS = {
    "gpt-4o": {"input": 0.0025, "output": 0.010},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gemini-2.5-flash": {"input": 0.0003, "output": 0.0025},
    "gemini-2.5-flash-lite": {"input": 0.0001, "output": 0.0004},
}

# Luồng chính: OpenAI (mặc định, không cần đặt gì trong .env).
# Không có key OpenAI? Dùng luồng thay thế Google Gemini (Phụ lục B
# trong LAB_GUIDE.md) — tên model đổi qua .env. NVIDIA NIM: Phụ lục C.
OPENAI_MODEL = os.getenv("LAB_MODEL", "gpt-4o")
OPENAI_MINI_MODEL = os.getenv("LAB_MINI_MODEL", "gpt-4o-mini")


# ===========================================================================
# PART 1 — API CƠ BẢN (Block 1: 15h00–15h40)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 1.1 — Gọi GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi OpenAI Chat Completions API, trả về nội dung phản hồi + độ trễ.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start_time
    response_text = response.choices[0].message.content or ""
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 1.2 — Gọi GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi API với model gpt-4o-mini — nhanh hơn và rẻ hơn.
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 1.3 — So sánh GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Gọi cả hai model với cùng một prompt và trả về dict so sánh.
    """
    gpt4o_answer, gpt4o_time = call_openai(prompt)
    mini_answer, mini_time = call_openai_mini(prompt)

    pricing = PRICING_PER_1K_TOKENS.get(
        OPENAI_MODEL, PRICING_PER_1K_TOKENS["gpt-4o"]
    )
    gpt4o_cost = (len(gpt4o_answer.split()) / 0.75) / 1000 * pricing["output"]

    return {
        "gpt4o_answer": gpt4o_answer,
        "mini_answer": mini_answer,
        "gpt4o_time": gpt4o_time,
        "mini_time": mini_time,
        "gpt4o_cost": gpt4o_cost,
    }


# ===========================================================================
# PART 2 — SYSTEM PROMPT & TOKEN (Block 2: 15h40–16h20)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 2.1 — Chat với system prompt (persona)
# ---------------------------------------------------------------------------
def chat_with_system_prompt(
    system_prompt: str,
    user_prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Gọi API với MESSAGES gồm 2 phần: system prompt và user prompt.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    start_time = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    latency = time.time() - start_time
    response_text = response.choices[0].message.content or ""
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 2.2 — Đếm token bằng tiktoken
# ---------------------------------------------------------------------------
def count_tokens(text: str, model: str = OPENAI_MODEL) -> int:
    """
    Đếm số token của một đoạn text bằng thư viện tiktoken.
    """
    try:
        import tiktoken

        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
    except Exception:
        return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Task 2.3 — Ước tính chi phí chính xác
# ---------------------------------------------------------------------------
def estimate_cost(prompt: str, response: str, model: str = OPENAI_MODEL) -> dict:
    """
    Tính chi phí một lượt gọi API dựa trên số token THẬT.
    """
    pricing = PRICING_PER_1K_TOKENS.get(
        model, PRICING_PER_1K_TOKENS["gpt-4o"]
    )
    prompt_tokens = count_tokens(prompt, model)
    completion_tokens = count_tokens(response, model)

    prompt_cost = (prompt_tokens / 1000) * pricing["input"]
    completion_cost = (completion_tokens / 1000) * pricing["output"]
    total_cost = prompt_cost + completion_cost

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "prompt_cost": prompt_cost,
        "completion_cost": completion_cost,
        "total_cost": total_cost,
    }


# ===========================================================================
# PART 3 — STREAMING & ĐỘ BỀN (Block 3: 16h30–17h10)
# ===========================================================================

# ---------------------------------------------------------------------------
# Task 3.1 — Chatbot streaming có lịch sử hội thoại
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Chatbot dòng lệnh tương tác dùng streaming.

    Hành vi:
        - Stream token từ OpenAI ngay khi chúng được sinh ra (in từng chunk).
        - Duy trì 4 lượt hội thoại gần nhất trong history.
        - Gõ 'quit', 'exit' hoặc 'bye' để thoát.

    Gợi ý:
        - Giữ list `history` gồm các dict {"role": ..., "content": ...}.
        - Dùng stream=True trong client.chat.completions.create() và lặp:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - Sau mỗi lượt, thêm phản hồi assistant vào history.
        - Cắt history còn 4 lượt cuối (8 message): history = history[-8:]
    """
def streaming_chatbot() -> None:
    """
    Chatbot dòng lệnh tương tác dùng streaming.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []
    print("=== Chatbot Streaming (gõ 'quit', 'exit', 'bye' để thoát) ===")
    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.strip().lower() in ("quit", "exit", "bye"):
            print("Tạm biệt!")
            break

        messages = history + [{"role": "user", "content": user_input}]
        response_stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            stream=True,
        )
        print("Bot: ", end="", flush=True)
        assistant_reply = ""
        for chunk in response_stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                print(delta, end="", flush=True)
                assistant_reply += delta
        print()

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": assistant_reply})
        history = history[-8:]


# ---------------------------------------------------------------------------
# Task 3.2 — Retry với exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Gọi fn(). Nếu ném exception, thử lại tối đa max_retries lần với
    exponential backoff (delay = base_delay * 2^attempt).
    """
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries:
                raise e
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)


# ===========================================================================
# PART 4 — MINI-PROJECT: TRỢ LÝ CLI HOÀN CHỈNH (Block 4: 17h10–17h50)
# ===========================================================================
def run_assistant(
    persona: str,
    get_input: Callable[[], str] = None,
    max_turns: int = None,
) -> dict:
    """
    Trợ lý CLI hoàn chỉnh — ghép mọi thứ bạn đã xây trong Part 1–3.
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if get_input is None:
        get_input = input

    history = []
    turns = 0
    tokens_used = 0
    total_cost = 0.0

    while True:
        if max_turns is not None and turns >= max_turns:
            break

        try:
            user_msg = get_input()
        except (EOFError, KeyboardInterrupt, StopIteration):
            break

        if user_msg.strip().lower() in ("quit", "exit", "bye"):
            break

        messages = [{"role": "system", "content": persona}] + history + [
            {"role": "user", "content": user_msg}
        ]

        def _call_api():
            return client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                stream=True,
            )

        stream = retry_with_backoff(_call_api)
        assistant_reply = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                print(delta, end="", flush=True)
                assistant_reply += delta

        turns += 1

        cost_dict = estimate_cost(user_msg, assistant_reply, OPENAI_MODEL)
        tokens_used += cost_dict["prompt_tokens"] + cost_dict["completion_tokens"]
        total_cost += cost_dict["total_cost"]

        history.append({"role": "user", "content": user_msg})
        history.append({"role": "assistant", "content": assistant_reply})
        history = history[-8:]

    return {
        "turns": turns,
        "tokens_used": tokens_used,
        "total_cost": total_cost,
        "history": history,
    }


# ===========================================================================
# BONUS (không bắt buộc — cho bạn nào xong sớm)
# ===========================================================================
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Chạy compare_models cho từng prompt trong list.
    """
    results = []
    for prompt in prompts:
        res = compare_models(prompt)
        res["prompt"] = prompt
        results.append(res)
    return results


def format_comparison_table(results: list[dict]) -> str:
    """
    Định dạng kết quả batch_compare thành bảng text dễ đọc.
    """
    header = f"{'Prompt':<40} | {'GPT-4o Answer':<40} | {'Mini Answer':<40} | {'4o Time (s)':<12} | {'Mini Time (s)':<12}"
    divider = "-" * len(header)
    rows = [header, divider]
    for r in results:
        p = (r['prompt'][:37] + '...') if len(r['prompt']) > 40 else r['prompt']
        a4o = (r['gpt4o_answer'][:37] + '...') if len(r['gpt4o_answer']) > 40 else r['gpt4o_answer']
        am = (r['mini_answer'][:37] + '...') if len(r['mini_answer']) > 40 else r['mini_answer']
        t4o = f"{r['gpt4o_time']:.2f}"
        tm = f"{r['mini_time']:.2f}"
        rows.append(f"{p:<40} | {a4o:<40} | {am:<40} | {t4o:<12} | {tm:<12}")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Entry point — demo chạy thật (cần OPENAI_API_KEY)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("==================================================")
    print("PART 1: SO SÁNH MODEL")
    print("==================================================")
    result = compare_models(
        "Giải thích khác biệt giữa temperature và top_p trong một câu."
    )
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n==================================================")
    print("PART 2: DEMO SYSTEM PROMPT, TOKEN & CHI PHÍ")
    print("==================================================")
    sys_prompt = "Bạn là giáo viên tiểu học thân thiện, giải thích mọi thứ thật dễ hiểu."
    usr_prompt = "Máy học (Machine Learning) là gì?"
    resp_text, lat = chat_with_system_prompt(sys_prompt, usr_prompt)
    tok_count = count_tokens(usr_prompt + " " + resp_text)
    cost_info = estimate_cost(usr_prompt, resp_text)

    print(f"System Prompt: {sys_prompt}")
    print(f"User Prompt  : {usr_prompt}")
    print(f"Response     : {resp_text}")
    print(f"Latency      : {lat:.3f}s")
    print(f"Tokens Count : {tok_count}")
    print(f"Cost Detail  : {cost_info}")

    print("\n==================================================")
    print("PART 3 & 4: TRỢ LÝ CLI (gõ 'quit' để thoát)")
    print("==================================================")
    stats = run_assistant(
        persona="Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn gọn bằng tiếng Việt.",
    )
    print("\n--- Thống kê phiên chat ---")
    for key, value in stats.items():
        if key != "history":
            print(f"{key}: {value}")

