# Sci-Surf 网站视觉设计规范（v1.0）

> **品牌主张**：Surf the Scientific Frontier  
> **产品定位**：面向研究人员的 AI 驱动个性化科学论文发现与多模态内容消化平台  
> **交付用途**：品牌识别、网站界面设计、前端实现、Codex 开发交接  
> **设计来源**：由旧版 `SCI-Surf` 字标、论文主图和本次生成的网站视觉概念板综合整理。

## 1. 品牌核心方向

**设计关键词**：探索（Exploration）、发现（Discovery）、可信赖（Trust）、智能（Intelligence）、流动（Flow）、科学（Science）。

Sci-Surf 的形象不应是传统学术数据库那样沉重，也不应是泛 AI 工具那样过度炫技。它应同时传达两种气质：

1. **SCI — 科学严谨**：黑色、精练的科技字体，强调证据、可靠性与研究工具属性。
2. **Surf — 自由探索**：明亮蓝色的动势手写字体，强调跨论文探索、连续发现与阅读乐趣。

建议用**蓝白色的轻量化科研工作台**承载产品，将流线与“浪潮”仅用于品牌页和局部引导；论文、证据、推荐质量本身才是界面的视觉主角。

### 1.1 品牌口号

- 英文主口号：**Surf the Scientific Frontier**
- 首页价值主张（建议）：**Discover research that moves you forward.**
- 首页副标题（建议）：*Personalized scientific paper discovery and multimodal digests, powered by AI.*

## 2. Logo 规范

### 2.1 结构与含义

- `SCI-`：深灰/黑色，现代粗斜体无衬线，稳健、有科技感。
- `Surf`：明亮品牌蓝色，具有速度与流动感的手写笔触。
- 下划流线：象征 *surfing*、知识海洋和持续前进。
- 橙色细节：仅用于流线末端的小面积点睛，避免抢占主视觉。

### 2.2 使用规范

| 应用场景 | 建议宽度 | 说明 |
|---|---:|---|
| 顶部导航栏（桌面） | 136–164px | 使用横版透明背景 Logo |
| 顶部导航栏（移动端） | 112–136px | 保证 `SCI-` 和 `Surf` 均清晰可辨 |
| 首页 Hero / 宣传图 | 210–280px | 可搭配独立文字口号 |
| PPT、论文 Demo 截图 | 按版面适配 | 避免横向拉伸或压缩 |

- 默认置于白色或非常浅蓝色背景上。深色背景需要另做反白版，不建议直接复用含黑色文字的版本。
- Logo 四周保持至少 `SCI-` 字母高度约 1/3 的保护空间。
- 不添加额外阴影、描边、发光效果；不要改变笔画比例或主辅色位置。
- 将小尺寸 favicon 作为单独设计任务：**不能直接把整个横向字标挤进 16×16 图标**。

**交付素材**：`logo/Sci-Surf_Logo.png`、`logo/Sci-Surf_Logo_Transparent.png`。

## 3. 品牌色彩系统

整体比例建议：**白色/极浅色 70%｜蓝色系 20%｜深色文字 8%｜橙色 2%**。这是视觉比例建议，并非严格计算约束。

| 色彩角色 | 色值 | 主要用途 |
|---|---|---|
| Primary Blue | `#0A6FFF` | 主按钮、链接、选中态、重点关键词 |
| Light Blue | `#E6F2FF` | 卡片浅底、标签、Hover 背景、局部波纹 |
| White | `#FFFFFF` | 全局底色、核心内容面板 |
| Soft Gray | `#F3F6FA` | 页面分区、次级容器、弱背景 |
| Accent Orange | `#FF8A00` | 小面积提示、重要发现、品牌流线点睛 |
| Charcoal | `#111827` | 标题、正文高对比文字 |

补充实用色：

| 色彩角色 | 色值 | 主要用途 |
|---|---|---|
| Muted Text | `#596579` | 论文来源、日期、摘要等次级信息 |
| Border | `#DCE5EF` | 卡片描边、输入框、分隔线 |
| Hover Blue | `#005DD9` | 主按钮 Hover |
| Soft Orange | `#FFF2E2` | 少量暖色状态标签背景 |
| Focus Ring | `#80B7FF` | 焦点可见性、键盘导航 |

**应用原则**：

- 蓝色表示“可交互”和“系统品牌”，不要给每块卡片都涂蓝。
- 橙色负责提示“值得注意”，**不要**让橙色与蓝色在主按钮上竞争。
- 不要仅凭颜色表达相关性或状态；应同时使用文字、图标或评分解释。
- 论文正文和摘要用深色文本，避免浅蓝字配白底影响阅读。

## 4. 字体与排版

### 4.1 字体

- **界面英文**：`Inter`；备选 `Source Sans 3`、系统 sans-serif。
- **界面中文**：`PingFang SC`（macOS） / `Noto Sans SC` / 系统无衬线。
- **论文内容**：标题使用无衬线，论文原始英文摘要与公式按阅读需求排版。
- **品牌字体**：`Surf` 的手写笔触仅用于 Logo，不要把手写体应用到页面段落或按钮。

