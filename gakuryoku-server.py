#!/usr/bin/env python3
"""全国学力調査 予想問題 採点サーバー"""

import http.server
import json
import subprocess
import os
import urllib.parse
from datetime import datetime

PORT = 8788

# 正解データ（選択肢・計算問題）
ANSWERS = {
    # 算数
    "math_1_1": {"type": "choice", "answer": "2", "point": 5},
    "math_1_2": {"type": "exact", "answer": "36", "unit": "L", "point": 5},
    "math_1_3": {"type": "exact", "answer": "18", "unit": "本", "point": 5},
    "math_1_4": {"type": "exact", "answer": "3", "unit": "箱", "point": 5},
    "math_1_5": {"type": "descriptive", "point": 10,
                 "criteria": "420人×3L×3日=3780L、3780÷2=1890本。式と言葉の両方で求め方を説明できているか。部分点あり。"},
    "math_2_1": {"type": "exact", "answer": "30", "unit": "cm2", "point": 5},
    "math_2_2": {"type": "descriptive", "point": 10,
                 "criteria": "六角形を2つの図形に分けて、それぞれの面積を公式で求めている。分け方を明示し、式と計算結果を書いている。"},
    "math_2_3": {"type": "multi_choice", "answer": ["1","3","4","5"], "point": 5},
    "math_3_1": {"type": "fraction", "answer": "17/12", "alt": ["1と5/12"], "point": 5},
    "math_3_2": {"type": "exact", "answer": "0.01", "point": 5},
    "math_3_3a": {"type": "fraction", "answer": "1/4", "point": 3},
    "math_3_3b": {"type": "fraction", "answer": "7/4", "alt": ["1と3/4"], "point": 3},
    "math_4_1": {"type": "exact", "answer": "270", "unit": "人", "point": 5},
    "math_4_2": {"type": "descriptive", "point": 10,
                 "criteria": "各サイズの1Lあたりの値段を求めて比較している。小:0.5円、中:約0.42円、大:0.4円で大サイズが最安。"},
    "math_4_3": {"type": "exact", "answer": "100", "unit": "回", "point": 5},
    "math_4_4": {"type": "choice", "answer": "2", "point": 5},
    # 国語
    "kokugo_1_1": {"type": "choice", "answer": "1", "point": 5},
    "kokugo_1_2": {"type": "choice", "answer": "2", "point": 5},
    "kokugo_1_3": {"type": "choice", "answer": "3", "point": 5},
    "kokugo_2_1": {"type": "choice", "answer": "1", "point": 5},
    "kokugo_2_2a": {"type": "kanji", "answer": "危険", "point": 3},
    "kokugo_2_2b": {"type": "kanji", "answer": "確認", "point": 3},
    "kokugo_2_3": {"type": "descriptive", "point": 15,
                   "criteria": "【メモ】から言葉や文を取り上げている。60字以上100字以内。防災マップの利点を具体的に書いている。"},
    "kokugo_3_1": {"type": "choice", "answer": "2", "point": 5},
    "kokugo_3_2": {"type": "descriptive", "point": 15,
                   "criteria": "【資料1】【資料2】から言葉や文を取り上げている。80字以上120字以内。なっとくしたことと理由を書いている。"},
}

