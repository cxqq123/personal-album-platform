# AGENTS.md — KMP + Compose Multiplatform 移动应用

> 本文件是 Hermes Agent 的项目契约。动手前必须先读它。
> 子 agent（`delegate_task`）同样会收到本文件，所以这里写的规则对它们**同样有约束力**。

## 1. 项目定位

一款小体量双端 App（Android + iOS），代码共享，目标 4–6 周内上架 App Store 与 Google Play。

**成功标准不是"代码写完"，而是"双端通过审核并在商店可见"。**

## 2. 技术栈（版本已锁定）

| 层 | 选型 |
| --- | --- |
| 语言 / UI | Kotlin Multiplatform + Compose Multiplatform（iOS + Android 共用 UI） |
| 架构 | commonMain 里 MVVM + 单向数据流：`State` / `Event` / `Effect` |
| 网络 | Ktor Client + `kotlinx.serialization` |
| 本地存储 | SQLDelight（需要键值对时用 multiplatform-settings） |
| DI | Koin |
| 导航 | `androidx.navigation:navigation-compose`（multiplatform 版）或 Decompose，**二选一，全项目统一** |
| 图片 | Coil 3（`coil-compose`，支持 KMP） |
| 内购 | RevenueCat KMP SDK（`purchases-kmp`）；**禁止**自己直连 StoreKit / Play Billing |
| 测试 | `kotlin.test` + Turbine（Flow）+ Koin `checkModules` |
| 构建 | Gradle Version Catalog（`gradle/libs.versions.toml`） |

**版本策略：锁定即冻结。**
Kotlin / AGP / Gradle / CMP 的版本必须成套兼容。**任何 agent 不得自行升级这些版本**，包括"顺手升级一下"。需要升级时开 issue 并附兼容性说明，由人批准。

## 3. 目录结构

```
composeApp/
  src/commonMain/kotlin/…    # 共享 UI + 业务逻辑（改动的主战场）
  src/commonTest/kotlin/…    # 共享单元测试
  src/androidMain/kotlin/…   # Android 平台实现（expect/actual 的 actual 端）
  src/iosMain/kotlin/…       # iOS 平台实现
iosApp/                      # Xcode 壳工程（只能在 macOS 上构建）
fastlane/                    # 发版流水线
docs/                        # 方案、决策记录、上架材料
```

## 4. 常用命令

```bash
# Android（Linux / macOS 均可）
./gradlew :composeApp:assembleDebug
./gradlew :composeApp:bundleRelease        # 产出 .aab
./gradlew :composeApp:allTests             # 共享逻辑测试
./gradlew :composeApp:testDebugUnitTest    # Android 单元测试
./gradlew check                            # 提交前必跑

# iOS：以下任务只能在 macOS + Xcode 上执行
./gradlew :composeApp:compileKotlinIosSimulatorArm64
./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64
```

## 5. 环境事实（不要试图绕过）

- 开发机是**阿里云 Linux 服务器**，只能构建 Android。
- **iOS 编译必须 macOS + Xcode**，由 GitHub Actions 的 `macos-15` runner 或云 Mac 完成。
- 在 Linux 上执行任何 `*Ios*` 的 Gradle 任务都会失败——**这是预期行为，不是需要修复的 bug**。不要为此改 build 配置。
- 服务器访问 Google 服务可能不通；涉及 Play Console / Firebase 的操作走 CI。

## 6. 完成定义（Definition of Done）

一个任务只有全部满足才算完成，缺一项就如实报告"未完成"，**不许说"已完成"**：

1. 新增的共享逻辑有 `commonTest` 覆盖，且 `./gradlew check` 通过；
2. Android 端在模拟器或真机上手动跑通主路径（附截图）；
3. iOS 端至少通过 `compileKotlinIosSimulatorArm64`（有 Mac 环境时附运行截图）；
4. 没有新增 `TODO` / `FIXME` 未记录到 issue；
5. PR 描述里写清：改了什么、为什么、怎么验证的。

## 7. 禁止事项

- ❌ 直接推 `main`、`git push --force`、改写已推送的历史。
- ❌ 修改签名配置、keystore、`iosApp.xcodeproj` 的 Signing & Capabilities、`fastlane` 的密钥读取逻辑。
- ❌ 自动执行 `fastlane ios release` / `android promote`（**提审与发布必须由人触发**）。
- ❌ 把 `.p8`、`.jks`、service account JSON、`local.properties` 写进仓库或贴进对话。
- ❌ 引入新依赖而不说明理由；引入 GPL/AGPL 类许可证的库。
- ❌ 为通过编译而删除或跳过测试（`@Ignore`、`--continue`、注释掉断言）。
- ❌ 在未经确认的情况下改动数据库 schema 或网络 API 契约。

## 8. 隐私与合规（写代码时就要满足）

- 任何权限（相机、定位、通知、相册）都必须有**具体用途文案**，且只在真正用到的界面请求。
- 收集任何用户数据前先更新 `docs/privacy.md` 与隐私清单，并盘点：收集什么、存在哪、传给谁、怎么删。
- 必须有**账号删除入口**（若有账号体系），否则 Apple 5.1.1 直接拒。
- 若有用户生成内容：必须有举报 + 屏蔽 + 客服联系方式，否则 1.2 拒。
- 数字内容/订阅必须走 IAP（3.1.1），禁止引导用户去外部支付。

## 9. 协作约定

- 一次只做一件事；大改动先出**方案 + 文件清单**，等人确认再动手。
- 改动前确认 Git 工作区干净；Hermes 会自动 checkpoint，但不要依赖它。
- 多文件重构优先 `delegate_task` 拆给子 agent，但**`commonMain` 同一时间只允许一个 agent 写**，避免冲突。
- 遇到不确定的产品决策，用 `clarify` 提问，**不要自己拍板**。

## 10. 发版

流程见 `skills/kmp-release/SKILL.md`。发版永远是人说"发版"之后才开始的显式动作。
