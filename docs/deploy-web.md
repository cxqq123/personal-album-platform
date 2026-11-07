# Web 端部署

> **由人执行，agent 不自动上线。** 这条规则写在 `AGENTS.md` 第 12 节。

## 三种部署方式

| 方式 | 适合 | 优点 | 代价 |
| --- | --- | --- | --- |
| **阿里云 OSS + CDN** | 国内访问为主 | 便宜、和服务器同云、备案后可加速 | 要自己配缓存策略与回源 |
| **Vercel** | 海外访问为主 | 零配置、自动预览环境、边缘缓存 | 国内访问不稳定 |
| **自建 Nginx** | 想完全掌控 / 小流量 | 无额外成本、调试直接 | 要自己搞 HTTPS、缓存、扩容 |

你这台阿里云服务器已有，**起步建议自建 Nginx + OSS 存图**；流量起来再换 OSS+CDN 静态托管。

## 部署前检查

```bash
cd web
npm ci
npm run lint && npm run test && npm run build   # 必须全绿
```

- [ ] `NEXT_PUBLIC_SITE_URL` 是**线上真实域名**（分享卡片的绝对地址依赖它）
- [ ] `NEXT_PUBLIC_API_BASE` 指向生产 API，不是 `localhost`
- [ ] 环境变量写在服务器侧，**不进仓库**
- [ ] 已确认本次没有改数据库 schema，或改动可向后兼容

## 自建 Nginx（推荐起步）

```nginx
server {
  listen 443 ssl http2;
  server_name album.example.com;

  # Next.js 静态产物
  root /srv/www/album/current;
  index index.html;

  location /_next/static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }

  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

```bash
# 构建 → 上传 → 切换软链 → 重载
cd web && npm run build
rsync -az --delete web/out/ prod:/srv/www/album/releases/$(date +%Y%m%d%H%M)/
ssh prod 'ln -sfn /srv/www/album/releases/$(ls -1t /srv/www/album/releases | head -1) /srv/www/album/current && nginx -s reload'
```

> 是否用 `out/`（静态导出）还是 Node 运行时，取决于有没有服务端逻辑。纯分享页用 `output: 'export'` 最省事；需要动态 OG 图或登录态就保留 Node 运行时。

## 回滚

保留最近 5 个 release 目录，切回上一个软链即可，**不要重新构建**：

```bash
ssh prod 'ls -1t /srv/www/album/releases | head -5'
ssh prod 'ln -sfn /srv/www/album/releases/<上一个> /srv/www/album/current && nginx -s reload'
```

## 上线后 10 分钟内必须验证

- [ ] 首页在**未登录、无缓存**的浏览器打开正常
- [ ] 随便挑一个分享页，粘贴到微信 / iMessage / Twitter，**能看到标题、描述、封面图**
- [ ] 手机 4G 下首屏 LCP < 2.5s
- [ ] 图片走 CDN 域名，不是主域名
- [ ] 404 页面和错误页不是白屏

## 常见事故

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 分享出去没预览图 | 分享页是客户端渲染，或 meta 用了相对路径 | 改 SSR/SSG + 绝对 URL |
| 更新后用户看到旧版 | `_next/static` 之外的文件被 CDN 缓存 | 只对带 hash 的静态资源设长缓存 |
| 图片加载慢 | 直传原图 | 走 CDN + `next/image` + 尺寸档位 |
| 国内打开白屏 | 用了 Google Fonts / 海外 CDN | 字体与静态资源本地化 |
