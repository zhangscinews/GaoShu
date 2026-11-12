# -*- coding: utf-8 -*-
"""
导数的概念及其几何意义 - 交互式教学应用（NiceGUI 4.0 兼容版）
"""

# ============================================
# 第一部分：导入需要的工具库
# ============================================
from nicegui import ui, app
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import platform
import base64
from io import BytesIO

# ============================================
# 第二部分：配置基础样式与中文字体
# ============================================
def configure_chinese_font():
    system = platform.system()
    if system == "Windows":
        font_path = "C:/Windows/Fonts/simhei.ttf"
    elif system == "Darwin":
        font_path = "/System/Library/Fonts/PingFang.ttc"
    else:
        font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
    try:
        font_prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
    except:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Noto Sans CJK JP']
    plt.rcParams['axes.unicode_minus'] = False

configure_chinese_font()

ui.page_title("导数的概念及其几何意义 - 交互式教学")
ui.colors(primary='#1f77b4', secondary='#ff7f0e', accent='#2ecc71',
          positive='#27ae60', negative='#e74c3c', info='#3498db', warning='#f39c12')

# 注入 KaTeX + 自动渲染脚本
ui.add_head_html("""
<link rel="stylesheet" href="https://lf9-cdn-tos.bytecdntp.com/cdn/expire-100-y/KaTeX/0.16.9/katex.min.css">
<script defer src="https://lf9-cdn-tos.bytecdntp.com/cdn/expire-100-y/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://lf9-cdn-tos.bytecdntp.com/cdn/expire-100-y/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
function renderMath() {
    if (typeof renderMathInElement !== 'undefined') {
        renderMathInElement(document.body, {
            delimiters: [
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},
                {left: "\\\\[", right: "\\\\]", display: true},
                {left: "\\\\(", right: "\\\\)", display: false}
            ],
            throwOnError: false
        });
    }
}
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(renderMath, 500);
    const observer = new MutationObserver(function() { setTimeout(renderMath, 100); });
    observer.observe(document.body, {childList: true, subtree: true});
});
</script>
<style>
    .content-container { max-width: 1200px; margin: 0 auto; padding: 20px; }
    .metric-card { text-align: center; padding: 15px; border-radius: 8px; background: #f8f9fa; }
    .metric-value { font-size: 1.8em; font-weight: bold; color: #1f77b4; }
    .metric-label { font-size: 0.9em; color: #666; }
</style>
""")

# ============================================
# 辅助函数
# ============================================
def mkd(text: str):
    return ui.markdown(text, extras=['latex']).classes("text-base leading-relaxed")

def show_plot(fig):
    """兼容性最好的显示方式：将 matplotlib 转 base64 并用 ui.image 显示"""
    plt.tight_layout()
    buf = BytesIO()
    # dpi=130 保证图片清晰度
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=130)
    base64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # 限制最大宽度，居中显示
    ui.image(f'data:image/png;base64,{base64_data}').classes('w-full max-w-2xl mx-auto')
    plt.close(fig)

# 主容器
main_container = ui.column().classes("content-container w-full")

def clear_main_content():
    main_container.clear()

# ============================================
# 第三部分：页面渲染函数
# ============================================

