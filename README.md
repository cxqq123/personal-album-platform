# personal-album-platform

个人相册平台 · Android + iOS 双端。

> 当前状态：**工程骨架**。仓库里是 KMP + Compose Multiplatform 的项目契约、CI 与上架流水线，业务功能尚未开始。

## 技术栈

- Kotlin Multiplatform + Compose Multiplatform（共享 UI 与业务逻辑）
- Ktor / kotlinx.serialization · SQLDelight · Koin · Coil 3
- 内购：RevenueCat KMP SDK

## 目录

```
composeApp/               共享代码（commonMain / androidMain / iosMain）
iosApp/                   Xcode 壳工程
.github/workflows/ci.yml  双端 CI：Linux 跑 Android，macOS 跑 iOS
fastlane/                 发版 lane（只到测试轨道，提审由人执行）
skills/kmp-release/       Hermes Agent 的发版技能
docs/roadmap-4-weeks.md   4 周上架计划
AGENTS.md                 项目契约：技术栈锁定、完成定义、禁止事项
```

## 环境要求

| 用途 | 要求 |
| --- | --- |
| Android 构建 | JDK 21 + Android SDK，Linux / macOS 均可 |
| iOS 构建 | **仅 macOS + Xcode**，由 GitHub Actions `macos-15` runner 承担 |
| 发版 | fastlane + 签名材料（存放在 CI secrets，不入库） |

## 快速开始

```bash
git clone git@github.com:cxqq123/personal-album-platform.git
cd personal-album-platform

# 用 kmp.jetbrains.com 向导生成的工程填充 composeApp/ 与 iosApp/

./gradlew :composeApp:assembleDebug   # Android
./gradlew check                       # 测试 + 静态检查
```

## 发版

见 [`skills/kmp-release/SKILL.md`](skills/kmp-release/SKILL.md)。
构建与上传可自动化，**App Store / Play 的提审始终由人手动执行。**

## 上架时间线

见 [`docs/roadmap-4-weeks.md`](docs/roadmap-4-weeks.md)。

## 许可

私有项目，未授权。
