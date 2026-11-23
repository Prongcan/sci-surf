# Sci-Surf 前端最小品牌迁移计划（v2.0）

> 仓库：<https://github.com/Algnite-Solutions/PaperIgnitionV1>  
> 日期：2026-11-23  
> 目标：**只修改 Logo（包括明/暗色版本与 favicon）、品牌配色及用户可见的 PaperIgnition 名称**；不改布局、不改交互、不改业务逻辑、不做 UI 重设计。  
> 本版根据四项实施反馈更新：Logo 尺寸/暗色版、统一 Hover 蓝、favicon 纳入交付、点赞态的浅红背景修复。

## 1. 范围确认

| 事项 | 本次是否修改 | 边界 |
| --- | --- | --- |
| Header 品牌 Logo | **是** | 原文字 Logo 替换成图片；保留首页链接和 Header 高度 |
| Logo 暗色版 | **是** | 同一字标，仅 `SCI-` 黑色改白色；不重新设计 Logo |
| favicon | **是** | 属于 Logo 品牌识别更新；制作独立的小尺寸符号，不缩放横向字标 |
| 全局品牌色 | **是** | 品牌红改蓝；保持蓝/白为主，橙和黑仅作为已有品牌元素的点缀 |
| 点赞激活背景 | **是** | 单点修复蓝字配红底；仅调整颜色 |
| 前端品牌文字 | **是** | 用户可见的 `PaperIgnition` / `Paper Ignition` → `Sci-Surf` |
| 布局、字号体系、导航、动画、交互、路由 | **否** | 保持现状；仅 Logo 的自然尺寸随素材调整 |
| 后端、orchestrator、API、数据库、环境变量、包名、存储键 | **否** | 保留内部 `paperignition` 技术标识 |
| 全量网站视觉概念板 | **否** | 不依据之前的概念图改版 |

## 2. 锁定品牌色（唯一值）

本次以现有《Sci-Surf 网站视觉设计规范（v1.0）》为准，统一使用如下色值：

| 角色 | 色值 | 用途 |
| --- | --- | --- |
| Primary Blue | `#0A6FFF` | 全局主品牌色、`Surf` 字标 |
| **Hover Blue** | **`#005DD9`** | **唯一的品牌 Hover / Dark Blue**；废弃旧计划的 `#0059D6` |
| Light Blue | `#E6F2FF` | 已点赞等既有品牌浅色状态底色 |
| White | `#FFFFFF` | 背景、暗色版 Logo 的 `SCI-` |
| Charcoal | `#111827` | 常规深色文字；不全局改变灰阶 |
| Accent Orange | `#FF8A00` | Logo 原有小面积橙色笔画；不新增橙色按钮 |

在 `frontend/src/styles/globals.css` 的 `@theme` 内修改/增加 **仅三项**：

```diff
 @theme {
   --font-sans: 'Inter', 'Noto Sans', ui-sans-serif, system-ui, sans-serif;
-  --color-brand: #dc2626;
-  --color-brand-dark: #b91c1c;
+  --color-brand: #0A6FFF;
+  --color-brand-dark: #005DD9;
+  --color-brand-soft: #E6F2FF;
 }
```

**约束：** 不进行全局 `red-* → blue-*` 替换。错误、删除、危险操作的红色、警告 amber 和成功 green 都保留。`#0059D6` 不得再出现在新增的品牌 UI 样式中。

> 可访问性注意：`#0A6FFF` 上的纯白小字号文字对比度约为 4.44:1，略低于普通文本 WCAG AA 的 4.5:1。验收时需要实际检查；若要求严格达标，应在不改变全局设计令牌的前提下，单独采用已批准的深蓝色处理小字号白字按钮，避免自行引入第三种品牌蓝色。

## 3. Logo 资源与显示尺寸

### 3.1 资产清单

| 新增文件 | 内容 | 来源/制作规则 |
| --- | --- | --- |
| `frontend/public/brand/sci-surf-logo-light.png` | 浅色背景 Logo | 使用现有透明 Logo，`SCI-` 黑色、`Surf` 蓝色、末端少量橙色 |
| `frontend/public/brand/sci-surf-logo-dark.png` | 暗色背景 Logo | **必须新增**：保留透明背景与造型，只将 `SCI-` 黑字改为白字；其他笔画不变 |
| `frontend/public/favicon.svg` | 浏览器小尺寸图标 | **本次替换原紫色 favicon**：独立、简洁、蓝色的 `S` / 波浪形符号；不要把完整横向字标缩至 16×16 |

