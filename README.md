# personal-album-platform

个人相册平台 · Android + iOS + Web 三端。

> 当前状态：**工程骨架**。仓库里是项目契约、CI、部署与上架流水线，业务功能尚未开始。

**两套 UI，一套业务逻辑。** App 用 Compose 写原生体验；Web 用 Next.js 写可被搜索引擎与分享卡片看见的页面。业务规则只写在 `shared/` 里。

## 技术栈

- **共享逻辑**：Kotlin Multiplatform（domain / data / api，不依赖 UI 框架）
- **App UI**：Compose Multiplatform（Android + iOS）
- **Web UI**：Next.js（App Router）+ TypeScript
- Ktor · kotlinx.serialization · SQLDelight · Koin · Coil 3
- 内购：RevenueCat KMP SDK

## 目录

```
shared/                    KMP 逻辑模块（唯一真相源），可编译到 JVM / iOS / JS
composeApp/                Compose UI（Android + iOS）
web/                       Next.js Web 端
iosApp/                    Xcode 壳工程
.github/workflows/ci.yml   四端 CI：shared / web / android / ios
fastlane/                  App 发版 lane（只到测试轨道，提审由人执行）
skills/kmp-release/        Hermes Agent 的发版技能
docs/roadmap-4-weeks.md    上架计划
docs/deploy-web.md         Web 部署与回滚
AGENTS.md                  项目契约：技术栈锁定、UI 边界、完成定义、禁止事项
```

## 环境要求

| 用途 | 要求 |
| --- | --- |
| shared / Android | JDK 21 + Android SDK，Linux / macOS 均可 |
| iOS | **仅 macOS + Xcode**，由 GitHub Actions `macos-15` 承担 |
| Web | Node 22 |

## 快速开始

```bash
git clone git@github.com:cxqq123/personal-album-platform.git
cd personal-album-platform

./gradlew :shared:allTests      # 共享逻辑
./gradlew :composeApp:assembleDebug
cd web && npm ci && npm run dev
```

## 发布

- App：见 [`skills/kmp-release/SKILL.md`](skills/kmp-release/SKILL.md)，构建可自动化，**提审由人手动执行**
- Web：见 [`docs/deploy-web.md`](docs/deploy-web.md)，**部署由人手动执行**

## 许可

私有项目，未授权。
