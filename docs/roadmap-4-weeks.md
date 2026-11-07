# 4 周上架计划（KMP + CMP，一人 + Hermes）

> 前提：阿里云 Linux 服务器已装好 Hermes；iOS 构建走 GitHub Actions `macos-15`。
> 「并行」表示这一列不占开发时间，但卡在别人手上，越早启动越好。

## 总览

| 周 | 主线 | 并行 / 卡点 |
| --- | --- | --- |
| W0 | 环境与账号 | Apple $99、Google $25 + 身份验证、**凑齐 12 个测试者** |
| W1 | 骨架跑通双端"Hello World" | 域名 + 隐私政策页；App 名/包名查重 |
| W2 | 核心功能 + 共享层测试 | Play Console 建应用、Data safety 初稿 |
| W3 | 打磨、内购/账号、双端真机验证 | **启动 Google 14 天封闭测试**；TestFlight 内测 |
| W4 | 素材、提审、回复审核 | App Store 首次提审（预留 3–7 天） |

---

## W0：不写代码的一周（但决定成败）

- [ ] Apple Developer Program 注册（个人 1–3 天；公司要 D-U-N-S，预留 2 周）
- [ ] Google Play 开发者账号 + 身份验证
- [ ] 税务与收款信息（两边都要，Apple 还要签 Paid Applications 协议）
- [ ] 想清楚 App 一句话定位 + 目标用户，**写进 `docs/product.md`**
- [ ] 包名/应用名查重，定 `com.yourco.appname`
- [ ] **招募 12 名 Google 封闭测试者**（同事、朋友、社群），建一个邮件列表
- [ ] 注册域名，准备 `/privacy` 页面（Hermes 可以生成）

> Google 的 12 人 × 14 天是硬性门槛。W3 启动测试 = 正好赶在 W4 提审前满足。

## W1：骨架

交付物：

- [ ] `kmp.jetbrains.com` 向导生成项目（Android + iOS + Compose UI）
- [ ] 版本目录锁定：Kotlin / AGP / Gradle / CMP 成套版本写进 `libs.versions.toml`
- [ ] 分层骨架：`data` / `domain` / `ui`，Koin 装配，导航跑通两个页面
- [ ] CI 绿：`./gradlew check` + iOS 编译任务在 macOS runner 上通过
- [ ] 真机各装一次：Android 侧载 + iOS 通过 Xcode 或 TestFlight

**验收**：一条命令出 Android 包；打 tag 能自动出 iOS 包并进 TestFlight。

## W2：核心功能

- [ ] 先把**数据契约**定下来（API / 本地表结构），再写 UI
- [ ] `commonMain` 里写业务逻辑，配套 `commonTest`
- [ ] 平台差异用 `expect/actual`，不要用 `if (isIOS)` 撒在业务代码里
- [ ] 每天跑一次 CI，保持绿

**验收**：核心流程在两端手动走通，`./gradlew check` 绿，无 `TODO` 遗留。

## W3：打磨 + 内测

- [ ] 内购（若有）：RevenueCat KMP SDK，两端各建一个测试商品，沙盒走通
- [ ] 账号体系（若有）：登录、**删除账号**、隐私政策链接
- [ ] iOS 专项：键盘/输入法、安全区、深色模式、动态字号、VoiceOver
- [ ] 崩溃与性能：冷启动、列表滚动、内存
- [ ] **Play Console 上传首个 AAB，开封闭测试，拉 12 人**
- [ ] TestFlight 内测，收集反馈

**验收**：12 人在跑；TestFlight 有可用构建；无 P0 崩溃。

## W4：提审

- [ ] 截图（6.9" / 6.5"；iPad 若支持）、图标、feature graphic
- [ ] 商店文案（中英）、关键词、支持 URL、隐私政策 URL
- [ ] App 隐私问卷 + `PrivacyInfo.xcprivacy`；Google Data safety 表单
- [ ] 审核备注 + 演示账号
- [ ] 提交，进入等待；同时准备回复模板

**验收**：两端状态为「Waiting for Review / In Review」，且你有回复审核的预案。

---

## KMP 特有的四个坑（提前知道能省一周）

1. **版本兼容矩阵**：Kotlin ↔ CMP ↔ AGP ↔ Xcode 必须成套。升级一个就全崩。锁死，别让 agent 顺手升。
2. **iOS 侧只能靠 CI 验证**：你在 Linux 上永远看不到 iOS 真实效果。**W1 就要把 CI 跑通**，否则后面每天都是盲写。
3. **Compose 在 iOS 上的细节**：文本输入、滚动回弹、无障碍语义、动态字体，和原生有差距。留出 W3 专门调，别指望"一次就对"。
4. **第三方 SDK 的 KMP 覆盖不全**：支付、推送、统计、地图，优先选官方支持 KMP 的（RevenueCat、Firebase 部分模块），否则写 `expect/actual` + 原生桥接，时间要单独估。

## Hermes 分工建议

| 交给 Hermes | 必须人做 |
| --- | --- |
| 骨架代码、样板、测试、迁移脚本 | 账号注册、税务、协议签署 |
| 商店文案、截图裁切、隐私政策草稿 | 提审点击、审核回复措辞 |
| CI / fastlane / 依赖调研 | 证书与密钥的生成与保管 |
| 崩溃日志归类、评论摘要 | 产品取舍、定价、是否上线 |
| 夜间依赖巡检、文档同步 | 任何涉及钱和法律的判断 |

> 一句话：**Hermes 写代码和跑流水线，你负责签字。**