现有透明 Logo 实际约为 `1938 × 601 px`（长宽比约 **3.22:1**）。此长宽比用于判断显示尺寸，不得通过设置独立宽高而拉伸图片。

**资源质量验收：** 新版深色 Logo 应由浅色 Logo 保形重着色，保留透明通道、清晰边缘与完整字标；在白色和深灰色背景下分别预览。深色 Logo **不是**将整个 Logo 变白，也不是加背景矩形。

**favicon 限定：** 仅交付一个简化品牌符号 SVG（及必要时浏览器使用的 PNG 备选）；不拓展到 App Icon、社媒头像、整套品牌插画。SVG 应有合理的 `viewBox`，在 16×16 / 32×32 浏览器标签尺寸下清晰可辨。原引用路径继续使用 `/favicon.svg`，无需改导航或路由。

### 3.2 Header 精确尺寸（不改变外层布局）

现有 Header 的容器是 `h-14`（**56px**）。用图片自适应宽度，不使用旧计划中的 `h-8`（32px）。

| 断点 | 显示高度 | 按 3.22:1 计算的宽度 | 目标 |
| --- | ---: | ---: | --- |
| 移动端 `< md` | `h-10` = **40px** | 约 **129px** | 满足移动端 112–136px 指引 |
| 桌面端 `md+` | `h-11` = **44px** | 约 **142px** | 落在桌面端 136–164px 指引 |

使用两个对应明暗色主题的资源，**保留原有 `<Link to="/">`**，不得变更主题 store 或额外引入依赖。实施参考：

```tsx
<Link to="/" className="flex items-center" aria-label="Sci-Surf home">
  <img
    src="/brand/sci-surf-logo-light.png"
    alt="Sci-Surf"
    className="block h-10 w-auto object-contain md:h-11 dark:hidden"
  />
  <img
    src="/brand/sci-surf-logo-dark.png"
    alt=""
    aria-hidden="true"
    className="hidden h-10 w-auto object-contain md:h-11 dark:block"
  />
</Link>
```

如暗色资源不可用，**不要**直接把黑字版本投放到暗色页眉；先生成并验收资产后再合并。`object-contain`、`w-auto` 确保不变形。确认窄屏 Logo、主题切换、菜单按钮不碰撞；不能以改变 header 高度或重排导航来修复。

## 4. 必须定点处理：点赞态蓝字配红底

文件：`frontend/src/components/paper/PaperActions.tsx`。

现有“已点赞”分支约在第 39 行：

```tsx
? 'text-brand bg-red-50 dark:bg-red-900/20'
```

仅替换为：

```tsx
? 'text-brand bg-brand-soft dark:bg-blue-900/20'
```

**原因：** 全局 `text-brand` 改蓝后，原有 `bg-red-50` 会形成蓝字红底；点赞状态属于品牌化的**选择状态**，而不是错误/危险语义。其他分支完全不改，包括 `Dislike` 的灰色已选态和 `Bookmark` 的 amber 收藏态。

## 5. 用户可见品牌名称替换

重点入口：

- `frontend/src/components/layout/Header.tsx`：文字 Logo → 图片 Logo（不另显示 `PaperIgnition` 文案）。
- `frontend/index.html`：`PaperIgnition - AI-Powered Academic Paper Discovery` → `Sci-Surf - AI-Powered Academic Paper Discovery`；确保 `<link rel="icon">` 仍引用新版 `/favicon.svg`。
- `frontend/src/components/layout/Footer.tsx`：显示名称 `PaperIgnition` → `Sci-Surf`；保留备案号、备案 URL 与年份逻辑。
- 其他 `frontend/` 内用户可见的展示文字：逐项搜索与替换。

**禁止：** 全仓库盲目替换、重命名路由、接口、数据库表、package、环境变量、localStorage key、日志标识等内部名称。`Sci-Surf` 为统一展示拼写；不要混用 `SciSurf` / `SCI-Surf` / `Sci Surf` 作为普通页面文案。

## 6. 执行步骤

### Step 0 — 创建分支与清单（只检查）

```bash
git switch -c chore/scisurf-branding
rg -n -i 'paper[ -]?ignition|sci[ -]?surf|#dc2626|#b91c1c|#0059D6' frontend
rg -n 'text-brand|bg-brand|border-brand|brand-dark|bg-red-|dark:bg-red-' frontend/src
```

将命中项标记为 A 用户可见品牌、B 品牌色、C 内部标识、D 语义状态色。尤其确认 `PaperActions.tsx`；对 `favicon.svg` 和暗色 Logo 做单独资产检查。

