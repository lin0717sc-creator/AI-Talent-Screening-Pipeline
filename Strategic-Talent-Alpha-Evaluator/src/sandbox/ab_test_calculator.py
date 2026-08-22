def calculate_ab_test_roi(manual_hours, manual_hourly_rate, ai_api_cost, ai_runtime_minutes):
    """
    冷酷的财务算账引擎：剥离虚荣指标，计算真实 ROI
    """
    # 对照组（V1.0）：纯人工成本
    v1_cost = manual_hours * manual_hourly_rate
    
    # 实验组（V2.0）：AI 引擎成本 (API 费用 + 极少量的运行时间成本)
    v2_cost = ai_api_cost + (ai_runtime_minutes / 60.0 * manual_hourly_rate)
    
    # 增量效应（Treatment Effect）计算
    redundancy_cost_reduction = v1_cost - v2_cost
    roi_percentage = (redundancy_cost_reduction / v1_cost) * 100
    
    print(f"💰 V1.0 人工对照组总成本: ${v1_cost}")
    print(f"⚡ V2.0 AI 实验组总成本: ${v2_cost}")
    print(f"🔥 增量效应 (Treatment Effect): 节省了 ${redundancy_cost_reduction}")
    print(f"📈 冗余成本消除 (Redundancy Cost Reduction): -{roi_percentage:.2f}%")
    
    return redundancy_cost_reduction

# 你的强控主权试射：
calculate_ab_test_roi(manual_hours=40, manual_hourly_rate=30, ai_api_cost=5.50, ai_runtime_minutes=15)
