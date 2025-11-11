import streamlit as st
import pandas as pd

# =============================
# 설정
# =============================
TARGET_SEMESTER = "25-2"

# =============================
# 트랙 정보 (기존 그대로 유지)
# =============================
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

# =============================
# 공통 함수
# =============================
def build_course_info():
    info = {}
    for data in track_courses.values():
        for course, credit, semesters in data.get("required", []):
            info[course] = (credit, semesters)
        for group in data.get("or_groups", []):
            for course, credit, semesters in group:
                info[course] = (credit, semesters)
        for pools in data.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    info[item[0]] = (item[1], item[2])
                else:
                    for course, credit, semesters in item:
                        info[course] = (credit, semesters)
    return info

course_info = build_course_info()

def evaluate_courses(info, completed):
    completed_names = {n for n, _ in completed}
    total, recommend = 0, []
    for course, credit, sem in info.get("required", []):
        if course in completed_names:
            total += credit
        elif TARGET_SEMESTER in sem:
            recommend.append((course, credit))
    for group in info.get("or_groups", []):
        if any(c in completed_names for c, _, _ in group):
            total += group[0][1]
        else:
            avail = [c for c in group if TARGET_SEMESTER in c[2]]
            if avail:
                recommend.append((avail[0][0], avail[0][1]))
    return total, recommend

def evaluate_pools(pools, completed):
    completed_names = {n for n, _ in completed}
    pool_status, recommendations = {}, {}
    for name, items in pools.items():
        pool_credit, rec = 0, []
        for item in items:
            if isinstance(item, tuple):
                c, cr, sem = item
                if c in completed_names:
                    pool_credit += cr
                elif TARGET_SEMESTER in sem:
                    rec.append((c, cr))
            else:
                if any(c in completed_names for c, _, _ in item):
                    pool_credit += item[0][1]
                else:
                    avail = [c for c in item if TARGET_SEMESTER in c[2]]
                    if avail:
                        rec.append((avail[0][0], avail[0][1]))
        pool_status[name] = pool_credit
        if pool_credit < 3:
            recommendations[name] = {"필요학점": 3 - pool_credit, "추천과목": rec}
    return pool_status, recommendations

def recommend_next_courses(completed):
    result = {}
    for track, info in track_courses.items():
        must = info.get("must_pass", [])
        missing = [c for c in must if c not in {n for n, _ in completed}]
        msg = f"⚠️ 반드시 이수해야 하는 과목 미이수: {', '.join(missing)}" if missing else None
        is_special = "특화" in track or "챌린저" in track
        if is_special:
            pool_status, pool_rec = evaluate_pools(info["pools"], completed)
            if pool_rec:
                result[track] = {"Pool별 필요학점": pool_rec}
                if msg: result[track]["메시지"] = msg
        else:
            total, recommend = evaluate_courses(info, completed)
            if info.get("pools"):
                pool_credit, pool_rec = evaluate_pools(info["pools"], completed)
                total += sum(pool_credit.values())
                recommend.extend(sum([v["추천과목"] for v in pool_rec.values()], []))
            need = 6 - total if "초급" in track else (9 - total if ("심화" in track or "전문" in track) else None)
            if need and need > 0:
                result[track] = {"필요학점": need, "추천과목": recommend}
                if msg: result[track]["메시지"] = msg
    return result

def get_completed_track_matches(completed):
    completed_names = {n for n, _ in completed}
    matches = {}
    for track, info in track_courses.items():
        all_courses = {c for c, _, _ in info.get("required", [])}
        for g in info.get("or_groups", []):
            all_courses |= {c for c, _, _ in g}
        for p in info.get("pools", {}).values():
            for item in p:
                all_courses |= {item[0]} if isinstance(item, tuple) else {c for c, _, _ in item}
        match = sorted(all_courses & completed_names)
        if match: matches[track] = match
    return matches

# =============================
# Streamlit UI
# =============================
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
completed_list = [(n.strip(), course_info.get(n.strip(), (3, []))[0]) for n in completed.split(",") if n.strip()]

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
            for t, inf in recs.items():
                st.markdown(f"### {t}")
                if "메시지" in inf:
                    st.warning(inf["메시지"])
                if "필요학점" in inf:
                    st.write(f"▶ 추가 필요 학점: {inf['필요학점']}학점")
                    df = pd.DataFrame(sorted(inf["추천과목"], key=lambda x: x[0]), columns=["과목명", "학점"])
                    df.index += 1
                    st.table(df)
                elif "Pool별 필요학점" in inf:
                    for pool, val in inf["Pool별 필요학점"].items():
                        st.write(f"▶ **{pool}**: 추가 필요 학점 {val['필요학점']}학점")
                        df = pd.DataFrame(sorted(val["추천과목"], key=lambda x: x[0]), columns=["과목명", "학점"])
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