# 0. 课程导入
def render_page0():
    clear_main_content()
    with main_container:
        ui.markdown("# 📖 导数的概念及其几何意义").classes("text-3xl font-bold")
        ui.markdown("## —— 大学高等数学 · 第二章第一节").classes("text-xl text-gray-600")
        ui.separator()

        ui.markdown("### 一、课程导入：两个经典问题").classes("text-xl font-semibold mt-4")
        mkd("导数这个概念，来源于17世纪科学研究中两个完全不同的问题：**变速直线运动的瞬时速度** 和 **平面曲线的切线斜率**。")

        with ui.grid(columns=2).classes("gap-6 mt-4 w-full"):
            with ui.card().classes("p-5 w-full"):
                ui.markdown("#### 问题1：变速直线运动的瞬时速度").classes("text-lg font-semibold")
                mkd(r"""
设物体做直线运动，位置随时间变化的函数为 $s = s(t)$：

1. 从 $t_0$ 到 $t_0+\Delta t$，物体走过的路程：$\Delta s = s(t_0+\Delta t) - s(t_0)$
2. 这段时间的**平均速度**：
$$\bar{v} = \frac{\Delta s}{\Delta t} = \frac{s(t_0+\Delta t) - s(t_0)}{\Delta t}$$
3. 当时间间隔 $\Delta t \to 0$ 时，平均速度无限接近 $t_0$ 时刻的**瞬时速度**：
$$v(t_0) = \lim_{\Delta t \to 0}\frac{\Delta s}{\Delta t} = \lim_{\Delta t \to 0}\frac{s(t_0+\Delta t) - s(t_0)}{\Delta t}$$
""")
                ui.separator()
                mkd("🚩 这是历史上牛顿研究导数的出发点：描述运动的瞬时变化率。")

            with ui.card().classes("p-5 w-full"):
                ui.markdown("#### 问题2：平面曲线的切线斜率").classes("text-lg font-semibold")
                mkd(r"""
给定曲线 $y=f(x)$，求在点 $M(x_0, f(x_0))$ 处的切线斜率：

1. 在曲线上另取一点 $N(x_0+\Delta x, f(x_0+\Delta x))$
2. 割线 $MN$ 的斜率：
$$k_{\text{割}} = \frac{\Delta y}{\Delta x} = \frac{f(x_0+\Delta x) - f(x_0)}{\Delta x}$$
3. 当 $N$ 沿曲线无限靠近 $M$（即 $\Delta x \to 0$）时，割线斜率的极限就是**切线斜率**：
$$k_{\text{切}} = \lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0}\frac{f(x_0+\Delta x) - f(x_0)}{\Delta x}$$
""")
                ui.separator()
                mkd("🚩 这是莱布尼茨研究导数的出发点：描述曲线的陡峭程度。")

        with ui.card().classes("p-4 bg-green-50 border-l-4 border-green-500 w-full mt-4"):
            mkd("""🎯 **本质发现**：两个完全不同的问题，最终都归结为同一个数学结构——
**函数增量与自变量增量之比，当自变量增量趋于0时的极限**。这就是今天要学的**导数**。""").classes("text-lg")

# 1. 导数的定义
def render_page1():
    clear_main_content()
    with main_container:
        ui.markdown("# 1. 导数的定义").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 一、严格定义").classes("text-xl font-semibold mt-4")
        mkd(r"""
设函数 $y=f(x)$ 在点 $x_0$ 的某邻域内有定义，当自变量 $x$ 在 $x_0$ 处取得增量 $\Delta x$ 时，
相应的函数增量为 $\Delta y = f(x_0+\Delta x) - f(x_0)$。如果极限

$$\lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x} = \lim_{\Delta x \to 0}\frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}$$

存在，则称函数 $y=f(x)$ 在点 $x_0$ 处**可导**，并称这个极限值为函数在点 $x_0$ 处的导数，记作：

$$f'(x_0),\quad y'\big|_{x=x_0},\quad \frac{dy}{dx}\big|_{x=x_0},\quad \frac{df}{dx}\big|_{x=x_0}$$
""")

        ui.markdown("### 二、导数定义的两种等价写法").classes("text-xl font-semibold mt-6")
        with ui.grid(columns=2).classes("gap-6 w-full"):
            with ui.card().classes("p-5 w-full"):
                mkd("**增量形式（最常用）：**")
                mkd(r"$$f'(x_0) = \lim_{h \to 0}\frac{f(x_0+h)-f(x_0)}{h}$$")
            with ui.card().classes("p-5 w-full"):
                mkd("**端点形式（常用于单侧导数）：**")
                mkd(r"$$f'(x_0) = \lim_{x \to x_0}\frac{f(x)-f(x_0)}{x-x_0}$$")

        ui.markdown("### 三、用定义求导数的三步法").classes("text-xl font-semibold mt-6")
        with ui.card().classes("p-4 bg-blue-50 border-l-4 border-blue-500 w-full"):
            mkd(r"""
📝 求导三步口诀：**一差、二比、三极限**

1. 求增量：$\Delta y = f(x_0+\Delta x)-f(x_0)$
2. 算比值：$\displaystyle \frac{\Delta y}{\Delta x} = \frac{f(x_0+\Delta x)-f(x_0)}{\Delta x}$
3. 取极限：$\displaystyle f'(x_0) = \lim_{\Delta x \to 0}\frac{\Delta y}{\Delta x}$
""").classes("text-lg")

        ui.markdown("### 四、导数的本质含义").classes("text-xl font-semibold mt-6")
        mkd(r"""
导数 $f'(x_0)$ 的本质，就是函数在 $x_0$ 处的**瞬时变化率**：

- 物理意义：瞬时速度、瞬时加速度、电流强度等；
- 几何意义：曲线在该点的切线斜率；
- 经济意义：边际成本、边际收益；
- 任何"变化快慢"的问题，最终都是导数问题。
""")

