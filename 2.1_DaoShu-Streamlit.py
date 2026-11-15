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
import os
import warnings

# 屏蔽 matplotlib mathtext 在重绘时偶发的解析告警，避免单条图例渲染失败导致整页崩溃
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.mathtext")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.offsetbox")
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib.legend")

# ============================================
# 第二部分：配置页面基础样式（无需修改）
# ============================================
st.set_page_config(
    page_title="导数的概念及其几何意义 - 交互式教学",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 容错版中文字体配置：每次画图前都会调用，保证图不会被重置回默认缺字体状态
def configure_chinese_font():
    # 先尝试加载同目录下的simhei.ttf
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "simhei.ttf")

    # 候选中文字体（按优先级）；末尾固定用 DejaVu Sans 兜底，
    # 保证数学符号在字体回退链里一定能找到字形。
    font_candidates = [
        'Noto Sans CJK SC',
        'Noto Sans CJK JP',
        'WenQuanYi Micro Hei',
        'SimHei',
        'Microsoft YaHei',
        'PingFang SC',
        'Arial Unicode MS',
    ]

    # 若同目录放了 simhei.ttf，优先注册并排到最前面（本地 Windows 常用）
    if os.path.exists(font_path):
        try:
            font_manager.fontManager.addfont(font_path)
            font_name = font_manager.FontProperties(fname=font_path).get_name()
            if font_name not in font_candidates:
                font_candidates.insert(0, font_name)
        except Exception:
            pass

    # 统一走 sans-serif 字体回退链：中文字体在前，DejaVu Sans 兜底
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = font_candidates + ['DejaVu Sans']

    # === 关键修复：彻底消除 U+2212 告警 ===
    # 1) 刻度负号改用 ASCII 连字符（不再用 U+2212 MINUS SIGN）
    plt.rcParams['axes.unicode_minus'] = False
    # 2) 数学公式字体使用 DejaVu Sans，这是 matplotlib 自带且 100% 含数学减号的字体；
    #    STIX/CM 在部分 matplotlib 版本下 mathtext 渲染时会回退到 default 字体导致告警。
    plt.rcParams['mathtext.fontset'] = 'dejavusans'
    # 3) 关闭 mathtext 缺字时向 'default' 字体的回退——这是 U+2212 告警的真正来源：
    #    旧版本 mathtext 遇到减号会先查当前字体，找不到就 fallback 到 default 字体，
    #    default 不含 U+2212 才刷出一长串告警。设为 None 让缺字直接落在 DejaVu 上。
    #    该键在不同 matplotlib 版本合法值不同（cm/stix/stixsans/None），用 try 兼容。
    for fallback_val in [None, 'cm', 'stix']:
        try:
            plt.rcParams['mathtext.fallback'] = fallback_val
            break
        except Exception:
            continue

# 首次全局配置一次
configure_chinese_font()


def prep_fig(fig, ax=None):
    """每次 plt.subplots() 创建新图后立即调用，重新刷一遍字体配置，
    防止 matplotlib 在新建 Figure 时重置 rcParams 回到缺字体默认值。"""
    configure_chinese_font()
    return fig, ax


def safe_pyplot(fig, key=None):
    """统一安全渲染：通过 BytesIO savefig 后用 st.image 显示，彻底避开
    st.pyplot 对 savefig kwargs 的透传警告，同时在渲染前统一刷字体、
    tight_layout，并在渲染后立即关闭 figure，避免 mathtext 重入异常。"""
    import io
    try:
        configure_chinese_font()
        try:
            fig.tight_layout(pad=1.0)
            fig.set_layout_engine(None)
        except Exception:
            pass
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=160, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, width='stretch')
    except Exception:
        # 兜底：去掉 tight_layout 再试一次最简渲染
        try:
            configure_chinese_font()
            fig.set_layout_engine(None)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=160)
            buf.seek(0)
            st.image(buf, width='stretch')
        except Exception:
            st.warning("当前图表渲染出现异常，请刷新页面重试。")
    finally:
        plt.close(fig)

