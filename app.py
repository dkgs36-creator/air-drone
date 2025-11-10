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
    "항공드론 심화": {
        "required": [
            ("전산응용제도", 3, ["25-1"]),
            ("머신러닝입문", 3, ["25-1"]),
            ("기초전자실험", 2, ["25-2"]),
            ("계측공학", 3, ["25-1"]),
            ("항공전자공학", 3, ["25-1"]),
            ("열역학1", 3, ["25-1"]),
            ("자료구조및실습", 3, ["25-2"]),
            ("이산수학", 3, ["25-1"]),
            ("항공드론동역학", 3, ["25-2"]),
            ("항공기기체시스템", 3, ["25-1"]),
            ("항행안전시설및공중항법", 3, ["25-1"]),
            ("회로이론2", 3, ["25-2"]),
            ("드론강화학습", 3, ["25-2"]),
            ("재료과학1", 3, ["25-1"]),
            ("배터리소재의이해", 3, ["25-2"]),
            ("항공역학", 3, ["25-1"]),
            ("지능센서공학", 3, ["25-2"]),
            ("항공우주구조역학", 3, ["25-1"]),            
            ("전자회로1", 3, ["25-1"]),
            ("전기자동차분배충전시스템", 1, ["25-1", "25-2"])    
        ],
        "or_groups": [
            [("재료역학1", 3, ["25-1"]), ("기초역학", 3, ["25-1"])],
            [("제어공학응용", 3, ["25-2"]),
             ("제어시스템설계", 3, ["25-1"]),
             ("자동제어", 3, ["25-1"])],
            [("전기전자공학", 3, ["25-1"]), ("전기전자개론및실습", 3, ["25-1"])]
        ],
        "pools": {}
    },
    "항공드론 시스템 전문": {
        "required": [
            ("항공드론비행제어", 3, ["25-2"]),
            ("기계가공시스템", 3, ["25-2"]),
            ("항공ICT공학", 3, ["25-1"]),
            ("항공드론CapstoneDesign1", 3, ["25-2"])
        ],
        "must_pass": ["항공드론CapstoneDesign1"],
        "or_groups": [
            [("복합재료", 3, ["25-1"]), ("반도체소재개론", 3, ["25-1"])]
        ],
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
                ("전산응용제도", 3, ["25-1"])
            ],
            "Pool C": [
                [("기초역학", 3, ["25-1"]), ("재료역학1", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("항공기기체시스템", 3, ["25-1"]),
                ("머신러닝입문", 3, ["25-1"]),
                [("전기전자개론및실습", 3, ["25-1"]), ("전기전자공학", 3, ["25-1"])],
                ("항행안전시설및공중항법", 3, ["25-1"])
            ]
        }
    },
    "드론 설계 특화 전문과정 (항공드론 특화 기초과정 이수 후 이수 가능)": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
               [("재료역학1", 3, ["25-1"]), ("기초역학", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("항공기기체시스템", 3, ["25-1"]),
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
    "항공드론 챌린저 마이크로디그리": {
        "required": [],
        "or_groups": [],
        "pools": {
            "Pool A": [
                ("전산응용제도", 3, ["25-1"]),
                ("드론테크노비즈니스개론", 3, ["25-2"])
            ],
            "Pool B": [
                [("기초역학", 3, ["25-1"]), ("재료역학1", 3, ["25-1"])],
                ("항공드론동역학", 3, ["25-2"]),
                ("머신러닝입문", 3, ["25-1"]),
                ("항공기기체시스템", 3, ["25-1"])
            ],
            "Pool C": [
                ("항공/드론/AI관련 경진대회 출전(비교과)", 0, ["25-2"])
            ]
        }
    },
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
            else:  # or-group
                for course, credit, semesters in item:
                    if course in completed_names:
                        total_credits += credit
                        break
                else:
                    available = [c for c in item if TARGET_SEMESTER in c[2]]
                    if available:
                        recommended.append((available[0][0], available[0][1]))
    return total_credits, recommended

def calculate_pool_credits_per_pool(pools, completed_courses):
    completed_names = {name for name, _ in completed_courses}
    pool_status = {}
    recommendations = {}

    for pool_name, pool_items in pools.items():
        pool_credit = 0
        pool_recommend = []

        for item in pool_items:
            if isinstance(item, tuple):
                course, credit, semesters = item
                if course in completed_names:
                    pool_credit += credit
                elif TARGET_SEMESTER in semesters:
                    pool_recommend.append((course, credit))
            else:  # or-group
                for course, credit, semesters in item:
                    if course in completed_names:
                        pool_credit += credit
                        break
                else:
                    available = [c for c in item if TARGET_SEMESTER in c[2]]
                    if available:
                        pool_recommend.append((available[0][0], available[0][1]))

        pool_status[pool_name] = pool_credit
        if pool_credit < 3:
            recommendations[pool_name] = {
                "필요학점": 3 - pool_credit,
                "추천과목": pool_recommend
            }

    return pool_status, recommendations

def calculate_earned_credits(track_info, completed_courses):
    completed_names = {name for name, _ in completed_courses}
    total_credits = 0
    recommended = []

    # Required courses
    for course, credit, semesters in track_info.get("required", []):
        if course in completed_names:
            total_credits += credit
        elif TARGET_SEMESTER in semesters:
            recommended.append((course, credit))

    # OR groups
    for group in track_info.get("or_groups", []):
        for course, credit, semesters in group:
            if course in completed_names:
                total_credits += credit
                break
        else:
            # 추천 가능한 과목 찾기
            available = [c for c in group if TARGET_SEMESTER in c[2]]
            if available:
                recommended.append((available[0][0], available[0][1]))

    return total_credits, recommended

def recommend_next_courses(completed_courses):
    recommendations = {}
    for track, info in track_courses.items():
        is_special = "특화" in track or "챌린저" in track or "파일럿" in track

        must_pass_courses = info.get("must_pass", [])
        missing_must = [c for c in must_pass_courses if c not in {n for n, _ in completed_courses}]
        must_message = None
        if missing_must:
            must_message = f"⚠️ 반드시 이수해야 하는 과목 미이수: {', '.join(missing_must)}"
        if is_special:
            pool_status, pool_recommendations = calculate_pool_credits_per_pool(info["pools"], completed_courses)
            if pool_recommendations:
                recommendations[track] = {
                    "Pool별 필요학점": pool_recommendations
                }
        else:
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
            elif "심화" in track or "전문" in track:
                needed = 9 - total_credits

            if needed is not None and needed > 0:
                recommendations[track] = {
                    "필요학점": needed,
                    "추천과목": recommended
                }

    return recommendations

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
st.title("✈️ 항공드론 MD 이수 확인 시스템")

st.markdown(
    """
    <h3 style="font-size:22px; color:darkblue;">로드맵 버전(2025.10.31.)</h3> 
    <p style="font-size:18px; color:black;">!입력방법!<br>
    1) 교과목간 구분은 ,(쉼표)로 입력<br>
    2) 교과목명은 정확하게 풀네임으로 작성<br>
    3) 교과목 뒤의 Ⅰ, Ⅱ 표기는 아라비아 숫자 1,2로 표기함<br>
    4) 띄어쓰기는 입력하지 않습니다.<br>
    <p style="font-size:18px; color:red;">*바른작성예: 회로이론2,혁신융합세미나(항공드론), 항공드론CapstoneDesign1</p>   
    """,
    unsafe_allow_html=True
)

completed = st.text_area("25년도에 수강한 과목명을 입력하세요")

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
            st.success("🎉 축하합니다! 모든 마이크로디그리 조건을 만족했을 수 있습니다.")
        else:
            st.subheader("📌 부족 학점 및 추천 과목")
            sorted_recs = sorted(recs.items(), key=lambda x: x[1].get("필요학점", 99) 
                                 if "필요학점" in x[1] else min([v["필요학점"] for v in x[1]["Pool별 필요학점"].values()], default=99))
            for t, inf in recs.items():
                st.markdown(f"### {t}")
                if "필요학점" in inf:
                    st.write(f"▶ 추가 필요 학점: {inf['필요학점']}학점")
                    df = pd.DataFrame(sorted(inf["추천과목"], key=lambda x: x[0]), columns=["과목명", "학점"])
                    df.index += 1
                    st.table(df)
                elif "Pool별 필요학점" in inf:
                    for pool_name, pool_info in inf["Pool별 필요학점"].items():
                        st.write(f"▶ **{pool_name}**: 추가 필요 학점 {pool_info['필요학점']}학점")
                        df = pd.DataFrame(sorted(pool_info["추천과목"], key=lambda x: x[0]), columns=["과목명", "학점"])
                        df.index += 1
                        st.table(df)

st.markdown(
    """
    <p style="font-size:15px; color:red;">이 프로그램은 참고용으로 25년도 교육과정에만 해당됩니다.<br>
    정확한 내용은 반드시 로드맵에서 확인해주세요!</p>
    📖 마이크로디그리 로드맵 보기: 
    <a href="https://docs.google.com/spreadsheets/d/1qSkAp4q1gao0iFL8uYXxpkAXxBQNLOGrnBdWZ4WZlLU/edit?gid=143772626#gid=143772626" target="_blank">여기</a><br>
    📖 마이크로디그리 신청하기: 
    <a href="https://forms.gle/yNhWM1f1nYe778t18" target="_blank">여기</a>
    """,
    unsafe_allow_html=True
)
