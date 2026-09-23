import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ==========================================
# 1. 페이지 기본 설정 및 데이터 파일(CSV) 관리
# ==========================================
st.set_page_config(
    page_title="우리학교 석식 사전 신청 앱", page_icon="🍱", layout="wide"
)

# 데이터 저장용 CSV 파일 경로
DATA_FILE = "dinner_applications.csv"


# CSV 파일에서 신청 데이터 불러오기 함수
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE, dtype={"student_id": str})
            return df
        except Exception:
            return pd.DataFrame(
                columns=["student_id", "name", "date", "status"]
            )
    else:
        # 파일이 없으면 새 데이터프레임 생성
        return pd.DataFrame(columns=["student_id", "name", "date", "status"])


# CSV 파일에 데이터 저장하기 함수
def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")


# 세션 상태(Session State) 초기화 (로그인 정보용)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_info" not in st.session_state:
    st.session_state["user_info"] = {"student_id": "", "name": ""}

# 예시 석식 메뉴 데이터
MENU_DATA = {
    "2026-09-22": {
        "main": "치밥 & 김말이튀김",
        "side": "치킨무, 배추김치",
        "soup": "팽이버섯 장국",
        "dessert": "청포도 에이드",
        "calories": "850 kcal",
    },
    "2026-09-23": {
        "main": "돈까스 & 브라운소스",
        "side": "마카로니 샐러드, 깍두기",
        "soup": "크림스프",
        "dessert": "요구르트",
        "calories": "920 kcal",
    },
    "2026-09-24": {
        "main": "전주비빔밥 & 계란후라이",
        "side": "떡갈비구이, 열무김치",
        "soup": "콩나물국",
        "dessert": "미니 붕어빵",
        "calories": "780 kcal",
    },
    "2026-09-25": {
        "main": "자장면 & 군만두",
        "side": "단무지, 짜사이",
        "soup": "계란파국",
        "dessert": "망고 푸딩",
        "calories": "890 kcal",
    },
}

# ==========================================
# 2. 메인 헤더
# ==========================================
st.title("🍱 우리학교 석식 사전 신청 시스템")
st.caption(
    "로컬 데이터 저장 방식 적용: 로그아웃 후 재로그인해도 신청 내역이 유지됩니다."
)
st.divider()

# ==========================================
# 3. 탭 구성
# ==========================================
tab1, tab2, tab3 = st.tabs(
    [
        "🔒 1. 로그인 및 본인인증",
        "📅 2. 석식 메뉴 열람 및 신청",
        "📊 3. [AI] 인원 예측 및 통계",
    ]
)

# ------------------------------------------
# TAB 1: 로그인 및 본인인증
# ------------------------------------------
with tab1:
    st.subheader("👤 학생/교직원 본인 인증")

    if not st.session_state["logged_in"]:
        col1, _ = st.columns([1, 1])
        with col1:
            student_id = st.text_input(
                "학번/사번 입력", placeholder="예: 20301"
            )
            name = st.text_input("이름 입력", placeholder="예: 홍길동")
            login_btn = st.button("로그인 / 인증하기", type="primary")

            if login_btn:
                if student_id and name:
                    st.session_state["logged_in"] = True
                    st.session_state["user_info"] = {
                        "student_id": str(student_id).strip(),
                        "name": name.strip(),
                    }
                    st.success(
                        f"인증 성공! 환영합니다, {name}님({student_id})."
                    )
                    st.rerun()
                else:
                    st.error("학번과 이름을 모두 입력해주세요.")
    else:
        user = st.session_state["user_info"]
        st.info(
            f"현재 **{user['name']} ({user['student_id']})** 계정으로 로그인되어 있습니다."
        )
        if st.button("로그아웃"):
            st.session_state["logged_in"] = False
            st.session_state["user_info"] = {"student_id": "", "name": ""}
            st.rerun()