# 2. 用定义求导数例题
def render_page2():
    clear_main_content()
    with main_container:
        ui.markdown("# 2. 例题：用定义求导数").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 例1：求常函数的导数").classes("text-xl font-semibold mt-4")
        mkd("求函数 $f(x) = C$（$C$ 为常数）的导数。")
        with ui.expansion("点击查看解题过程").classes("w-full"):
            mkd(r"""
1. 求增量：$\Delta y = f(x+h)-f(x) = C - C = 0$
2. 算比值：$\displaystyle \frac{\Delta y}{h} = \frac{0}{h} = 0$
3. 取极限：$\displaystyle f'(x) = \lim_{h\to 0}\frac{\Delta y}{h} = 0$

**结论**：常数的导数等于0，即 $(C)' = 0$。
""")

        ui.separator().classes("my-6")
        ui.markdown("### 例2：求幂函数 $f(x)=x^2$ 的导数").classes("text-xl font-semibold mt-4")
        with ui.expansion("点击查看解题过程").classes("w-full"):
            mkd(r"""
1. 求增量：$\Delta y = (x+h)^2 - x^2 = 2xh + h^2$
2. 算比值：$\displaystyle \frac{\Delta y}{h} = \frac{2xh+h^2}{h} = 2x + h$
3. 取极限：$\displaystyle f'(x) = \lim_{h\to 0}(2x+h) = 2x$

**结论**：$(x^2)' = 2x$。推广：$(x^n)' = nx^{n-1}$。
""")

        ui.separator().classes("my-6")
        ui.markdown("### 例3：求正弦函数 $f(x)=\\sin x$ 的导数").classes("text-xl font-semibold mt-4")
        with ui.expansion("点击查看解题过程").classes("w-full"):
            mkd(r"""
1. 求增量：$\Delta y = \sin(x+h) - \sin x = 2\cos\left(x+\frac{h}{2}\right)\sin\frac{h}{2}$
2. 算比值：$\displaystyle \frac{\Delta y}{h} = \cos\left(x+\frac{h}{2}\right)\cdot\frac{\sin(h/2)}{h/2}$
3. 取极限：利用 $\lim_{t\to 0}\frac{\sin t}{t}=1$，得 $f'(x) = \cos x$

**结论**：$(\sin x)' = \cos x$，同理 $(\cos x)' = -\sin x$。
""")

        with ui.card().classes("p-4 bg-yellow-50 border-l-4 border-yellow-500 w-full mt-6"):
            mkd(r"""
⚠️ **注意**：用定义求导是基础方法，后续会学求导公式表，做题时直接用公式即可，不用每次都走三步法。
但三步法是理解导数概念的核心，考试常考分段函数在分界点的导数，必须用定义计算。
""")

# 3. 单侧导数与导函数
def render_page3():
    clear_main_content()
    with main_container:
        ui.markdown("# 3. 单侧导数与导函数").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 一、左导数与右导数").classes("text-xl font-semibold mt-4")
        mkd(r"""
导数是一个双侧极限，因此可以定义单侧导数：

- **左导数**：$\displaystyle f'_-(x_0) = \lim_{h \to 0^-}\frac{f(x_0+h)-f(x_0)}{h}$
- **右导数**：$\displaystyle f'_+(x_0) = \lim_{h \to 0^+}\frac{f(x_0+h)-f(x_0)}{h}$

函数在某点可导的**充要条件**是：左导数和右导数都存在且相等：

$$f'(x_0)\text{ 存在} \iff f'_-(x_0) = f'_+(x_0)$$
""")
        with ui.card().classes("p-4 bg-blue-50 border-l-4 border-blue-500 w-full"):
            ui.label("🚩 这个充要条件主要用于判断分段函数在分界点处是否可导。")

        ui.markdown("### 二、导函数").classes("text-xl font-semibold mt-6")
        mkd(r"""
如果函数 $y=f(x)$ 在开区间 $I$ 内每一点都可导，就称 $f(x)$ 在 $I$ 内可导。
这时对任意 $x\in I$，都对应一个确定的导数值 $f'(x)$，这就构成了一个新的函数，
称为**导函数**（简称导数），记作：

$$y',\quad f'(x),\quad \frac{dy}{dx},\quad \frac{df(x)}{dx}$$

⚠️ 注意区分：

- $f'(x_0)$ 是一个**具体的数**，表示在 $x_0$ 点的导数值；
- $f'(x)$ 是一个**函数**，是 $f(x)$ 的导函数。
- 关系：$f'(x_0) = f'(x)\big|_{x=x_0}$
""")

