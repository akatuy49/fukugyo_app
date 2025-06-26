import streamlit as st
from openai import OpenAI

# Streamlit SecretsからAPIキーを取得
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("🔍 あなたにぴったりの副業診断（AI版）")

st.markdown("以下の質問に答えて、あなたに合う副業タイプをAIが診断します。")

# 質問1
q1 = st.selectbox("Q1. 1日に使える作業時間はどのくらいですか？", 
                  ["選択してください", "30分未満", "1時間前後", "2〜3時間", "4時間以上"])

# 質問2
q2 = st.multiselect("Q2. 得意・できること（複数選択可）", 
                    ["パソコンの基本操作", "文章を書くこと", "デザイン・動画編集", "SNSや発信が好き", "特にない"])

# 質問3
q3 = st.selectbox("Q3. あなたの性格に近いものは？", 
                  ["選択してください", "コツコツ継続型", "人と話すのが好き", "新しいこと好き", "安定志向"])

# 質問4
q4 = st.multiselect("Q4. 興味・趣味があること", 
                    ["美容・ファッション", "読書・映画・アニメ", "食べること・料理", "ゲーム・ガジェット", "整理整頓・お金の管理"])

# 質問5
q5 = st.selectbox("Q5. 年齢層は？", 
                  ["選択してください", "〜24歳", "25〜34歳", "35〜44歳", "45歳以上"])

# 質問6
q6 = st.selectbox("Q6. 家族構成は？", 
                  ["選択してください", "一人暮らし", "実家暮らし", "夫婦のみ", "子どもあり", "介護あり"])

# 診断ボタン
if st.button("診断する"):
    if "選択してください" in [q1, q3, q5, q6] or not q2 or not q4:
        st.warning("すべての質問に回答してください。")
    else:
        prompt = f"""
あなたは副業診断の専門家です。
以下のユーザー情報をもとに、その人に合った副業のタイプを自然な日本語で提案してください。
診断結果には以下の内容を含めてください：
- タイプ名（例：SNSクリエイター型など）
- 特徴（なぜそのタイプに当てはまるか）
- おすすめ副業ジャンル（3つ程度）

【ユーザー情報】
作業時間：{q1}
得意なこと：{", ".join(q2)}
性格：{q3}
趣味・関心：{", ".join(q4)}
年齢層：{q5}
家族構成：{q6}
"""

        try:
            with st.spinner("AIが診断中です..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "あなたは親しみやすく丁寧な口調の副業診断アドバイザーです。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8
                )
                result = response.choices[0].message.content
                st.subheader("🎯 あなたへの診断結果")
                st.write(result)

        except Exception as e:
            st.error(f"エラーが発生しました：{e}")
