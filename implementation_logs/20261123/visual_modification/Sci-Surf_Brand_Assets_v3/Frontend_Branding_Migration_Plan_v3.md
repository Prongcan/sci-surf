# Sci-Surf 前端品牌迁移执行计划 v3.0（素材验收版）

> 适用仓库：`Algnite-Solutions/PaperIgnitionV1`；日期：2026-11-23  
> **严格范围：只更换 Logo（含亮/暗版和 favicon）、品牌配色、用户可见的品牌名称。** 不重设计页面，不改布局/交互/业务逻辑。

## 1. 本版解决的素材问题

| v2 实施阻塞项 | v3 交付情况 | 验收依据 |
| --- | --- | --- |
| 亮色 Logo 是 RGB 白底、4:1 | **已替换**：RGBA 透明图，1938×601 | PNG mode `RGBA`，有真实透明像素 |
| 暗色 Logo 与亮色版造型不同、存在脏边 | **已替换**：从同一透明母版生成，只对 `SCI-` 做白色重着色 | 尺寸/Alpha 通道完全一致；蓝色 `Surf` 与橙色笔画像素不变 |
| Logo 比例导致 40/44px 预计宽度不正确 | **已修复**：两版都为 1938:601 ≈ 3.2246:1 | `40×3.2246≈129px`，`44×3.2246≈142px` |
| 只有 favicon 高清概念 PNG，没有 SVG、尺寸验收 | **已交付**：真正基于 SVG `<path>` 的 `favicon.svg`、16/32px PNG、16/32/48px ICO；带浅色/深色预览 | SVG 可解析；位图为真实尺寸；`previews/` 有小尺寸验收图 |

**重要**：此前资源包中的 `Sci-Surf_Logo_Light.png`（RGB 白底）、`Sci-Surf_Logo_Dark.png`（带光晕的生成图）和仅作为概念图的旧 Favicon **不再用于上线**。以 `Sci-Surf_Brand_Assets_v3.zip` 里的新版素材为唯一来源。

## 2. 品牌色（统一值）

| 作用 | 色值 |
| --- | --- |
| 主题蓝（Primary） | `#0A6FFF` |
| 悬停蓝（Hover，唯一） | `#005DD9` |
| 浅蓝背景 | `#E6F2FF` |
| 白色 | `#FFFFFF` |
| 文字黑灰（既有 UI 保留） | `#111827` |
| 少量橙色点缀（不新增橙色操作按钮） | `#FF8A00` |

在 `frontend/src/styles/globals.css` 的 `@theme` 中定点修改：

```diff
- --color-brand: #dc2626;
- --color-brand-dark: #b91c1c;
+ --color-brand: #0A6FFF;
+ --color-brand-dark: #005DD9;
+ --color-brand-soft: #E6F2FF;
```

请勿全局 `red-*` → `blue-*`。错误、删除、警告等语义色不变。`#0059D6` 不再用于新的品牌样式。**对比度提醒**：白字与 `#0A6FFF` 对比度约 `4.44:1`，小字号白字按钮若需 WCAG AA 4.5:1，请在具体按钮使用已批准的 `#005DD9` 深蓝，不要再添加新品牌蓝色。

## 3. 将资源直接放入 Vite 前端

ZIP 已包含可直接复制的 `frontend/public/` 子目录：

```text
Sci-Surf_Brand_Assets_v3/
├── frontend/public/
│   ├── brand/
│   │   ├── sci-surf-logo-light.png   # 1938×601 RGBA
│   │   └── sci-surf-logo-dark.png    # 1938×601 RGBA
│   ├── favicon.svg                   # 真正 SVG 路径，小尺寸独立符号
│   ├── favicon.ico                   # 16/32/48 多尺寸
│   ├── favicon-16x16.png
│   └── favicon-32x32.png
├── logo/                              # 品牌素材原始交付目录
├── favicon/                           # 各尺寸导出物
├── previews/                          # 明暗页眉 / 16px、32px 验收图
├── README.md
└── SHA256SUMS.txt
```

导入方式（在项目根目录，且 ZIP 已解压）：

```bash
cp -R path/to/Sci-Surf_Brand_Assets_v3/frontend/public/. frontend/public/
```

不要将 RGB 白底图或带光晕的旧暗色图混进 `frontend/public/brand/`。

## 4. Header 替换（保持结构、56px 高度）

现有 Header 为 `h-14 = 56px`，无须更改。用以下图像替换文字字标，保留原有首页跳转：

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