# 4. 可导与连续的关系
def render_page4():
    clear_main_content()
    with main_container:
        ui.markdown("# 4. 可导与连续的关系").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 核心定理").classes("text-xl font-semibold mt-4")
        with ui.card().classes("p-4 bg-green-50 border-l-4 border-green-500 w-full"):
            mkd("**定理**：如果函数 $y=f(x)$ 在点 $x_0$ 处可导，则函数在该点必连续。").classes("text-lg")

        ui.markdown("### 证明过程").classes("text-xl font-semibold mt-4")
        mkd(r"""
已知 $f(x)$ 在 $x_0$ 处可导，即极限

$$\lim_{\Delta x\to 0}\frac{\Delta y}{\Delta x} = f'(x_0)$$

存在。根据极限与无穷小的关系：

$$\frac{\Delta y}{\Delta x} = f'(x_0) + \alpha, \quad \text{其中}\ \alpha\to 0\ (\Delta x\to 0)$$

两边同乘 $\Delta x$ 得：

$$\Delta y = f'(x_0)\Delta x + \alpha\cdot\Delta x$$

当 $\Delta x\to0$ 时，$\Delta y\to0$，根据连续的定义，函数在 $x_0$ 处连续。
""")

        ui.markdown("### 注意：反之不成立！").classes("text-xl font-semibold mt-6")
        with ui.card().classes("p-4 bg-red-50 border-l-4 border-red-500 w-full"):
            mkd(r"""
❌ 连续**不一定**可导！函数在某点连续是可导的**必要不充分条件**。

典型反例：

1. **尖点反例**：$f(x) = |x|$ 在 $x=0$ 处连续，但左导数=-1，右导数=1，不相等，因此不可导；
2. **垂直切线反例**：$f(x) = \sqrt[3]{x}$ 在 $x=0$ 处连续，但导数为无穷大，切线垂直于x轴，不可导。
""").classes("text-lg")

        with ui.grid(columns=2).classes("gap-6 mt-6 w-full"):
            with ui.card().classes("p-4 w-full"):
                fig1, ax1 = plt.subplots(figsize=(5, 4))
                x1 = np.linspace(-2, 2, 200)
                y1 = np.abs(x1)
                ax1.plot(x1, y1, linewidth=2, color='#1f77b4')
                ax1.scatter(0, 0, color='red', zorder=5, s=50)
                ax1.set_title('反例1: f(x)=|x| 在x=0处尖点不可导', fontsize=12)
                ax1.grid(alpha=0.3)
                ax1.set_aspect('equal')
                show_plot(fig1)

            with ui.card().classes("p-4 w-full"):
                fig2, ax2 = plt.subplots(figsize=(5, 4))
                x2 = np.linspace(-2, 2, 200)
                y2 = np.cbrt(x2)
                ax2.plot(x2, y2, linewidth=2, color='#ff7f0e')
                ax2.axvline(x=0, color='red', linestyle='--', label='垂直切线')
                ax2.scatter(0, 0, color='red', zorder=5, s=50)
                ax2.set_title('反例2: f(x)=∛x 在x=0处垂直切线不可导', fontsize=12)
                ax2.grid(alpha=0.3)
                ax2.set_aspect('equal')
                ax2.legend()
                show_plot(fig2)

