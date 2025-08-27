
import streamlit as st
import pandas as pd

track_courses = {
    "항공드론 초급": {
        "required": [
            ("항공우주학개론", 2, ["25-1", "25-2"]), 
            ("항공우주산업개론", 2, ["25-1", "25-2"]), 
            ("드론테크노비즈니스개론", 3, ["25-2"]), 
            ("혁신융합세미나(항공드론)", 1, ["25-1"]),
            ("항공드론창의설계", 3, ["25-2"]), 
            ("비행원리및모의조종실습", 1, ["25-2"])
        ],
        "or_groups": []
    },
    "항공드론 시스템 심화": {
        "required": [
            ("전산응용제도", 3, ["25-1"]), 
            ("항공우주구조역학", 3, ["25-1"]), 
            ("항공역학", 3, ["25-1"]),
            ("계측공학", 3, ["25-1"]), 
            ("배터리소재의이해", 3, ["25-2"]), 
            ("열역학1", 3, ["25-1"])
        ],
        "or_groups": [
            [("재료역학1", 3, ["25-1"]), ("기초역학", 3, ["25-1"])],
            [("항공드론동역학", 3, ["25-2"]), ("모빌리티동역학", 3, ["25-2"])],
            [("제어공학응용", 3, ["25-2"]), ("제어시스템설계", 3, ["25-1"]), ("자동제어", 3, ["25-1"])]
        ]
    },
    "항공드론 AI 심화": {
        "required": [
            ("이산수학", 3, ["25-1"]), 
            ("AI프로그래밍", 3, ["25-1", "25-2"]), 
            ("딥러닝", 3, ["25-1"]), 
            ("머신러닝입문", 3, ["25-1"]), 
            ("드론강화학습", 3, ["25-2"]), 
            ("지능센서공학", 3, ["25-2"])
        ],
        "or_groups": [
            [("컴퓨터비전", 3, ["25-1"]), ("영상처리", 3, ["25-1"])],
            [("자료구조및실습", 3, ["25-2"]), ("자료구조", 3, ["25-1"])]
        ]
    },
    "항공드론 활용 및 MRO 심화": {
        "required": [
            ("항공기기체시스템", 3, ["25-1"]), 
            ("재료과학1", 3, ["25-1"])
        ],
        "or_groups": [
            [("전기전자공학", 3, ["25-1"]), ("회로이론1", 3, ["25-1"]), ("전기전자개론및실습", 3, ["25-1"]), ("기초전자실험", 3, ["25-2"])]
        ]
    }
}

TARGET_SEMESTER = "25-2"

def build_course_info(track_courses):
    course_info = {}
    for track, info in track_courses.items():
        for course, credit, semesters in info["required"]:
            course_info[course] = (credit, semesters)
        for group in info.get("or_groups", []):
            for course, credit, semesters in group:
                course_info[course] = (credit, semesters)
    return course_info

course_info = build_course_info(track_courses)

def calculate_earned_credits(track_info, completed_courses):
    completed_names = set(name for name, _ in completed_courses)
    total_credits = 0
    recommended = []

    for course, credit, semesters in track_info.get("required", []):
        if course in completed_names:
            total_credits += credit
        elif TARGET_SEMESTER in semesters:
            recommended.append((course, credit))

    for group in track_info.get("or_groups", []):
        group_satisfied = False
        for course, credit, semesters in group:
            if course in completed_names:
                total_credits += credit
                group_satisfied = True
                break
        if not group_satisfied:
            available = [c for c in group if TARGET_SEMESTER in c[2]]
            if available:
                recommended.append((available[0][0], available[0][1]))

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
        track_courses_list = [c for c, _, _ in info["required"]]
        for group in info.get("or_groups", []):
            track_courses_list.extend([c for c, _, _ in group])
        matched = [c for c in track_courses_list if c in completed_names]
        if matched:
            matches[track] = matched

    return matches

# === Streamlit UI ===
st.title("✈️ 항공드론 MD 추천 시스템")

st.markdown(
    """
    <h3 style="font-size:22px; color:darkblue;">당신에게 적합한 항공드론 마이크로디그리를 추천해드립니다!</h3>
    <p style="font-size:18px; color:black;">
    25-1학기(여름학기 포함)에 수강완료(F학점 제외)한 전체과목을 입력해주세요.<br>
    과목명은 풀네임 입력! 구분은 쉼표로! 과목명에 띄어쓰기가 있는 경우는 입력X! <br>
    교과목에Ⅰ이 포함되어 있으면 아라비아 숫자 1로 입력!<br>
    예: <span style="color:green;">항공우주산업개론,AI프로그래밍,재료과학1 / 틀린예: 머신러닝 입문, 재료과학Ⅰ</span><br><br>
    <span style="color:red;">추가로 필요한 수강학점이 적은 순으로 추천됩니다!<br>
    25-2학기 기준입니다. 내년에는 이수해야 할 교과목이 달라질 수 있습니다!</span>
    </p>
    """,
    unsafe_allow_html=True
)

completed = st.text_area("여기에 과목을 입력하세요")

completed_list = []
for c in completed.split(","):
    c = c.strip()
    if not c:
        continue
    if c in course_info:
        credit, semesters = course_info[c]
        completed_list.append((c, credit))
    else:
        completed_list.append((c, 3))  

if st.button("추천 확인"):
    if not completed_list:
        st.write("❗ 과목을 입력해주세요.")
    else:
        matches = get_completed_track_matches(completed_list)
        if matches:
            st.subheader("현재 이수한 과목")
            for track, matched_courses in matches.items():
                st.write(f"- **{track}**: {', '.join(matched_courses)}")

        recs = recommend_next_courses(completed_list)
        if not recs:
            st.write("추천할 트랙이 없습니다. 이미 이수 조건을 만족했을 수 있습니다.")
        else:
            st.subheader("📌 부족 학점 및 추천 과목")
            for track, info in recs.items():
                st.markdown(f"### {track}")
                st.write(f"👉 추가 필요 학점: {info['필요학점']}")

                df = pd.DataFrame(info["추천과목"], columns=["과목명", "학점"])
                df = df.sort_values(by="과목명", ascending=True).reset_index(drop=True) 
                df.index += 1  
                st.table(df)

st.markdown("📖 [마이크로디그리 과정표 보러가기](https://docs.google.com/spreadsheets/d/1YA47-Sxiu7Yw7lzuBNxR3cMA0uVkwb-jxkxMHhFCBT4/edit?usp=sharing)")
