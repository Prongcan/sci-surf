# Sci-Surf 阿里云 ECS 部署记录：Nginx 与 Vite 前端

> 整理日期：2026-11-22  
> 目的：记录在阿里云 Ubuntu ECS 上配置 Nginx、排查 502、修复 Node.js/Vite 环境、构建并启动 Sci-Surf 前端的完整过程。

## 1. 部署环境与架构

| 项目 | 当前信息 |
| --- | --- |
| 云服务器 | 阿里云 ECS，Ubuntu 22.04 |
| ECS 公网 IP | `8.130.190.218`（此前使用；以控制台实际显示为准） |
| 项目根目录 | `/root/scisurf/PaperIgnitionV1` |
| 前端目录 | `/root/scisurf/PaperIgnitionV1/frontend` |
| Conda 环境 | `scisurf` |
| 前端技术栈 | React + Vite |
| 前端预览端口 | `127.0.0.1:4173` |
| Web 服务器 | Nginx 1.18.0 |
| Nginx HTTP 端口 | `80` |

当前采用的请求路径：

```text
浏览器 / SSH 隧道
       │
       ▼
ECS Nginx（127.0.0.1:80；服务器监听 80）
       │ proxy_pass
       ▼
Vite Preview（127.0.0.1:4173）
       │
       ▼
Sci-Surf 前端构建结果（frontend/dist）
```

**状态说明：** 已确认 Nginx 运行正常，且 Vite Preview 成功显示 `http://127.0.0.1:4173/`。启动成功后，尚需再次执行 `curl` 验证整条 Nginx → Vite 链路；后端 API 是否运行也需要单独检查。

## 2. 安装和配置 Nginx

### 2.1 安装

在 ECS 上运行：

```bash
sudo apt update
sudo apt install -y nginx
```

### 2.2 创建站点配置

```bash
sudo nano /etc/nginx/sites-available/scisurf
```

站点配置如下：

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:4173;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

- `listen 80`：接收 HTTP 请求。
- `server_name _`：占位名称，不是对所有域名自动匹配的特殊通配符；在只有该站点或其作为默认站点时，可以处理直接通过 IP 发来的请求。
- `proxy_pass`：将请求代理到本机 4173 端口。
- `proxy_set_header`：保留请求主机、客户端 IP 和原始协议等信息。

### 2.3 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/scisurf \
  /etc/nginx/sites-enabled/scisurf

# 禁用 Ubuntu Nginx 默认站点（如果存在）
sudo rm -f /etc/nginx/sites-enabled/default
```

如果软链接已经存在，不要重复创建。

### 2.4 检查并启动 Nginx

```bash
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
sudo systemctl status nginx --no-pager
```

实际观察到：

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
Active: active (running)
```

说明配置语法正确，Nginx 最终已经成功运行。早先曾出现启动失败，日志中有 `bind() to 0.0.0.0:80 failed`（端口绑定失败），但随后的状态显示 `active (running)`，因此该早期问题已经不再阻止启动。

## 3. 排查 `502 Bad Gateway`

### 3.1 现象

```bash
curl -I http://127.0.0.1
```

返回：

```text
HTTP/1.1 502 Bad Gateway
Server: nginx/1.18.0 (Ubuntu)
```

含义：Nginx 可以响应，但无法正常连接上游应用。

### 3.2 排查命令

```bash
# 是否有服务监听 4173
sudo ss -lntp | grep 4173

# 直接测试前端服务
curl -I http://127.0.0.1:4173

# 读取 Nginx 错误日志
sudo tail -n 20 /var/log/nginx/error.log
```

实际观察到：

```text
curl: (7) Failed to connect to 127.0.0.1 port 4173 ... Connection refused
```

Nginx 日志显示：

```text
connect() failed (111: Connection refused) while connecting to upstream
upstream: "http://127.0.0.1:4173/"
```

**结论：** 当时 `4173` 端口没有程序监听。Nginx 本身正常，问题在于 Sci-Surf 前端没有启动。

## 4. 修复 npm 与 Node.js 环境

### 4.1 `ENOENT: package.json`：执行目录错误

最初在项目根目录运行：

```bash
cd /root/scisurf/PaperIgnitionV1
npm run build
```

报错：

```text
npm ERR! code ENOENT
npm ERR! enoent .../PaperIgnitionV1/package.json
```

原因：该目录没有 `package.json`，前端配置文件位于 `frontend` 子目录。

修正：

```bash
cd /root/scisurf/PaperIgnitionV1/frontend
ls -l package.json
```

后续 `npm` 命令应在 `frontend` 目录执行。

### 4.2 Vite 报 `Unexpected token '.'`：Node.js 版本太旧

当时运行：

```bash
npm run preview -- --host 127.0.0.1 --port 4173 --strictPort
```

报错片段：

```text
module.enableCompileCache?.()
                         ^
SyntaxError: Unexpected token '.'
```

这是旧版 Node.js 无法解析可选链语法 `?.` 的典型表现。处理思路是在现有 Conda 环境中升级 Node.js。

检查原有环境：

```bash
node -v
npm -v
which node
```

采用的升级命令：

```bash
conda install -n scisurf -c conda-forge nodejs=24 -y
conda activate scisurf
hash -r
node -v
npm -v
which node
```

> Node.js 24 是推荐安装版本。此处未记录升级后 `node -v` 的原始输出；实际版本请以服务器查询结果为准。

## 5. 构建与启动 Sci-Surf 前端

### 5.1 进入正确目录

```bash
conda activate scisurf
cd /root/scisurf/PaperIgnitionV1/frontend
```

### 5.2 安装依赖、构建

```bash
npm install
npm run build
```

