import streamlit as st
import pandas as pd

TARGET_SEMESTER = "25-2"
FUTURE_SEMESTER = "26"

track_courses = {
    "항공드론 초급": {
        "required": [
            ("항공우주학개론", 2, ["25-1", "25-2"]),
            [("항공우주산업개론", 2, ["25-1", "25-2"]), ("드론시스템과미래산업", 2, [FUTURE_SEMESTER])],
            ("드론테크노비즈니스개론", 3, ["25-2"]),
            ("혁신융합세미나(항공드론)", 1, ["25-1"]),
            ("항공드론창의설계", 3, ["25-2"]),
            ("비행원리및모의조종실습", 1, ["25-2"]),
            ("드론기초실습", 2, [FUTURE_SEMESTER])
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
            ("열역학1", 3, ["25-1"]),
            ("자료구조및실습", 3, ["25-2"]),
            ("이산수학", 3, ["25-1"]),
            ("항공드론동역학", 3, ["25-2"]),
            ("항공기기체시스템", 3, ["25-1"]),
            ("드론강화학습", 3, ["25-2"]),
            ("배터리소재의이해", 3, ["25-2"]),
            ("항공역학", 3, ["25-1"]),
            ("지능센서공학", 3, ["25-2"]),
            ("항공우주구조역학", 3, ["25-1"]),
            ("전기자동차분배충전시스템", 1, ["25-1", "25-2"]),
            ("드론임베디드프로그래밍", 3, [FUTURE_SEMESTER]),
            ("항공드론기초전기전자", 3, [FUTURE_SEMESTER]),
            ("항공드론신소재입문", 3, [FUTURE_SEMESTER]),
            ("드론기체제작실습", 3, [FUTURE_SEMESTER]),
            ("드론비즈니스창업론", 3, [FUTURE_SEMESTER]),
            ("배터리시스템설계", 3, [FUTURE_SEMESTER]),
            ("영상처리및응용", 3, [FUTURE_SEMESTER]),
            ("항공드론전기동력입문", 3, [FUTURE_SEMESTER])
        ],
        "or_groups": [
            [("재료역학1", 3, ["25-1"]), ("기초역학", 3, ["25-1"])],
            [("제어공학응용", 3, ["25-2"]), ("제어시스템설계", 3, ["25-1"]), ("자동제어", 3, ["25-1"])],
            [("전기전자공학", 3, ["25-1"]), ("전기전자개론및실습", 3, ["25-1"])],
            [("항공전자공학", 3, ["25-1"]), ("에비오닉스입문", 3, [FUTURE_SEMESTER])],
            [("항행안전시설및공중항법", 3, ["25-1"]), ("항행안전시설및항법", 3, [FUTURE_SEMESTER])],
            [("회로이론2", 3, ["25-2"]), ("회로시스템", 3, [FUTURE_SEMESTER])],
            [("재료과학1", 3, ["25-1"]), ("드론부품용신소재응용", 3, [FUTURE_SEMESTER])],
            [("전자회로1", 3, ["25-1"]), ("항공드론전자회로", 3, [FUTURE_SEMESTER])]
        ],
        "pools": {}
    },
    "항공드론 시스템 전문": {
        "required": [
            ("항공드론비행제어", 3, ["25-2"]),
            ("항공ICT공학", 3, ["25-1"]),
            ("드론운용IT시스템", 3, [FUTURE_SEMESTER]),
            ("항공드론CapstoneDesign1", 3, ["25-2"]),
            ("항공드론AI플래닝", 3, [FUTURE_SEMESTER]),
            ("생성형AI응용", 3, [FUTURE_SEMESTER]),
            ("드론임베디드시스템설계", 3, [FUTURE_SEMESTER]),
            ("항공MRO실습", 3, [FUTURE_SEMESTER]),
            ("AI자율비행", 3, [FUTURE_SEMESTER])
        ],
        "must_pass": ["항공드론CapstoneDesign1"],
        "or_groups": [
            [("복합재료", 3, ["25-1"]), ("반도체소재개론", 3, ["25-1"])],
            [("확률론적로봇공학", 3, ["25-1"]), ("확률론적드론공학", 3, [FUTURE_SEMESTER])],
            [("기계가공시스템", 3, ["25-2"]), ("스마트설계제조", 3, [FUTURE_SEMESTER])]
        ],
        "pools": {}
    },
}

def build_course_info(track_courses):
    course_info = {}

    def add_course(course, credit, semesters):
        if course not in course_info:
            course_info[course] = (credit, semesters)

    for info in track_courses.values():
        for item in info.get("required", []):
            if isinstance(item, tuple):
                add_course(*item)
            elif isinstance(item, list):
                for course, credit, semesters in item:
                    add_course(course, credit, semesters)

        for group in info.get("or_groups", []):
            if isinstance(group, list):
                for course, credit, semesters in group:
                    add_course(course, credit, semesters)

        for pools in info.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    add_course(*item)
                elif isinstance(item, list):
                    for course, credit, semesters in item:
                        add_course(course, credit, semesters)

    return course_info


course_info = build_course_info(track_courses)