# 5. 几何意义：割线变切线（核心交互环节）
def render_page5():
    clear_main_content()
    with main_container:
        ui.markdown("# 5. 导数的几何意义：割线逼近切线 ✨").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 一、几何意义核心结论").classes("text-xl font-semibold mt-4")
        with ui.card().classes("p-4 bg-green-50 border-l-4 border-green-500 w-full"):
            mkd(r"""
函数 $y=f(x)$ 在点 $x_0$ 处的导数 $f'(x_0)$，在几何上表示**曲线 $y=f(x)$ 在点 $M(x_0,f(x_0))$ 处的切线斜率**：

$$k_{\text{切}} = f'(x_0) = \tan\alpha$$

其中 $\alpha$ 是切线与x轴正方向的夹角。
""").classes("text-lg")

        ui.markdown("### 二、交互演示：拖动滑块看割线如何变成切线").classes("text-xl font-semibold mt-4")
        with ui.card().classes("p-4 bg-blue-50 border-l-4 border-blue-500 w-full"):
            ui.label("💡 拖动下方的Δx滑块，让N点靠近M点，观察割线斜率如何逼近切线斜率：")

        with ui.card().classes("p-4 w-full"):
            with ui.grid(columns=3).classes("gap-4 w-full"):
                with ui.column().classes("w-full"):
                    ui.label("选择演示函数").classes("text-sm text-gray-600")
                    func_choice = ui.select(
                        ["f(x) = x²（抛物线）", "f(x) = sin(x)（正弦曲线）", "f(x) = x³（三次曲线）"],
                        value="f(x) = x²（抛物线）"
                    ).classes("w-full")
                with ui.column().classes("w-full"):
                    ui.label("定点M的横坐标 x₀").classes("text-sm text-gray-600")
                    x0_slider = ui.slider(min=-1.5, max=1.5, value=1.0, step=0.1).props('label-always').classes("w-full")
                with ui.column().classes("w-full"):
                    ui.label("Δx（N点与M点的水平距离）").classes("text-sm text-gray-600")
                    delta_x_slider = ui.slider(min=0.01, max=2.0, value=1.0, step=0.01).props('label-always').classes("w-full")

        plot_container = ui.card().classes("p-4 w-full")
        metric_container = ui.grid(columns=3).classes("gap-4 mt-4 w-full")

        def update_plot(e=None):
            func = func_choice.value
            x0 = x0_slider.value
            delta_x = delta_x_slider.value

            if func == "f(x) = x²（抛物线）":
                f = lambda x: x ** 2
                f_prime = lambda x: 2 * x
            elif func == "f(x) = sin(x)（正弦曲线）":
                f = lambda x: np.sin(x)
                f_prime = lambda x: np.cos(x)
            else:
                f = lambda x: x ** 3
                f_prime = lambda x: 3 * x ** 2

            y0 = f(x0)
            slope_tangent = f_prime(x0)
            x_N = x0 + delta_x
            y_N = f(x_N)
            slope_secant = (y_N - y0) / delta_x

            plot_container.clear()
            with plot_container:
                fig, ax = plt.subplots(figsize=(8, 5))

                if func == "f(x) = x³（三次曲线）":
                    x_plot = np.linspace(-2, 2.5, 500)
                else:
                    x_plot = np.linspace(-2.5, 3.5, 500)

                ax.plot(x_plot, f(x_plot), linewidth=2.2, label=r"曲线 $y=f(x)$", color='#1f77b4')

                x_sec = np.linspace(x0 - 0.8, x_N + 0.8, 100)
                y_sec = y0 + slope_secant * (x_sec - x0)
                ax.plot(x_sec, y_sec, color='orange', linestyle='--', linewidth=2.2,
                        label=fr"割线MN，斜率 $k={slope_secant:.3f}$")

                x_tan = np.linspace(x0 - 2.5, x0 + 2.5, 100)
                y_tan = y0 + slope_tangent * (x_tan - x0)
                ax.plot(x_tan, y_tan, color='red', linewidth=2.2,
                        label=fr"切线，斜率 $k={slope_tangent:.3f}$")

                ax.scatter(x0, y0, color='red', s=120, zorder=5, edgecolor='white', linewidth=1.2,
                           label=fr"M点 $({x0:.1f}, {y0:.2f})$")
                ax.scatter(x_N, y_N, color='orange', s=120, zorder=5, edgecolor='white', linewidth=1.2,
                           label=fr"N点 $({x_N:.2f}, {y_N:.2f})$")

                ax.plot([x0, x_N], [y0, y0], 'k--', alpha=0.6, linewidth=1.2)
                ax.plot([x_N, x_N], [y0, y_N], 'k--', alpha=0.6, linewidth=1.2)
                ax.annotate(r'$\Delta x$', ((x0 + x_N) / 2, y0 - 0.2), fontsize=13, ha='center')
                ax.annotate(r'$\Delta y$', (x_N + 0.1, (y0 + y_N) / 2), fontsize=13, va='center')

                ax.axhline(0, color='gray', linewidth=0.8)
                ax.axvline(0, color='gray', linewidth=0.8)
                ax.grid(alpha=0.3, linestyle='--')
                ax.legend(fontsize=11, loc='upper left')

                all_y = np.concatenate([f(x_plot), y_sec, y_tan, [y0 - 1, y_N + 1]])
                ax.set_ylim(bottom=np.min(all_y) - 0.5, top=np.max(all_y) + 0.5)
                ax.set_xlim(np.min(x_plot) - 0.2, np.max(x_plot) + 0.2)
                ax.set_xlabel('x', fontsize=12)
                ax.set_ylabel('y', fontsize=12)
                show_plot(fig)

            metric_container.clear()
            with metric_container:
                with ui.card().classes("metric-card"):
                    ui.label("当前Δx大小").classes("metric-label")
                    ui.label(f"{delta_x:.2f}").classes("metric-value")
                with ui.card().classes("metric-card"):
                    ui.label("割线斜率").classes("metric-label")
                    ui.label(f"{slope_secant:.3f}").classes("metric-value")
                with ui.card().classes("metric-card"):
                    ui.label("切线斜率（精确导数值）").classes("metric-label")
                    ui.label(f"{slope_tangent:.3f}").classes("metric-value")
                    ui.label(f"差值：{slope_secant - slope_tangent:+.3f}").classes("text-sm text-gray-600")

        func_choice.on('update:modelValue', update_plot)
        x0_slider.on('update:modelValue', update_plot)
        delta_x_slider.on('update:modelValue', update_plot)
        update_plot()

        ui.separator().classes("my-6")
        with ui.card().classes("p-4 bg-blue-50 border-l-4 border-blue-500 w-full"):
            mkd(r"""
🎯 **观察发现**：当 $\Delta x$ 越接近0，割线斜率和切线斜率的差值就越接近0，割线最终与切线重合。
这就是导数几何意义的动态过程——**切线是割线的极限位置**。
""").classes("text-lg")

