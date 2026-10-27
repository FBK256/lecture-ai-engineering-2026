"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:
    """会話履歴を引き継いで質問し、トークン数と回答を返す。"""

    # 同じchatオブジェクトを使用することで会話履歴を維持する
    response = chat.send_message(question)

    usage = response.usage_metadata

    # 入力トークン数と出力トークン数を表示する
    if usage is not None:
        # 入力トークン数を表示する
        print(f"入力トークン数: {usage.prompt_token_count}")

        # 出力トークン数を表示する
        print(f"出力トークン数: {usage.candidates_token_count}")

    # LLMの回答本文を返す
    return response.text or ""


def main() -> None:
    """対話ループを実行する。"""

    parser = argparse.ArgumentParser(description="会話履歴を保持してLLMに質問する")
    parser.add_argument("question",nargs="?",default=DEFAULT_QUESTION,help="最初の質問（省略時は講座に固有の質問）")
    args = parser.parse_args()

    # APIクライアントを作成する
    client = genai.Client(api_key=get_api_key())

    # 会話セッションを作成する
    # このセッション内では過去の質問と回答が引き継がれる
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print("終了するには exit、quit、または Ctrl+C を入力してください。")
    print()

    # コマンドライン引数の質問を最初の質問として処理する
    question = args.question

    try:
        while True:
            print(f"[質問] {question}")

            # 質問を送信し、回答を表示する
            answer = ask(chat, question)
            print(f"[回答]\n{answer}\n")

            # 次の質問を受け付ける
            question = input("質問を入力してください: ").strip()

            # 終了コマンドを判定する
            if question.lower() in {"exit", "quit"}:
                print("対話を終了します。")
                break

            # 空の質問は送信しない
            if not question:
                continue

    except KeyboardInterrupt:
        # Ctrl+Cで安全に終了する
        print("\n対話を終了します。")

    except errors.APIError as e:
        # Gemini APIのエラーを表示する
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)

    finally:
        # APIクライアントを閉じる
        client.close()


if __name__ == "__main__":
    main()
