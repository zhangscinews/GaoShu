# -*- coding: utf-8 -*-
"""
导数的概念及其几何意义 - 交互式教学应用
适用：大学高等数学（同济版上册 第二章第一节）
作者：J. Zhang, et al.
使用方法：在当前目录打开终端，执行 streamlit run 导数交互教学.py
"""

# ============================================
# 第一部分：导入需要的工具库（无需修改，自动安装即可）
# ============================================
import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform
import os

# ============================================
# 第二部分：配置页面基础样式（无需修改）
# ============================================
st.set_page_config(
    page_title="导数的概念及其几何意义 - 交互式教学",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 容错版中文字体配置：找不到自带字体就自动用系统字体，不会报错
def configure_chinese_font():
    # 先尝试加载同目录下的simhei.ttf
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "simhei.ttf")
    
    font_loaded = False
    if os.path.exists(font_path):
        try:
            font_manager.fontManager.addfont(font_path)
            font_prop = font_manager.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            font_loaded = True
        except:
            pass
    
    # 如果找不到自带字体，自动用系统已安装的中文字体（兼容云端Linux/Windows/Mac）
    if not font_loaded:
        plt.rcParams['font.sans-serif'] = [
            'Noto Sans CJK SC',
            'Noto Sans CJK JP',
            'WenQuanYi Micro Hei',
            'SimHei',
            'Microsoft YaHei',
            'PingFang SC',
            'Arial Unicode MS',
            'DejaVu Sans'
        ]
    
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
        "8. 计算实践与代码实现✨",
        "9. 课程思政"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 使用提示：\n"
    "1. 左侧切换教学环节\n"
    "2. 带✨的环节有交互滑块，可以拖动参数看动态效果\n"
    "3. 所有公式支持自动渲染，和教材一致\n"
    "4. 第 8 页为「计算实践与代码实现」（含5道例题和可拖动交互滑块），第 9 页为「课程思政」"
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
        ax1.set_xlim(-2,2)
        ax1.set_ylim(-0.5,2.5)
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
        ax2.set_xlim(-2,2)
        ax2.set_ylim(-2,2)
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
        index=None,
        key="q1"
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
        index=None,
        key="q2"
    )
    if q2:
        if q2 == "B. 连续但不可导":
            st.success("✅ 回答正确！f(x)=|x|在0点是尖点，左右导数不相等，不可导。")
        else:
            st.error("❌ 不对哦，回忆我们讲过的尖点反例。")
    
    st.markdown("---")
    q3 = st.text_input("3. 用定义求f(x)=x³在x=1处的导数f'(1) = ?（输入数字即可）", key="q3")
    if q3:
        if q3.strip() == "3":
            st.success("✅ 回答正确！f'(x)=3x²，因此f'(1)=3。")
        else:
            st.error("❌ 答案是3，回忆幂函数求导公式或用三步法计算。")

    # ==============================================
    # 新增练习题（保留原有3道题不变，在此基础上增加）
    # ==============================================
    st.markdown("---")
    st.markdown("#### 🎯 进阶练习")

    # 练习4：导数定义的等价形式
    st.markdown("---")
    q4 = st.radio(
        "4. 下列极限中，等于 $f'(x_0)$ 的是（  ）",
        [
            "A. $\\lim\\limits_{h\\to 0}\\dfrac{f(x_0+2h)-f(x_0)}{h}$",
            "B. $\\lim\\limits_{h\\to 0}\\dfrac{f(x_0)-f(x_0-h)}{h}$",
            "C. $\\lim\\limits_{h\\to 0}\\dfrac{f(x_0+h)-f(x_0-h)}{h}$",
            "D. $\\lim\\limits_{h\\to 0}\\dfrac{f(x_0+h)+f(x_0-h)-2f(x_0)}{h}$"
        ],
        index=None,
        key="q4"
    )
    if q4:
        if q4.startswith("B"):
            st.success("✅ 回答正确！令t=-h，$\\lim\\limits_{h\\to 0}\\dfrac{f(x_0)-f(x_0-h)}{h}=\\lim\\limits_{t\\to 0}\\dfrac{f(x_0+t)-f(x_0)}{t}=f'(x_0)$，正好是导数的增量形式。")
            with st.expander("点击查看其他选项错在哪里"):
                st.markdown("""
                - A选项结果是 $2f'(x_0)$，分子是2h的增量，分母是h，差了系数2；
                - C选项结果是 $2f'(x_0)$，分子是从x₀-h到x₀+h共2h的增量，分母是h，差了系数2；
                - D选项结果是0，分子是二阶增量，除以h极限为0。
                """)
        else:
            st.error("❌ 不对哦，回忆导数增量形式的定义，分子分母的增量必须对应。")

    # 练习5：常数函数导数
    st.markdown("---")
    q5 = st.radio(
        "5. 常数函数 $f(x)=5$ 的导数 $f'(x)$ 等于（  ）",
        ["A. 5", "B. 0", "C. 1", "D. 不存在"],
        index=None,
        key="q5"
    )
    if q5:
        if q5 == "B. 0":
            st.success("✅ 回答正确！常数的增量恒为0，差商为0，极限为0，因此常数的导数是0——常数函数不变化，变化率自然为0。")
        else:
            st.error("❌ 不对哦，回忆我们讲过的常数函数求导例题，常数不随x变化，变化率是0。")

    # 练习6：滑块交互实践题（猜导数值）
    st.markdown("---")
    st.markdown("##### 🎮 交互实践题：猜一猜x=1处的导数是多少？")
    st.markdown("拖动下方滑块选择你猜测的数值，提交后可以看到真实导数值和你的误差：")
    guess_slope = st.slider("你猜测 $f(x)=x^2$ 在x=1处的导数值是：", min_value=0.0, max_value=4.0, value=1.0, step=0.1, key="q6_slider")
    submit_q6 = st.button("提交答案", key="q6_submit")
    if submit_q6:
        true_slope = 2.0
        error = abs(guess_slope - true_slope)
        if error < 0.01:
            st.success(f"🎉 完全正确！f'(1)=2.0，你的猜测值是{guess_slope:.1f}，误差{error:.3f}，和真实值完全一致！")
        elif error < 0.5:
            st.info(f"很接近了！真实值是2.0，你的猜测值是{guess_slope:.1f}，误差{error:.3f}，再回忆一下幂函数求导公式：$(x^2)'=2x$。")
        else:
            st.warning(f"差距有点大哦！真实值是2.0，你的猜测值是{guess_slope:.1f}，误差{error:.3f}。记住：抛物线在x=1处的切线斜率是2，对应切线方程是y=2x-1。")
        
        # 绘制图像展示
        fig_q6, ax_q6 = plt.subplots(figsize=(8,5))
        x_q6 = np.linspace(-1, 3, 400)
        ax_q6.plot(x_q6, x_q6**2, linewidth=2.2, color='#1f77b4', label=r"$y=x^2$")
        ax_q6.plot(x_q6, 2*x_q6 - 1, linewidth=2.2, color='red', label=r"真实切线 $y=2x-1$，斜率=2")
        if error >= 0.5:
            ax_q6.plot(x_q6, guess_slope*(x_q6 - 1) + 1, linewidth=2, color='orange', linestyle='--', label=fr"你猜测的切线，斜率={guess_slope:.1f}")
        ax_q6.scatter(1, 1, color='black', s=120, zorder=5, label="切点(1,1)")
        ax_q6.axhline(0, color='gray', linewidth=0.8)
        ax_q6.axvline(0, color='gray', linewidth=0.8)
        ax_q6.grid(alpha=0.3, linestyle='--')
        ax_q6.legend(fontsize=11)
        ax_q6.set_xlabel('x', fontsize=12)
        ax_q6.set_ylabel('y', fontsize=12)
        ax_q6.set_title("抛物线在(1,1)处的切线", fontsize=13)
        ax_q6.set_ylim(-1, 5)
        plt.tight_layout()
        st.pyplot(fig_q6)

    # 练习7：切线方程计算
    st.markdown("---")
    q7 = st.radio(
        "7. 曲线 $y=x^2$ 在点 $(2,4)$ 处的切线方程是（  ）",
        ["A. $y=4x-4$", "B. $y=2x$", "C. $y=4x+4$", "D. $y=2x+2$"],
        index=None,
        key="q7"
    )
    if q7:
        if q7.startswith("A"):
            st.success("✅ 回答正确！f'(x)=2x，f'(2)=4，代入点斜式：y-4=4(x-2)，整理得y=4x-4。")
        else:
            st.error("❌ 不对哦，先求切点处的导数值得到斜率，再代入点斜式公式计算。")
            st.info("提示：点斜式方程是$y-y_0 = f'(x_0)(x-x_0)$，x=2处导数f'(2)=4，y0=4，代入计算即可。")

    # 练习8：可导性判断（分段函数）
    st.markdown("---")
    q8 = st.radio(
        "8. 设函数 $f(x)=\\begin{cases}x^2, & x\\leq1 \\\\ ax+b, & x>1\\end{cases}$ 在x=1处可导，则a、b的值为（  ）",
        ["A. a=1, b=2", "B. a=2, b=-1", "C. a=2, b=1", "D. a=-2, b=1"],
        index=None,
        key="q8"
    )
    if q8:
        if q8.startswith("B"):
            st.success("✅ 回答正确！可导必连续，且左右导数相等：")
            with st.expander("点击查看完整推导过程"):
                st.markdown("""
                1. **连续性条件**：x=1处左极限=右极限=函数值，即$1^2 = a\\cdot1 + b$，得 $a+b=1$；
                2. **可导性条件**：左导数=右导数，x=1处左导数f'_-(1)=2×1=2，右导数f'_+(1)=a，因此a=2；
                3. 代入a=2到连续性条件，得b=1-a=-1。
                因此a=2, b=-1，选B。
                """)
        else:
            st.error("❌ 不对哦，分段函数在分界点可导需要同时满足两个条件：连续（左右极限相等）、左右导数相等。")

