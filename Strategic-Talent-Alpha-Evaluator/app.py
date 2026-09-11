import streamlit as st
import pandas as pd
import os
import json  # 🚀 新增：用于解析大模型落锁的 JSON 证据矩阵
import plotly.graph_objects as go  # 引入工业级雷达图引擎

# ==========================================
# 👑 V6.0 决策层高管可视化大屏
# ==========================================

# 1. 页面全局配置
st.set_page_config(page_title="Talent Alpha 战略看板", page_icon="👑", layout="wide")

# ==========================================
# 🎛️ 模块三 ：保留交互灵魂 - 动态筛选侧边栏
# ==========================================
st.sidebar.header("🎛️ 高管动态控制台")
st.sidebar.markdown("拖拽下方滑块，实时动态过滤黄金大盘。")
alpha_threshold = st.sidebar.slider("🏆 Talent Alpha 最低及格线", min_value=0, max_value=100, value=50, step=5)
st.sidebar.divider()
st.sidebar.caption("🇸🇬 亚太区智能战略人才发现引擎 V6.0")

# 主界面标题
st.title("👑 V6.0 Strategic-Talent-Alpha-Evaluator")
st.markdown("### 🇸🇬 亚太区人才资产分布")
st.divider()

# 2. 物理数据流安全加载机制 (完美保留红黄绿三盘读取)
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

# 动态阈值过滤
if not df_green_raw.empty and 'Talent_Alpha' in df_green_raw.columns:
    df_green = df_green_raw[df_green_raw['Talent_Alpha'] >= alpha_threshold].copy()
else:
    df_green = df_green_raw

# 3. 顶层 KPI 商业磁贴 (旧人基础指标 + 新人 LLM 战报)
total_candidates = len(df_green_raw) + len(df_yellow) + len(df_red)
v6_active = '吹牛杠杆率' in df_green_raw.columns  # 嗅探 V6.0 特性是否激活