# 6. 切线与法线方程
def render_page6():
    clear_main_content()
    with main_container:
        ui.markdown("# 6. 切线方程与法线方程").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 一、公式").classes("text-xl font-semibold mt-4")
        mkd(r"""
根据导数的几何意义，曲线 $y=f(x)$ 在点 $M(x_0,y_0)$ 处：

1. **切线方程**（过点M，斜率为 $f'(x_0)$）：
$$y - y_0 = f'(x_0)(x - x_0)$$

2. **法线方程**（过点M，与切线垂直，斜率为 $-1/f'(x_0)$，当 $f'(x_0)\neq0$ 时）：
$$y - y_0 = -\frac{1}{f'(x_0)}(x - x_0)$$

特殊情况：

- 若 $f'(x_0)=0$，切线水平 $y=y_0$，法线垂直 $x=x_0$；
- 若 $f'(x_0)=\infty$，切线垂直 $x=x_0$，法线水平 $y=y_0$。
""")

        ui.markdown("### 二、例题").classes("text-xl font-semibold mt-6")
        mkd(r"求抛物线 $y=x^2$ 在点 $(1,1)$ 处的切线方程和法线方程。")
        with ui.expansion("点击查看解答").classes("w-full"):
            mkd(r"""
**解**：首先求导：$f'(x)=2x$，因此在 $x=1$ 处导数 $f'(1)=2$。

- 切线方程：$y - 1 = 2(x - 1)$，即 $y = 2x - 1$
- 法线方程：$y - 1 = -\frac{1}{2}(x - 1)$，即 $y = -\frac{1}{2}x + \frac{3}{2}$
""")

            fig, ax = plt.subplots(figsize=(6, 5))
            x = np.linspace(-2, 4, 400)
            ax.plot(x, x ** 2, label=r"$y = x^2$", linewidth=2, color='#1f77b4')
            ax.plot(x, 2 * x - 1, label=r"切线 $y = 2x - 1$", color='red', linewidth=2)
            ax.plot(x, -0.5 * x + 1.5, label=r"法线 $y = -\frac{1}{2}x + \frac{3}{2}$", color='green', linewidth=2)
            ax.scatter(1, 1, color='black', s=120, zorder=5, edgecolor='white', linewidth=1.2)

            ax.set_xlim(-2, 4)
            ax.set_ylim(-2, 4)
            ax.axhline(0, color='gray', linewidth=0.8)
            ax.axvline(0, color='gray', linewidth=0.8)
            ax.grid(alpha=0.3, linestyle='--')
            ax.legend(fontsize=11, loc='upper left')
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('y', fontsize=12)
            ax.set_title(r'抛物线 $y=x^2$ 在点 $(1,1)$ 处的切线与法线', fontsize=13)
            show_plot(fig)

