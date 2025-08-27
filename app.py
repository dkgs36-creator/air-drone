import streamlit as st
import pandas as pd

TARGET_SEMESTER = "25-2"

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
        "or_groups": [],
        "pools": {}
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
            [("제어공학응용", 3, ["25-2"]),
             ("제어시스템설계", 3, ["25-1"]),
             ("자동제어", 3, ["25-1"])]
        ],
        "pools": {}
    },
    "항공드론 AI 심화": {
        "required": [
            ("이산수학", 3, ["25-1"]),
            ("AI프로그래밍", 3, ["25-1", "25‑2"]),
            ("딥러닝", 3, ["25-1"]),
            ("머신러닝입문", 3, ["25-1"]),
            ("드론강화학습", 3, ["25-2"]),
            ("지능센서공학", 3, ["25-2"])
        ],
        "or_groups": [
            [("컴퓨터비전", 3, ["25-1"]), ("영상처리", 3, ["25-1"])],
            [("자료구조및실습", 3, ["25-2"]), ("자료구조", 3, ["25-1"])]
        ],
        "pools": {}
    },
    "항공드론 활용 및 MRO 심화": {
        "required": [
            ("항공기기체시스템", 3, ["25-1"]),
            ("재료과학1", 3, ["25-1"])
        ],
        "or_groups": [
            [("전기전자공학", 3, ["25-1"]), ("회로이론1", 3, ["25-1"]),
             ("전기전자개론및실습", 3, ["25-1"]), ("기초전자실험", 3, ["25-2"])]
        ],
        "pools": {}
    },
    "항공드론 시스템 전문": {
        "required": [
            ("항공드론비행제어", 3, ["25-2"])
        ],
        "or_groups": [],
        "pools": {}
    },
    "항공드론 AI 전문": {
        "required": [
            ("항공드론CapstoneDesign", 3, ["25-2"])
        ],
        "or_groups": [],
        "pools": {}
    },
    "항공드론 특화 기초과정": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
                ("항공우주학개론", 2, ["25-1", "25-2"]),
                ("항공우주산업개론", 2, ["25-1", "25-2"]),
                ("드론테크노비즈니스개론", 3, ["25-2"]),
                ("항공드론창의설계", 3, ["25-2"]),
                ("비행원리및모의조종실습", 1, ["25-2"])
            ],
            "Pool B": [
                ("AI프로그래밍", 3, ["25-1"]),
                ("전산응용제도", 3, ["25-1"])
            ],
            "Pool C": [
                [("기초역학", 3, ["25-1"]), ("재료역학1", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("머신러닝입문", 3, ["25-1"]),
                ("기초전자실험", 3, ["25-2"])
            ]
        }
    },
    "드론 설계 특화 전문과정 (항공드론 특화 기초과정 이수 후 이수 가능)": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
                [("기초역학", 3, ["25-1"]), ("재료역학1", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("전산응용제도", 3, ["25-1"])
            ],
            "Pool B": [
                ("항공우주구조역학", 3, ["25-1"])
            ],
            "Pool C": [
                [("제어시스템설계", 3, ["25-1"]),
                 ("자동제어", 3, ["25-1"]),
                 ("제어공학응용", 3, ["25-2"])],
                ("항공ICT공학", 3, ["25-1"]),
                ("지능센서공학", 3, ["25-2"])
            ]
        }
    },
    "드론 AI 특화 전문과정 (항공드론 특화 기초과정 이수 후 이수 가능)": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
                ("AI프로그래밍", 3, ["25-1"]),
                ("머신러닝입문", 3, ["25-1"])
            ],
            "Pool B": [
                ("드론강화학습", 3, ["25-2"]),
                ("딥러닝", 3, ["25-1"])
            ],
            "Pool C": [
                [("영상처리", 3, ["25-1"]), ("컴퓨터비전", 3, ["25-1"])]
            ]
        }
    },
    "항공드론 챌린저 마이크로디그리": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
                ("전산응용제도", 3, ["25-1"]),
                ("AI프로그래밍", 3, ["25-1"]),
                ("드론테크노비즈니스개론", 3, ["25-2"])
            ],
            "Pool B": [
                [("기초역학", 3, ["25-1"]), ("재료역학1", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("머신러닝입문", 3, ["25-1"])
            ],
            "Pool C": [
                ("항공/드론/AI관련 경진대회 출전(비교과)", 0, ["25-2"])
            ]
        }
    }
}

def build_course_info(track_courses):
    course_info = {}
    for info in track_courses.values():
        for course, credit, semesters in info.get("required", []):
            course_info[course] = (credit, semesters)
        for group in info.get("or_groups", []):
            for course, credit, semesters in group:
                course_info[course] = (credit, semesters)
        for pools in info.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    course, credit, semesters = item
                    course_info[course] = (credit, semesters)
                else:
                    for course, credit, semesters in item:
                        course_info[course] = (credit, semesters)
    return course_info

course_info = build_course_info(track_courses)