# 8. 计算实践与代码实现✨ 【关键：判断条件和导航文字完全一致，带✨】
elif page == "8. 计算实践与代码实现✨":
    st.title("8. 计算实践与代码实现✨")
    st.markdown("---")
    
    st.markdown(r"""
    ### 📌 学习目标
    把导数的定义与几何意义落到 **手算 + 机算** 两个层面：既能熟练推导公式，又能用 Python 快速计算、验证与可视化。
    """)
    st.info("💡 下面三道典型题给出详细计算过程与 Python 代码；两道计算题配有可拖动参数的交互滑块，可以实时观察动态效果。")

    # ---------- 典型题一 ----------
    st.markdown("---")
    st.markdown(r"### 典型题一：用定义求 $f(x)=\dfrac{1}{x}\ (x\neq 0)$ 的导数")
    st.markdown(r"**思路**：分式函数，按「一差、二比、三极限」三步走，关键是先**通分**。")
    with st.expander("📝 点击查看详细计算过程（典型题一）", expanded=True):
        st.markdown(r"""
        **第一步（求增量）**——通分：
        $$\Delta y=f(x+\Delta x)-f(x)=\frac{1}{x+\Delta x}-\frac{1}{x}=\frac{x-(x+\Delta x)}{x(x+\Delta x)}=\frac{-\Delta x}{x(x+\Delta x)}$$

        **第二步（算比值）**：
        $$\frac{\Delta y}{\Delta x}=\frac{-1}{x(x+\Delta x)}$$

        **第三步（取极限）**：
        $$f'(x)=\lim_{\Delta x\to 0}\frac{-1}{x(x+\Delta x)}=-\frac{1}{x^{2}}$$

        **结论**：$\left(\dfrac{1}{x}\right)'=-\dfrac{1}{x^{2}}$。
        """)
    st.markdown("**Python 代码（数值差商验证）**：")
    st.code(r'''import numpy as np

# 待求导的函数
def f(x):
    return 1.0 / x

# 数值差商：用 (f(x0+h)-f(x0))/h 近似导数
def diff_quotient(func, x0, h):
    return (func(x0 + h) - func(x0)) / h

x0 = 2.0
true_val = -1.0 / x0**2          # 理论值 f'(2) = -0.25
print(f"x0 = {x0}，理论导数值 f'(2) = {true_val}")

for h in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    approx = diff_quotient(f, x0, h)
    print(f"h = {h:.0e}  差商 = {approx:.10f}  误差 = {abs(approx - true_val):.2e}")''', language="python")
    st.success(r"运行可见：$h$ 越小，差商越接近 $-0.25$，与手算结论完全一致。")

    # ---------- 典型题二 ----------
    st.markdown("---")
    st.markdown(r"### 典型题二：用定义求 $f(x)=\sqrt{x}\ (x>0)$ 的导数")
    st.markdown(r"**思路**：根式函数，关键是**分子有理化**。")
    with st.expander("📝 点击查看详细计算过程（典型题二）", expanded=True):
        st.markdown(r"""
        **第一步（求增量）**——分子有理化：
        $$\Delta y=\sqrt{x+\Delta x}-\sqrt{x}=\frac{\left(\sqrt{x+\Delta x}-\sqrt{x}\right)\left(\sqrt{x+\Delta x}+\sqrt{x}\right)}{\sqrt{x+\Delta x}+\sqrt{x}}=\frac{\Delta x}{\sqrt{x+\Delta x}+\sqrt{x}}$$

        **第二步（算比值）**：
        $$\frac{\Delta y}{\Delta x}=\frac{1}{\sqrt{x+\Delta x}+\sqrt{x}}$$

        **第三步（取极限）**：
        $$f'(x)=\lim_{\Delta x\to 0}\frac{1}{\sqrt{x+\Delta x}+\sqrt{x}}=\frac{1}{2\sqrt{x}}$$

        **结论**：$\left(\sqrt{x}\right)'=\dfrac{1}{2\sqrt{x}}\ (x>0)$。
        """)
    st.markdown("**Python 代码（数值验证）**：")
    st.code(r'''import numpy as np

def f(x):
    return np.sqrt(x)

def diff_quotient(func, x0, h):
    return (func(x0 + h) - func(x0)) / h

x0 = 4.0
true_val = 1.0 / (2.0 * np.sqrt(x0))      # 理论值 f'(4) = 0.25
print(f"x0 = {x0}，理论导数值 f'(4) = {true_val}")

for h in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
    approx = diff_quotient(f, x0, h)
    print(f"h = {h:.0e}  差商 = {approx:.10f}  误差 = {abs(approx - true_val):.2e}")''', language="python")
    st.success(r"差商随 $h\to 0$ 稳定收敛到 $0.25$，验证了 $(\sqrt{x})'=\dfrac{1}{2\sqrt{x}}$。")

    # ---------- 典型题三 ----------
    st.markdown("---")
    st.markdown(r"### 典型题三：求 $y=x^{3}-3x$ 在点 $(2,2)$ 处的切线与法线方程")
    st.markdown(r"**思路**：这是导数几何意义与求导公式的综合应用。")
    with st.expander("📝 点击查看详细计算过程（典型题三）", expanded=True):
        st.markdown(r"""
        **第一步（求导数）**：由幂函数求导公式 $(x^{n})'=nx^{n-1}$ 得
        $$y'=3x^{2}-3$$

        **第二步（求切点处的斜率）**：切点 $M(2,2)$，横坐标 $x_0=2$，
        $$k=y'(2)=3\times 2^{2}-3=9$$

        **第三步（写出方程）**：
        - 切线方程：$y-2=9(x-2)$，即 $y=9x-16$；
        - 法线方程：$y-2=-\dfrac{1}{9}(x-2)$，即 $y=-\dfrac{1}{9}x+\dfrac{20}{9}$。
        """)
    st.markdown("**Python 代码（求解并绘图）**：")
    st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 3*x