# 侧边栏导航：和教案7个环节完全对应
st.sidebar.title("📚 课程导航")
page = st.sidebar.radio(
    "选择教学环节",
    [
        "0. 课程导入：两个经典问题✨",
        "1. 导数的定义",
        "2. 用定义求导数例题",
        "3. 单侧导数与导函数",
        "4. 可导与连续的关系",
        "5. 几何意义：割线变切线✨",
        "6. 切线与法线方程",
        "7. 课堂小结与练习",
        "8. 计算实践与代码实现✨",
        "9. 课程思政",
        "10. 课后习题与代码实现✨"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 使用提示：\n"
    "1. 左侧切换教学环节.\n"
    "2. 带✨的环节有交互滑块，可以拖动参数看动态效果.\n"
    "3. 所有公式支持自动渲染，和教材一致.\n"
    "4. 第 8 页为「计算实践与代码实现」，第 9 页为「课程思政」\n"
    "5. 第 10 页为「课后习题与代码实现」，20 道习题全部附答案与可运行 Python 代码（数值差商验证＋解析对照，部分题含绘图）；第 9、10 题另附符号求导与纯数值两种方法.\n"
    "6. 参考书目：\n"
    "    - 高等数学（同济版）\n"
    "    - 数学分析新讲\n"
    "    - 斯图尔特微积分\n"
    "    - 普林斯顿微积分读本\n"
    "    - 托马斯微积分...\n"
    "7. ★ 全平台共设 11 处课堂引入点，与《两课时板书设计》第五章总表一一对应，\n"
    "   代码中以「★引入 1~11」标注，可按分钟号对照使用.\n"
)

# ============================================
# 第三部分：每个页面的实际内容（按教案逐节编写）
# ============================================

# 0. 课程导入
if page == "0. 课程导入：两个经典问题✨":
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
        1. 从 $t_0$ 到 $t_0+\\Delta t$，物体走过的路程：$\\Delta s = s(t_0+\\Delta t) - s(t_0)$
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
        1. 在曲线上另取一点 $N(x_0+\\Delta x, f(x_0+\\Delta x))$
        2. 割线 $MN$ 的斜率：
        $$k_{\\text{割}} = \\frac{\\Delta y}{\\Delta x} = \\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x}$$
        3. 当 $N$ 沿曲线无限靠近 $M$（即 $\\Delta x \\to 0$）时，割线斜率的极限就是**切线斜率**：
        $$k_{\\text{切}} = \\lim_{\\Delta x \\to 0}\\frac{\\Delta y}{\\Delta x} = \\lim_{\\Delta x \\to 0}\\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x}$$
        """)
        
        st.info("🚩 这是莱布尼茨研究导数的出发点：描述曲线的陡峭程度。")

    # ==================================================================
    # ★引入 1（第一节 第 3 分钟）｜首页「课程导入：两个经典问题」
    # 操作要点：打开问题 1，拖动 Δt 滑块由大变小；也可在「精确输入」框里直接键入
    #           0.00001 这类小量（滑块与输入框自动同步），让学生看着平均速度稳定到一个数
    # 教学作用：把板书上写的 Δs/Δt 变成"会动的数"，直观看到平均速度趋于瞬时速度
    # ==================================================================
    st.markdown("---")
    st.markdown(r"### ✨ 交互演示：拖动 $\Delta t$ 滑块 / 直接输入数值，看平均速度怎么稳定到一个数")
    st.info(r"板书上写的 $\dfrac{\Delta s}{\Delta t}$ 是一个**会动的数**。拖动下面的 $\Delta t$ 滑块由大变小，"
            r"盯住「平均速度」那一栏：它会一点点逼近、最后稳定在 $t_0$ 时刻的瞬时速度上——"
            r"这正是导数定义里那个极限的直观过程。"
            "\n\n"
            r"滑块最小只能拖到 $0.01$ 秒。若想亲手试一试 $0.00001$ 这样的小量，"
            r"请在下面的**精确输入**框里直接键入数值——滑块与输入框会自动保持同步。")

    # ---- 滑块与「精确输入」框双向同步：谁最后被改动，就以谁为准 ----
    # 滑块负责粗调（Δt 最小 0.01 s）；输入框负责精调（可键入 0.00001 甚至更小）
    if "imp1_t0_slider" not in st.session_state:
        st.session_state["imp1_t0_slider"] = 2.0
    if "imp1_t0_input" not in st.session_state:
        st.session_state["imp1_t0_input"] = 2.0
    if "imp1_dt_slider" not in st.session_state:
        st.session_state["imp1_dt_slider"] = 1.50
    if "imp1_dt_input" not in st.session_state:
        st.session_state["imp1_dt_input"] = 1.50

    def _imp1_t0_from_slider():
        st.session_state["imp1_t0_input"] = float(st.session_state["imp1_t0_slider"])

    def _imp1_t0_from_input():
        v_in = float(st.session_state["imp1_t0_input"])
        st.session_state["imp1_t0_slider"] = min(max(v_in, 0.5), 3.0)

    def _imp1_dt_from_slider():
        st.session_state["imp1_dt_input"] = float(st.session_state["imp1_dt_slider"])

    def _imp1_dt_from_input():
        v_in = float(st.session_state["imp1_dt_input"])
        st.session_state["imp1_dt_slider"] = min(max(v_in, 0.01), 2.0)

    c_t0, c_dt = st.columns(2)
    with c_t0:
        st.slider("定点 t₀（s）：拖动粗调", min_value=0.5, max_value=3.0, step=0.1,
                  key="imp1_t0_slider", on_change=_imp1_t0_from_slider)
        st.number_input("↳ 精确输入 t₀（s）", min_value=0.5, max_value=3.0,
                        step=0.1, format="%.2f",
                        key="imp1_t0_input", on_change=_imp1_t0_from_input)
    with c_dt:
        st.slider("时间间隔 Δt（s）：请由大往小拖", min_value=0.01, max_value=2.0,
                  step=0.01, key="imp1_dt_slider", on_change=_imp1_dt_from_slider)
        st.number_input("↳ 精确输入 Δt（s）：可直接键入 0.00001", min_value=0.000001,
                        max_value=2.0, step=0.00001, format="%.6f",
                        key="imp1_dt_input", on_change=_imp1_dt_from_input)

    # 真值统一取「精确输入」框（拖滑块时回调已把滑块值同步进输入框）
    t0_demo = float(st.session_state["imp1_t0_input"])
    dt_demo = float(st.session_state["imp1_dt_input"])

    # 数值显示：极小的量自动提高精度，避免 Δt = 0.00001 被显示成 0.00
    def _fmt_num(x, dec_big=4, dec_small=6):
        ax_ = abs(x)
        s = f"{x:.{dec_big}f}" if (ax_ == 0 or ax_ >= 1e-3) else f"{x:.{dec_small}f}"
        return s.rstrip("0").rstrip(".") if "." in s else s

    # 位置函数取 s(t) = t²（相当于自由落体取 g = 2），则瞬时速度 v(t) = s'(t) = 2t
    s_demo = lambda t: t ** 2
    v_demo = lambda t: 2.0 * t

    s0_demo = s_demo(t0_demo)
    s1_demo = s_demo(t0_demo + dt_demo)
    v_avg_demo = (s1_demo - s0_demo) / dt_demo
    v_ins_demo = v_demo(t0_demo)

    m1, m2, m3 = st.columns(3)
    m1.metric("Δt 大小", f"{_fmt_num(dt_demo)} s")
    m2.metric("平均速度 Δs/Δt", f"{v_avg_demo:.6f} m/s")
    m3.metric("瞬时速度 v(t₀)=2t₀", f"{v_ins_demo:.6f} m/s",
              delta=f"{v_avg_demo - v_ins_demo:+.6f}（与平均速度之差）")

    st.caption(f"小提示：本例 s(t)=t²，平均速度恒等于 2t₀+Δt，它与瞬时速度之差恰好就是 Δt 本身"
               f"（当前 Δt = {_fmt_num(dt_demo)} s，所以两者之差就是 {_fmt_num(dt_demo)}）——"
               f"Δt 越接近 0，平均速度就越精确地逼近瞬时速度。")

    # ---- Δt 很小时割线与切线在整图上几乎重合，可勾选局部放大看清夹角 ----
    zoom_flag = st.checkbox("🔍 局部放大 t₀ 附近（Δt 很小时特别有用）",
                            value=False, key="imp1_zoom")
    if zoom_flag:
        half = max(8.0 * dt_demo, 1e-7)
        x_lo, x_hi = t0_demo - half, t0_demo + half
        y_half = max(abs(v_ins_demo) * half * 1.8, 1e-7)
        y_lo, y_hi = s0_demo - y_half, s0_demo + y_half
    else:
        x_lo, x_hi = 0.0, 6.0
        y_lo, y_hi = -1.5, max(s1_demo, s0_demo) + 4.0

    fig_imp, ax_imp = plt.subplots(figsize=(8, 5))
    fig_imp, ax_imp = prep_fig(fig_imp, ax_imp)
    t_plot = np.linspace(0, 6, 400)
    ax_imp.plot(t_plot, s_demo(t_plot), linewidth=2.2, color='#1f77b4', label=r"位置曲线 $s=t^2$")

    tt_sec = np.linspace(x_lo, x_hi, 100)
    ax_imp.plot(tt_sec, s0_demo + v_avg_demo * (tt_sec - t0_demo), '--', linewidth=2.2,
                color='orange', label=fr"割线（平均速度），斜率 $={v_avg_demo:.6g}$")
    tt_tan = np.linspace(x_lo, x_hi, 100)
    ax_imp.plot(tt_tan, s0_demo + v_ins_demo * (tt_tan - t0_demo), linewidth=2.2,
                color='red', label=fr"切线（瞬时速度），斜率 $={v_ins_demo:.6g}$")

    ax_imp.scatter([t0_demo], [s0_demo], color='red', s=110, zorder=5,
                   edgecolor='white', linewidth=1.2, label=fr"$t_0={t0_demo:g}$")
    ax_imp.scatter([t0_demo + dt_demo], [s1_demo], color='orange', s=110, zorder=5,
                   edgecolor='white', linewidth=1.2, label=fr"$t_0+\Delta t={t0_demo + dt_demo:g}$")
    ax_imp.plot([t0_demo, t0_demo + dt_demo], [s0_demo, s0_demo], 'k--', alpha=0.6, linewidth=1.2)
    ax_imp.plot([t0_demo + dt_demo, t0_demo + dt_demo], [s0_demo, s1_demo], 'k--', alpha=0.6, linewidth=1.2)
    y_span = y_hi - y_lo            # 标注按视图大小取相对偏移，放大视图下也不会跑出画面
    ax_imp.annotate(r"$\Delta t$", ((2.0 * t0_demo + dt_demo) / 2.0, s0_demo - 0.10 * y_span),
                    fontsize=13, ha='center')
    ax_imp.annotate(r"$\Delta s$", (t0_demo + dt_demo + 0.02 * (x_hi - x_lo),
                                    (s0_demo + s1_demo) / 2.0), fontsize=13, va='center')

    ax_imp.axhline(0, color='gray', linewidth=0.8)
    ax_imp.axvline(0, color='gray', linewidth=0.8)
    ax_imp.grid(alpha=0.3, linestyle='--')
    ax_imp.legend(fontsize=10, loc='upper left')
    ax_imp.set_xlabel('t（s）', fontsize=12)
    ax_imp.set_ylabel('s（m）', fontsize=12)
    ax_imp.set_xlim(x_lo, x_hi)
    ax_imp.set_ylim(y_lo, y_hi)

    safe_pyplot(fig_imp, key="imp1_vel")

    st.success("🎯 观察发现：Δt 越接近 0，平均速度与瞬时速度的差就越小，割线不断向切线靠拢。\n\n"
               "这个「最后稳定到的数」，就是 s(t) 在 t₀ 处的导数——它正是导数定义里那个极限。")


    
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
    1. 求增量：$\\Delta y = f(x_0+\\Delta x)-f(x_0)$
    2. 算比值：$\\displaystyle \\frac{\\Delta y}{\\Delta x} = \\frac{f(x_0+\\Delta x)-f(x_0)}{\\Delta x}$
    3. 取极限：$\\displaystyle f'(x_0) = \\lim_{\\Delta x \\to 0}\\frac{\\Delta y}{\\Delta x}$
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
    
    # ★引入 3（第一节 第 31 分钟）｜「2. 例题：用定义求导数」：逐段展开例 1（常函数）、例 2（幂函数 x²）
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
    st.markdown("### 例2：求一次函数 $f(x)=ax+b$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = [a(x+h)+b] - (ax+b) = ah$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{ah}{h} = a$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0} a = a$
        
        **结论**：$(ax+b)' = a$。特别地，当 $a=1,b=0$ 时，$(x)' = 1$。
        """)
    
    st.markdown("---")
    st.markdown("### 例3：求幂函数 $f(x)=x^2$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = (x+h)^2 - x^2 = 2xh + h^2$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{2xh+h^2}{h} = 2x + h$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0}(2x+h) = 2x$
        
        **结论**：$(x^2)' = 2x$。
        """)
    
    st.markdown("---")
    st.markdown("### 例4：求幂函数 $f(x)=\\sqrt{x}=x^{\\frac{1}{2}}$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：
        $$\\Delta y = \\sqrt{x+h} - \\sqrt{x} = \\frac{(\\sqrt{x+h}-\\sqrt{x})(\\sqrt{x+h}+\\sqrt{x})}{\\sqrt{x+h}+\\sqrt{x}} = \\frac{h}{\\sqrt{x+h}+\\sqrt{x}}$$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{1}{\\sqrt{x+h}+\\sqrt{x}}$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0}\\frac{1}{\\sqrt{x+h}+\\sqrt{x}} = \\frac{1}{2\\sqrt{x}} = \\frac{1}{2}x^{-\\frac{1}{2}}$
        
        **结论**：$(\\sqrt{x})' = \\dfrac{1}{2\\sqrt{x}}$。这是幂函数求导公式 $(x^n)' = nx^{n-1}$ 在 $n=1/2$ 时的结果。
        """)
    
    st.markdown("---")
    st.markdown("### 例5：求幂函数 $f(x)=\\dfrac{1}{x}=x^{-1}$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：
        $$\\Delta y = \\frac{1}{x+h} - \\frac{1}{x} = \\frac{x - (x+h)}{x(x+h)} = \\frac{-h}{x(x+h)}$$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\frac{-1}{x(x+h)}$
        3. 取极限：$\\displaystyle f'(x) = \\lim_{h\\to 0}\\frac{-1}{x(x+h)} = -\\frac{1}{x^2} = -x^{-2}$
        
        **结论**：$\\left(\\dfrac{1}{x}\\right)' = -\\dfrac{1}{x^2}$。这是幂函数求导公式在 $n=-1$ 时的结果。
        """)
    
    st.markdown("---")
    st.markdown("### 🔶 幂函数求导通用公式")
    st.success("""
    综合以上幂函数例题，可以得到**幂函数求导公式**：
    $$(x^n)' = nx^{n-1}$$
    其中 $n$ 为任意实数，$x$ 在公式有定义的范围内。
    
    例如：
    - $(x^3)' = 3x^2$
    - $(x^{10})' = 10x^9$
    - $\\left(\\dfrac{1}{x^2}\\right)' = (x^{-2})' = -2x^{-3} = -\\dfrac{2}{x^3}$
    """)
    
    st.markdown("---")
    st.markdown("### 例6：求指数函数 $f(x)=a^x$（$a>0,a\\neq1$）的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = a^{x+h} - a^x = a^x(a^h - 1)$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = a^x \\cdot \\frac{a^h - 1}{h}$
        3. 取极限：利用等价无穷小 $a^h - 1 \\sim h\\ln a$（$h\\to0$），得
        $$\\lim_{h\\to0}\\frac{a^h-1}{h} = \\ln a$$
        因此 $f'(x) = a^x \\ln a$。
        
        **结论**：$(a^x)' = a^x \\ln a$。
        """)
    
    st.markdown("---")
    st.markdown("### 例7：求自然指数函数 $f(x)=e^x$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        在例6中令 $a=e$，由于 $\\ln e = 1$，直接得到：
        
        **结论**：$(e^x)' = e^x$。
        
        🚩 这是一个非常特殊的结果：**自然指数函数 $e^x$ 的导数等于它本身**，这也是 $e$ 在数学中如此重要的原因之一——它在求导运算下保持不变。
        """)
    
    st.markdown("---")
    st.markdown("### 例8：求正弦函数 $f(x)=\\sin x$ 的导数")
    with st.expander("点击查看解题过程"):
        st.markdown("""
        1. 求增量：$\\Delta y = \\sin(x+h) - \\sin x = 2\\cos\\left(x+\\frac{h}{2}\\right)\\sin\\frac{h}{2}$
        2. 算比值：$\\displaystyle \\frac{\\Delta y}{h} = \\cos\\left(x+\\frac{h}{2}\\right)\\cdot\\frac{\\sin(h/2)}{h/2}$
        3. 取极限：利用重要极限 $\\lim_{t\\to 0}\\frac{\\sin t}{t}=1$，得 $f'(x) = \\cos x$
        
        **结论**：$(\\sin x)' = \\cos x$，同理可得 $(\\cos x)' = -\\sin x$。
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
    
    st.markdown("---")
    st.markdown("### 三、常见基本初等函数的导函数")
    st.success("""
    📝 基本求导公式表（必须牢记，后续所有求导计算的基础）：
    
    | 原函数 $f(x)$ | 导函数 $f'(x)$ | 备注 |
    | :---: | :---: | :--- |
    | $C$（常数） | $0$ | 常数的导数为0 |
    | $x^n$ | $nx^{n-1}$ | 幂函数求导公式，n为任意实数 |
    | $\\sin x$ | $\\cos x$ | 正弦求导得余弦 |
    | $\\cos x$ | $-\\sin x$ | 余弦求导得负正弦 |
    | $a^x$ | $a^x \\ln a$ | 指数函数求导，$a>0,a\\neq1$ |
    | $e^x$ | $e^x$ | 自然指数函数导数等于自身 |
    | $\\log_a x$ | $\\dfrac{1}{x\\ln a}$ | 对数函数求导，$a>0,a\\neq1$ |
    | $\\ln x$ | $\\dfrac{1}{x}$ | 自然对数求导 |
    """)
    
    st.markdown("---")
    st.markdown("### 四、例题：求常见函数的导函数")
    st.markdown("#### 例1：求下列函数的导函数")
    with st.expander("点击查看解答"):
        st.markdown("""
        1. $f(x) = x^5$：由幂函数公式，$f'(x) = 5x^{5-1} = 5x^4$
        2. $f(x) = \\sqrt[3]{x} = x^{\\frac{1}{3}}$：$f'(x) = \\dfrac{1}{3}x^{\\frac{1}{3}-1} = \\dfrac{1}{3}x^{-\\frac{2}{3}} = \\dfrac{1}{3\\sqrt[3]{x^2}}$
        3. $f(x) = 2^x$：由指数函数公式，$f'(x) = 2^x \\ln 2$
        4. $f(x) = \\log_2 x$：由对数函数公式，$f'(x) = \\dfrac{1}{x\\ln 2}$
        5. $f(x) = \\ln x$：$f'(x) = \\dfrac{1}{x}$
        """)
    
    st.markdown("---")
    st.markdown("#### 例2：分段函数在分界点处的可导性判断")
    st.markdown("讨论函数 $f(x) = \\begin{cases} x^2, & x \\leq 1 \\\\ ax+b, & x>1 \\end{cases}$ 在 $x=1$ 处的连续性与可导性，并确定 $a,b$ 使函数在 $x=1$ 处可导。")
    with st.expander("点击查看解答"):
        st.markdown("""
        **第一步：先保证连续**：
        - 左极限：$\\lim\\limits_{x\\to1^-}f(x) = \\lim\\limits_{x\\to1^-}x^2 = 1$
        - 右极限：$\\lim\\limits_{x\\to1^+}f(x) = \\lim\\limits_{x\\to1^+}(ax+b) = a+b$
        - 函数值：$f(1) = 1^2 = 1$
        连续要求三者相等，因此 $a+b = 1$。
        
        **第二步：再保证可导**：
        - 左导数：$f'_-(1) = \\lim\\limits_{h\\to0^-}\\dfrac{(1+h)^2 - 1}{h} = \\lim\\limits_{h\\to0^-}\\dfrac{2h+h^2}{h} = 2$
        - 右导数：$f'_+(1) = \\lim\\limits_{h\\to0^+}\\dfrac{a(1+h)+b - 1}{h} = \\lim\\limits_{h\\to0^+}\\dfrac{ah + (a+b-1)}{h} = a$
        （这里利用了连续条件 $a+b=1$，分子常数项为0）
        可导要求左右导数相等，因此 $a=2$。
        
        **第三步：求解参数**：
        代入 $a=2$ 到连续条件 $a+b=1$，得 $b = -1$。
        
        **结论**：当 $a=2, b=-1$ 时，函数在 $x=1$ 处连续且可导，且 $f'(1)=2$。
        """)
    
    st.markdown("---")
    st.info("""
    💡 方法总结：对于分段函数在分界点的可导性问题，解题顺序固定：
    1. **先求连续条件**：利用"左极限=右极限=函数值"，得到一个关于参数的方程；
    2. **再求左右导数**：回到导数定义，分别计算分界点处的左导数和右导数；
    3. **令左右导数相等**：得到第二个方程；
    4. **联立求解**参数。
    
    记住口诀：**先定连续，再比导数**。
    """)

# 4. 可导与连续的关系
elif page == "4. 可导与连续的关系":
    st.title("4. 可导与连续的关系")
    st.markdown("---")
    
    # ★引入 8（第二节 第 24 分钟）｜「4. 可导与连续的关系」：先看「可导 ⇒ 连续」的证明，再看反例
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
    2. **垂直切线反例**：$f(x) = \\sqrt[3]{x}$ 在 $x=0$ 处连续，但差商 $\\dfrac{f(0+\\Delta x)-f(0)}{\\Delta x}=\\dfrac{1}{\\sqrt[3]{\\Delta x^{2}}}\\to+\\infty$，切线垂直于 x 轴，故 $f'(0)$ 不存在。
    """)
    
    # 绘制两个反例图像
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(5,4))
        fig1, ax1 = prep_fig(fig1, ax1)
        x1 = np.linspace(-2,2,200)
        y1 = np.abs(x1)
        ax1.plot(x1, y1, linewidth=2, color='#1f77b4')
        ax1.scatter(0,0, color='red', zorder=5, s=50)
        ax1.set_title('反例1: f(x)=|x| 在x=0处尖点不可导', fontsize=12)
        ax1.grid(alpha=0.3)
        ax1.set_xlim(-2,2)
        ax1.set_ylim(-0.5,2.5)

        safe_pyplot(fig1, key="contra_absx")
    
    with col2:
        fig2, ax2 = plt.subplots(figsize=(5,4))
        fig2, ax2 = prep_fig(fig2, ax2)
        x2 = np.linspace(-2,2,200)
        y2 = np.cbrt(x2)
        ax2.plot(x2, y2, linewidth=2, color='#ff7f0e')
        ax2.axvline(x=0, color='red', linestyle='--', label='垂直切线')
        ax2.scatter(0,0, color='red', zorder=5, s=50)
        ax2.set_title(r'反例2: $f(x)=\sqrt[3]{x}$ 在x=0处垂直切线不可导', fontsize=12)
        ax2.grid(alpha=0.3)
        ax2.set_xlim(-2,2)
        ax2.set_ylim(-2,2)
        ax2.legend()

        safe_pyplot(fig2, key="contra_cbrt")

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
    
    # ★引入 6（第二节 第 5 分钟｜全课最关键的一次）｜「5. 导数的几何意义：割线逼近切线✨」：拖 Δx 令 N 点趋近 M 点
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
    fig, ax = prep_fig(fig, ax)
    
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
    

    # 铺满页面宽度，投影时更大更清楚，图高度按8:5比例自动适配
    safe_pyplot(fig, key="secant_tangent")

    
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
    
    # ★引入 7（第二节 第 15 分钟）｜「6. 切线方程与法线方程」：对照例题的方程与配图，印证板书两个公式
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
        fig, ax = prep_fig(fig, ax)
        x = np.linspace(-2, 4, 400)
        ax.plot(x, x**2, label=r"$y = x^2$", linewidth=2, color='#1f77b4')
        ax.plot(x, 2*x - 1, label=r"切线 $y = 2x - 1$", color='red', linewidth=2)
        ax.plot(x, -0.5*x + 1.5, label=r"法线 $y = -\frac{1}{2}x + \frac{3}{2}$", color='green', linewidth=2)
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
        

        safe_pyplot(fig, key="tangent_normal_para")


# 7. 课堂小结与练习
elif page == "7. 课堂小结与练习":
    st.title("7. 课堂小结与课堂练习")
    st.markdown("---")
    
    st.markdown("### 一、本节课核心知识点总结")
    st.markdown("""
    1. **一个定义**：导数是函数增量与自变量增量之比的极限，本质是瞬时变化率；
    2. **一个方法**：用定义求导三步法——一差、二比、三极限；
    3. **一个充要条件**：某点可导 $\\iff$ 左右导数都存在且相等；
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
    # ★引入 5（第一节 第 44 分钟）｜「7. 课堂小结与课堂练习」：交互实践题「猜一猜 x=1 处的导数是多少」
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
        fig_q6, ax_q6 = prep_fig(fig_q6, ax_q6)
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

        safe_pyplot(fig_q6, key="guess_tangent_q6")

    # ★引入 10（第二节 第 42 分钟）｜「7. 课堂练习」练习 7、8：当堂核对切线方程与分段函数可导性判断
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

plt.show()''', language="python")

    # ================= 交互计算题 =================
    st.markdown("---")
    st.markdown("## 🎛️ 计算题（拖动滑块，实时观察动态效果）")

    # ---------- 计算题四 ----------
    # ★引入 4（第一节 第 40 分钟）｜「8. 计算实践与代码实现✨」：拖 x₀ 看切线动态追踪；计算题五对 sin x 验证导数
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

    safe_pyplot(fig4, key="tan_norm_dyn_t4")

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
    fig5, (axA, axB) = prep_fig(fig5, (axA, axB))

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

    # 针对 loglog 的字体警告修复
    from matplotlib.ticker import FuncFormatter
    h_grid = np.logspace(-6, 0, 200)
    approx_grid = (np.sin(x0_t5 + h_grid) - np.sin(x0_t5)) / h_grid
    err_grid = np.maximum(np.abs(approx_grid - true_t5), 1e-18)
    axB.loglog(h_grid, err_grid, linewidth=2.0, color="#1f77b4", label=r"$|\frac{\Delta y}{\Delta x}-f'(x_0)|$")
    axB.scatter([h_t5], [max(abs(approx_t5 - true_t5), 1e-18)], color="red", s=120, zorder=5, label="当前 h")
    
    # 强制重新格式化对数轴的刻度标签，使用纯 ASCII 减号，绕过 LogFormatter
    axB.xaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:g}"))
    axB.yaxis.set_major_formatter(FuncFormatter(lambda val, pos: f"{val:g}"))
    
    axB.grid(alpha=0.3, linestyle="--", which="both")
    axB.legend(fontsize=10)
    axB.set_xlabel("h（对数坐标）", fontsize=12)
    axB.set_ylabel("误差", fontsize=12)
    axB.set_title("误差随 h 的变化", fontsize=12)


    safe_pyplot(fig5, key="sinx_converge_t5")

    d1, d2, d3 = st.columns(3)
    d1.metric("当前 h", f"{h_t5:.3f}")
    d2.metric("差商值", f"{approx_t5:.6f}")
    d3.metric("真实导数值 cos(x₀)", f"{true_t5:.6f}", delta=f"{approx_t5 - true_t5:+.2e}")

    st.info("🎯 观察结论：h 越小，割线斜率越接近切线斜率；当 h 小到一定程度后，由于计算机浮点舍入误差，误差反而略有回升，这正说明「取极限」是数学上的理想过程。")

# 9. 课程思政
elif page == "9. 课程思政":
    # ★引入 11（课后）｜「9. 课程思政」：把课堂结论延伸到科学精神与文化自信
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
    公元3世纪我国数学家刘徽提出割圆术："割之弥细，所失弥少，割之又割，以至于不可割，则与圆合体而无所失矣"，用正多边形逼近圆周率，正是同样的思想。直到约 1400 年后的 17 世纪，牛顿与莱布尼茨才系统创立微积分，这充分说明我们的祖先早已掌握了这种辩证思维。

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

        这正是极限思想的雏形，比牛顿、莱布尼茨在 17 世纪系统创立微积分早约 1400 年（古希腊阿基米德另有"穷竭法"，但其方法与结果均不如刘徽简洁精确）。
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

# 10. 课后习题与代码实现✨
elif page == "10. 课后习题与代码实现✨":
    # ★引入 11（课后）｜「10. 课后习题与代码实现」：布置 20 道课后题（重点：习题 9 幂函数求导、习题 17 分段函数求参数）
    st.title("10. 课后习题与代码实现✨")
    st.markdown("---")
    st.info("💡 本节对应同济版《高等数学》上册**习题 2-1 导数概念**共 20 题。每题均给出标准答案与解析，**全部 20 题都附可直接运行的 Python 代码**进行数值/符号/绘图验证。点击每个题目的「展开」即可查看详情。")

    # ---------- 习题 1（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 1（角速度问题）")
    st.markdown(r"设物体绕定轴旋转，在时间间隔 $[0,t]$ 内转过角度 $\theta=\theta(t)$。如果旋转是非匀速的，应怎样确定该物体在时刻 $t_0$ 的角速度？")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        在时间间隔 $[t_0,\,t_0+\Delta t]$ 内的平均角速度：
        $$\bar{\omega}=\frac{\Delta\theta}{\Delta t}=\frac{\theta(t_0+\Delta t)-\theta(t_0)}{\Delta t}.$$
        当 $\Delta t\to 0$，平均角速度的极限即为 $t_0$ 时刻的**瞬时角速度**：
        $$\omega=\lim_{\Delta t\to 0}\bar{\omega}=\lim_{\Delta t\to 0}\frac{\Delta\theta}{\Delta t}=\theta'(t_0).$$
        """)
    with st.expander("🐍 Python 代码（数值差商验证瞬时角速度）", expanded=False):
        st.code(r'''import numpy as np

# 举例：角度函数 θ(t) = t^2 (弧度)，其角速度 ω(t)=θ'(t)=2t
def theta(t):
    return t**2

t0 = 3.0
true_omega = 2*t0                     # 理论角速度 θ'(3)=6
print(f"t0 = {t0} 时，理论瞬时角速度 ω(t0) = {true_omega}")

# 用差商逼近导数
for dt in [0.1, 0.01, 0.001, 0.0001]:
    omega_approx = (theta(t0+dt) - theta(t0))/dt
    print(f"Δt={dt:<6}  平均角速度={omega_approx:.8f}  误差={abs(omega_approx-true_omega):.2e}")''', language="python")

    # ---------- 习题 2（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 2（冷却速度问题）")
    st.markdown(r"物体温度 $T=T(t)$，如何确定时刻 $t$ 的冷却速度？")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        在 $[t,\,t+\Delta t]$ 内平均冷却速度：
        $$\bar{v}=\frac{\Delta T}{\Delta t}=\frac{T(t+\Delta t)-T(t)}{\Delta t}.$$
        时刻 $t$ 的冷却速度：
        $$v=\lim_{\Delta t\to 0}\frac{\Delta T}{\Delta t}=T'(t).$$
        """)
    with st.expander("🐍 Python 代码（牛顿冷却定律数值验证）", expanded=False):
        st.code(r'''import numpy as np

# 牛顿冷却：T(t) = T_env + (T0-T_env)*exp(-kt)，此处取 T_env=20, T0=100, k=0.1
T_env, T0, k = 20.0, 100.0, 0.1
def T(t):
    return T_env + (T0 - T_env)*np.exp(-k*t)
def v_true(t):                       # T'(t) = -k(T0-T_env)exp(-kt)
    return -k*(T0 - T_env)*np.exp(-k*t)

t = 5.0
print(f"t={t} 时，理论冷却速度 v(t)=T'(t) = {v_true(t):.6f}")
print("  （负值表示温度下降）")
for dt in [0.1, 0.01, 0.001, 0.0001]:
    v_approx = (T(t+dt)-T(t))/dt
    print(f"Δt={dt:<6}  数值平均速度={v_approx:.8f}  误差={abs(v_approx-v_true(t)):.2e}")''', language="python")

    # ---------- 习题 3（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 3（边际成本问题）")
    st.markdown(r"成本函数 $C(x)=2000+100x-0.1x^2$（元），试求：(1) 生产 100 件时的边际成本；(2) 生产第 101 件产品的成本，并与(1)比较。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        (1) $C'(x)=100-0.2x$，故 $C'(100)=100-20=80$（元/件）。

        (2) $C(101)=2000+100\times101-0.1\times101^2=11079.9$（元）；$C(100)=11000$（元）；
        $C(101)-C(100)=79.9$（元）。即第 101 件成本 79.9 元，与边际成本 80 非常接近，说明**边际成本近似表达产量达到 x 单位时再增加一单位产品所需的成本**。
        """)
    with st.expander("🐍 Python 代码", expanded=False):
        st.code(r'''def C(x):
    return 2000 + 100*x - 0.1*x**2

def Cp(x):                      # 边际成本 = C'(x)
    return 100 - 0.2*x

print(f"(1) C'(100) = {Cp(100)} 元/件")
print(f"(2) C(101) = {C(101):.2f} 元")
print(f"    C(100) = {C(100):.2f} 元")
print(f"    C(101)-C(100) = {C(101)-C(100):.2f} 元")''', language="python")

    # ---------- 习题 4（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 4（按定义求 $f'(-1)$）")
    st.markdown(r"设 $f(x)=10x^2$，按定义求 $f'(-1)$。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"由导数定义：")
        st.latex(
            r"\begin{aligned}"
            r"f'(-1)&=\lim_{\Delta x\to 0}\frac{f(-1+\Delta x)-f(-1)}{\Delta x}\\"
            r"&=\lim_{\Delta x\to 0}\frac{10(-1+\Delta x)^2-10}{\Delta x}\\"
            r"&=\lim_{\Delta x\to 0}\frac{-20\,\Delta x+10(\Delta x)^2}{\Delta x}\\"
            r"&=\lim_{\Delta x\to 0}(-20+10\,\Delta x)=-20."
            r"\end{aligned}"
        )
        st.markdown(r"故 $\boldsymbol{f'(-1)=-20}$。")
    with st.expander("🐍 Python 代码（数值差商 + 解析导数验证）", expanded=False):
        st.code(r'''import numpy as np

def f(x):
    return 10*x**2

def fp_true(x):                   # 解析导数 f'(x)=20x
    return 20*x

x0 = -1.0
print(f"解析结果：f'({x0}) = {fp_true(x0)}")
print("数值差商逼近：")
for h in [0.1, 0.01, 0.001, 0.0001, 1e-6]:
    fp = (f(x0+h)-f(x0))/h
    print(f"  h={h:<8g}  数值导数={fp: .8f}  误差={abs(fp-fp_true(x0)):.2e}")''', language="python")

    # ---------- 习题 5（奇数·附代码）----------
    st.markdown("---")
    st.markdown(r"#### 习题 5（证明 $(\cos x)'=-\sin x$）")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"用和差化积公式：")
        st.latex(
            r"\begin{aligned}"
            r"(\cos x)'&=\lim_{\Delta x\to 0}\frac{\cos(x+\Delta x)-\cos x}{\Delta x}\\"
            r"&=\lim_{\Delta x\to 0}\frac{-2\sin\!\left(x+\dfrac{\Delta x}{2}\right)\sin\dfrac{\Delta x}{2}}{\Delta x}\\"
            r"&=\lim_{\Delta x\to 0}\left[-\sin\!\left(x+\frac{\Delta x}{2}\right)\right]"
            r"\cdot\frac{\sin\dfrac{\Delta x}{2}}{\dfrac{\Delta x}{2}}\\"
            r"&=-\sin x."
            r"\end{aligned}"
        )
    with st.expander("🐍 Python 代码（数值差商验证）", expanded=False):
        st.code(r'''import numpy as np

def f(x):
    return np.cos(x)

def diff_q(x, h=1e-6):
    return (f(x+h)-f(x))/h

for x0 in [0.0, 0.5, 1.0, np.pi/2, 2.0]:
    approx = diff_q(x0)
    true   = -np.sin(x0)
    print(f"x={x0:6.3f}  数值导数={approx: .8f}  真值=-sinx={true: .8f}  误差={abs(approx-true):.2e}")''', language="python")

    # ---------- 习题 6（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 6（利用导数定义识别极限）")
    st.markdown(r"设 $f'(x_0)$ 存在，指出下列极限中 $A$ 表示什么。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        (1) $\displaystyle A=\lim_{\Delta x\to0}\frac{f(x_0-\Delta x)-f(x_0)}{\Delta x}=-f'(x_0)$；

        (2) $\displaystyle A=\lim_{x\to0}\frac{f(x)}{x}=\lim_{x\to0}\frac{f(x)-f(0)}{x-0}=f'(0)$（因 $f(0)=0$）；

        (3) $\displaystyle A=\lim_{h\to0}\frac{f(x_0+h)-f(x_0-h)}{h}=2f'(x_0)$。
        """)
    with st.expander("🐍 Python 代码（以具体函数数值验证三个极限）", expanded=False):
        st.code(r'''import numpy as np

# 取 f(x)=sinx, x0=1, 则 f'(x0)=cos(1)
def f(x): return np.sin(x)
x0 = 1.0
fp_true = np.cos(x0)
print(f"f(x)=sinx, x0={x0}, f'(x0)=cos(x0)={fp_true:.8f}\n")

# (1) A = -f'(x0)
for dx in [0.1, 0.01, 0.001, 1e-6]:
    A1 = (f(x0-dx)-f(x0))/dx
    print(f"(1) Δx={dx:<8g}  A={A1: .8f}  理论=-f'(x0)={-fp_true:.8f}")
print()

# (2) A = f'(0) = cos(0) = 1
for h in [0.1, 0.01, 0.001, 1e-6]:
    A2 = f(h)/h
    print(f"(2) x={h:<8g}   A={A2: .8f}  理论=f'(0)=1.00000000")
print()

# (3) A = 2f'(x0)
for h in [0.1, 0.01, 0.001, 1e-6]:
    A3 = (f(x0+h)-f(x0-h))/h
    print(f"(3) h={h:<8g}   A={A3: .8f}  理论=2f'(x0)={2*fp_true:.8f}")''', language="python")

    # ---------- 习题 7（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 7（分段函数单侧导数选择题）")
    st.markdown(r"设 $f(x)=\begin{cases}\dfrac{2}{3}x^3,&x\le 1,\\[4pt]x^2,&x>1,\end{cases}$ 则 $f(x)$ 在 $x=1$ 处（  ）。")
    st.markdown("(A) 左、右导数都存在 &nbsp;&nbsp; (B) 左导数存在，右导数不存在 &nbsp;&nbsp; (C) 左导数不存在，右导数存在 &nbsp;&nbsp; (D) 左、右导数都不存在")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $f(1)=\dfrac23$，
        $f'_-(1)=\lim\limits_{x\to1^-}\dfrac{\frac23x^3-\frac23}{x-1}=\lim\limits_{x\to1^-}\dfrac23(x^2+x+1)=2$；
        $f'_+(1)=\lim\limits_{x\to1^+}\dfrac{x^2-\frac23}{x-1}=\infty$。
        故左导数存在，右导数不存在，应选 **(B)**。
        """)
    with st.expander("🐍 Python 代码（数值逼近验证左右导数）", expanded=False):
        st.code(r'''import numpy as np

def f(x):
    return (2/3)*x**3 if x <= 1 else x**2

f1 = 2/3
# 右导数：x 从右侧逼近 1
print("从右侧（x→1+）逼近：")
for eps in [0.1, 0.01, 0.001, 0.0001]:
    x = 1 + eps
    print(f"  x={x:.5f}  (f(x)-f(1))/(x-1)={(f(x)-f1)/eps: .4f}")
# 左导数：x 从左侧逼近 1
print("从左侧（x→1-）逼近：")
for eps in [0.1, 0.01, 0.001, 0.0001]:
    x = 1 - eps
    print(f"  x={x:.5f}  (f(x)-f(1))/(x-1)={(f(x)-f1)/(-eps): .4f}")
print("=> 左侧收敛到 2，右侧发散到 ∞，与解答一致。")''', language="python")

    # ---------- 习题 8（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 8（含绝对值的可导性条件）")
    st.markdown(r"设 $f(x)$ 可导，$F(x)=f(x)(1+|\sin x|)$，则 $f(0)=0$ 是 $F(x)$ 在 $x=0$ 处可导的（  ）。")
    st.markdown("(A) 充分必要条件 &nbsp;&nbsp; (B) 充分但非必要 &nbsp;&nbsp; (C) 必要但非充分 &nbsp;&nbsp; (D) 既非充分也非必要")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $F'_+(0)=f'(0)+f(0)$，$F'_-(0)=f'(0)-f(0)$，
        故 $F'_+(0)=F'_-(0)\iff f(0)=0$，应选 **(A)**。
        """)
    with st.expander("🐍 Python 代码（取 f(x)=x 与 f(x)=x+1 数值对比左右导数）", expanded=False):
        st.code(r'''import numpy as np

def test(f_case, label):
    """用左右差商检验 F(x)=f(x)(1+|sin x|) 在 x=0 的左右导数。"""
    F = lambda x: f_case(x)*(1+abs(np.sin(x)))
    h = 1e-6
    Fp_right = (F(h)-F(0))/h
    Fp_left  = (F(-h)-F(0))/(-h)
    print(f"【{label}】 f(0)={f_case(0)}")
    print(f"  F'_+(0) ≈ {Fp_right:.6f},  F'_-(0) ≈ {Fp_left:.6f}")
    print(f"  左右导数差 = {abs(Fp_right-Fp_left):.2e}  →  {'可导' if abs(Fp_right-Fp_left)<1e-3 else '不可导'}\n")

# 情形1：f(0)=0，取 f(x)=x (f'(0)=1)
test(lambda x: x,           "f(x)=x, f(0)=0")
# 情形2：f(0)≠0，取 f(x)=x+1 (f(0)=1, f'(0)=1)
test(lambda x: x+1,         "f(x)=x+1, f(0)=1")
print("=> 仅当 f(0)=0 时左右导数相等，即 f(0)=0 是充要条件，选(A)。")''', language="python")

    # ---------- 习题 9（奇数·附代码：方法1 sympy + 方法2 numpy）----------
    st.markdown("---")
    st.markdown("#### 习题 9（幂函数求导）")
    st.markdown(r"求下列函数的导数：")
    st.markdown(r"(1) $y=x^4$；(2) $y=\sqrt[3]{x^2}$；(3) $y=x^{1.6}$；(4) $y=\dfrac{1}{\sqrt{x}}$；(5) $y=\dfrac{1}{x^2}$；(6) $y=x^3\sqrt[5]{x}$。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        统一化归为幂函数 $x^\alpha$，再用公式 $(x^\alpha)'=\alpha x^{\alpha-1}$：

        (1) $y'=4x^3$；
        (2) $y=x^{2/3}$，$y'=\dfrac23 x^{-1/3}=\dfrac{2}{3\sqrt[3]{x}}$；
        (3) $y'=1.6\,x^{0.6}$；
        (4) $y=x^{-1/2}$，$y'=-\dfrac12 x^{-3/2}=-\dfrac{1}{2x\sqrt{x}}$；
        (5) $y=x^{-2}$，$y'=-2x^{-3}=-\dfrac{2}{x^3}$；
        (6) $y=x^{3+1/5}=x^{16/5}$，$y'=\dfrac{16}{5}x^{11/5}=\dfrac{16}{5}x^2\sqrt[5]{x}$。
        """)
    with st.expander("🐍 Python 代码·方法 1：sympy 符号求导（保留）", expanded=False):
        st.code(r'''from sympy import symbols, diff, simplify, Rational, Pow, root
x = symbols('x')

f1 = x**4
f2 = Pow(x, Rational(2,3))           # x^(2/3)
f3 = x**1.6
f4 = x**Rational(-1,2)               # 1/√x
f5 = x**(-2)
f6 = x**3 * root(x, 5)               # x^3 * x^(1/5)

for i, f in enumerate([f1,f2,f3,f4,f5,f6], 1):
    print(f"({i}) y = {f}")
    print(f"    y' = {simplify(diff(f,x))}")''', language="python")
    with st.expander("🐍 Python 代码·方法 2：纯 numpy 数值验证（无需 sympy）", expanded=False):
        st.code(r'''import numpy as np

# 把 6 个函数写成 (lambda 表达式, 解析导数 lambda, 名称, 测试点) 的列表
# 说明：对于 x^α 在 x>0 时直接用 x**α；f2、f4 等含根号/分式取 x0=1（正值域内）
funcs = [
    (lambda x: x**4,                   lambda x: 4*x**3,                       "y=x^4",               2.0),
    (lambda x: x**(2/3),               lambda x: (2/3)*x**(-1/3),              "y=x^(2/3)",           1.0),
    (lambda x: x**1.6,                 lambda x: 1.6*x**0.6,                   "y=x^1.6",             1.0),
    (lambda x: 1/np.sqrt(x),           lambda x: -0.5*x**(-1.5),               "y=1/sqrt(x)",         1.0),
    (lambda x: 1/x**2,                 lambda x: -2/x**3,                      "y=1/x^2",             2.0),
    (lambda x: x**(16/5),              lambda x: (16/5)*x**(11/5),             "y=x^3·x^(1/5)=x^(16/5)", 1.0),
]
h = 1e-7
for i,(f,fp,name,x0) in enumerate(funcs,1):
    # 中心差商 (f(x+h)-f(x-h))/(2h) 精度更高
    num  = (f(x0+h)-f(x0-h))/(2*h)
    true = fp(x0)
    print(f"({i}) {name:<28} 在 x={x0}: 数值导数≈{num: .8f}, 解析导数={true: .8f}, 误差={abs(num-true):.2e}")''', language="python")

    # ---------- 习题 10（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 10（运动规律求瞬时速度）")
    st.markdown(r"已知物体的运动规律为 $s=t^3$(m)，求这物体在 $t=2$(s) 时的速度。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        **解**：速度是位移对时间的导数，即 $v=\dfrac{\mathrm{d}s}{\mathrm{d}t}$。按导数定义，
        $$v(t_0)=\lim_{\Delta t\to0}\frac{s(t_0+\Delta t)-s(t_0)}{\Delta t}=\lim_{\Delta t\to0}\frac{(t_0+\Delta t)^3-t_0^3}{\Delta t}=\lim_{\Delta t\to0}\left(3t_0^2+3t_0\Delta t+\Delta t^2\right)=3t_0^2,$$
        故 $v=3t^2$，当 $t=2$ 时
        $$v\big|_{t=2}=3\times2^2=12\ \text{(m/s)}.$$
        """)
    with st.expander("🐍 Python 代码·方法 1：中心差商逼近瞬时速度", expanded=False):
        st.code(r'''import numpy as np

# 运动规律 s(t)=t^3，速度是位移对时间的导数 v(t)=s'(t)=3t^2
def s(t):
    return t**3

def v(t):
    return 3 * t**2

t0 = 2.0
print(f"解析速度 v({t0}) = s'({t0}) = 3 * {t0}^2 = {v(t0):.1f} m/s")

# 用中心差商 (s(t0+h)-s(t0-h)) / (2h) 逼近瞬时速度
for h in [1e-1, 1e-2, 1e-3, 1e-4, 1e-6]:
    v_num = (s(t0 + h) - s(t0 - h)) / (2 * h)
    print(f"h = {h:<6}  数值速度 = {v_num:.8f} m/s  误差 = {abs(v_num - v(t0)):.2e}")''', language="python")
    with st.expander("🐍 Python 代码·方法 2：前向差商（定义式原样）", expanded=False):
        st.code(r'''import numpy as np

# 严格按定义式 v(t0)=lim [s(t0+dt)-s(t0)]/dt 来算，不取对称点
def s(t):
    return t**3

t0, v_true = 2.0, 12.0
print(f"理论速度 v({t0}) = {v_true:.1f} m/s")

for dt in [1e-1, 1e-2, 1e-3, 1e-4, 1e-6]:
    v_num = (s(t0 + dt) - s(t0)) / dt
    print(f"dt = {dt:<6}  差商 = {v_num:.8f} m/s  误差 = {abs(v_num - v_true):.2e}")''', language="python")
    with st.expander("🐍 Python 代码·方法 3：画 s-t 曲线与 t=2 处的切线（斜率即速度）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

s = lambda t: t**3
v = lambda t: 3 * t**2
t0 = 2.0

t = np.linspace(0, 3, 400)
plt.figure(figsize=(6, 4))
plt.plot(t, s(t), color='#1f77b4', linewidth=2, label=r'$s=t^3$')
plt.plot(t, s(t0) + v(t0) * (t - t0), '--', color='red',
         label=fr'tangent at t=2, slope={v(t0):.0f} (= speed)')
plt.scatter([t0], [s(t0)], color='black', zorder=5, label='(2, 8)')
plt.xlabel('t (s)')
plt.ylabel('s (m)')
plt.legend()
plt.grid(alpha=0.3)

plt.show()''', language="python")

    # ---------- 习题 11（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 11（偶函数导数在 0 点）")
    st.markdown(r"如果 $f(x)$ 为偶函数，且 $f'(0)$ 存在，证明 $f'(0)=0$。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        由 $f(-x)=f(x)$，两边对 $x$ 求导得 $-f'(-x)=f'(x)$。令 $x=0$，得 $-f'(0)=f'(0)$，故 $f'(0)=0$。

        也可直接用定义：
        $$f'(0)=\lim_{h\to0}\frac{f(h)-f(0)}{h}=\lim_{h\to0}\frac{f(-h)-f(0)}{h}=-\lim_{h\to0}\frac{f(-h)-f(0)}{-h}=-f'(0),$$
        所以 $f'(0)=0$。
        """)
    with st.expander("🐍 Python 代码（以 $f(x)=\\cos x$ 数值验证）", expanded=False):
        st.code(r'''import numpy as np

def f(x): return np.cos(x)        # 偶函数

h = 1e-6
fp_forward  = (f(h)-f(0))/h
fp_backward = (f(-h)-f(0))/(-h)
print(f"右差商 = {fp_forward: .8f}")
print(f"左差商 = {fp_backward: .8f}")
print(f"平均 ≈ f'(0) = {(fp_forward+fp_backward)/2: .8f}   # 理论为 0")''', language="python")

    # ---------- 习题 12（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 12（曲线切线与法线）")
    st.markdown(r"求曲线 $y=\cos x$ 在点 $\left(\dfrac{\pi}{6},\dfrac{\sqrt3}{2}\right)$ 和点 $\left(\dfrac{\pi}{3},\dfrac12\right)$ 处的切线斜率。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $y'=-\sin x$，在 $x=\dfrac\pi6$ 处斜率 $k=-\dfrac12$；
        在 $x=\dfrac\pi3$ 处斜率 $k=-\dfrac{\sqrt3}{2}$。
        """)
    with st.expander("🐍 Python 代码（数值差商求斜率 + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x): return np.cos(x)
def fp_num(x, h=1e-6): return (f(x+h)-f(x))/h

pts = [np.pi/6, np.pi/3]
for x0 in pts:
    y0 = f(x0)
    k  = fp_num(x0)
    print(f"x={x0:.4f} (={x0/np.pi:.2f}π), y={y0:.4f}, 切线斜率≈{k:.6f}")

x = np.linspace(-0.5, 2.0, 400)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, f(x), linewidth=2, label=r"$y=\cos x$")
for x0 in pts:
    y0 = f(x0); k = fp_num(x0)
    ax.plot(x, y0+k*(x-x0), "--", linewidth=2, label=f"切线@x={x0/np.pi:.2f}π")
    ax.scatter([x0],[y0], s=80, zorder=5)
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)