def calculate_earned_credits(track_info, completed_courses):
    completed_names = {name for name, _ in completed_courses}
    total_credits = 0
    recommended = []
    for course, credit, semesters in track_info.get("required", []):
        if course in completed_names:
            total_credits += credit
        elif TARGET_SEMESTER in semesters:
            recommended.append((course, credit))
    for group in track_info.get("or_groups", []):
        for course, credit, semesters in group:
            if course in completed_names:
                total_credits += credit
                break
        else:
            available = [c for c in group if TARGET_SEMESTER in c[2]]
            if available:
                recommended.append((available[0][0], available[0][1]))
    return total_credits, recommended

def calculate_pool_credits(pools, completed_courses):
    completed_names = {name for name, _ in completed_courses}
    total_credits = 0
    recommended = []
    for pool_items in pools.values():
        for item in pool_items:
            if isinstance(item, tuple):
                course, credit, semesters = item
                if course in completed_names:
                    total_credits += credit
                elif TARGET_SEMESTER in semesters:
                    recommended.append((course, credit))
            else:
                for course, credit, semesters in item:
                    if course in completed_names:
                        total_credits += credit
                        break
                else:
                    available = [c for c in item if TARGET_SEMESTER in c[2]]
                    if available:
                        recommended.append((available[0][0], available[0][1]))
    return total_credits, recommended

def recommend_next_courses(completed_courses):
    recommendations = {}
    for track, info in track_courses.items():
        total_credits = 0
        recommended = []

        rc, rr = calculate_earned_credits(info, completed_courses)
        total_credits += rc
        recommended.extend(rr)

        if info.get("pools"):
            pc, pr = calculate_pool_credits(info["pools"], completed_courses)
            total_credits += pc
            recommended.extend(pr)

        needed = None
        if "초급" in track:
            needed = 6 - total_credits
        elif "심화" in track or "특화" in track:
            needed = 9 - total_credits
        elif "전문" in track:
            needed = 9 - total_credits
        elif "특화" in track:
            needed = 9 - total_credits
        elif "챌린저" in track:
            needed = 6 - total_credits

        if needed is not None and needed > 0:
            recommendations[track] = {"필요학점": needed, "추천과목": recommended}

    return dict(sorted(recommendations.items(), key=lambda x: x[1]["필요학점"]))

def get_completed_track_matches(completed_courses):
    completed_names = {name for name, _ in completed_courses}
    matches = {}
    for track, info in track_courses.items():
        all_courses = {c for c, _, _ in info.get("required", [])}
        for group in info.get("or_groups", []):
            all_courses |= {c for c, _, _ in group}
        for pools in info.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    all_courses.add(item[0])
                else:
                    all_courses |= {c for c, _, _ in item}
        matched = all_courses & completed_names
        if matched:
            matches[track] = sorted(matched)
    return matches

# === Streamlit UI ===
st.title("✈️ 항공드론 MD 추천 시스템")

st.markdown(
    """
    <h3 style="font-size:22px; color:darkblue;">당신에게 적합한 항공드론 마이크로디그리를 추천드립니다!</h3>
    <p style="font-size:18px; color:black;">
    25‑1학기(여름학기 포함)에 수강한(F제외) 과목을 쉼표로 구분하여 입력해주세요.<br>
    과목명은 풀네임으로! 로마자(I)는 숫자(1)로! 띄어쓰기는 X<br>
    예시: 머신러닝입문,재료과학1 (O) / 머신러닝 입문,재료과학I (X)
    </p>
    <p style="font-size:16px; color:red;">
    추가로 이수할 학점이 적은 순으로 추천됩니다.<br>
    마이크로디그리 간 과목이 중복되는 경우 한 과정만 인정합니다.<br>
    25-2학기 개설교과목에만 해당하며 다음 학기는 변동될 수 있습니다.<br>
    참고용으로만 사용 부탁드리며 반드시 로드맵에서 추가로 확인해주시기 바랍니다!<br> 
    특히 교과지정형 /교과-비교과 융합형 MD는 꼭 추가 확인해주세요!
    </p>
    """,
    unsafe_allow_html=True
)

completed = st.text_area("25-1학기에 수강한 과목명을 입력하세요")

completed_list = []
for item in completed.split(","):
    name = item.strip()
    if not name:
        continue
    credit, semesters = course_info.get(name, (3, []))
    completed_list.append((name, credit))

if st.button("추천 확인"):
    if not completed_list:
        st.write("❗ 과목을 입력해주세요.")
    else:
        matches = get_completed_track_matches(completed_list)
        if matches:
            st.subheader("✅ 현재 이수한 과목 (트랙별)")
            for t, cs in matches.items():
                st.write(f"- **{t}**: {', '.join(cs)}")
        recs = recommend_next_courses(completed_list)
        if not recs:
            st.write("축하합니다! 모든 마이크로디그리 조건을 만족했을 수 있습니다.")
        else:
            st.subheader("📌 부족 학점 및 추천 과목")
            for t, inf in recs.items():
                st.markdown(f"### {t}")
                st.write(f"▶ 추가 필요 학점: {inf['필요학점']}")
                df = pd.DataFrame(inf["추천과목"], columns=["과목명", "학점"])
                df.index += 1
                st.table(df)

st.markdown("📖 마이크로디그리 로드맵 보기: [여기](https://docs.google.com/spreadsheets/d/1YA47-Sxiu7Yw7lzuBNxR3cMA0uVkwb-jxkxMHhFCBT4/edit?usp=sharing)")