- 移动端 `h-10` = 40px，高度自适应得到宽度约 129px。
- 桌面端 `md:h-11` = 44px，宽度约 142px。
- 不设置独立的固定宽度，不拉伸、不裁剪、不加背景矩形。
- 真机/浏览器验证不同宽度导航是否碰撞，不能修改原有整体布局来掩盖问题。

## 5. favicon 与页面标题

替换 `frontend/public/favicon.svg`（现有紫色图标）。保留 `frontend/index.html` 现有图标引用路径，或确保其写作：

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
```

图标不是横向字标缩小，而是独立蓝色 `S` / 流线简化符号。PNG 16×16 / 32×32 和 ICO 已交付以供必要时回退，不要求额外更改浏览器配置。`<title>` 的用户可见名称由 `PaperIgnition` 改成 `Sci-Surf`，描述部分保留原文。

## 6. PaperActions 的定点配色修复

`frontend/src/components/paper/PaperActions.tsx` 已点赞状态：

```diff
- 'text-brand bg-red-50 dark:bg-red-900/20'
+ 'text-brand bg-brand-soft dark:bg-blue-900/20'
```

只改这条品牌化状态颜色。删除危险色、错误色、收藏 amber、其他状态全部不改。

## 7. 用户可见品牌名称

- `frontend/src/components/layout/Header.tsx`：旧文字品牌换为图片，链接逻辑不动。
- `frontend/src/components/layout/Footer.tsx`：`PaperIgnition` → `Sci-Surf`（年份、备案链接不动）。
- `frontend/index.html`：`<title>` 文字替换，图标链接继续有效。
- 搜索 `frontend/` 其余用户可见品牌名称，逐项确认后替换。

不要替换技术性 `paperignition`：路径、包名、API 字段、环境变量、数据库、路由、日志/缓存存储键、backend/orchestrator 源代码均不在此任务范围。

## 8. 验收与命令

先搜索：

```bash
rg -n -i 'paper[ -]?ignition|#dc2626|#b91c1c|#0059D6' frontend
rg -n 'text-brand|bg-brand|brand-dark|bg-red-|dark:bg-red-' frontend/src
```

再验证：

```bash
cd frontend
npm run build
npm run lint
cd ..
git diff --check
git diff --stat
```

**验收清单**：

- [ ] 两版 Logo 均为 `1938×601`、`RGBA` 透明图，不带底色；暗色版仅 `SCI-` 反白。
- [ ] Header 仍为 56px，Logo 移动端 40px 高 / 约 129px 宽，桌面端 44px 高 / 约 142px 宽。
- [ ] 明暗模式下字标可读、无光晕脏边，与菜单/按钮不碰撞，Logo 仍链接首页。
- [ ] 新 `favicon.svg` 能加载，分别在 16px、32px 标签尺寸下可辨；检查 `previews/` 样本。
- [ ] 全局悬停蓝仅 `#005DD9`，主品牌蓝 `#0A6FFF`；已点赞蓝字浅蓝底。
- [ ] `PaperIgnition` 在用户可见位置均改为 `Sci-Surf`，内部技术标识不受影响。
- [ ] 不改布局、功能、路由、后端、部署配置，build/lint 通过；如存在历史 lint 错误需单独说明。

## 9. Codex 精简任务指令

> 使用交付包 `Sci-Surf_Brand_Assets_v3` 对 PaperIgnitionV1 的 `frontend/` 做**严格最小品牌迁移**。素材已经提供，**不要重新生成 Logo/Favicon**。将随包 `frontend/public/` 内容复制进仓库；亮/暗 Logo 都是 1938×601 透明 PNG、相同轮廓与 Alpha；favicon.svg 是独立矢量 S。Header 保持 56px 高，使用图片 `h-10 md:h-11 w-auto`，保留亮/暗主题切换及首页链接。全局品牌色更新为 `#0A6FFF`、悬停深蓝统一 `#005DD9`、浅蓝 `#E6F2FF`。修复 `PaperActions.tsx` 已点赞态蓝字红底问题，只替换用户可见 `PaperIgnition` 为 `Sci-Surf`（标题、页脚、相关文案），绝不改内部 `paperignition` 技术标识、布局、业务逻辑、API、后端及 orchestrator。最后运行 build/lint、检查 git diff 和明暗模式/16px favicon 实际效果。

---

**交付边界提醒：本包已完成品牌素材制作与静态检查；尚未在你的运行中仓库执行前端代码修改或浏览器端验收。**
