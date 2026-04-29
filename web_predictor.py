"""
超精密加工工件疲劳寿命在线预测工具
用于 2026 年全国大学生统计建模大赛
"""

import streamlit as st
import numpy as np

# ========== 页面标题 ==========
st.set_page_config(page_title="工件寿命预测", page_icon="🔧")
st.title("🔧 超精密加工工件疲劳寿命预测")
st.caption("基于指数模型 Nf = 3.311 · e^(-0.836·Ra)  |  R² = 0.659")

# ========== 输入区 ==========
st.markdown("### 📋 输入工艺参数")
col1, col2, col3 = st.columns(3)

with col1:
    f = st.number_input("进给量 f (mm/r)", min_value=0.03, max_value=0.18, value=0.10, step=0.01)

with col2:
    vc = st.number_input("切削速度 vc (m/min)", min_value=50, max_value=300, value=200, step=10)

with col3:
    ap = st.number_input("背吃刀量 ap (μm)", min_value=1, max_value=20, value=5, step=1)

# ========== 预测按钮 ==========
if st.button("🔍 开始预测", type="primary"):

    # 第一阶段：f → Ra
    Ra = 12.5 * (f ** 1.8)

    # 第二阶段：Ra → 寿命
    Nf = 3.311 * np.exp(-0.836 * Ra)

    # 预测区间
    se = 0.42
    ln_Nf = np.log(Nf)
    lower = np.exp(ln_Nf - 1.96 * se)
    upper = np.exp(ln_Nf + 1.96 * se)

    # ========== 结果输出 ==========
    st.markdown("---")
    st.markdown("### 📊 预测结果")

    c1, c2, c3 = st.columns(3)
    c1.metric("表面粗糙度 Ra", f"{Ra:.3f} μm")
    c2.metric("工件疲劳寿命 Nf", f"{Nf:.2f} ×10⁵ 次")
    c3.metric("相对基准变化", f"{(Nf/2.45 - 1)*100:+.1f}%")

    st.info(f"📏 95% 预测区间：**[{lower:.2f}, {upper:.2f}] ×10⁵ 次**")

    # 计算过程
    with st.expander("📐 查看计算步骤"):
        st.markdown(f"""
        1. **第一阶段**：经验公式 Ra = 12.5 · f^1.8
           - Ra = 12.5 × {f:.2f}^1.8 = **{Ra:.3f} μm**

        2. **第二阶段**：指数模型 Nf = 3.311 · e^(-0.836·Ra)
           - Nf = 3.311 × e^(-0.836 × {Ra:.3f}) = **{Nf:.2f} ×10⁵ 次**

        3. **预测区间**（基于残差标准误 se = 0.42）
           - 95% PI = [{lower:.2f}, {upper:.2f}] ×10⁵ 次
        """)

st.markdown("---")
st.caption("四川工程职业技术大学 | 2026 年全国大学生统计建模大赛")