# Sci-Surf 前端品牌视觉最小修改计划

> 项目：<https://github.com/Algnite-Solutions/PaperIgnitionV1>  
> 类型：前端 Branding Update（非 UI 重设计）  
> 原则：**只改 Logo、品牌配色、用户可见的产品名称；不改布局、业务功能和系统标识。**

## 1. 目标与范围

将 PaperIgnition 的前端用户界面更新为 **Sci-Surf**：

1. **Logo**：用已提供的新版 Sci-Surf 官方 Logo 替换当前页眉中的文字 Logo；必要时制作同样图形的暗色背景适配版。
2. **配色**：将当前红色品牌色更换为蓝色，保持白色/浅灰页面背景，以少量橙色和黑色作为辅助。只调整品牌视觉，不将所有颜色一键替换。
3. **品牌文字**：将前端用户可见的 `PaperIgnition`、`Paper Ignition` 和相应的品牌组合文字替换为 `Sci-Surf`。浏览器标题和页脚包含在内。

**不做：** 首页重设计、导航调整、组件重构、按钮或卡片样式大改、字体替换、业务文案改写、路由更名、API/数据库/后端/任务调度修改、仓库或包名重命名。

## 2. 已确认的代码位置

当前仓库前端采用 React + TypeScript + Vite + Tailwind CSS v4。已核对以下具体位置：

| 文件 | 当前情况 | 修改方式 |
| --- | --- | --- |
| `frontend/src/styles/globals.css` | `@theme` 中 `--color-brand: #dc2626;`、`--color-brand-dark: #b91c1c;` | 只修改这两个品牌色变量 |
| `frontend/src/components/layout/Header.tsx` | 页眉 Logo 为 `Paper` + `Ignition` 两个 `<span>` | 替换为新的 Sci-Surf Logo 图片，保留现有首页链接及导航逻辑 |
| `frontend/index.html` | `<title>PaperIgnition - AI-Powered Academic Paper Discovery</title>` | 替换品牌名，保留后半部分原文 |
| `frontend/src/components/layout/Footer.tsx` | 页脚含 `PaperIgnition` | 替换为 `Sci-Surf`，**保留备案号、备案链接和年份逻辑** |
| `frontend/src/stores/theme.ts` | 明暗主题状态保存及切换 | **不修改主题逻辑**，只核验 Logo 在两种主题中清晰可读 |
| `frontend/src/components/layout/MobileNav.tsx` | 登录按钮使用 `bg-brand` / `hover:bg-brand-dark` | 原则上无需修改，继承全局品牌色即可 |
| `frontend/public/favicon.svg`（由 `index.html` 引用） | favicon 链接已存在，具体图形未核对 | 仅当 favicon 为旧品牌时才替换图案，不改变 favicon 引用结构 |

> 上表是已确认的重点入口，不代表全站品牌字符串已穷举；执行前必须进行前端范围内的全文搜索。

## 3. 视觉规范（本次实施用到的最小子集）

| Token | 色值 | 用途 |
| --- | --- | --- |
| Primary Blue | `#0A6FFF` | 品牌 Logo 蓝色、链接、主按钮、选中态等已有品牌位置 |
| Hover Blue | `#0059D6` | 原 `brand-dark` 对应的 hover/active 品牌色 |
| Light Blue | `#E6F2FF` | 仅在已有品牌浅色背景需要调整时使用 |
| White | `#FFFFFF` | 保留原白色主背景 |
| Charcoal | `#111827` | 黑色/深色文字；不全局替换当前灰阶 |
| Accent Orange | `#FF8A00` | Logo 或既有品牌装饰的少量点缀，**不新增橙色组件** |

`globals.css` 的预期最小修改：

```css
@theme {
  --font-sans: 'Inter', 'Noto Sans', ui-sans-serif, system-ui, sans-serif;
  --color-brand: #0A6FFF;
  --color-brand-dark: #0059D6;
}
```

注意区分 **品牌红色** 与 **语义红色**：删除/失败/错误等语义红色保留；成功的绿色、警告的 amber、标签分类色、图表语义色等原则上保留。不要批量把所有 `red-*` 或任意十六进制颜色替换为蓝色。现有 dark mode 保持可用。

## 4. 分步执行

### Step 0 — 创建独立分支并盘点（不改代码）

```bash
git switch -c chore/scisurf-branding
rg -n -i 'paper[ -]?ignition|paperignition|#dc2626|#b91c1c' frontend
rg -n 'text-brand|bg-brand|border-brand|brand-dark|red-[0-9]+' frontend/src
```

对搜索结果分类：

- A 类：**用户可见的品牌文案** → 替换为 Sci-Surf。
- B 类：**品牌颜色** → 使用新蓝色 token。
- C 类：**技术标识/逻辑代码**（API URL、数据库名、localStorage key、配置键、变量、包名、资源路径、测试夹具等）→ 不修改。
- D 类：**语义颜色**（错误/危险红，警告橙，成功绿等）→ 不修改。

如果 `rg` 不可用，可使用 `grep -RniE`。

### Step 1 — 置入 Logo 并替换页眉