def calculate_earned_credits(track_info, completed_courses):
    completed_names = {name for name, _ in completed_courses}
    total_credits = 0
    recommended = []

    for item in track_info.get("required", []):
        if isinstance(item, tuple):
            course, credit, semesters = item
            if course in completed_names:
                total_credits += credit
            else:
                label = "(26년도 예정)" if FUTURE_SEMESTER in semesters else ""
                if any(s in semesters for s in ["25-1", TARGET_SEMESTER, FUTURE_SEMESTER]):
                    recommended.append((f"{course} {label}".strip(), credit))
        elif isinstance(item, list):
            taken = False
            for course, credit, semesters in item:
                if course in completed_names:
                    total_credits += credit
                    taken = True
                    break
            if not taken:
                available = [c for c in item if any(s in c[2] for s in ["25-1", TARGET_SEMESTER, FUTURE_SEMESTER])]
                if available:
                    c, credit, semesters = available[0]
                    label = "(26년도 예정)" if FUTURE_SEMESTER in semesters else ""
                    recommended.append((f"{c} {label}".strip(), credit))

    for group in track_info.get("or_groups", []):
        if isinstance(group, list):
            taken = False
            for course, credit, semesters in group:
                if course in completed_names:
                    total_credits += credit
                    taken = True
                    break
            if not taken:
                available = [c for c in group if any(s in c[2] for s in ["25-1", TARGET_SEMESTER, FUTURE_SEMESTER])]
                if available:
                    c, credit, semesters = available[0]
                    label = "(26년도 예정)" if FUTURE_SEMESTER in semesters else ""
                    recommended.append((f"{c} {label}".strip(), credit))

    return total_credits, recommended


def recommend_next_courses(completed_courses):
    recommendations = {}
    for track, info in track_courses.items():
        must_pass_courses = info.get("must_pass", [])
        missing_must = [c for c in must_pass_courses if c not in {n for n, _ in completed_courses}]
        must_message = None
        if missing_must:
            must_message = f"⚠️ 반드시 이수해야 하는 과목 미이수: {', '.join(missing_must)}"

        rc, rr = calculate_earned_credits(info, completed_courses)
        total_credits = rc
        recommended = rr

        needed = None
        if "초급" in track:
            needed = 6 - total_credits
        elif "심화" in track or "전문" in track:
            needed = 9 - total_credits

        if needed is not None and needed > 0:
            rec_info = {"필요학점": needed, "추천과목": recommended}
            if must_message:
                rec_info["메시지"] = must_message
            recommendations[track] = rec_info

    return recommendations

def get_completed_track_matches(completed_courses):
    completed_names = {name for name, _ in completed_courses}
    matches = {}

    for track, info in track_courses.items():
        all_courses = set()

        for item in info.get("required", []):
            if isinstance(item, tuple):
                c, _, _ = item
                all_courses.add(c)
            elif isinstance(item, list):
                for c, _, _ in item:
                    all_courses.add(c)

        for group in info.get("or_groups", []):
            if isinstance(group, list):
                for c, _, _ in group:
                    all_courses.add(c)
            elif isinstance(group, tuple):
                c, _, _ = group
                all_courses.add(c)

        for pool in info.get("pools", {}).values():
            for item in pool:
                if isinstance(item, tuple):
                    c, _, _ = item
                    all_courses.add(c)
                elif isinstance(item, list):
                    for c, _, _ in item:
                        all_courses.add(c)

        matched = all_courses & completed_names
        if matched:
            matches[track] = sorted(matched)

    return matches

st.title("✈️ 항공드론 MD 이수 확인 시스템")

st.markdown(
    """
    <h3 style="font-size:22px; color:darkblue;">로드맵 버전(2025.10.31.)</h3> 
    <p style="font-size:18px; color:black;">!입력방법!<br>
    1) 교과목간 구분은 ,(쉼표)로 입력<br>
    2) 교과목명은 정확하게 풀네임으로 작성<br>
    3) 교과목 뒤의 Ⅰ, Ⅱ 표기는 아라비아 숫자 1,2로 표기함<br>
    4) 띄어쓰기는 입력하지 않습니다.<br>
    <p style="font-size:18px; color:red;">*바른작성예: 회로이론2,혁신융합세미나(항공드론),항공드론CapstoneDesign1</p>   
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
        st.warning("❗ 과목을 입력해주세요.")
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
            for t, inf in recs.items():
                st.markdown(f"### {t}")
                if "메시지" in inf:
                    st.warning(inf["메시지"])

                if "필요학점" in inf:
                    st.write(f"▶ 추가 필요 학점: {inf['필요학점']}학점")
                    df = pd.DataFrame(sorted(inf["추천과목"], key=lambda x: x[0]), columns=["과목명", "학점"])
                    df.index += 1
                    st.table(df)

st.markdown(
    """
    <p style="font-size:15px; color:red;">
    이 프로그램은 참고용으로 25년도 교육과정에만 해당되며 26년도 교과목은 미확정 상태입니다.<br>
    정확한 내용은 반드시 공식 로드맵에서 확인해주세요!
    </p>
    📖 마이크로디그리 로드맵 보기: 
    <a href="https://docs.google.com/spreadsheets/d/1qSkAp4q1gao0iFL8uYXxpkAXxBQNLOGrnBdWZ4WZlLU/edit?gid=143772626#gid=143772626" target="_blank">여기</a><br>
    📖 마이크로디그리 신청하기: 
    <a href="https://forms.gle/yNhWM1f1nYe778t18" target="_blank">여기</a>
    """,
    unsafe_allow_html=True
)
