
import streamlit as st

track_courses = {
    "항공드론 초급": {
        "required": [
            ("항공우주학개론", 2), ("항공우주산업개론", 2), ("드론테크노비즈니스개론", 3),
            ("항공드론창의설계", 3), ("비행원리및모의조종실습", 1), ("AI입문", 3), ("컴퓨터프로그래밍", 3)
        ],
        "or_groups": []
    },
    "항공드론 시스템 심화": {
        "required": [
            ("전산응용제도", 3), ("열역학I", 3), ("항공우주구조역학", 3), ("항공역학I", 3),
            ("계측공학", 3), ("항공기개념설계", 3), ("신호및시스템", 3),
            ("배터리소재의이해", 3), ("임베디드SW입문", 3)
        ],
        "or_groups": [
            [("재료역학I", 3), ("기초역학", 3)],
            [("항공드론동역학", 3), ("모빌리티동역학", 3)],
            [("열역학I", 3), ("재료열역학", 3)],
            [("제어공학응용", 3), ("제어시스템설계", 3), ("자동제어", 3)]
        ]
    },
    "항공드론 AI 심화": {
        "required": [
            ("이산수학", 3), ("AI프로그래밍", 3), ("딥러닝", 3), 
            ("머신러닝입문", 3), ("드론강화학습", 3), ("지능센서공학", 3)
        ],
        "or_groups": [
            [("컴퓨터비전", 3), ("영상처리", 3)],
            [("자료구조및실습", 3), ("자료구조", 3)]
        ]
    },
    "항공드론 활용 및 MRO 심화": {
        "required": [
            ("항공기기체시스템", 3), ("재료과학I", 3)
        ],
        "or_groups": [
            [("전기전자공학", 3), ("회로이론I", 3), ("전기전자개론및실습", 3), ("기초전자실험", 3)]
        ]
    }
}

def calculate_earned_credits(track_info, completed_courses):
    completed_names = set(name for name, _ in completed_courses)
    total_credits = 0
    recommended = []

    for course, credit in track_info.get("required", []):
        if course in completed_names:
            total_credits += credit
        else:
            recommended.append((course, credit))

    for group in track_info.get("or_groups", []):
        group_satisfied = False
        for course, credit in group:
            if course in completed_names:
                total_credits += credit
                group_satisfied = True
                break
        if not group_satisfied:
            recommended.append(group[0])

    return total_credits, recommended
    
def recommend_next_courses(completed_courses):
    recommendations = {}
    for track, info in track_courses.items():
        total_credits, recommended = calculate_earned_credits(info, completed_courses)
        if "초급" in track and total_credits < 6:
            recommendations[track] = {"필요학점": 6 - total_credits, "추천과목": recommended}
        elif "심화" in track and total_credits < 9:
            recommendations[track] = {"필요학점": 9 - total_credits, "추천과목": recommended}
    recommendations = dict(
        sorted(recommendations.items(), key=lambda x: x[1]["필요학점"])
    )
    return recommendations

def get_completed_track_matches(completed_courses):
    completed_names = set(name for name, _ in completed_courses)
    matches = {}

    for track, info in track_courses.items():
        track_courses_list = [c for c, _ in info["required"]]
        for group in info.get("or_groups", []):
            track_courses_list.extend([c for c, _ in group])
        matched = [c for c in track_courses_list if c in completed_names]
        if matched:
            matches[track] = matched

    return matches

# === Streamlit UI ===
st.title("✈️ 항공드론 MD 추천 시스템")
import streamlit as st

st.markdown(
    """
    <h3 style="font-size:22px; color:darkblue;">당신에게 적합한 항공드론 수준형 마이크로디그리를 추천해드립니다!</h3>
    <p style="font-size:18px; color:black;">
    25-1학기(여름학기 포함)에 수강완료(F학점 제외)한 전체과목을 입력해주세요.<br>
    입력시 과목명 구분은 쉼표로 입력! 과목명에 띄어쓰기가 있는 경우는 입력X! <br>
    예: <span style="color:green;">항공우주산업개론,AI프로그래밍,</span><br><br>
    추가로 필요한 수강학점이 적은 순으로 추천됩니다!
    </p>
    """,
    unsafe_allow_html=True
)

completed = st.text_area("여기에 과목을 입력하세요")
completed_list = [(c.strip(), 3) for c in completed.split(",") if c.strip()]

if st.button("추천 확인"):
    if not completed_list:
        st.write("❗ 과목을 입력해주세요.")
    else:
        # ✅ 1) 입력한 과목이 속한 트랙 표시
        matches = get_completed_track_matches(completed_list)
        if matches:
            st.subheader("✅ 입력한 과목이 속한 트랙")
            for track, matched_courses in matches.items():
                st.write(f"- **{track}**: {', '.join(matched_courses)}")

        # ✅ 2) 부족 학점 + 추천 과목 표시
        recs = recommend_next_courses(completed_list)
        if not recs:
            st.write("추천할 트랙이 없습니다. 이미 이수 조건을 만족했을 수 있습니다.")
        else:
            st.subheader("📌 부족 학점 및 추천 과목")
            for track, info in recs.items():
                st.markdown(f"### {track}")
                st.write(f"👉 추가 필요 학점: {info['필요학점']}")
                st.write("추천 과목:")
                for course, credit in info["추천과목"]:
                    st.write(f"- {course} ({credit}학점)")
