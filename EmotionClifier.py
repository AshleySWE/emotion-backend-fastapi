from transformers import pipeline
import torch

# 建立情緒分類器（英文模型，中文也能跑，但效果可能稍弱）
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)


def analyze_emotion(note: str):
    # 呼叫模型做分類
    results = classifier(note)[0]
    # 依照分數排序
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    # 取出最高分的情緒
    top_emotion = sorted_results[0]
    return {
        "note": note,
        "emotion": top_emotion['label'],
        "confidence": round(top_emotion['score'], 3),
        "all_scores": sorted_results
    }


# 測試
user_note = "Work for another 3 hours and 59 minutes today Labor laws stipulate: \nFor every 4 hours worked, there should be at least a 30 minute break Every time \nI work overtime I have to be careful not to exceed 4 hours Who has time for that 30 minutes : )"
result = analyze_emotion(user_note)

print("分析結果：")
print(f"主要情緒：{result['emotion']} (信心 {result['confidence']})")
print("完整分數：", result["all_scores"])