# 7. 课堂小结与练习
def render_page7():
    clear_main_content()
    with main_container:
        ui.markdown("# 7. 课堂小结与课堂练习").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 一、本节课核心知识点总结").classes("text-xl font-semibold mt-4")
        mkd(r"""
1. **一个定义**：导数是函数增量与自变量增量之比的极限，本质是瞬时变化率；
2. **一个方法**：用定义求导三步法——一差、二比、三极限；
3. **一个充要条件**：某点可导 ⇨ 左右导数存在且相等；
4. **一个关系**：可导必连续，连续不一定可导；
5. **一个几何意义**：导数是切线斜率，切线是割线的极限位置；
6. **两个方程**：切线方程、法线方程公式。
""")

        ui.markdown("### 二、课堂小练习").classes("text-xl font-semibold mt-6")

        ui.label("1. 函数f(x)在x₀处连续是在该点可导的（  ）").classes("font-semibold")
        q1 = ui.radio(
            ["A. 充分但不必要条件", "B. 必要但不充分条件", "C. 充分必要条件", "D. 既不充分也不必要条件"],
            value=None
        )
        q1_result = mkd("")
        def check_q1():
            if q1.value == "B. 必要但不充分条件":
                q1_result.set_content("✅ 回答正确！可导必连续，连续不一定可导。")
                q1_result.classes("text-lg text-green-600 font-semibold")
            elif q1.value is not None:
                q1_result.set_content("❌ 不对哦，回忆可导与连续的关系定理。")
                q1_result.classes("text-lg text-red-600 font-semibold")
        q1.on('update:modelValue', lambda e: check_q1())

        ui.separator().classes("my-4")

        ui.label("2. 函数f(x)=|x|在x=0处（  ）").classes("font-semibold")
        q2 = ui.radio(
            ["A. 连续且可导", "B. 连续但不可导", "C. 不连续但可导", "D. 不连续也不可导"],
            value=None
        )
        q2_result = mkd("")
        def check_q2():
            if q2.value == "B. 连续但不可导":
                q2_result.set_content("✅ 回答正确！f(x)=|x|在0点是尖点，左右导数不相等，不可导。")
                q2_result.classes("text-lg text-green-600 font-semibold")
            elif q2.value is not None:
                q2_result.set_content("❌ 不对哦，回忆我们讲过的尖点反例。")
                q2_result.classes("text-lg text-red-600 font-semibold")
        q2.on('update:modelValue', lambda e: check_q2())

        ui.separator().classes("my-4")

        ui.label("3. 用定义求 f(x)=x³ 在 x=1 处的导数 f'(1) = ?（输入数字即可）").classes("font-semibold")
        q3 = ui.input()
        q3_result = mkd("")
        def check_q3():
            if q3.value and q3.value.strip() == "3":
                q3_result.set_content("✅ 回答正确！f'(x)=3x²，因此 f'(1)=3。")
                q3_result.classes("text-lg text-green-600 font-semibold")
            elif q3.value:
                q3_result.set_content("❌ 答案是3，回忆幂函数求导公式或用三步法计算。")
                q3_result.classes("text-lg text-red-600 font-semibold")
        q3.on('update:modelValue', lambda e: check_q3())