def grade_simple(qid, user_answer):
    """選択肢・計算問題の採点"""
    if qid not in ANSWERS:
        return {"score": 0, "max": 0, "feedback": "問題IDが不明です。"}

    q = ANSWERS[qid]
    user_answer = user_answer.strip()
    max_point = q["point"]

    if q["type"] == "choice":
        correct = user_answer == q["answer"]
        return {
            "score": max_point if correct else 0,
            "max": max_point,
            "correct": correct,
            "feedback": "正解！" if correct else f"不正解。正解は {q['answer']} です。"
        }

    elif q["type"] == "exact":
        # 数値の比較（単位を除去）
        clean = user_answer.replace("L","").replace("本","").replace("箱","").replace("人","").replace("回","").replace("円","").replace("cm2","").replace("cm²","").strip()
        correct = clean == q["answer"]
        return {
            "score": max_point if correct else 0,
            "max": max_point,
            "correct": correct,
            "feedback": "正解！" if correct else f"不正解。正解は {q['answer']}{q.get('unit','')} です。"
        }

    elif q["type"] == "multi_choice":
        user_set = set(user_answer.replace(" ","").replace(",","").replace("、",""))
        answer_set = set(q["answer"])
        correct = user_set == answer_set
        return {
            "score": max_point if correct else 0,
            "max": max_point,
            "correct": correct,
            "feedback": "正解！" if correct else f"不正解。正解は {','.join(q['answer'])} です。"
        }

    elif q["type"] == "fraction":
        # 分数の比較
        clean = user_answer.strip()
        correct = clean == q["answer"] or clean in q.get("alt", [])
        return {
            "score": max_point if correct else 0,
            "max": max_point,
            "correct": correct,
            "feedback": "正解！" if correct else f"不正解。正解は {q['answer']} です。"
        }

    elif q["type"] == "kanji":
        correct = user_answer.strip() == q["answer"]
        return {
            "score": max_point if correct else 0,
            "max": max_point,
            "correct": correct,
            "feedback": "正解！" if correct else f"不正解。正解は「{q['answer']}」です。"
        }

    return {"score": 0, "max": max_point, "feedback": "採点できませんでした。"}


def grade_descriptive(qid, user_answer):
    """記述問題のAI採点"""
    if qid not in ANSWERS:
        return {"score": 0, "max": 0, "feedback": "問題IDが不明です。"}

    q = ANSWERS[qid]
    max_point = q["point"]

    if not user_answer or len(user_answer.strip()) < 5:
        return {"score": 0, "max": max_point, "feedback": "回答が短すぎます。もう少し詳しく書きましょう。"}

    prompt = f"""あなたは小学6年生の全国学力調査の採点者です。以下の記述問題の回答を採点してください。

【採点基準】
{q['criteria']}

【配点】{max_point}点

【生徒の回答】
{user_answer}

以下のJSON形式で回答してください。他の文字は一切含めないでください：
{{"score": 点数(0-{max_point}の整数), "feedback": "具体的なフィードバック(50字以内)"}}"""

    try:
        result = subprocess.run(
            ["claude", "--print"],
            input=prompt,
            capture_output=True, text=True, timeout=60
        )
        output = result.stdout.strip()
        # JSON部分を抽出
        start = output.find("{")
        end = output.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(output[start:end])
            return {
                "score": min(int(data.get("score", 0)), max_point),
                "max": max_point,
                "feedback": data.get("feedback", "採点完了")
            }
    except Exception as e:
        print(f"AI grading error: {e}")

    return {"score": 0, "max": max_point, "feedback": "AI採点中にエラーが発生しました。もう一度お試しください。"}


class GradeHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/grade":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.requestfile.read(content_length) if hasattr(self, 'requestfile') else self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            qid = data.get("qid", "")
            answer = data.get("answer", "")
            q = ANSWERS.get(qid, {})

            if q.get("type") == "descriptive":
                result = grade_descriptive(qid, answer)
            else:
                result = grade_simple(qid, answer)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))

        elif self.path == "/api/grade-all":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            answers = data.get("answers", {})
            results = {}
            total_score = 0
            total_max = 0

            for qid, answer in answers.items():
                q = ANSWERS.get(qid, {})
                if q.get("type") == "descriptive":
                    r = grade_descriptive(qid, answer)
                else:
                    r = grade_simple(qid, answer)
                results[qid] = r
                total_score += r.get("score", 0)
                total_max += r.get("max", 0)

            response = {
                "results": results,
                "total_score": total_score,
                "total_max": total_max,
                "percentage": round(total_score / total_max * 100, 1) if total_max > 0 else 0,
                "timestamp": datetime.now().isoformat()
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.path = "/docs/gakuryoku-yosou-2026.html"
        super().do_GET()

    def translate_path(self, path):
        return os.path.join("/Users/yuika/Desktop", path.lstrip("/"))


if __name__ == "__main__":
    print(f"採点サーバー起動: http://localhost:{PORT}")
    print(f"問題数: {len(ANSWERS)}問")
    print(f"記述問題: {sum(1 for q in ANSWERS.values() if q['type'] == 'descriptive')}問（AI採点）")
    server = http.server.HTTPServer(("", PORT), GradeHandler)
    server.serve_forever()