- 将提供的新 Logo 透明 PNG 放到 `frontend/public/` 下，例如 `frontend/public/brand/sci-surf-logo.png`。
- 修改 `frontend/src/components/layout/Header.tsx` 中当前由 `Paper` / `Ignition` 组成的品牌区：改为 `<img src="/brand/sci-surf-logo.png" alt="Sci-Surf" ... />`，保持外层原有 `<Link to="/">` 不变。
- 按原页眉 `h-14` 高度控制图片展示高度，例如 `h-8 w-auto object-contain`；优先保留原有高度与导航间距，避免文字或按钮挤出。
- 在手机宽度检查 Logo 与菜单按钮是否碰撞。
- 现有 dark mode 若让 Logo 黑色字失去对比度，则另提供同造型的深色背景 Logo（将 `SCI-` 处理为白色，`Surf` 保持蓝色），根据 `dark` 样式切换展示；不要修改 theme store 或引入新主题库。
- 如果 favicon 使用旧品牌图案，可在原路径替换为新品牌图标；该操作属于 Logo 替换，不扩展到其他资源。

### Step 2 — 替换品牌色

只调整 `frontend/src/styles/globals.css` 中：

```diff
- --color-brand: #dc2626;
- --color-brand-dark: #b91c1c;
+ --color-brand: #0A6FFF;
+ --color-brand-dark: #0059D6;
```

检查已使用 `text-brand`、`bg-brand`、`hover:bg-brand-dark` 的页面、按钮和链接是否自动变蓝。如个别页面另有硬编码的 **品牌红色**，只对明确属于品牌用途的实例进行定点修改。保留原有白色/灰色底色、间距、边框、圆角、阴影与动画。

### Step 3 — 替换前端显示名称

- `frontend/index.html`：文档标题改成 `Sci-Surf - AI-Powered Academic Paper Discovery`。
- `frontend/src/components/layout/Footer.tsx`：页脚展示名改为 `Sci-Surf`，备案链接和号码不动。
- 对 Step 0 搜索到的其他实际用户可见品牌文案逐一调整。
- 区分产品品牌名与内部代码标识：**不要**简单运行全仓库自动替换命令。
- 原有导航条目 `Explore` / `Favorites` / `Search`、页面业务描述等保持不变。

### Step 4 — 验证与复核

在 `frontend/` 下：

```bash
npm run build
npm run lint
```

人工检查：首页/Explore、Search、Favorites、登录界面、页脚、移动端导航、亮色与暗色模式，以及主按钮/高亮链接。确认：

- [ ] 所有用户可见的旧品牌名称已替换，拼写统一为 `Sci-Surf`。
- [ ] 页眉 Logo 清晰、比例正确，点击仍返回首页；亮/暗主题均可读。
- [ ] 旧红色品牌按钮/高亮变蓝；语义错误红色和警告色未受影响。
- [ ] 现有布局、导航、功能、事件行为和路由未改变。
- [ ] 页面 title、页脚版权、备案信息正确。
- [ ] `npm run build` 通过；`npm run lint` 通过，或明确说明已有的非本次修改问题。

最后核对改动范围：

```bash
git diff --name-only
git diff --check
git diff
```

原则上仅应出现前端品牌相关文件。不得混入 API、数据库、后端、orchestrator 和大规模自动格式化修改。

## 5. 交付标准

交付一次独立提交或 PR，并在说明中写明：

1. 修改了哪些文件、各自对应 Logo/颜色/名称哪一项。
2. 新增了哪些 Logo 资源文件。
3. 构建与 lint 结果。
4. 若发现旧品牌字样存在于 API/数据库/内部变量中，列为“有意保留”，**不擅自修改**。

**最重要的验收原则：用户打开后看到的是 Sci-Surf，使用起来仍然是完全相同的 PaperIgnition 前端。**

## 6. 可直接交给 Codex 的执行指令

> 在当前仓库中完成一次严格限范围的前端 Sci-Surf 品牌迁移。只允许：(1) 将 Header 的 PaperIgnition 文字 Logo 换为提供的 Sci-Surf 透明 Logo；(2) 将全局品牌色 `#dc2626` / `#b91c1c` 改为蓝色 `#0A6FFF` / `#0059D6`，以及少量明确属于品牌用途的硬编码颜色；(3) 将所有前端用户可见的 PaperIgnition 品牌名称统一换成 Sci-Surf，包括 document title 和 footer。保留全部现有布局、路由、导航、按钮行为、功能逻辑、主题切换、样式尺寸、语义颜色。不要修改后端、API、数据库、存储键、环境变量、包名或目录名，不要全仓库替换字符串，也不要根据视觉概念板重做页面。先搜索并列出命中项，按“品牌展示/内部标识/语义颜色”分类，再执行修改。最后运行 `npm run build`、`npm run lint` 并总结变更文件与验证结果。

## 7. 源文件参考（检查于 2026-11-23）

- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/src/styles/globals.css>
- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/src/components/layout/Header.tsx>
- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/src/components/layout/Footer.tsx>
- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/src/components/layout/MobileNav.tsx>
- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/src/stores/theme.ts>
- <https://raw.githubusercontent.com/Algnite-Solutions/PaperIgnitionV1/main/frontend/index.html>