# 8. 完整讲稿与板书
def render_page8():
    clear_main_content()
    with main_container:
        ui.markdown("# 🗒️ 完整讲稿与板书设计").classes("text-3xl font-bold")
        ui.separator()

        ui.markdown("### 板书总布局（三栏式黑板）").classes("text-xl font-semibold mt-4")
        ui.markdown("""
| 左侧副板书区（图形/草稿） | 中心主板书区（保留全课） | 右侧副板书区（例题演算） |
|--------------------------|--------------------------|--------------------------|
| 割线→切线示意图<br>反例图像 | 一、导数定义<br>二、三步求导法<br>三、单侧导数/导函数<br>四、可导与连续关系<br>五、几何意义<br>六、切线法线方程 | 例题1-3演算过程<br>学生提问草稿 |
""")

        ui.markdown("### 开场讲稿").classes("text-xl font-semibold mt-6")
        mkd(r"""
> "同学们好，今天我们开始学导数。大家有没有想过，坐高铁的时候，仪表盘显示的'时速300公里'到底是什么？如果我说你在某一个'瞬间'的速度，那这个瞬间时间长度是0啊，路程除以0怎么会有意义？这就是当年牛顿研究的问题——瞬时速度，也就是我们今天导数的来源。"
""")

        ui.markdown("### 核心环节讲稿").classes("text-xl font-semibold mt-6")
        mkd(r"""
> "大家看屏幕上的这个交互演示：当N点离M很远的时候，割线很陡；你拖动滑块让N一点点靠近M，割线就会绕着M点转，最后稳定在一个位置——这个位置就是切线。这个转动过程中，割线斜率的极限，就是导数。所以导数不是什么神秘的东西，它就是割线斜率的极限，就是切线的斜率。"
""")
        mkd(r"""
> "大家一定要记住：可导一定连续，但连续不一定可导。就像 $|x|$ 那个尖点，图形是连在一起的，但是在尖点那里，左边斜率是 -1，右边斜率是 1，左边和右边对不上，所以这一点就没有切线，也就不可导。"
""")

# ============================================
# 第四部分：布局搭建
# ============================================
page_options = [
    ("0. 课程导入：两个经典问题", render_page0),
    ("1. 导数的定义", render_page1),
    ("2. 用定义求导数例题", render_page2),
    ("3. 单侧导数与导函数", render_page3),
    ("4. 可导与连续的关系", render_page4),
    ("5. 几何意义：割线变切线✨", render_page5),
    ("6. 切线与法线方程", render_page6),
    ("7. 课堂小结与练习", render_page7),
    ("🗒️ 完整讲稿与板书", render_page8),
]

def on_page_change(e):
    for name, fn in page_options:
        if name == e.value:
            fn()
            break

with ui.left_drawer(fixed=True).classes("p-4 bg-gray-50"):
    ui.markdown("## 📚 课程导航").classes("text-xl font-bold mb-4")
    radio = ui.radio(
        [opt[0] for opt in page_options],
        value=page_options[0][0],
        on_change=on_page_change, 
    ).classes("w-full")
    
    ui.separator().classes("my-4")
    with ui.card().classes("p-3 bg-blue-50 text-sm w-full"):
        ui.label("💡 使用提示：")
        ui.label("1. 左侧切换教学环节")
        ui.label("2. 带✨的环节有交互滑块，可以拖动参数看动态效果")
        ui.label("3. 所有公式支持自动渲染，和教材一致")
        ui.label("4. 讲稿与板书可在最后一页查看完整内容")

with ui.footer().classes("bg-gray-100 p-4 text-center text-gray-600"):
    ui.label("📐 导数的概念及其几何意义 · 大学高等数学交互式教学应用")

# 默认加载第一页
render_page0()

# ============================================
# 第五部分：启动应用
# ============================================
if __name__ in {"__main__", "__mp_main__"}:
    from nicegui import native
    ui.run(
        title="导数的概念及其几何意义 - 交互式教学",
        port=native.find_open_port(),   # 自动找空闲端口，避免 8080 被占用
        reload=False,                   # 打包时必须关闭热重载
        show=False,                     # native 模式下无需自动开浏览器
        #native=True,                    # 启用原生桌面窗口（配合 --windowed）
        window_size=(1200, 800),
        language="zh-CN",
    )