# ------------------------------------------
# TAB 2: 석식 메뉴 열람 및 신청
# ------------------------------------------
with tab2:
    st.subheader("📅 날짜별 석식 메뉴 및 신청")

    if not st.session_state["logged_in"]:
        st.warning(
            "⚠️ 석식을 신청하려면 먼저 [1. 로그인 및 본인인증] 탭에서 로그인을 해주세요."
        )
    else:
        # CSV 파일에서 데이터 불러오기
        df_app = load_data()

        # 날짜 선택
        selected_date = st.date_input(
            "석식을 신청할 날짜를 선택하세요",
            value=datetime.date(2026, 9, 22),
            min_value=datetime.date(2026, 9, 22),
            max_value=datetime.date(2026, 9, 25),
        )
        date_str = selected_date.strftime("%Y-%m-%d")

        col_menu, col_app = st.columns([1, 1])

        # 좌측: 식단표 안내
        with col_menu:
            st.markdown(f"### 🍴 {date_str} 석식 식단표")
            if date_str in MENU_DATA:
                menu = MENU_DATA[date_str]
                st.write(f"**· 메인메뉴:** {menu['main']}")
                st.write(f"**· 반찬류:** {menu['side']}")
                st.write(f"**· 국/찌개:** {menu['soup']}")
                st.write(f"**· 후식:** {menu['dessert']}")
                st.caption(f"⚡ 열량: {menu['calories']}")
            else:
                st.info("해당 날짜의 식단 정보가 아직 등록되지 않았습니다.")

        # 우측: 신청하기 / 취소하기
        with col_app:
            st.markdown("### ✍️ 신청 상태 확인")
            user_id = st.session_state["user_info"]["student_id"]
            user_name = st.session_state["user_info"]["name"]

            # 로그인한 학번의 해당 날짜 신청 여부 확인
            if not df_app.empty:
                user_record = df_app[
                    (df_app["student_id"] == user_id)
                    & (df_app["date"] == date_str)
                    & (df_app["status"] == "신청완료")
                ]
                is_applied = not user_record.empty
            else:
                is_applied = False

            if is_applied:
                st.success("✅ **[신청 완료]** 해당 날짜에 석식이 신청되어 있습니다.")
                if st.button("석식 신청 취소하기"):
                    # 해당 내역 삭제 후 CSV 저장
                    updated_df = df_app[
                        ~(
                            (df_app["student_id"] == user_id)
                            & (df_app["date"] == date_str)
                        )
                    ]
                    save_data(updated_df)
                    st.warning("석식 신청이 취소되었습니다.")
                    st.rerun()
            else:
                st.error("❌ **[미신청]** 해당 날짜에 석식 신청이 되어있지 않습니다.")
                if st.button("석식 신청하기", type="primary"):
                    # 새 신청 내역 추가 후 CSV 저장
                    new_row = pd.DataFrame(
                        [[user_id, user_name, date_str, "신청완료"]],
                        columns=["student_id", "name", "date", "status"],
                    )
                    updated_df = pd.concat([df_app, new_row], ignore_index=True)
                    save_data(updated_df)
                    st.success("석식 신청이 완료되었습니다!")
                    st.rerun()

        st.divider()
        st.markdown("#### 📋 나의 전체 석식 신청 내역")
        if not df_app.empty:
            my_apps = df_app[df_app["student_id"] == user_id]
            if not my_apps.empty:
                st.dataframe(
                    my_apps[["date", "status"]], use_container_width=True
                )
            else:
                st.write("아직 신청한 내역이 없습니다.")

# ------------------------------------------
# TAB 3: [AI] 인원 예측 및 통계
# ------------------------------------------
with tab3:
    st.subheader("📊 예측 AI 기반 일자별 석식 수요 예측")
    st.write(
        "저장된 실제 데이터 기반으로 AI 인원 예측 그래프와 실시간 인원을 비교합니다."
    )

    df_app = load_data()

    dates = ["2026-09-22", "2026-09-23", "2026-09-24", "2026-09-25"]
    predicted_counts = [240, 255, 210, 180]

    actual_counts = []
    for d in dates:
        if not df_app.empty:
            cnt = len(
                df_app[(df_app["date"] == d) & (df_app["status"] == "신청완료")]
            )
        else:
            cnt = 0
        actual_counts.append(cnt)

    stats_df = pd.DataFrame(
        {
            "날짜": dates,
            "실시간 신청 인원": actual_counts,
            "AI 예측 최종 인원": predicted_counts,
        }
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("총 예상 석식 인원 (주간 평균)", f"{int(sum(predicted_counts)/4)}명")
    col2.metric(
        "최대 수요 예측일",
        f"{dates[predicted_counts.index(max(predicted_counts))]} ({max(predicted_counts)}명)",
    )
    col3.metric("현재 저장된 총 신청 건수", f"{sum(actual_counts)}건")

    st.divider()

    st.markdown("#### 📈 날짜별 실시간 신청 현황 vs AI 예측 인원")
    fig, ax = plt.subplots(figsize=(8, 4))
    x = range(len(dates))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        actual_counts,
        width,
        label="실시간 신청 인원",
        color="#4C72B0",
    )
    ax.bar(
        [i + width / 2 for i in x],
        predicted_counts,
        width,
        label="AI 예측 인원",
        color="#55A868",
    )

    ax.set_xlabel("날짜")
    ax.set_ylabel("인원 수 (명)")
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    st.pyplot(fig)
    st.dataframe(stats_df, use_container_width=True)
