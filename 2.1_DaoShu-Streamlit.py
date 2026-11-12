
# -*- coding: utf-8 -*-
"""
导数的概念及其几何意义 - 交互式教学应用
适用：大学高等数学（同济版上册 第二章第一节）
作者：AI教学助手
使用方法：在当前目录打开终端，执行 streamlit run 导数交互教学.py
"""

# ============================================
# 第一部分：导入需要的工具库（无需修改，自动安装即可）
# ============================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform

# ============================================
# 第二部分：配置页面基础样式（无需修改）
# ============================================
st.set_page_config(
    page_title="导数的概念及其几何意义 - 交互式教学",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
def configure_chinese_font():
    # 直接加载同目录下的simhei.ttf，不依赖任何系统字体，100%生效
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "simhei.ttf")
    
    # 加载字体并清空matplotlib字体缓存，防止不生效
    font_manager.fontManager.addfont(font_path)
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
    

configure_chinese_font()

# 侧边栏导航：和教案7个环节完全对应
st.sidebar.title("📚 课程导航")
page = st.sidebar.radio(
    "选择教学环节",
    [
        "0. 课程导入：两个经典问题",
        "1. 导数的定义",
        "2. 用定义求导数例题",
        "3. 单侧导数与导函数",
        "4. 可导与连续的关系",
        "5. 几何意义：割线变切线✨",
        "6. 切线与法线方程",
        "7. 课堂小结与练习",
        "🗒️ 完整讲稿与板书"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 使用提示：\n"
    "1. 左侧切换教学环节\n"
    "2. 带✨的环节有交互滑块，可以拖动参数看动态效果\n"
    "3. 所有公式支持自动渲染，和教材一致\n"
    "4. 讲稿与板书可在最后一页查看完整内容"
)

# ============================================
# 第三部分：每个页面的实际内容（按教案逐节编写）
# ============================================

# 0. 课程导入
if page == "0. 课程导入：两个经典问题":
    st.title("📖 导数的概念及其几何意义")
    st.subheader("—— 大学高等数学 · 第二章第一节")
    st.markdown("---")
    
    st.markdown("### 一、课程导入：两个经典问题")
    st.markdown("导数这个概念，来源于17世纪科学研究中两个完全不同的问题：**变速直线运动的瞬时速度** 和 **平面曲线的切线斜率**。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 问题1：变速直线运动的瞬时速度")
        st.markdown("""
        设物体做直线运动，位置随时间变化的函数为 $s = s(t)$：
        1. 从 $t_0$ 到 $t_0+\Delta t$，物体走过的路程：$\Delta s = s(t_0+\Delta t) - s(t_0)$
        2. 这段时间的**平均速度**：
        $$\\bar{v} = \\frac{\\Delta s}{\\Delta t} = \\frac{s(t_0+\\Delta t) - s(t_0)}{\\Delta t}$$
        3. 当时间间隔 $\\Delta t \\to 0$ 时，平均速度无限接近 $t_0$ 时刻的**瞬时速度**：
        $$v(t_0) = \\lim_{\\Delta t \\to 0}\\frac{\\Delta s}{\\Delta t} = \\lim_{\\Delta t \\to 0}\\frac{s(t_0+\\Delta t) - s(t_0)}{\\Delta t}$$
        """)
        
        st.info("🚩 这就是历史上牛顿研究导数的出发点：描述运动的瞬时变化率。")
    
    with col2:
        st.markdown("#### 问题2：平面曲线的切线斜率")
        st.markdown("""
        给定曲线 $y=f(x)$，求在点 $M(x_0, f(x_0))$ 处的切线斜率：
        1. 在曲线上另取一点 $N(x_0+\Delta x, f(x_0+\Delta x))$
        2. 割线 $MN$ 的斜率：
        $$k_{\\text{割}} = \\frac{\\Delta y}{\\Delta x} = \\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x}$$
        3. 当 $N$ 沿曲线无限靠近 $M$（即 $\\Delta x \\to 0$）时，割线斜率的极限就是**切线斜率**：
        $$k_{\\text{切}} = \\lim_{\\Delta x \\to 0}\\frac{\\Delta y}{\\Delta x} = \\lim_{\\Delta x \\to 0}\\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x}$$
        """)
        
        st.info("🚩 这是莱布尼茨研究导数的出发点：描述曲线的陡峭程度。")
    
    st.markdown("---")
    st.success("""
    🎯 本质发现：两个完全不同的问题，最终都归结为同一个数学结构——
    **函数增量与自变量增量之比，当自变量增量趋于0时的极限**。
    这就是今天要学的**导数**。
    """)

# 1. 导数的定义
elif page == "1. 导数的定义":
    st.title("1. 导数的定义")
    st.markdown("---")
    
    st.markdown("### 一、严格定义")
    st.markdown("""
    设函数 $y=f(x)$ 在点 $x_0$ 的某邻域内有定义，当自变量 $x$ 在 $x_0$ 处取得增量 $\\Delta x$ 时，
    相应的函数增量为 $\\Delta y = f(x_0+\\Delta x) - f(x_0)$。如果极限
    $$\\lim_{\\Delta x \\to 0}\\frac{\\Delta y}{\\Delta x} = \\lim_{\\Delta x \\to 0}\\frac{f(x_0+\\Delta x)-f(x_0)}{\\Delta x}$$
    存在，则称函数 $y=f(x)$ 在点 $x_0$ 处**可导**，并称这个极限值为函数 $y=f(x)$ 在点 $x_0$ 处的导数，记作：
    $$f'(x_0),\\quad y'\\big|_{x=x_0},\\quad \\frac{dy}{dx}\\big|_{x=x_0},\\quad \\frac{df}{dx}\\big|_{x=x_0}$$
    """)
    
    st.markdown("### 二、导数定义的两种等价写法")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**增量形式（最常用）：**")
        st.latex(r"f'(x_0) = \lim_{h \to 0}\frac{f(x_0+h)-f(x_0)}{h}")
    with col2:
        st.markdown("**端点形式（常用于单侧导数）：**")
        st.latex(r"f'(x_0) = \lim_{x \to x_0}\frac{f(x)-f(x_0)}{x-x_0}")
    
    st.markdown("### 三、用定义求导数的三步法")
    st.info("""
    📝 求导三步口诀：**一差、二比、三极限**
    1. 求增量：$\Delta y = f(x_0+\Delta x)-f(x_0)$
    2. 算比值：$\displaystyle \\frac{\Delta y}{\Delta x} = \\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}$
    3. 取极限：$\displaystyle f'(x_0) = \lim_{\Delta x \\to 0}\\frac{\Delta y}{\Delta x}$
    """)
    
    st.markdown("### 四、导数的本质含义")
    st.markdown("""
    导数 $f'(x_0)$ 的本质，就是函数在 $x_0$ 处的**瞬时变化率**：
    - 物理意义：瞬时速度、瞬时加速度、电流强度等；
    - 几何意义：曲线在该点的切线斜率；
    - 经济意义：边际成本、边际收益；
    - 任何"变化快慢"的问题，最终都是导数问题。
    """)

# 2. 用定义求导数例题
elif page == "2. 用定义求导数例题":
    st.title("2. 例题：用定义求导数")
    st.markdown("---")
    
    st.markdown("### 例1：求常函数的导数")
    st.markdown("求函数 $f(x) = C$（$C$ 为常数）的导数。")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = f(x+h)-f(x) = C - C = 0$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{0}{h} = 0$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0}\\frac{\\Delta y}{h} = 0$
        
        **结论**：常数的导数等于0，即 $(C)' = 0$。
        """)
    
    st.markdown("---")
    st.markdown("### 例2：求幂函数 $f(x)=x^2$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = (x+h)^2 - x^2 = 2xh + h^2$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{2xh+h^2}{h} = 2x + h$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0}(2x+h) = 2x$
        
        **结论**：$(x^2)' = 2x$。推广：$(x^n)' = nx^{n-1}$。
        """)
    
    st.markdown("---")
    st.markdown("### 例3：求正弦函数 $f(x)=\\sin x$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = \\sin(x+h) - \\sin x = 2\\cos\\left(x+\\frac{h}{2}\\right)\\sin\\frac{h}{2}$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\cos\\left(x+\\frac{h}{2}\\right)\\cdot\\frac{\\sin(h/2)}{h/2}$
        3. 取极限：利用 $\\lim_{t\\to 0}\\frac{\\sin t}{t}=1$，得 $f'(x) = \\cos x$
        
        **结论**：$(\\sin x)' = \\cos x$，同理 $(\\cos x)' = -\\sin x$。
        """)
    
    st.markdown("---")
    st.warning("""
    ⚠️ 注意：用定义求导是基础方法，后续我们会学习求导公式表，做题时直接用公式即可，不用每次都走三步法。
    但三步法是理解导数概念的核心，考试常考分段函数在分界点的导数，必须用定义计算。
    """)

# 3. 单侧导数与导函数
elif page == "3. 单侧导数与导函数":
    st.title("3. 单侧导数与导函数")
    st.markdown("---")
    
    st.markdown("### 一、左导数与右导数")
    st.markdown("""
    导数是一个双侧极限，因此可以定义单侧导数：
    - **左导数**：$\\displaystyle f'_-(x_0) = \\lim_{h \\to 0^-}\\frac{f(x_0+h)-f(x_0)}{h}$
    - **右导数**：$\\displaystyle f'_+(x_0) = \\lim_{h \\to 0^+}\\frac{f(x_0+h)-f(x_0)}{h}$
    
    函数在某点可导的**充要条件**是：左导数和右导数都存在且相等：
    $$f'(x_0)\\text{ 存在} \\iff f'_-(x_0) = f'_+(x_0)$$
    """)
    
    st.info("🚩 这个充要条件主要用于判断分段函数在分界点处是否可导。")
    
    st.markdown("### 二、导函数")
    st.markdown("""
    如果函数 $y=f(x)$ 在开区间 $I$ 内每一点都可导，就称 $f(x)$ 在 $I$ 内可导。
    这时对任意 $x\\in I$，都对应一个确定的导数值 $f'(x)$，这就构成了一个新的函数，
    称为**导函数**（简称导数），记作：
    $$y',\\quad f'(x),\\quad \\frac{dy}{dx},\\quad \\frac{df(x)}{dx}$$
    
    ⚠️ 注意区分：
    - $f'(x_0)$ 是一个**具体的数**，表示在 $x_0$ 点的导数值；
    - $f'(x)$ 是一个**函数**，是 $f(x)$ 的导函数。
    关系：$f'(x_0) = f'(x)\\big|_{x=x_0}$
    """)

# 4. 可导与连续的关系
elif page == "4. 可导与连续的关系":
    st.title("4. 可导与连续的关系")
    st.markdown("---")
    
    st.markdown("### 核心定理")
    st.success("**定理**：如果函数 $y=f(x)$ 在点 $x_0$ 处可导，则函数在该点必连续。")
    
    st.markdown("### 证明过程")
    st.markdown("""
    已知 $f(x)$ 在 $x_0$ 处可导，即极限
    $$\\lim_{\\Delta x\\to 0}\\frac{\\Delta y}{\\Delta x} = f'(x_0)$$
    存在。根据极限与无穷小的关系：
    $$\\frac{\\Delta y}{\\Delta x} = f'(x_0) + \\alpha, \\quad \\text{其中}\\alpha\\to 0\\ (\\Delta x\\to0)$$
    两边同乘 $\\Delta x$ 得：
    $$\\Delta y = f'(x_0)\\Delta x + \\alpha\\cdot\\Delta x$$
    当 $\\Delta x\\to0$ 时，$\\Delta y\\to0$，根据连续的定义，函数在 $x_0$ 处连续。
    """)
    
    st.markdown("### 注意：反之不成立！")
    st.error("""
    ❌ 连续**不一定**可导！函数在某点连续是可导的**必要不充分条件**。
    
    典型反例：
    1. **尖点反例**：$f(x) = |x|$ 在 $x=0$ 处连续，但左导数=-1，右导数=1，不相等，因此不可导；
    2. **垂直切线反例**：$f(x) = \\sqrt[3]{x}$ 在 $x=0$ 处连续，但导数为无穷大，切线垂直于x轴，不可导。
    """)
    
    # 绘制两个反例图像
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(5,4))
        x1 = np.linspace(-2,2,200)
        y1 = np.abs(x1)
        ax1.plot(x1, y1, linewidth=2, color='#1f77b4')
        ax1.scatter(0,0, color='red', zorder=5, s=50)
        ax1.set_title('反例1: f(x)=|x| 在x=0处尖点不可导', fontsize=12)
        ax1.grid(alpha=0.3)
        ax1.set_aspect('equal')
        st.pyplot(fig1)
    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(5,4))
        x2 = np.linspace(-2,2,200)
        y2 = np.cbrt(x2)
        ax2.plot(x2, y2, linewidth=2, color='#ff7f0e')
        ax2.axvline(x=0, color='red', linestyle='--', label='垂直切线')
        ax2.scatter(0,0, color='red', zorder=5, s=50)
        ax2.set_title('反例2: f(x)=∛x 在x=0处垂直切线不可导', fontsize=12)
        ax2.grid(alpha=0.3)
        ax2.set_aspect('equal')
        ax2.legend()
        st.pyplot(fig2)

# 5. 几何意义：割线变切线（核心交互环节）
elif page == "5. 几何意义：割线变切线✨":
    st.title("5. 导数的几何意义：割线逼近切线✨")
    st.markdown("---")
    
    st.markdown("### 一、几何意义核心结论")
    st.success("""
    函数 $y=f(x)$ 在点 $x_0$ 处的导数 $f'(x_0)$，在几何上表示**曲线 $y=f(x)$ 在点 $M(x_0,f(x_0))$ 处的切线斜率**：
    $$k_{\\text{切}} = f'(x_0) = \\tan\\alpha$$
    其中 $\\alpha$ 是切线与x轴正方向的夹角。
    """)
    
    st.markdown("### 二、交互演示：拖动滑块看割线如何变成切线")
    st.info("💡 拖动下方的Δx滑块，让N点靠近M点，观察割线斜率如何逼近切线斜率：")
    
    # 交互参数选择
    func_choice = st.selectbox(
        "选择演示函数",
        ["f(x) = x²（抛物线）", "f(x) = sin(x)（正弦曲线）", "f(x) = x³（三次曲线）"],
        index=0
    )
    x0 = st.slider("选择定点M的横坐标x₀", min_value=-1.5, max_value=1.5, value=1.0, step=0.1)
    delta_x = st.slider("Δx（N点与M点的水平距离）", min_value=0.01, max_value=2.0, value=1.0, step=0.01)
    
    # 定义函数
    if func_choice == "f(x) = x²（抛物线）":
        f = lambda x: x**2
        f_prime = lambda x: 2*x
    elif func_choice == "f(x) = sin(x)（正弦曲线）":
        f = lambda x: np.sin(x)
        f_prime = lambda x: np.cos(x)
    else:
        f = lambda x: x**3
        f_prime = lambda x: 3*x**2
    
    y0 = f(x0)
    slope_tangent = f_prime(x0)
    x_N = x0 + delta_x
    y_N = f(x_N)
    slope_secant = (y_N - y0)/delta_x
    
        # 绘图（横版适配投影，不瘦长）
    fig, ax = plt.subplots(figsize=(8, 5))  # 8:5宽屏比例，适合教室投影
    
    # 根据函数动态设置绘图范围，避免x³y值过高把图拉变形
    if func_choice == "f(x) = x³（三次曲线）":
        x_plot = np.linspace(-2, 2.5, 500)  # x³增长太快，缩小x范围
    else:
        x_plot = np.linspace(-2.5, 3.5, 500)
    
    ax.plot(x_plot, f(x_plot), linewidth=2.2, label=r"曲线 $y=f(x)$", color='#1f77b4')
    
    # 画割线
    x_sec = np.linspace(x0-0.8, x_N+0.8, 100)
    y_sec = y0 + slope_secant*(x_sec - x0)
    ax.plot(x_sec, y_sec, color='orange', linestyle='--', linewidth=2.2, 
            label=fr"割线MN，斜率$k={slope_secant:.3f}$")
    
    # 画切线
    x_tan = np.linspace(x0-2.5, x0+2.5, 100)
    y_tan = y0 + slope_tangent*(x_tan - x0)
    ax.plot(x_tan, y_tan, color='red', linewidth=2.2, 
            label=fr"切线，斜率$k={slope_tangent:.3f}$（即$f'({x0:.1f})$）")
    
    # 标记M、N点
    ax.scatter(x0, y0, color='red', s=120, zorder=5, edgecolor='white', linewidth=1.2,
               label=fr"M点$({x0:.1f}, {y0:.2f})$")
    ax.scatter(x_N, y_N, color='orange', s=120, zorder=5, edgecolor='white', linewidth=1.2,
               label=fr"N点$({x_N:.2f}, {y_N:.2f})$")
    
    # 画Δx、Δy辅助虚线
    ax.plot([x0, x_N], [y0, y0], 'k--', alpha=0.6, linewidth=1.2)
    ax.plot([x_N, x_N], [y0, y_N], 'k--', alpha=0.6, linewidth=1.2)
    # 标注位置自适应，不会跑出图外
    ax.annotate(r'$\Delta x$', ((x0+x_N)/2, y0-0.2), fontsize=13, ha='center')
    ax.annotate(r'$\Delta y$', (x_N+0.1, (y0+y_N)/2), fontsize=13, va='center')
    
    # 坐标轴美化
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper left')  # 图例放左上角，不挡曲线
    
    # 自动设置y轴范围，留0.5边距不截断
    all_y = np.concatenate([f(x_plot), y_sec, y_tan, [y0-1, y_N+1]])
    ax.set_ylim(bottom=np.min(all_y)-0.5, top=np.max(all_y)+0.5)
    ax.set_xlim(np.min(x_plot)-0.2, np.max(x_plot)+0.2)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    
    plt.tight_layout()
    # 铺满页面宽度，投影时更大更清楚，图高度按8:5比例自动适配
    st.pyplot(fig, use_container_width=False)

    
    col1, col2, col3 = st.columns(3)
    col1.metric("当前Δx大小", f"{delta_x:.2f}")
    col2.metric("割线斜率", f"{slope_secant:.3f}")
    col3.metric("切线斜率（精确导数值）", f"{slope_tangent:.3f}", delta=f"{slope_secant - slope_tangent:.3f}（差值）")
    
    st.markdown("---")
    st.info("""
    🎯 观察发现：当Δx越接近0，割线斜率和切线斜率的差值就越接近0，割线最终与切线重合。
    这就是导数几何意义的动态过程——**切线是割线的极限位置**。
    """)

# 6. 切线与法线方程
elif page == "6. 切线与法线方程":
    st.title("6. 切线方程与法线方程")
    st.markdown("---")
    
    st.markdown("### 一、公式")
    st.markdown("""
    根据导数的几何意义，曲线 $y=f(x)$ 在点 $M(x_0,y_0)$ 处：
    
    1. **切线方程**（过点M，斜率为 $f'(x_0)$）：
    $$y - y_0 = f'(x_0)(x - x_0)$$
    
    2. **法线方程**（过点M，与切线垂直，斜率为 $-1/f'(x_0)$，当 $f'(x_0)\\neq0$ 时）：
    $$y - y_0 = -\\frac{1}{f'(x_0)}(x - x_0)$$
    
    特殊情况：
    - 若 $f'(x_0)=0$，切线水平 $y=y_0$，法线垂直 $x=x_0$；
    - 若 $f'(x_0)=\\infty$，切线垂直 $x=x_0$，法线水平 $y=y_0$。
    """)
    
    st.markdown("### 二、例题")
    st.markdown("求抛物线 $y=x^2$ 在点 $(1,1)$ 处的切线方程和法线方程。")
    with st.expander("点击查看解答"):
        st.markdown("""
        解：首先求导：$f'(x)=2x$，因此在x=1处导数 $f'(1)=2$。
        - 切线方程：$y - 1 = 2(x - 1)$，即 $y = 2x - 1$
        - 法线方程：$y - 1 = -\\frac{1}{2}(x - 1)$，即 $y = -\\frac{1}{2}x + \\frac{3}{2}$
        """)
        
        # 画图展示
        fig, ax = plt.subplots(figsize=(5, 5))
        x = np.linspace(-2, 4, 400)
        ax.plot(x, x**2, label=r"$y = x^2$", linewidth=2, color='#1f77b4')
        ax.plot(x, 2*x - 1, label=r"切线 $y = 2x - 1$", color='red', linewidth=2)
        ax.plot(x, -0.5*x + 1.5, label=r"法线 $y = -\dfrac{1}{2}x + \dfrac{3}{2}$", color='green', linewidth=2)
        ax.scatter(1, 1, color='black', s=120, zorder=5, edgecolor='white', linewidth=1.2)
        
        # 手动设置坐标轴范围，不要用 set_aspect('equal')
        ax.set_xlim(-2, 4)
        ax.set_ylim(-2, 4)
        
        # 画x轴y轴参考线
        ax.axhline(0, color='gray', linewidth=0.8)
        ax.axvline(0, color='gray', linewidth=0.8)
        
        ax.grid(alpha=0.3, linestyle='--')
        ax.legend(fontsize=11, loc='upper left')
        ax.set_xlabel('x', fontsize=12)
        ax.set_ylabel('y', fontsize=12)
        ax.set_title(r'抛物线 $y=x^2$ 在点 $(1,1)$ 处的切线与法线', fontsize=13)
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=False)


# 7. 课堂小结与练习
elif page == "7. 课堂小结与练习":
    st.title("7. 课堂小结与课堂练习")
    st.markdown("---")
    
    st.markdown("### 一、本节课核心知识点总结")
    st.markdown("""
    1. **一个定义**：导数是函数增量与自变量增量之比的极限，本质是瞬时变化率；
    2. **一个方法**：用定义求导三步法——一差、二比、三极限；
    3. **一个充要条件**：某点可导 ⇨ 左右导数存在且相等；
    4. **一个关系**：可导必连续，连续不一定可导；
    5. **一个几何意义**：导数是切线斜率，切线是割线的极限位置；
    6. **两个方程**：切线方程、法线方程公式。
    """)
    
    st.markdown("### 二、课堂小练习")
    
    q1 = st.radio(
        "1. 函数f(x)在x₀处连续是在该点可导的（  ）",
        ["A. 充分但不必要条件", "B. 必要但不充分条件", "C. 充分必要条件", "D. 既不充分也不必要条件"],
        index=None
    )
    if q1:
        if q1 == "B. 必要但不充分条件":
            st.success("✅ 回答正确！可导必连续，连续不一定可导。")
        else:
            st.error("❌ 不对哦，回忆可导与连续的关系定理。")
    
    st.markdown("---")
    q2 = st.radio(
        "2. 函数f(x)=|x|在x=0处（  ）",
        ["A. 连续且可导", "B. 连续但不可导", "C. 不连续但可导", "D. 不连续也不可导"],
        index=None
    )
    if q2:
        if q2 == "B. 连续但不可导":
            st.success("✅ 回答正确！f(x)=|x|在0点是尖点，左右导数不相等，不可导。")
        else:
            st.error("❌ 不对哦，回忆我们讲过的尖点反例。")
    
    st.markdown("---")
    q3 = st.text_input("3. 用定义求f(x)=x³在x=1处的导数f'(1) = ?（输入数字即可）")
    if q3:
        if q3.strip() == "3":
            st.success("✅ 回答正确！f'(x)=3x²，因此f'(1)=3。")
        else:
            st.error("❌ 答案是3，回忆幂函数求导公式或用三步法计算。")

# 8. 完整讲稿与板书
elif page == "🗒️ 完整讲稿与板书":
    st.title("🗒️ 完整讲稿与板书设计")
    st.markdown("---")
    st.markdown("""
    ### 板书总布局（三栏式黑板）
    
    | 左侧副板书区（图形/草稿） | 中心主板书区（保留全课） | 右侧副板书区（例题演算） |
    |--------------------------|--------------------------|--------------------------|
    | 割线→切线示意图<br>反例图像 | 一、导数定义<br>二、三步求导法<br>三、单侧导数/导函数<br>四、可导与连续关系<br>五、几何意义<br>六、切线法线方程 | 例题1-3演算过程<br>学生提问草稿 |
    
    ### 开场讲稿
    > "同学们好，今天我们开始学导数。大家有没有想过，坐高铁的时候，仪表盘显示的'时速300公里'到底是什么？如果我说你在某一个'瞬间'的速度，那这个瞬间时间长度是0啊，路程除以0怎么会有意义？这就是当年牛顿研究的问题——瞬时速度，也就是我们今天导数的来源。"
    
    ### 核心环节讲稿
    > "大家看屏幕上的这个交互演示：当N点离M很远的时候，割线很陡；你拖动滑块让N一点点靠近M，割线就会绕着M点转，最后稳定在一个位置——这个位置就是切线。这个转动过程中，割线斜率的极限，就是导数。所以导数不是什么神秘的东西，它就是割线斜率的极限，就是切线的斜率。"
    
    > "大家一定要记住：可导一定连续，但连续不一定可导。就像|x|那个尖点，图形是连在一起的，但是在尖点那里，左边斜率是-1，右边斜率是1，左边和右边对不上，所以这一点就没有切线，也就不可导。"
    
    """)

# ============================================
# 第四部分：页脚
# ============================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>📐 导数的概念及其几何意义 · 大学高等数学交互式教学应用</div>",
    unsafe_allow_html=True
)