Vite 构建产物通常位于 `frontend/dist/`。如果没有构建成功，应先处理构建错误，再启动 Preview。

### 5.3 启动前端（已成功）

```bash
npm run preview -- --host 127.0.0.1 --port 4173 --strictPort
```

用户实际返回的成功输出：

```text
> frontend@0.0.0 preview
> vite preview --host 127.0.0.1 --port 4173 --strictPort

  ➜ Local: http://127.0.0.1:4173/
  ➜ press h + enter to show help
```

参数含义：

| 参数 | 作用 |
| --- | --- |
| `--host 127.0.0.1` | 只允许服务器本机访问，适合由 Nginx 反向代理 |
| `--port 4173` | 使用 4173 端口 |
| `--strictPort` | 端口被占用时直接报错，不自动换端口 |

**注意：** 该命令以前台进程运行，关闭对应 SSH 会话可能导致 Vite 退出。长期部署应改用 `systemd` 或由 Nginx 直接托管 `dist` 静态文件。

## 6. 验证整体链路

保持 Vite Preview 的终端不关闭，另开 SSH 会话执行：

```bash
# 1. 检查 Vite 前端
curl -I http://127.0.0.1:4173

# 2. 检查 Nginx 是否已不再返回 502
curl -I http://127.0.0.1

# 3. 查看端口监听状态
sudo ss -lntp | grep -E ':(80|4173)\b'
```

预期：前两项返回正常 HTTP 状态（通常 `200 OK`），端口 80 和 4173 均有对应进程监听。

### 6.1 通过 Mac SSH 隧道访问 Nginx

在 Mac 本地运行：

```bash
ssh -N -L 8888:127.0.0.1:80 scisurf-ecs
```

然后浏览器访问：

```text
http://127.0.0.1:8888
```

如果只想直接访问 Vite 而不经过 Nginx：

```bash
ssh -N -L 8888:127.0.0.1:4173 scisurf-ecs
```

SSH 隧道命令运行后终端看起来“没有反应”是正常的：它会持续保持连接，直到按 `Ctrl+C` 结束。

### 6.2 Nginx 和直接访问 4173 的区别

| 访问方式 | 安全组需要开放的 Web 端口 | Vite 监听地址 |
| --- | --- | --- |
| 经 Nginx 代理 | 80（HTTPS 上线后为 443） | `127.0.0.1:4173` |
| 直接公网访问 Vite | 4173 | `0.0.0.0:4173` |
| 仅 SSH 隧道访问 | 无需开放公网 Web 端口 | `127.0.0.1:4173` 即可 |

当前采用的是 **Nginx → `127.0.0.1:4173`**，所以不需要对公网开放 4173。

> **合规提醒：** 若 ECS 在中国内地且尚未取得必要的 ICP 备案，不应直接面向公网提供网站服务；可以先使用 SSH 隧道测试。备案条件也会影响后续域名 `sci-surf.com` 的正式上线。

## 7. 后端 API 的待办项

Nginx 错误日志中出现以下路径：

```text
GET /api/health
GET /api/digests/recommendations/...
POST /api/auth/login-email
```

当前 Nginx 配置的 `location /` 会将所有请求（包括 `/api/*`）转发到 `4173`。如果后端是独立运行的 API 服务，还需要核对后端实际端口，并为 `/api/` 配置单独的代理规则，或确认前端已有正确的 API 转发配置。

可以先检查后端进程和监听端口：

```bash
sudo ss -lntp
```

找到实际端口之后再测试对应的 `/api/health`，避免在端口尚未确认时假定后端已经运行。

## 8. 日常启动与维护速查

### 前端启动

```bash
ssh scisurf-ecs
conda activate scisurf
cd /root/scisurf/PaperIgnitionV1/frontend
npm run preview -- --host 127.0.0.1 --port 4173 --strictPort
```

### 修改前端代码后重新构建

```bash
cd /root/scisurf/PaperIgnitionV1/frontend
npm run build
```

如有正在运行的 Preview 进程，应根据实际部署方式重启或刷新服务，以确保使用新的构建产物。

### Nginx 常用命令

```bash
# 检查配置
sudo nginx -t

# 重新加载配置
sudo systemctl reload nginx

# 查看状态
sudo systemctl status nginx --no-pager

# 查看报错
sudo tail -n 50 /var/log/nginx/error.log
```

## 9. Demo 账号

已注册供前端 `Try Demo` 按钮使用的 Demo 账号：

| 字段 | 值 |
| --- | --- |
| 用户名 | `Demo User` |
| 登录邮箱 | `demo@example.com` |
| 登录密码 | `paperignition_demo` |

前端的 `Try Demo` 按钮通过 `frontend/src/stores/auth.ts` 中的 `demoLogin()` 发起登录，登录凭据定义于 `frontend/src/lib/constants.ts`。登录成功后，前端使用后端返回的 `username`（预期为 `Demo User`）读取该账号的个性化推荐。

`BlogBot@gmail.com` 不是 Demo 登录账号；它是用户未登录时展示公共推荐流所使用的默认用户。

## 10. 后续建议

1. **验证 Nginx → Vite 链路**：确认此前的 502 已消失。
2. **配置长期运行方式**：优先考虑 Nginx 托管 Vite 构建产物，或使用 systemd 管理前端。
3. **确认后端 API 端口**：避免前端可以打开但登录、推荐等功能失败。
4. **完成域名与 HTTPS 正式上线**：在符合备案要求后配置 GoDaddy DNS、HTTPS 和必要的安全组规则。

---

**最终已确认的关键进展：** Nginx `active (running)`；Sci-Surf 前端 Vite Preview 成功启动并监听 `127.0.0.1:4173`。最后的端到端 HTTP 验证和后端联通性尚待检查。
