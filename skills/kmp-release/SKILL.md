---
name: kmp-release
description: 在 KMP + Compose Multiplatform 项目里执行一次发版：校验版本、双端构建、上传 TestFlight 与 Google Play 内测轨道、起草发行说明。当用户说「发版 / 出包 / 传一下测试版 / 上 TestFlight」时使用。不用于日常开发构建。
---

# KMP 双端发版

## 何时使用

用户明确要求发版、出包或上传测试版时。**日常 `assembleDebug` 不需要走这个流程。**

## 前置检查（任一项不满足就停下并报告）

```bash
git status --porcelain          # 必须为空
git branch --show-current       # 必须是 release/* 或 main
./gradlew check                 # 必须通过
```

- [ ] 版本号已更新：`composeApp/build.gradle.kts` 的 `versionName` / `versionCode`
- [ ] iOS `CFBundleShortVersionString` / `CFBundleVersion` 与 Android 对齐（build 号单独递增，不回退）
- [ ] `CHANGELOG.md` 有本次条目
- [ ] 本次改动涉及的权限/数据收集已在 `docs/privacy.md` 更新

**版本号规则（硬性）**：`versionName` 每次提审必须严格递增；Apple 拒绝重复的 `CFBundleVersion`，Google 拒绝重复的 `versionCode`。**绝不重发同一个号。**

## 步骤

### 1. 生成发行说明

从 `git log <上次tag>..HEAD` 提炼 3–6 条面向用户的中文说明 + 英文说明（App Store 需要）。

**不写**内部重构、不写"修复若干问题"这种废话，不承诺未实现的功能。

### 2. 构建并上传 Android（可在本机/Linux）

```bash
./gradlew :composeApp:bundleRelease
```

产物：`composeApp/build/outputs/bundle/release/composeApp-release.aab`

上传到 **internal** 轨道（不是 production）：

```bash
bundle exec fastlane android beta
```

### 3. 构建并上传 iOS（需要 macOS runner）

**不要在本机尝试。** 触发 CI：

```bash
git tag v<versionName> && git push origin v<versionName>
```

CI 会跑 `fastlane ios beta`，产物进 TestFlight。

### 4. 等人确认

上传成功后，**停下来，把以下信息报给用户**，不要继续提审：

- 版本号与 build 号
- Android 轨道链接 / TestFlight 构建号
- 发行说明全文
- 本次新增的权限或数据收集

提审（`deliver` / `supply` 到 production）**必须由人手动执行**。

## 失败处理

| 现象 | 处理 |
| --- | --- |
| iOS 签名失败 | 检查 `MATCH_PASSWORD` 与 match 仓库权限；不要改 Xcode 签名设置绕过 |
| TestFlight 提示 build 重复 | 递增 `CFBundleVersion`，不要复用 |
| Play 拒绝 AAB | 检查 target API level 与 64 位支持；看 Console 的详细错误 |
| Gradle 在 CI 上 OOM | 调 `org.gradle.jvmargs=-Xmx4g`，不要删测试 |

## 红线

- 不执行 `fastlane ios release` / `android promote`。
- 不动 keystore、`.p8`、service account JSON。
- 不在日志或对话里打印任何密钥内容。
- 构建失败不通过修改签名/跳过测试"解决"。
- 版本号只增不减。