### 4.2 桌面字号建议

| 栏位 | 字号 | 字重 | 行高 |
|---|---:|---:|---:|
| 首页主标题 | 40–52px | 700 | 1.15 |
| 一级分区标题 | 24–30px | 650–700 | 1.3 |
| 卡片论文标题 | 17–20px | 600–650 | 1.4 |
| 标准正文 | 15–16px | 400 | 1.6 |
| 辅助信息 | 12–14px | 400–500 | 1.5 |
| 按钮/导航 | 14–15px | 550–650 | 1.3 |

建议文字内容区域宽度为 680–760px，以保障长段文献摘要和生成博客的可读性。

## 5. 布局与组件规范

### 5.1 布局

- 桌面内容最大宽度：`1200–1280px`，居中布局。
- 页面背景：白色为主，分区交替使用 `#F3F6FA`。
- 8px 间距系统：`4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px`。
- 面板圆角：`12–16px`；按钮圆角：`8–10px`；小标签圆角：`999px`。
- 卡片边框：`1px solid #DCE5EF`；阴影保持很浅，不能出现强悬浮质感。
- 桌面建议 3 列推荐卡片；平板 2 列；手机 1 列。

### 5.2 组件状态

**主按钮**：蓝底白字，Hover 使用深蓝；`Loading` 使用内置转圈指示；`Disabled` 降低饱和度并禁用点击。

**次按钮**：白底蓝色描边和蓝字，用于次级操作，如 `View Details`、`Edit Interests`。

**输入框**：白底、浅灰描边；聚焦时蓝色描边和明确 focus ring；长兴趣输入建议使用多行 textarea。

**论文卡片**：以**题名**为最强信息，摘要、发表日期、arXiv 来源、标签为次级信息；推荐理由 `Why this paper?` 和 `Read Digest` 作为核心交互。

**标签**：浅蓝背景、深色文字，用于研究方向；橙色仅用于“New Insight”等少量亮点状态。

**导航**：顶部保留品牌 Logo、Daily Feed、Explore、My Interests 等核心入口；不必把论文图中的所有内部 Pipeline 都当成主导航项。

## 6. 关键页面的视觉设计

### 6.1 首次使用 / Day 0 Onboarding

**目的**：把自然语言研究兴趣转化为可持续更新的研究兴趣档案。

建议页面结构：

1. 左侧品牌文案：`Tell us what you're curious about.`
2. 主要输入框：允许用户自由描述感兴趣的问题、方法、领域与应用场景。
3. 右侧轻量线稿/波纹插画：象征兴趣向论文网络扩散，不用复杂拟人卡通。
4. 提交后展示结构化研究兴趣 Profile，并允许用户修正。
5. 主要按钮：`Build My Research Profile`。

**视觉要点**：让自然语言输入成为首屏焦点；“理解兴趣”的 AI 能力应清楚但不过度拟人化。

### 6.2 Daily Feed / 每日个性化推荐

**目的**：快速判断“今天有哪些新论文值得读，为什么推荐给我”。

建议页面结构：

1. 顶部：`Your Daily Scientific Feed`、日期和研究兴趣摘要。
2. 推荐区：约 5 篇精选论文，以纵向列表或宽卡片优先，避免窄卡片造成标题拥挤。
3. 每篇显示题名、作者/来源、研究主题、1–2 句话推荐理由。
4. 操作：`Read Digest`、`View Paper`、收藏、相关/不相关反馈。
5. 侧边栏（可选）：用户兴趣 Profile 与更新入口。

**视觉要点**：推荐“理由”优先于纯装饰图；通过层级、留白和可扫描性体现专业性。

### 6.3 Paper Detail / 多模态博客消化

**目的**：从“读推荐”自然过渡到“理解研究”。

建议页面结构：

- 顶部论文信息：完整标题、作者、arXiv 链接、推荐理由。
- 主区域：博客式 Digest，使用章节标题、关键段落、论文原图/方法图及必要的引用链接。
- 右侧目录（桌面可选）：支持跳转与长文阅读。
- 底部：相关推荐、保存和反馈入口。

**视觉要点**：Digest 是可读的科研内容，不应做成营销海报；数学公式、图片、引用要清晰、可追溯。

### 6.4 Research Interest Profile / 研究兴趣管理

- 使用可编辑标签、主题组和自然语言描述组合展示兴趣。
- 允许用户主动修正 Profile 和删除不准确的研究方向。
- 用蓝色标识选中、灰色表示非重点；避免仅靠自动生成的热力图传达用户偏好。

## 7. 论文主图如何转化为网页设计语言

论文主图反映了三个重要模块，设计可保持同样的逻辑，但应该精简给终端用户：

| 论文主图/系统阶段 | 用户可见的表达 | 建议视觉元素 |
|---|---|---|
| Day 0 User Onboarding | Describe Your Interests | 输入框 + 蓝色兴趣标签 |
| Paper Content Processing | We Read and Organize New Papers | 文档 / 索引 / 图文信息图标 |
| Daily Recommendation | Discover Today's Papers | 推荐列表 + 相关性解释 |
| User Profile Verbalization | Your Interests Evolve | 柔和反馈循环箭头 |

