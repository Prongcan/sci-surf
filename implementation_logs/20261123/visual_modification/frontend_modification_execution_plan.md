# Sci-Surf 前端品牌迁移执行记录

日期：2026-11-23；工作分支：`frontend_modification`。

## 基线与范围

- 基线提交：`32de43c`，保存迁移前的生产配置、现有方案与视觉素材。
- 本次仅改前端页眉字标、favicon、品牌色、点赞选中态及用户可见品牌名称。
- 保留路由、业务逻辑、主题存储、后端与部署配置；`orchestrator/orchestrator/` 中的论文缓存不纳入 Git。
- 素材来源：`Sci-Surf_Brand_Assets_v3/frontend/public/`。

## 实施步骤

1. 搜索前端旧品牌文字、颜色与语义红色，区分展示文案和技术标识。
2. 复制 v3 明暗 Logo 与 favicon SVG；在 Header 使用 `h-10 md:h-11`，保持 56px 容器与首页链接。
3. 更新 `@theme` 三个品牌色变量；定点调整 PaperActions 已点赞背景。
4. 替换浏览器标题和页脚中的用户可见名称。
5. 运行 `npm run build`、`npm run lint`、`git diff --check`，核对变更范围。检查 v3 提供的明暗和 16/32px 预览；若无法运行浏览器，明确记录未完成的实际页面检查。

## 已知验收点

- `#0A6FFF` 配白色小字的对比度略低于 4.5:1；本次遵循锁定的品牌色，后续需由设计方确认是否将小字主按钮单独改用 `#005DD9`。

## 执行结果

- 已复制 v3 两版透明 Logo、SVG favicon 及小尺寸 PNG/ICO；更新 Header、全局品牌色、点赞已选态、页面标题和 Footer。
- `npm run build`：使用仓库环境中的 `node:22-alpine` 容器执行，通过。宿主机 Node 12 无法解析当前 TypeScript 和 ESLint 依赖的语法。
- `npm run lint`：同一容器执行，存在两处未修改文件的既有错误：`src/components/ui/Toast.tsx` 的 `react-refresh/only-export-components`，以及 `src/pages/VerifyEmailPage.tsx` 的 `react-hooks/set-state-in-effect`。
- 旧品牌名称搜索：用户可见位置已替换；`src/lib/constants.ts` 的 `paperignition_demo` 为内部测试密码标识，保留。
- 已检查 v3 提供的明暗 Header、16/32px favicon 静态预览。尚未进行真实浏览器的交互及多断点页面验收。
