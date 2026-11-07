# 上架计划（三端：Android / iOS / Web）

> 前提：阿里云 Linux 服务器已装好 Hermes；iOS 构建走 GitHub Actions `macos-15`；Web 部署在自有服务器。
> 「并行」表示不占开发时间，但卡在别人手上，越早启动越好。

## 总览

| 周 | App 主线 | Web 主线 | 并行 / 卡点 |
| --- | --- | --- | --- |
| W0 | 环境与账号 | 域名 + 隐私政策页 | Apple $99、Google $25 + 身份验证、**凑齐 12 个测试者** |
| W1 | 骨架跑通双端 | Next.js 骨架 + shared JS 打通 | 包名/应用名查重 |
| W2 | 核心功能 + shared 测试 | 分享页（SSR）+ OG 卡片 | Play Console 建应用 |
| W3 | 打磨、内购、双端真机 | 图片 CDN + 首屏优化 | **启动 Google 14 天封闭测试**；TestFlight |
| W4 | 素材、提审、回复 | Web 上线 + 收录验证 | App Store 首次提审（预留 3–7 天） |

---

## W0：不写代码的一周（但决定成败）

- [ ] Apple Developer Program（个人 1–3 天；公司要 D-U-N-S，预留 2 周）
- [ ] Google Play 开发者账号 + 身份验证
- [ ] 税务与收款信息（两边都要，Apple 还要签 Paid Applications 协议）
- [ ] 域名 + HTTPS 证书（Web 与分享卡片都依赖）
- [ ] 隐私政策页上线（两端商店 + Web 都要可访问 URL）
- [ ] **招募 12 名 Google 封闭测试者**，建邮件列表
- [ ] 写清 App 与 Web 的**分工**：Web 是分享/浏览入口，还是完整客户端？写进 `docs/product.md`

## W1：骨架（三端同时打通）

- [ ] `kmp.jetbrains.com` 生成工程，拆出 `shared` 模块（纯逻辑，无 Compose）
- [ ] `shared` 加 `js(IR)` target，产出 `jsProductionLibraryDistribution`
- [ ] `web/` 用 `file:` 依赖引入 shared 产物，跑通一个「读 shared 数据并渲染」的页面
- [ ] 版本目录锁定 Kotlin / AGP / Gradle / CMP / Next.js
- [ ] CI 四个 job 全绿

**验收**：`shared` 的同一份逻辑，在 App 与 Web 上跑出相同结果。

## W2：核心功能

- [ ] 先定数据契约（API / 表结构 / 图片存储路径），再写 UI
- [ ] 业务规则进 `shared`，配套 `commonTest`
- [ ] App：列表 + 详情 + 上传
- [ ] Web：分享页（SSR）+ OG meta + 404

**验收**：两端手动走通主路径；Web 分享链接在微信/iMessage 有预览图。

## W3：打磨与内测

- [ ] 内购（若有）：RevenueCat，两端沙盒走通
- [ ] 账号体系（若有）：登录、**删除账号**、隐私链接
- [ ] App 专项：键盘、安全区、深色模式、动态字号、VoiceOver
- [ ] 相册专项：1 万张列表滚动、双指缩放、HEIC、内存峰值
- [ ] Web 专项：图片 CDN、`next/image`、LCP < 2.5s、移动端适配
- [ ] **Play 封闭测试上线，拉 12 人**
- [ ] TestFlight 内测

## W4：提审与上线

- [ ] App 截图（6.9"/6.5"）、图标、feature graphic
- [ ] 商店文案（中英）、关键词、支持 URL
- [ ] 隐私问卷 + `PrivacyInfo.xcprivacy`；Google Data safety
- [ ] 审核备注 + 演示账号
- [ ] Web 部署到生产，验证分享卡片与 404
- [ ] 提交提审

---

## 三端特有的坑

1. **版本矩阵**：Kotlin ↔ CMP ↔ AGP ↔ Xcode ↔ Next.js，升级一个可能全崩。锁死。
2. **iOS 只能靠 CI 验证**：W1 就要把 CI 跑通，否则后面盲写。
3. **`shared` 被污染**：只要有人在里面 `import` 了 Compose，Web 就废了。这条要靠 review 守住。
4. **Web 做得像 App**：Canvas 渲染拿不到 SEO。分享页必须是真 DOM。
5. **三端时间不一致**：EXIF 时间戳、服务器时区、用户本地时区，必须在 `shared` 里统一定义。
6. **图片存储成本**：原图 + 多档缩略图，存储与流量会随时间线性涨。上线前定好清理策略。

## Hermes 分工

| 交给 Hermes | 必须人做 |
| --- | --- |
| 骨架、样板、测试、迁移脚本 | 账号注册、税务、协议签署 |
| 商店文案、截图裁切、隐私页草稿 | 提审点击、审核回复措辞 |
| CI / fastlane / 部署脚本 | 证书与密钥保管、生产部署 |
| 崩溃归类、评论摘要、SEO 建议 | 产品取舍、定价、是否上线 |