plt.show()''', language="python")

    # ---------- 习题 13（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 13（余弦曲线的切线与法线方程）")
    st.markdown(r"求曲线 $y=\cos x$ 上点 $\left(\dfrac{\pi}{3},\dfrac12\right)$ 处的切线方程和法线方程。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $y'=-\sin x$，在 $x=\pi/3$ 处 $k=-\sin\frac{\pi}{3}=-\dfrac{\sqrt3}{2}$。

        - 切线：$y-\dfrac12=-\dfrac{\sqrt3}{2}\left(x-\dfrac{\pi}{3}\right)$；
        - 法线（与切线垂直，斜率 $\dfrac{2}{\sqrt3}$）：$y-\dfrac12=\dfrac{2}{\sqrt3}\left(x-\dfrac{\pi}{3}\right)$。
        """)
    with st.expander("🐍 Python 代码（求解 + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

x0, y0 = np.pi/3, 0.5
k_t = -np.sin(x0)                     # 切线斜率
k_n = -1/k_t                          # 法线斜率
print(f"切线斜率 = {k_t:.4f}")
print(f"法线斜率 = {k_n:.4f}")

x = np.linspace(-0.5, 2.5, 400)
y_cos = np.cos(x)
y_tan = y0 + k_t*(x-x0)
y_nor = y0 + k_n*(x-x0)

fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, y_cos, linewidth=2, label=r"$y=\cos x$")
ax.plot(x, y_tan, "r--", linewidth=2, label="切线")
ax.plot(x, y_nor, "g--", linewidth=2, label="法线")
ax.scatter([x0],[y0], s=100, color="black", zorder=5, label=r"$(\pi/3,\,1/2)$")
ax.axhline(0,color="gray",lw=0.8); ax.axvline(0,color="gray",lw=0.8)
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)
ax.set_xlabel("x"); ax.set_ylabel("y")
ax.set_title(r"$y=\cos x$ 在 $(\pi/3,\,1/2)$ 处的切线与法线")

plt.show()''', language="python")

    # ---------- 习题 14（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 14（求使切线水平/斜率为 1 的点）")
    st.markdown(r"求曲线 $y=e^x$ 在点 $(0,1)$ 处的切线方程；并求曲线上哪一点的切线与直线 $y=x$ 平行。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $y'=e^x$，在 $(0,1)$ 处斜率为 1，切线方程为 $y=x+1$；
        令 $e^x=1$，得 $x=0$，即在 $(0,1)$ 点切线与 $y=x$ 平行。
        """)
    with st.expander("🐍 Python 代码（数值求切点 + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x): return np.exp(x)

# (0,1) 处切线斜率
x0 = 0.0
k0 = (f(x0+1e-7)-f(x0-1e-7))/(2e-7)
print(f"(0,1) 处切线斜率≈{k0:.6f}，切线方程：y = x + 1")

# 解方程 e^x = 1，得 x=0
x_sol = 0.0
print(f"使切线平行于 y=x 的点：({x_sol}, {f(x_sol):.0f})")

x = np.linspace(-2, 2, 400)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, f(x), linewidth=2, label=r"$y=e^x$")
ax.plot(x, x+1, "r--", linewidth=2, label=r"切线 $y=x+1$")
ax.plot(x, x, "g:", linewidth=1.5, label=r"$y=x$")
ax.scatter([0],[1], s=100, color="black", zorder=5, label="(0,1)")
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)

plt.show()''', language="python")

    # ---------- 习题 15（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 15（抛物线上平行于割线的切线）")
    st.markdown(r"在抛物线 $y=x^2$ 上取横坐标 $x_1=1$ 及 $x_2=3$ 的两点，作过这两点的割线。问该抛物线上哪一点的切线平行于这条割线？")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        割线端点 $(1,1),(3,9)$，割线斜率 $k=\dfrac{9-1}{3-1}=4$。
        切线斜率 $y'=2x=4$，得 $x=2$，对应点 $(2,4)$。
        """)
    with st.expander("🐍 Python 代码（求解 + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

x1, x2 = 1.0, 3.0
y1, y2 = x1**2, x2**2
k_sec = (y2-y1)/(x2-x1)
x0 = k_sec/2               # 由 2x = k_sec 得 x0
y0 = x0**2
print(f"割线斜率 = {k_sec}")
print(f"切点 = ({x0}, {y0})")

x = np.linspace(0, 4, 400)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, x**2, linewidth=2, label=r"$y=x^2$")
ax.plot(x, y1+k_sec*(x-x1), "--", linewidth=2, color="orange", label=f"割线, k={k_sec:.0f}")
ax.plot(x, y0+k_sec*(x-x0), "--", linewidth=2, color="red",    label="平行切线")
ax.scatter([x1,x2],[y1,y2], color="orange", s=100, zorder=5, label="割线端点")
ax.scatter([x0],[y0], color="red", s=120, zorder=5, label=f"切点({x0:.0f},{y0:.0f})")
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)