st.markdown("#### 📡 实时战局监控 (Real-time Telemetry)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("总并发资产 (Total Ingested)", f"{total_candidates} 人")
col2.metric("🟢 黄金池生还者 (Filtered)", f"{len(df_green)} 人", f"已拦截低于 {alpha_threshold} 分者")
col3.metric("🟡 灰度审计 (Human Audit)", f"{len(df_yellow)} 人")
col4.metric("🔴 风险熔断 (Fatal Graveyard)", f"{len(df_red)} 人")

# 🚀 新增 LLM 战报 KPI
if v6_active:
    st.markdown("#### 🧠 LLM 降维打击战报")
    llm1, llm2, llm3 = st.columns(3)
    ppt_gods = len(df_green[df_green['吹牛杠杆率'] == 'High'])
    honest_coders = len(df_green[df_green['诚实自洽护航'] == True])
    
    llm1.metric("🚨 击落 PPT 战神", f"{ppt_gods} 人", "- 触发分数腰斩", delta_color="inverse")
    llm2.metric("🛡️ 护航诚实螺丝钉", f"{honest_coders} 人", "+ 触发诚实溢价")
    llm3.metric("⚙️ 核心决策引擎", "DeepSeek + Pandas Pipeline")

st.divider()

# 4. 商业降维视觉呈现 (完美融合：左侧动态染色表 + 右侧雷达图)
col_left, col_right = st.columns([2, 1])

# 初始化选中变量，供底部调查板使用
selected_candidate = None
c_data = None

with col_left:
    st.subheader(f"🏆 黄金战神排行榜 (Alpha ≥ {alpha_threshold})")
    if not df_green.empty:
        # 提取高管最关心的字段 (兼容 V5的 strategic_advice 和 V6的 LLM_高管点评)
        display_cols = ['email', 'Talent_Alpha', 'Tech_Score']
        if v6_active:
            display_cols.extend(['吹牛杠杆率', '诚实自洽护航', 'LLM_高管点评'])
        else:
            display_cols.extend(['Project_Score', 'strategic_advice'])
            
        safe_cols = [c for c in display_cols if c in df_green.columns]
        view_df = df_green[safe_cols].head(10).copy()
        
        # 🚀 注入新人：前端视觉灵魂 - Pandas Styler 动态染色
        def apply_executive_styles(val, col_name):
            if col_name == '吹牛杠杆率' and val == 'High':
                return 'background-color: #7d0000; color: white; font-weight: bold;'
            if col_name == '诚实自洽护航' and val == True:
                return 'background-color: #004d00; color: white; font-weight: bold;'
            return ''

        styled_df = view_df.style.apply(
            lambda x: [apply_executive_styles(v, x.name) for v in x], axis=0
        )
        
        # 兼容旧人的列宽与格式化配置
        st.dataframe(
            styled_df,
            use_container_width=True,
            column_config={
                "email": "候选人标识",
                "Talent_Alpha": st.column_config.NumberColumn("👑 Alpha 综合分", format="%.1f"),
                "LLM_高管点评": "🤖 AI 战略短评",
                "strategic_advice": "🤖 AI 战略短评"
            }
        )
    else:
        st.warning("🚨 当前阈值下黄金大盘为空，请调低侧边栏的分数底线！")

with col_right:
    # 🎛️ 模块一 (旧人)：完美保留雷达图
    st.subheader("🎯 战神多维能力雷达")
    if not df_green.empty:
        candidate_list = df_green['email'].head(10).tolist()
        # 记录选中者，后续联动调查板
        selected_candidate = st.selectbox("选择候选人生成雷达图：", candidate_list)

        if selected_candidate:
            c_data = df_green[df_green['email'] == selected_candidate].iloc[0]
            
            tech_val = float(c_data.get('Tech_Score', 0))
            proj_val = float(c_data.get('Project_Score', 0))
            stab_val = float(c_data.get('stability_score', 80))
            
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


# ==========================================
# 🚀 5. 深度调查大厅 (与上方选择器完美联动)
# ==========================================
if c_data is not None:
    st.divider()
    
    # 安全提取证据矩阵 (兼容 Pandas 的 NaN 和 JSON 字符串)
    raw_evidence = c_data.get("evidence_matrix", "{}")
    if pd.isna(raw_evidence):
        raw_evidence = "{}"
        
    if isinstance(raw_evidence, str):
        try:
            evidence = json.loads(raw_evidence)
        except:
            evidence = {}
    else:
        evidence = raw_evidence

    # 使用 Expander 折叠卡片
    with st.expander(f"🕵️ 深度审查档案: {selected_candidate}", expanded=True):
        st.markdown("### 📋 案件调查板 (Evidence-Based Intelligence)")
        
        # 采用 7:3 的左右分栏布局
        c1, c2 = st.columns([7, 3])
        
        with c1:
            # 🎯 核心主张
            claim = evidence.get('core_claim', '系统未提取到核心主张 (可能是旧版数据)')
            st.markdown(f"**🎯 核心主张 (Claim):**\n> {claim}")
            
            # 🟢 捕获证据
            supported = evidence.get('supporting_evidence', ["无明确证据"])
            supported_md = "\n".join([f"* 🟢 {item}" for item in supported])
            st.markdown(f"**捕获证据 (Evidence):**\n{supported_md}")
            
            # 🔴 缺失证据
            missing = evidence.get('missing_evidence', ["无"])
            missing_md = "\n".join([f"* 🔴 {item}" for item in missing])
            st.markdown(f"**缺失关键证据 (Missing):**\n{missing_md}")
            
        with c2:
            # ⚖️ 自洽度判定红绿灯
            consistency = evidence.get('consistency_score', 'Unknown')
            color_map = {"High": "#00CC66", "Medium": "#FF9900", "Low": "#FF3333"}
            color = color_map.get(consistency, "white")
            
            st.markdown("**⚖️ 证据自洽度 (Consistency):**")
            st.markdown(f"<h2 style='color:{color}; margin-top:0px;'>{consistency}</h2>", unsafe_allow_html=True)
            
        # 🤖 底部横穿 AI 短评
        strategic_advice = c_data.get('LLM_高管点评', c_data.get('strategic_advice', '无建议'))
        st.info(f"**🤖 AI 战略断案:** {strategic_advice}")