import streamlit as st
import pandas as pd

# === 기본 설정 ===
TARGET_SEMESTER = "25-2"

# === 트랙 데이터 ===
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
            [("제어공학응용", 3, ["25-2"]), ("제어시스템설계", 3, ["25-1"]), ("자동제어", 3, ["25-1"])],
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
            "Pool B": [("전산응용제도", 3, ["25-1"])],
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
            "Pool B": [("항공우주구조역학", 3, ["25-1"])],
            "Pool C": [
               [("제어시스템설계", 3, ["25-1"]), ("자동제어", 3, ["25-1"]), ("제어공학응용", 3, ["25-2"])],
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
            "Pool C": [("항공/드론/AI관련 경진대회 출전(비교과)", 0, ["25-2"])]
        }
    },
}

# === 공통 유틸 ===
def build_course_info(data):
    info = {}
    for track in data.values():
        for key in ["required", "or_groups"]:
            for item in track.get(key, []):
                if isinstance(item, tuple):
                    course, credit, sems = item
                    info[course] = (credit, sems)
                else:
                    for c, cr, s in item:
                        info[c] = (cr, s)
        for pools in track.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    c, cr, s = item
                    info[c] = (cr, s)
                else:
                    for c, cr, s in item:
                        info[c] = (cr, s)
    return info

course_info = build_course_info(track_courses)

# === 계산 함수 ===
def evaluate_courses(items, completed):
    total, rec = 0, []
    for entry in items:
        if isinstance(entry, tuple):
            name, credit, sems = entry
            if name in completed:
                total += credit
            elif TARGET_SEMESTER in sems:
                rec.append((name, credit))
        else:
            for n, c, s in entry:
                if n in completed:
                    total += c
                    break
            else:
                avail = [c for c in entry if TARGET_SEMESTER in c[2]]
                if avail:
                    rec.append((avail[0][0], avail[0][1]))
    return total, rec

def evaluate_pools(pools, completed):
    pool_status, recommendations = {}, {}
    for pool_name, pool_items in pools.items():
        earned, rec = evaluate_courses(pool_items, completed)
        pool_status[pool_name] = earned
        if earned < 3:
            recommendations[pool_name] = {
                "필요학점": 3 - earned,
                "추천과목": rec
            }
    return pool_status, recommendations

def recommend_next_courses(completed_courses):
    completed_names = {n for n, _ in completed_courses}
    recs = {}
    for track, info in track_courses.items():
        is_special = "특화" in track or "챌린저" in track
        must_pass = info.get("must_pass", [])
        missing_must = [m for m in must_pass if m not in completed_names]
        must_msg = f"⚠️ 필수 과목 미이수: {', '.join(missing_must)}" if missing_must else None

        if is_special:
            pool_stat, pool_rec = evaluate_pools(info["pools"], completed_names)
            if pool_rec:
                recs[track] = {"Pool별 필요학점": pool_rec, "메시지": must_msg}
        else:
            earned, rec = evaluate_courses(info.get("required", []), completed_names)
            or_earned, or_rec = evaluate_courses(info.get("or_groups", []), completed_names)
            total = earned + or_earned
            rec.extend(or_rec)
            if info.get("pools"):
                p_total, p_rec = evaluate_courses(info["pools"].values(), completed_names)
                total += p_total
                rec.extend(p_rec)
            need = 6 if "초급" in track else 9
            if total < need:
                recs[track] = {"필요학점": need - total, "추천과목": rec, "메시지": must_msg}
    return recs

def get_completed_matches(completed_courses):
    completed_names = {n for n, _ in completed_courses}
    matches = {}
    for track, info in track_courses.items():
        all_courses = set()
        for section in ["required", "or_groups"]:
            for item in info.get(section, []):
                if isinstance(item, tuple):
                    all_courses.add(item[0])
                else:
                    for c, _, _ in item:
                        all_courses.add(c)
        for pools in info.get("pools", {}).values():
            for item in pools:
                if isinstance(item, tuple):
                    all_courses.add(item[0])
                else:
                    for c, _, _ in item:
                        all_courses.add(c)
        matched = all_courses & completed_names
        if matched:
            matches[track] = sorted(matched)
    return matches

# === Streamlit UI ===
st.title("✈️ 항공드론 MD 이수 확인 시스템")
st.markdown(
    """
    <h4>로드맵 버전 (2025.10.31.)</h4>
    <p>교과목은 쉼표(,)로 구분해 입력해주세요.<br>
    예: 회로이론2,항공드론CapstoneDesign1,드론테크노비즈니스개론</p>
    """, unsafe_allow_html=True
)

completed = st.text_area("이수한 과목을 입력하세요:")

completed_list = [(n.strip(), course_info.get(n.strip(), (3, []))[0])
                  for n in completed.split(",") if n.strip()]

if st.button("추천 확인"):
    if not completed_list:
        st.warning("과목을 입력해주세요.")
    else:
        matches = get_completed_matches(completed_list)
        if matches:
            st.subheader("✅ 현재 이수 과목 (트랙별)")
            for t, cs in matches.items():
                st.write(f"- **{t}**: {', '.join(cs)}")

        recs = recommend_next_courses(completed_list)
        if not recs:
            st.success("🎉 모든 마이크로디그리 조건을 충족했습니다!")
        else:
            st.subheader("📌 부족 학점 및 추천 과목")
            for t, inf in recs.items():
                st.markdown(f"### {t}")
                if inf.get("메시지"):
                    st.warning(inf["메시지"])

                if "필요학점" in inf:
                    st.write(f"▶ 추가 필요 학점: **{inf['필요학점']}학점**")
                    df = pd.DataFrame(sorted(inf["추천과목"], key=lambda x: x[0]),
                                      columns=["과목명", "학점"])
                    df.index += 1
                    st.table(df)
                elif "Pool별 필요학점" in inf:
                    for pool_name, pool_data in inf["Pool별 필요학점"].items():
                        st.write(f"▶ **{pool_name}**: 추가 필요 학점 {pool_data['필요학점']}학점")
                        df = pd.DataFrame(sorted(pool_data["추천과목"], key=lambda x: x[0]),
                                          columns=["과목명", "학점"])
                        df.index += 1
                        st.table(df)

st.markdown(
    """
    <hr>
    <p style="font-size:14px; color:red;">이 프로그램은 2025년도 로드맵 기준 참고용입니다.<br>
    📖 <a href="https://docs.google.com/spreadsheets/d/1qSkAp4q1gao0iFL8uYXxpkAXxBQNLOGrnBdWZ4WZlLU/edit?gid=143772626" target="_blank">마이크로디그리 로드맵 보기</a><br>
    📝 <a href="https://forms.gle/yNhWM1f1nYe778t18" target="_blank">마이크로디그리 신청하기</a></p>
    """, unsafe_allow_html=True
)