plt.show()''', language="python")

    # ---------- 习题 16（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 16（分段函数在 0 点的连续性与可导性）")
    st.markdown(r"讨论下列函数在 $x=0$ 处的连续性与可导性：(1) $y=|\sin x|$；(2) $y=\begin{cases}x^2\sin\dfrac{1}{x},&x\neq0,\\0,&x=0.\end{cases}$")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        (1) $f(0^+)=f(0^-)=f(0)=0$，连续；$f'_+(0)=1$，$f'_-(0)=-1$，**不可导**。

        (2) $\lim_{x\to0}x^2\sin\frac1x=0=f(0)$，连续；
        $f'(0)=\lim_{x\to0}\frac{f(x)-f(0)}{x}=\lim_{x\to0}x\sin\frac1x=0$，**可导且 $f'(0)=0$**。
        """)
    with st.expander("🐍 Python 代码（数值检验左右导数与极限）", expanded=False):
        st.code(r'''import numpy as np

# (1) f(x)=|sinx|
f1 = lambda x: abs(np.sin(x))
h = 1e-7
fp_right = (f1(h)-f1(0))/h
fp_left  = (f1(-h)-f1(0))/(-h)
print("【(1) f(x)=|sinx|】")
print(f"  f(0+h)≈{f1(h):.8f}, f(0-h)≈{f1(-h):.8f}  → 连续")
print(f"  右导数≈{fp_right:.6f}, 左导数≈{fp_left:.6f}  → 不相等，不可导\n")