def fp(x):
    return 3*x**2 - 3

x0, y0 = 2.0, 2.0
k = fp(x0)                        # 切线斜率 = 9
print(f"切点 M({x0}, {y0})，切线斜率 k = {k}")

x = np.linspace(-1, 4, 400)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, f(x), linewidth=2, color="#1f77b4", label=r"$y=x^3-3x$")
ax.plot(x, y0 + k*(x - x0), "--", linewidth=2, color="red", label=r"切线 $y=9x-16$")
ax.plot(x, y0 - (x - x0)/k, "--", linewidth=2, color="green", label=r"法线 $y=-\frac{1}{9}x+\frac{20}{9}$")
ax.scatter([x0], [y0], color="black", s=90, zorder=5, label=r"切点 $M(2,2)$")
ax.axhline(0, color="gray", linewidth=0.8)
ax.axvline(0, color="gray", linewidth=0.8)
ax.grid(alpha=0.3, linestyle="--")
ax.legend(fontsize=11)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(r"$y=x^3-3x$ 在点 $(2,2)$ 处的切线与法线")
plt.tight_layout()
plt.show()''', language="python")

    # ================= 交互计算题 =================
    st.markdown("---")
    st.markdown("## 🎛️ 计算题（拖动滑块，实时观察动态效果）")

    # ---------- 计算题四 ----------
    st.markdown(r"### 计算题四：抛物线 $y=x^{2}$ 在点 $(x_0,x_0^{2})$ 处的切线动态追踪")
    st.markdown(r"""
    **计算过程**：由 $f'(x)=2x$ 得 $f'(x_0)=2x_0$，由点斜式得切线方程
    $$y-x_0^{2}=2x_0(x-x_0)\quad\Longrightarrow\quad y=2x_0\,x-x_0^{2}$$
    """)
    st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2

def fp(x):
    return 2*x

x0 = 1.0
y0, k = f(x0), fp(x0)
print(f"切点 M({x0}, {y0})，切线斜率 k = {k}，切线方程 y = {k}x + ({-x0**2})")

x = np.linspace(-2.5, 2.5, 400)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, f(x), linewidth=2, color="#1f77b4", label=r"$y=x^2$")
ax.plot(x, y0 + k*(x - x0), "--", linewidth=2, color="red", label="切线")
ax.scatter([x0], [y0], color="black", s=90, zorder=5, label=f"M({x0}, {y0})")
ax.grid(alpha=0.3, linestyle="--")
ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.tight_layout()
plt.show()''', language="python")
    st.markdown("**👉 拖动下面的滑块，观察切线随切点的动态变化：**")

    x0_t4 = st.slider("切点 M 的横坐标 x₀（计算题四）", min_value=-2.0, max_value=2.0, value=1.0, step=0.1, key="t4_x0")

    y0_t4 = x0_t4 ** 2
    k_t4 = 2 * x0_t4
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    x4 = np.linspace(-2.5, 2.5, 400)
    ax4.plot(x4, x4**2, linewidth=2.2, color="#1f77b4", label=r"曲线 $y=x^2$")
    ax4.plot(x4, y0_t4 + k_t4*(x4 - x0_t4), "--", linewidth=2.2, color="red",
             label=fr"切线 $y={k_t4:.1f}x{(-x0_t4**2):+.1f}$")
    ax4.scatter([x0_t4], [y0_t4], color="black", s=120, zorder=5, edgecolor="white", linewidth=1.2,
                label=fr"$M({x0_t4:.1f},\ {y0_t4:.2f})$")
    ax4.axhline(0, color="gray", linewidth=0.8)
    ax4.axvline(0, color="gray", linewidth=0.8)
    ax4.grid(alpha=0.3, linestyle="--")
    ax4.legend(fontsize=11, loc="upper left")
    ax4.set_xlabel("x", fontsize=12)
    ax4.set_ylabel("y", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig4)

    c1, c2, c3 = st.columns(3)
    c1.metric("切点横坐标 x₀", f"{x0_t4:.1f}")
    c2.metric("切线斜率 f'(x₀)=2x₀", f"{k_t4:.1f}")
    c3.metric("切线方程", f"y = {k_t4:.1f}x {(-x0_t4**2):+.1f}")

    # ---------- 计算题五 ----------
    st.markdown("---")
    st.markdown(r"### 计算题五：差商逼近导数——对 $f(x)=\sin x$ 验证 $f'(x_0)=\cos x_0$")
    st.markdown(r"""
    **计算过程**：由和差化积公式
    $$\sin(x+h)-\sin x=2\cos\left(x+\frac{h}{2}\right)\sin\frac{h}{2}$$
    于是差商
    $$\frac{\sin(x+h)-\sin x}{h}=\cos\left(x+\frac{h}{2}\right)\cdot\frac{\sin(h/2)}{h/2}$$
    令 $h\to 0$，由重要极限 $\lim\limits_{t\to 0}\dfrac{\sin t}{t}=1$，得
    $$f'(x)=\cos x\cdot 1=\cos x$$
    """)
    st.code(r'''import numpy as np

def f(x):
    return np.sin(x)

x0 = 1.0
true_val = np.cos(x0)
print(f"x0 = {x0}，理论导数值 cos(x0) = {true_val:.8f}")

for h in [1.0, 0.5, 0.1, 0.01, 0.001, 0.0001]:
    approx = (f(x0 + h) - f(x0)) / h
    print(f"h = {h:<8}  差商 = {approx:.8f}  误差 = {abs(approx - true_val):.2e}")''', language="python")
    st.markdown("**👉 拖动滑块改变 x₀ 与增量 h，观察差商如何逼近导数：**")

    col_a, col_b = st.columns(2)
    with col_a:
        x0_t5 = st.slider("定点 x₀（计算题五）", min_value=-3.0, max_value=3.0, value=1.0, step=0.1, key="t5_x0")
    with col_b:
        h_t5 = st.slider("增量 h（计算题五）", min_value=0.001, max_value=1.0, value=0.5, step=0.001, key="t5_h")

    approx_t5 = (np.sin(x0_t5 + h_t5) - np.sin(x0_t5)) / h_t5
    true_t5 = np.cos(x0_t5)

    fig5, (axA, axB) = plt.subplots(1, 2, figsize=(14, 5))

    xx = np.linspace(x0_t5 - 2.2, x0_t5 + 2.2, 400)
    axA.plot(xx, np.sin(xx), linewidth=2.2, color="#1f77b4", label=r"曲线 $y=\sin x$")
    axA.plot(xx, np.sin(x0_t5) + true_t5 * (xx - x0_t5), linewidth=2.0, color="red",
             label=fr"切线，k=cos={true_t5:.3f}")
    xs = np.linspace(x0_t5 - 2.2, x0_t5 + h_t5 + 2.2, 100)
    axA.plot(xs, np.sin(x0_t5) + approx_t5 * (xs - x0_t5), "--", linewidth=2.0, color="orange",
             label=fr"割线，k={approx_t5:.3f}")
    axA.scatter([x0_t5, x0_t5 + h_t5], [np.sin(x0_t5), np.sin(x0_t5 + h_t5)],
                color="black", s=100, zorder=5)
    axA.axhline(0, color="gray", linewidth=0.8)
    axA.grid(alpha=0.3, linestyle="--")
    axA.legend(fontsize=10, loc="upper left")
    axA.set_xlabel("x", fontsize=12)
    axA.set_ylabel("y", fontsize=12)
    axA.set_title("割线逼近切线", fontsize=12)

    h_grid = np.logspace(-6, 0, 200)
    approx_grid = (np.sin(x0_t5 + h_grid) - np.sin(x0_t5)) / h_grid
    err_grid = np.maximum(np.abs(approx_grid - true_t5), 1e-18)
    axB.loglog(h_grid, err_grid, linewidth=2.0, color="#1f77b4", label=r"$|\frac{\Delta y}{\Delta x}-f'(x_0)|$")
    axB.scatter([h_t5], [max(abs(approx_t5 - true_t5), 1e-18)], color="red", s=120, zorder=5, label="当前 h")
    axB.grid(alpha=0.3, linestyle="--", which="both")
    axB.legend(fontsize=10)
    axB.set_xlabel("h（对数坐标）", fontsize=12)
    axB.set_ylabel("误差", fontsize=12)
    axB.set_title("误差随 h 的变化", fontsize=12)

    plt.tight_layout()
    st.pyplot(fig5)

    d1, d2, d3 = st.columns(3)
    d1.metric("当前 h", f"{h_t5:.3f}")
    d2.metric("差商值", f"{approx_t5:.6f}")
    d3.metric("真实导数值 cos(x₀)", f"{true_t5:.6f}", delta=f"{approx_t5 - true_t5:+.2e}")

    st.info("🎯 观察结论：h 越小，割线斜率越接近切线斜率；当 h 小到一定程度后，由于计算机浮点舍入误差，误差反而略有回升，这正说明「取极限」是数学上的理想过程。")