首页 `How It Works` 只需 **3 步：Tell Us Your Interests → Discover Relevant Papers → Understand with AI Digests**。将检索、索引、全论文重排和用户反馈更新等技术实现留在论文 / About / 技术说明中。

## 8. 图形语言与交互动效

### 8.1 图形语言

- **Wave & Flow**：一到两条柔和的浅蓝波纹，主要用于 Hero、底部 Banner 和空状态。
- **Knowledge Cards**：论文图像、文档卡片与摘要块，直观对应产品价值。
- **Scientific Workflow**：扁平化圆角模块 + 细箭头，来自论文主图的工程逻辑。
- **Network & Data**：少量节点连线，表示主题关系与兴趣变化。

### 8.2 动效

- Hover：`120–180ms`，颜色变化 + 1–2px 轻微位移即可。
- 页面模块显示：`180–250ms` 的淡入，避免大幅弹跳。
- 可在 Hero 中使用极缓慢的背景波形，但优先保证性能。
- 必须尊重 `prefers-reduced-motion`。

## 9. 响应式、可访问性与工程约束

- 移动端断点参考：`<640px`；平板：`640–1023px`；桌面：`≥1024px`。
- 手机下导航折叠，推荐列表一列，正文保持舒适行距。
- 所有交互区域应保持足够点击面积，提供键盘 focus 状态和清楚的标签。
- 正文和功能性文字以 WCAG AA 文本对比度为设计目标；蓝底白字按钮要实际测量对比度。
- 论文内容可能很长：提供标题截断策略、摘要展开、图片 loading/placeholder 状态。
- 页面优先使用 SVG 图标和 CSS 波纹；不要以大张无语义背景图替代真实 UI。

## 10. 可直接交给前端的 CSS Tokens

```css
:root {
  --color-primary: #0A6FFF;
  --color-primary-hover: #005DD9;
  --color-primary-soft: #E6F2FF;
  --color-surface: #FFFFFF;
  --color-page-soft: #F3F6FA;
  --color-accent: #FF8A00;
  --color-accent-soft: #FFF2E2;
  --color-text: #111827;
  --color-text-muted: #596579;
  --color-border: #DCE5EF;
  --color-focus: #80B7FF;

  --font-ui: Inter, 'Source Sans 3', 'PingFang SC', 'Noto Sans SC', sans-serif;
  --radius-button: 10px;
  --radius-card: 14px;
  --radius-pill: 999px;
  --content-max: 1240px;
  --shadow-card: 0 4px 18px rgba(17, 24, 39, 0.045);
  --transition-ui: 160ms ease;
}

body {
  background: var(--color-surface);
  color: var(--color-text);
  font-family: var(--font-ui);
}

.sci-button-primary {
  border: 0;
  border-radius: var(--radius-button);
  background: var(--color-primary);
  color: #fff;
  font-weight: 600;
  padding: 11px 18px;
  transition: background var(--transition-ui);
}

.sci-button-primary:hover { background: var(--color-primary-hover); }
.sci-button-primary:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 2px;
}

.sci-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  box-shadow: var(--shadow-card);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
```

## 11. 建议实施顺序（前端 / Codex）

1. **P0 - Brand Foundation**：加载 Logo、导入配色 Tokens、字体、卡片、按钮、输入框样式；优先完成桌面和移动端顶部导航。
2. **P1 - Product Core**：改造 Day 0 兴趣输入、Daily Feed 列表、推荐理由和按钮层级。
3. **P2 - Reading Experience**：统一 Paper Detail / Multimodal Digest 的阅读宽度、论文图、来源和长文目录。
4. **P3 - Polish**：首页波纹图形、空状态、响应式微调、loading、动效和无障碍检查。

**验收建议**：在 1440px 桌面、1024px 平板、390px 手机三种宽度截屏比对；以信息是否容易扫描、用户能否理解推荐理由、论文 Digest 是否易读为首要标准，而不是与概念板逐像素相同。

## 12. 文件与说明

```text
Sci-Surf_Visual_Package/
├── Sci-Surf_Visual_Design_Guide.md        # 当前文本规范
├── logo/
│   ├── Sci-Surf_Logo.png                 # 新 Logo，白底高清原始图
│   └── Sci-Surf_Logo_Transparent.png     # 新 Logo，透明背景裁切版
├── design/
│   ├── Sci-Surf_Visual_Board.png         # 整体视觉概念板
│   └── Sci-Surf_Visual_Board.pdf         # 视觉概念板 PDF（可分享/打印）
└── reference/
    └── Sci-Surf_Paper_Main_Figure.png    # 用户提供的论文主图，供设计参照
```

> **边界说明**：PDF 是本次视觉概念板的排版版本，**不是完整 Sci-Surf 论文 PDF**。概念板内的示例标题、论文条目、标签属于 UI 示意，不应作为真实研究数据或实际产品功能的证明。色值与规范以本 Markdown 为准。