# (2) f(x)=x^2 sin(1/x)，x≠0；f(0)=0
def f2(x):
    return np.where(x==0, 0.0, x**2*np.sin(1.0/x))
# 在 0 点附近画 f(x) 看极限；并算差商
xs = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
print("【(2) f(x)=x^2·sin(1/x)】")
print("  x 趋近 0 时 f(x) 的值：")
for x in xs:
    print(f"    x={x:<8g}  f(x)={f2(x): .10f}")
print("  x 趋近 0 时差商 f(x)/x：")
for x in xs:
    print(f"    x={x:<8g}  f(x)/x={f2(x)/x: .10f}  → 趋近 0，故 f'(0)=0")''', language="python")

    # ---------- 习题 17（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 17（分段函数连续可导求参数）")
    st.markdown(r"设 $f(x)=\begin{cases}x^2,&x\le 1,\\ax+b,&x>1,\end{cases}$ 为使 $f(x)$ 在 $x=1$ 处连续且可导，$a,b$ 应取什么值？")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        **连续**：$\lim_{x\to1^-}f(x)=\lim_{x\to1^+}f(x)=f(1)$，即 $1=a+b$。

        **可导**：$f'_-(1)=2$，$f'_+(1)=a$，故 $a=2$；代入连续性条件得 $b=-1$。
        即 $\boldsymbol{a=2,\;b=-1}$。
        """)
    with st.expander("🐍 Python 代码（数值检验连续与可导）", expanded=False):
        st.code(r'''import numpy as np