# 9. 课程思政
elif page == "9. 课程思政":
    st.title("9. 课程思政：从导数的诞生看科学精神与文化自信")
    st.markdown("---")

    st.markdown(r"""
    ### 一、一条主线：两个问题，一个概念——在差异中寻找统一是科学的灵魂
    导数的诞生，源于17世纪科学革命浪潮中两个看似毫不相干的问题——**运动学的瞬时速度**与**几何学的切线斜率**。

    牛顿站在物理学的视角，为了描述天体运动和自由落体，追问"某一瞬间的速度到底是多少"。如果速度等于路程除以时间，那一瞬间时间长度为零，路程也是零，"零除以零"怎么会有意义？这个在中世纪被认为是哲学悖论的问题，被牛顿用"流数术"给出了数学解答。

    莱布尼茨站在几何学的视角，为了画曲线的切线、计算曲线下的面积，从图形的局部陡峭程度出发，独立推导出了完全相同的数学公式。两个人，一个在英伦三岛研究力学，一个在欧洲大陆研究几何，相隔千里、从未谋面，却在同一段时间里，走到了同一个数学结构面前。

    这不是偶然的巧合，而是科学发展的必然：
    - 17世纪大航海需要精确的航海天文表，炮弹弹道计算需要知道瞬时速度；
    - 透镜制造需要画曲线切线求法线，建筑工程需要计算曲线形构件的受力；
    - 当生产实践提出了共同的数学问题，不同领域的探索者最终会殊途同归。

    这告诉我们一个朴素又深刻的道理：**透过纷繁的现象看本质，在表面的差异中寻找内在的统一**，正是科学抽象的伟力。
    从瞬时速度到切线斜率，从化学反应速率到人口增长率，从电流强度到边际成本——世间万事万物的"变化快慢"，都被同一个叫做"导数"的概念精准描述。这种跨领域的普适性，正是数学最迷人的魅力，也是一代代科学家追求"统一理论"的根本动力。

    对我们同学来说，这种思维方式同样重要：学习不要死记硬背零散的知识点，要学会透过题目看背后共通的数学结构；遇到不同领域的问题，要善于发现它们背后统一的规律，这才是真正学会了数学。
    """)

    st.markdown(r"""
    ### 二、量变到质变：极限思想中的唯物辩证法
    导数的核心是极限，极限思想里蕴含着最朴素也最深刻的辩证法——**量变与质变的对立统一**。

    我们回头看割线逼近切线的过程：当Δx=2的时候，割线很陡，和切线差得很远；Δx=1的时候，近了一点；Δx=0.1的时候，已经很像切线了；Δx=0.01、0.001……这个过程中，N点一点点靠近M点，割线一点点转动，斜率一点点接近切线斜率——这是连续的、不显著的**量变**。
    但是只要Δx还不等于0，它就永远是割线，不是切线；只有当Δx→0这个临界时刻，割线才发生了质的飞跃，从"连接两点的斜线"变成了"只碰一点的切线"，斜率从平均变化率变成了瞬时变化率——这就是**质变**。

    这种"量变积累到临界点引发质变"的规律，绝不仅仅存在于数学里：
    - 大家常说的"压垮骆驼的最后一根稻草"，是量变到质变；
    - 水滴石穿、绳锯木断，是量变到质变；
    - 学习知识从"听不懂"到"突然开窍"，也是长期积累后的质变；
    - 国家科技发展从跟跑到并跑再到领跑，同样是一代代科研工作者持续积累的结果。

    导数的定义还体现了**近似与精确、有限与无限的对立统一**：
    我们用有限的差商近似瞬时速度，只要Δx还没到0，就永远是近似值；但通过取极限这个飞跃，无限多个近似值最终收敛到了一个精确的导数值——近似中包含着精确的种子，无限过程最终得到了有限的、确定的结果。
    公元3世纪我国数学家刘徽提出割圆术："割之弥细，所失弥少，割之又割，以至于不可割，则与圆合体而无所失矣"，用正多边形逼近圆周率，正是同样的思想。1400多年后西方数学家才系统建立极限理论，这充分说明我们的祖先早已掌握了这种辩证思维。

    希望大家从极限思想里体会到：做学问、做事情都不要急于求成，要重视一点一滴的积累。今天学会一个公式、明天弄懂一个概念，看起来微不足道，但只要坚持下去，积累到临界点自然会迎来质的飞跃；反过来，哪怕每天只偷懒一点点，长期积累也会产生巨大的差距。这就是数学教给我们的人生哲理。
    """)

    st.markdown(r"### 三、数学名家故事")
    with st.expander("🕰️ 故事一：牛顿的「奇迹年」", expanded=True):
        st.markdown(r"""
        艾萨克·牛顿（Isaac Newton，1643—1727）在 1665—1666 年瘟疫流行期间，从剑桥回到家乡伍尔索普庄园，
        闭门潜心研究近两年，完成了微积分（流数术）的雏形、万有引力定律的思考、光的色散实验等开创性工作，
        史称牛顿的「奇迹年」（Annus Mirabilis）。

        **启示**：耐得住寂寞、坐得住冷板凳，是科学突破的重要前提。

        牛顿谦逊地说：「如果我看得更远，那是因为我站在巨人的肩膀上。」
        这句话也提醒我们：任何成就都离不开前人的积累，要学会感恩与传承。
        """)
    with st.expander("🕰️ 故事二：莱布尼茨与优美的数学符号"):
        st.markdown(r"""
        戈特弗里德·莱布尼茨（Gottfried Leibniz，1646—1716）从求曲线切线的问题出发，
        独立创立了微积分，并创造了 $\mathrm{d}y/\mathrm{d}x$、$\int$ 等简洁优美的符号，一直沿用至今。
        他还是哲学家、外交家，被誉为「最后一位通才」。

        **启示**：广阔的视野与跨学科的思维方式，往往孕育着创新。
        """)
    with st.expander("🕰️ 故事三：优先权之争与科学协作"):
        st.markdown(r"""
        牛顿与莱布尼茨曾就微积分的发明权争论多年。今天回看，
        两人其实是「殊途同归」——科学发现往往是时代发展到一定阶段的必然产物。

        **启示**：学术协作、尊重他人劳动，比争一时之功更有价值。
        """)
    with st.expander("🕰️ 故事四：从「无穷小」到严格定义——柯西与魏尔斯特拉斯"):
        st.markdown(r"""
        18 世纪，微积分基础中的「无穷小量」究竟是不是零，长期饱受质疑，引发了「第二次数学危机」。
        19 世纪，柯西（Cauchy）建立极限理论（1821 年《分析教程》），
        魏尔斯特拉斯（Weierstrass）进一步用 $\varepsilon\text{-}\delta$ 语言给出严格定义，
        导数才获得了牢固的逻辑基础。

        **启示**：追求严谨、敢于质疑，是数学乃至一切科学的精神底色。
        """)
    with st.expander("🕰️ 故事五：刘徽割圆术——中华数学的极限智慧"):
        st.markdown(r"""
        公元 3 世纪，魏晋数学家刘徽在《九章算术注》中提出「割圆术」，
        用圆内接正多边形逼近圆，写下：
        「割之弥细，所失弥少，割之又割，以至于不可割，则与圆合体而无所失矣。」

        这正是极限思想的雏形，比西方同类思想早了约 1400 年。
        在此基础上，祖冲之将圆周率精确到小数点后 7 位（介于 $3.1415926$ 与 $3.1415927$ 之间），领先世界近千年。

        **启示**：中华数学源远流长，我们应当坚定文化自信。
        """)

    st.markdown(r"""
    ### 四、数学服务于国家发展
    - **高铁**：时速 350 公里的列车平稳运行，需要对速度、加速度（位移的一阶、二阶导数）进行精确控制；
    - **航天**：火箭发射、卫星变轨，本质是对运动变化率的精确计算；
    - **人工智能**：深度学习中的梯度下降算法，正是沿着导数（梯度）方向寻找损失函数的最小值；
    - **经济学与工程**：边际成本、边际收益、最优化设计，都离不开导数这个工具。

    一句话：**基础数学是科技自立自强的基石，数学强则科技强。**
    """)

    st.markdown(r"""
    ### 五、学习寄语
    学习导数，不只是记住一个公式，更要体会其中的思想方法：
    - **分解问题**：把求导过程拆成「一差、二比、三极限」三步；
    - **用极限刻画瞬时**：从近似走向精确，体会有限与无限的转化；
    - **分清充分与必要**：可导必连续，连续不一定可导，逻辑要严谨。

    愿大家把追求严谨、勇于创新的数学精神，带进今后的学习与生活之中。
    """)

    st.success("🌟 青年强则国家强。愿同学们以数学为翼，在科学的天空中飞得更高、更远！")

# ============================================
# 第四部分：页脚
# ============================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>📐 导数的概念及其几何意义 · 大学高等数学交互式教学应用</div>",
    unsafe_allow_html=True
)