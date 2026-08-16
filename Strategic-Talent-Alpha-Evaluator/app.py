import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go  # 引入工业级雷达图引擎

# ==========================================
# 👑 V5.0 决策层高管可视化大屏 (Dashboard UI - 完全体)
# ==========================================

# 1. 页面全局配置
st.set_page_config(page_title="Talent Alpha 战略看板", page_icon="👑", layout="wide")

# ==========================================
# 🎛️ 模块三：注入交互灵魂 - 动态筛选侧边栏
# ==========================================
st.sidebar.header("🎛️ 高管动态控制台")
st.sidebar.markdown("拖拽下方滑块，实时动态过滤黄金大盘。")
# 设置动态滑块，默认过滤分数设为 50
alpha_threshold = st.sidebar.slider("🏆 Talent Alpha 最低及格线", min_value=0, max_value=100, value=50, step=5)
st.sidebar.divider()
st.sidebar.caption("🇸🇬 亚太区智能战略人才发现引擎 V5.0")

# 主界面标题
st.title("👑 V5.0 Strategic-Talent-Alpha-Evaluator")
st.markdown("### 🇸🇬 亚太区人才资产分布与高潜战神雷达")
st.divider()

# 2. 物理数据流安全加载机制
@st.cache_data
def load_assets():
    base_dir = "data/03_processed"
    
    def safe_read(file_name):
        path = os.path.join(base_dir, file_name)
        return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

    df_green = safe_read("cleaned_v1_master.csv")
    df_yellow = safe_read("cleaned_v1_master_human_audit.csv")
    df_red = safe_read("cleaned_v1_master_rejected_audit.csv")
    
    return df_green, df_yellow, df_red

df_green_raw, df_yellow, df_red = load_assets()

# 根据侧边栏的滑块，实时过滤黄金大盘
if not df_green_raw.empty and 'Talent_Alpha' in df_green_raw.columns:
    df_green = df_green_raw[df_green_raw['Talent_Alpha'] >= alpha_threshold].copy()
else:
    df_green = df_green_raw

# 3. 顶层 KPI 商业磁贴
total_candidates = len(df_green_raw) + len(df_yellow) + len(df_red)

col1, col2, col3, col4 = st.columns(4)
col1.metric("总并发资产 (Total Ingested)", f"{total_candidates} 人")
col2.metric("🟢 过滤后黄金池 (Filtered)", f"{len(df_green)} 人", f"已拦截低于 {alpha_threshold} 分者")
col3.metric("🟡 灰度审计 (Human Audit)", f"{len(df_yellow)} 人")
col4.metric("🔴 风险熔断 (Fatal Graveyard)", f"{len(df_red)} 人")

st.divider()

# 4. 商业降维视觉呈现
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader(f"🏆 黄金战神排行榜 (Alpha ≥ {alpha_threshold})")
    if not df_green.empty:
        # 提取高管最关心的核心业务字段，优先展示战略短评
        display_cols = ['email', 'Talent_Alpha', 'Tech_Score', 'Project_Score', 'strategic_advice']
        safe_cols = [c for c in display_cols if c in df_green.columns]
        
        # 模块二：释放最值钱的资产 - 战略短评直接呈现在表格中
        st.dataframe(
            df_green[safe_cols].head(10), 
            use_container_width=True,
            column_config={
                "email": "候选人标识",
                "Talent_Alpha": st.column_config.NumberColumn("👑 Alpha 综合分", format="%.1f"),
                "strategic_advice": "🤖 AI 战略推断 (Strategic Advice)"
            }
        )
    else:
        st.warning("🚨 当前阈值下黄金大盘为空，请调低侧边栏的分数底线！")

with col_right:
    # 模块一：战神雷达图
    st.subheader("🎯 战神多维能力雷达")
    if not df_green.empty:
        # 提供一个下拉菜单，让面试官可以选择看谁的雷达图
        candidate_list = df_green['email'].head(10).tolist()
        selected_candidate = st.selectbox("选择候选人生成雷达图：", candidate_list)
        
        if selected_candidate:
            c_data = df_green[df_green['email'] == selected_candidate].iloc[0]
            
            # 安全获取分数，如果没有字段则默认给 0
            tech_val = float(c_data.get('Tech_Score', 0))
            proj_val = float(c_data.get('Project_Score', 0))
            stab_val = float(c_data.get('stability_score', 80)) # 稳定性字段防崩兜底
            
            # 渲染 Plotly 动态雷达图
            fig = go.Figure(data=go.Scatterpolar(
                r=[tech_val, proj_val, stab_val],
                theta=['Tech (技术底座)', 'Project (商业产出)', 'Stability (系统忠诚度)'],
                fill='toself',
                line_color='#FF4B4B'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(100, tech_val, proj_val)])),
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("无数据，无法生成雷达图。")    