a, b = 2, -1
def f(x):
    return x**2 if x <= 1 else a*x + b

# 连续性
print(f"f(1) = {f(1)}")
print(f"f(1+1e-6) = {f(1+1e-6):.6f}")
print(f"f(1-1e-6) = {f(1-1e-6):.6f}")

# 左右导数数值逼近
h = 1e-6
fl = (f(1-h)-f(1))/(-h)
fr = (f(1+h)-f(1))/h
print(f"左导数(数值) ≈ {fl:.4f}, 右导数(数值) ≈ {fr:.4f}")
print("两值均为 2，可导条件满足；f(1+h)→1，连续条件满足。")''', language="python")

    # ==================================================================
    # ★引入 9（第二节 第 34 分钟）｜第 10 页习题 17 的视觉复核
    # 操作要点：拖动 a、b，观察曲线在分段点 x = 1 处是否光滑衔接
    # 教学作用：对刚算完的例 10 做几何复核——参数取错时曲线出现断口或折角
    # ==================================================================
    st.markdown("---")
    st.markdown(r"#### ✨ 交互复核：拖动 $a$、$b$，看曲线在 $x=1$ 处是否光滑衔接")
    st.info(r"把 $a$、$b$ 调成别的数，盯住 $x=1$ 处曲线的**断口**与**折角**："
            r"只有同时满足「连续」（$a+b=1$）和「左右导数相等」（$a=2$）时，两支曲线才会光滑接上。"
            r"这就是例 10「先由连续定一个参数、再由可导定另一个参数」的几何对照。")

    ca, cb = st.columns(2)
    with ca:
        a_t17 = st.slider("参数 a（习题 17 复核）", min_value=-3.0, max_value=4.0, value=3.0,
                          step=0.5, key="imp9_a")
    with cb:
        b_t17 = st.slider("参数 b（习题 17 复核）", min_value=-4.0, max_value=3.0, value=2.0,
                          step=0.5, key="imp9_b")

    lim_left = 1.0                 # lim(x→1⁻) x²  = 1
    lim_right = a_t17 + b_t17      # lim(x→1⁺)(ax+b) = a+b
    d_left = 2.0                   # f'_-(1) = 2
    d_right = a_t17                # f'_+(1) = a
    is_cont = abs(lim_left - lim_right) < 1e-9
    is_deriv = is_cont and abs(d_left - d_right) < 1e-9

    k1, k2, k3 = st.columns(3)
    k1.metric("左极限 / 右极限", f"{lim_left:.2f} / {lim_right:.2f}")
    k2.metric("左导数 / 右导数", f"{d_left:.2f} / {d_right:.2f}")
    k3.metric("当前取值", f"a = {a_t17:.1f}，b = {b_t17:.1f}")

    if is_deriv:
        st.success(f"✅ 光滑衔接：a = {a_t17:.1f}、b = {b_t17:.1f} 使 a + b = 1 且 a = 2，曲线在 x=1 处连续且可导，没有折角。")
    elif is_cont:
        st.warning(f"⚠️ 接上了但有折角：左右导数 {d_left:.1f} ≠ {d_right:.1f}，函数在 x=1 处连续但不可导。")
    else:
        st.error(f"❌ 连断口都没接上：左右极限 {lim_left:.2f} ≠ {lim_right:.2f}，函数在 x=1 处不连续，更谈不上可导。")

    fig17, ax17 = plt.subplots(figsize=(8, 5))
    fig17, ax17 = prep_fig(fig17, ax17)
    xl17 = np.linspace(-0.5, 1.0, 200)
    xr17 = np.linspace(1.0, 2.8, 200)
    ax17.plot(xl17, xl17 ** 2, linewidth=2.4, color='#1f77b4', label=r"$y=x^2\ (x\leq 1)$")
    ax17.plot(xr17, a_t17 * xr17 + b_t17, linewidth=2.4, color='#ff7f0e', linestyle='--',
              label=fr"$y={a_t17:.1f}x{b_t17:+.1f}\ (x>1)$")
    ax17.scatter([1.0], [1.0], color='black', s=110, zorder=5, edgecolor='white',
                 linewidth=1.2, label=r"分段点 $(1,1)$")
    ax17.axhline(0, color='gray', linewidth=0.8)
    ax17.axvline(0, color='gray', linewidth=0.8)
    ax17.grid(alpha=0.3, linestyle='--')
    ax17.legend(fontsize=10, loc='upper left')
    ax17.set_xlabel('x', fontsize=12)
    ax17.set_ylabel('y', fontsize=12)
    ax17.set_xlim(-0.5, 2.8)
    ax17.set_ylim(-3.0, 8.0)


    safe_pyplot(fig17, key="piecewise_q17")

    # ---------- 习题 18（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 18（分段函数单侧导数）")
    st.markdown(r"已知 $f(x)=\begin{cases}x^2,&x\ge0,\\-x,&x<0,\end{cases}$ 求 $f'_+(0)$ 与 $f'_-(0)$，又 $f'(0)$ 是否存在？")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $f'_-(0)=\lim_{x\to0^-}\frac{-x}{x}=-1$；
        $f'_+(0)=\lim_{x\to0^+}\frac{x^2}{x}=0$。
        左右导数不相等，故 **$f'(0)$ 不存在**。
        """)
    with st.expander("🐍 Python 代码（数值检验左右导数 + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.where(x>=0, x**2, -x)

h = 1e-7
fp_left  = (f(-h)-f(0))/(-h)
fp_right = (f(h)-f(0))/h
print(f"f'_-(0) ≈ {fp_left:.6f}  （理论=-1）")
print(f"f'_+(0) ≈ {fp_right:.6f}  （理论=0）")
print(f"左右差={abs(fp_left-fp_right):.6f}  → 不相等，f'(0) 不存在")

x = np.linspace(-1.5, 1.5, 400)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, f(x), linewidth=2, label=r"$f(x)$")
# 画两条"单侧切线"
ax.plot(x, 0*x, "r--", linewidth=1.5, label=r"右切线 $y=0$（斜率=0）")
ax.plot(x, -x,  "g--", linewidth=1.5, label=r"左切线 $y=-x$（斜率=-1）")
ax.scatter([0],[0], color="black", s=80, zorder=5)
ax.axhline(0,color="gray",lw=0.8); ax.axvline(0,color="gray",lw=0.8)
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)

plt.show()''', language="python")

    # ---------- 习题 19（奇数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 19（分段函数求导函数）")
    st.markdown(r"已知 $f(x)=\begin{cases}\sin x,&x<0,\\x,&x\ge0,\end{cases}$ 求 $f'(x)$。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        $f'_-(0)=\lim_{x\to0^-}\dfrac{\sin x}{x}=1$；$f'_+(0)=\lim_{x\to0^+}\dfrac{x}{x}=1$。
        故 $f'(0)=1$，从而
        $$f'(x)=\begin{cases}\cos x,&x<0,\\1,&x\ge0.\end{cases}$$
        """)
    with st.expander("🐍 Python 代码（数值验证 f'(0)=1 并绘制导函数）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return np.sin(x) if x < 0 else x

h = 1e-6
fl = (f(-h)-f(0))/(-h)
fr = (f(h)-f(0))/h
print(f"左导数 ≈ {fl:.6f}, 右导数 ≈ {fr:.6f}, 平均 ≈ {(fl+fr)/2:.6f}")

x = np.linspace(-np.pi, np.pi, 400)
fp = np.where(x<0, np.cos(x), 1.0)
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(x, fp, linewidth=2, color="#1f77b4", label=r"$f'(x)$")
ax.scatter([0],[1], color="red", s=100, zorder=5, label=r"$f'(0)=1$")
ax.axhline(0, color="gray", lw=0.8); ax.axvline(0, color="gray", lw=0.8)
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)

plt.show()''', language="python")

    # ---------- 习题 20（偶数·附代码）----------
    st.markdown("---")
    st.markdown("#### 习题 20（双曲线切线与坐标轴三角形面积）")
    st.markdown(r"证明：双曲线 $xy=a^2$ 上任一点处的切线与两坐标轴构成的三角形面积都等于 $2a^2$。")
    with st.expander("📖 答案与解析", expanded=False):
        st.markdown(r"""
        设切点 $(x_0,y_0)$，则 $y_0=\dfrac{a^2}{x_0}$。切线斜率 $k=-\dfrac{a^2}{x_0^2}$，
        切线方程为 $y-y_0=-\dfrac{a^2}{x_0^2}(x-x_0)$，整理为截距式 $\dfrac{x}{2x_0}+\dfrac{y}{2y_0}=1$。
        故切线在 x、y 轴上的截距分别为 $2x_0,\,2y_0$，所围三角形面积
        $$A=\frac12|2x_0|\cdot|2y_0|=2|x_0y_0|=2a^2.$$
        """)
    with st.expander("🐍 Python 代码（数值验证面积恒为 2a² + 绘图）", expanded=False):
        st.code(r'''import numpy as np
import matplotlib.pyplot as plt

a = 2.0                    # 取 a=2
print(f"取 a={a}, 则理论面积 2a² = {2*a**2}\n")

fig, ax = plt.subplots(figsize=(8,5))
x = np.linspace(0.2, 6, 400)
ax.plot(x, a**2/x, linewidth=2, label=fr"$xy=a^2\;(a={a})$")

for x0 in [1.0, 2.0, 3.0, 4.0]:
    y0 = a**2/x0
    k  = -a**2/(x0**2)     # 切线斜率
    # 截距
    x_intercept = 2*x0     # 与 x 轴交点
    y_intercept = 2*y0     # 与 y 轴交点
    area = 0.5*abs(x_intercept)*abs(y_intercept)
    print(f"切点 ({x0:.1f}, {y0:.2f}): x截距={x_intercept:.2f}, y截距={y_intercept:.2f}, 面积={area:.4f}")
    # 画切线
    tx = np.linspace(0.1, x_intercept+0.2, 100)
    ax.plot(tx, y0+k*(tx-x0), "--", linewidth=1.2, alpha=0.7)
    # 三角形填色
    tri_x = [0, x_intercept, 0, 0]
    tri_y = [0, 0, y_intercept, 0]
    ax.fill(tri_x, tri_y, alpha=0.12)
    ax.scatter([x0],[y0], s=50, zorder=5)

ax.set_xlim(0, 10); ax.set_ylim(0, 10)
ax.axhline(0,color="gray",lw=0.8); ax.axvline(0,color="gray",lw=0.8)
ax.grid(alpha=0.3, ls="--"); ax.legend(fontsize=11)
ax.set_aspect("equal")

plt.show()''', language="python")

    st.markdown("---")
    st.success("🎯 至此，习题 2-1 全部 20 题解答完毕。**所有题目均附可独立运行的 Python 代码**：奇数题侧重符号/绘图验证，偶数题侧重数值/定义验证；第 9 题提供 sympy 符号求导与纯 numpy 数值验证两种方法。可复制代码到本地运行，直观验证理论结果。")

# ============================================
# 第四部分：页脚
# ============================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>📐 导数的概念及其几何意义 · 大学交互式高等数学教学平台</div>",
    unsafe_allow_html=True
)