### Step 1 — 生成/导入三份 Logo 资产

1. 导入 `sci-surf-logo-light.png`；基于同一字标重着色生成 `sci-surf-logo-dark.png`。
2. 将当前紫色 `favicon.svg` 替换成适合 16×16 的蓝色简化品牌符号。
3. 在亮色/暗色背景分别检查 Logo；在实际标签页尺寸检查 favicon。

### Step 2 — 替换 Header 字标

使用第 3.2 节的图片样式，保持原 `<Link to="/">`、导航、主题切换、移动菜单、页眉 56px 高度和所有业务逻辑。

### Step 3 — 统一品牌色与点赞背景

按第 2 节修改 `globals.css`，按第 4 节 **仅定点**调整 `PaperActions.tsx` 点赞已选态；不得触及其他红色语义状态。

### Step 4 — 替换前端品牌文字

按第 5 节修改浏览器标题、页脚及其它前端展示文字；保留技术内部标识。

### Step 5 — 验证、审查 Diff

```bash
cd frontend
npm run build
npm run lint
cd ..
git diff --name-only
git diff --check
git diff
```

**验收清单**：

- [ ] 手机端 Logo 40px 高、约 129px 宽；桌面端 44px 高、约 142px 宽；无裁剪/拉伸/与菜单碰撞。
- [ ] Header 维持 56px；亮/暗主题都显示正确版本，`SCI-` 明暗可读，Logo 点击仍返回首页。
- [ ] 浏览器标签显示新 Sci-Surf 小图标；16px 和 32px 无糊成一团的问题。
- [ ] 只有一种 Hover Blue：`#005DD9`；没有新增的 `#0059D6`。
- [ ] “已点赞”显示蓝字配浅蓝底（暗色主题为适配的深蓝透明底）；其余语义状态不变。
- [ ] 页面 title、Footer、所有可见品牌文案为 `Sci-Surf`，没有遗漏旧名称。
- [ ] 原布局、导航、业务逻辑、路由、功能未被修改；后端与 orchestrator 未被碰触。
- [ ] `npm run build` 和 `npm run lint` 通过；如 lint 存在预先遗留错误，明确区分。
- [ ] Git Diff 中除 Logo/favicons 和前端品牌相关文件外，没有杂项。

## 7. 交付清单

1. 一个专用分支/PR，严格局限于这次 Branding Update。
2. 三份品牌资产：浅色 Logo、暗色 Logo、单独 favicon。
3. Header、全局品牌色、点赞状态、document title、Footer 和其它用户可见名称的最小代码改动。
4. 简短变更报告：修改文件、替换的展示名称、保留的技术标识、build/lint 结果、明暗/移动端截图。

## 8. 交给 Codex 的精简指令

> 在现有 PaperIgnitionV1 仓库中实施严格限范围的 **Sci-Surf 品牌迁移**：只调整 (1) Header 的 Logo，包括明/暗两套透明字标及新的小图标 favicon；(2) 全局品牌红转蓝，主色 `#0A6FFF`、唯一 Hover 蓝 `#005DD9`、浅蓝 `#E6F2FF`；(3) 前端所有用户可见的 `PaperIgnition` / `Paper Ignition` 名称为 `Sci-Surf`。Logo 目前透明资源比例约 3.22:1；Header 保持 56px，不得用 h-8，移动端 `h-10` (~129px 宽)、桌面端 `md:h-11` (~142px 宽)。暗色版只将 `SCI-` 改白，保留 `Surf` 蓝与橙色小笔画；favicon 使用简化蓝色 S/波浪符号，替换原紫色图案，不能缩小整个横向 Logo。特别修复 `frontend/src/components/paper/PaperActions.tsx`：`text-brand bg-red-50 dark:bg-red-900/20` 改为 `text-brand bg-brand-soft dark:bg-blue-900/20`；保留错误/删除红、警告 amber、成功绿和收藏 amber。页面布局、Header 高度、交互逻辑、主题 store、路由、API、后端、orchestrator、包名、配置键和存储键一律不改。先搜索并分类品牌文字/品牌色/内部标识/语义色；再实施最小 Diff；最后运行 `npm run build`、`npm run lint` 并报告变更和视觉验收。若深色 Logo 或 favicon 无法高质量制作，标记为未完成，不要用错误素材替代并宣称完成。

---

**最终判定：这仍然是 Logo（含 favicon）、配色、品牌名称三类修改，不是 UI 重设计。**
