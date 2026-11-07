# AGENTS.md — 三端应用（Android / iOS / Web）

> 本文件是 Hermes Agent 的项目契约。动手前必须先读它。
> 子 agent（`delegate_task`）同样会收到本文件，规则同样有约束力。

## 1. 项目定位

个人相册平台：**Android + iOS + Web 三端**。

**两套 UI，一套业务逻辑。** App 端用 Compose 写原生体验；Web 端用 DOM 写可被搜索引擎和分享卡片看见的页面。这不是妥协，是刻意设计——Canvas 渲染的 UI 拿不到 SEO。

成功标准不是"代码写完"，而是"双端过审 + Web 可被收录"。

## 2. 技术栈（版本已锁定）

| 层 | 选型 |
| --- | --- |
| 共享逻辑 | Kotlin Multiplatform：`domain` / `data` / `api`，**不依赖任何 UI 框架** |
| App UI | Compose Multiplatform（Android + iOS） |
| Web UI | Next.js（App Router）+ TypeScript |
| 网络 | Ktor Client + `kotlinx.serialization` |
| 本地存储 | SQLDelight（App）；Web 用浏览器存储，不直接碰数据库 |
| DI | Koin（App）；Web 用显式依赖注入，不引 Koin |
| 图片 | Coil 3（App）；Web 用 `next/image` + CDN |
| 内购 | RevenueCat KMP SDK（App 专属） |
| 测试 | `kotlin.test` + Turbine；Web 用 Vitest |

**版本策略：锁定即冻结。**
Kotlin / AGP / Gradle / CMP / Next.js 的版本必须成套兼容。**任何 agent 不得自行升级**，需要升级时开 issue 附兼容性说明，由人批准。

## 3. 目录结构

```
shared/                     # 纯 KMP 逻辑模块，可编译到 JVM / iOS / JS
  src/commonMain/kotlin/    # 业务规则、数据模型、API 客户端（唯一真相源）
  src/commonTest/kotlin/
  src/jsMain/               # 供 web 消费的 JS 入口
composeApp/                 # Compose UI
  src/commonMain/kotlin/    # 共享 UI（两端一样的部分）
  src/androidMain/kotlin/
  src/iosMain/kotlin/
web/                        # Next.js（App Router）
  src/app/                  # 路由与页面
  src/lib/                  # 轻量适配层，调用 shared 编译出的 JS
iosApp/                     # Xcode 壳工程（只能 macOS 构建）
fastlane/                   # App 发版流水线
docs/
```

**依赖方向单向**：`web` / `composeApp` → `shared`。`shared` 不得反向依赖任何 UI 模块。

## 4. 常用命令

```bash
# 共享逻辑（三端共用）
./gradlew :shared:allTests
./gradlew :shared:jsProductionLibraryDistribution   # 产出供 web 使用的 JS

# App
./gradlew :composeApp:assembleDebug
./gradlew :composeApp:bundleRelease
./gradlew check

# iOS：只能在 macOS + Xcode 执行
./gradlew :composeApp:compileKotlinIosSimulatorArm64

# Web
cd web && npm ci && npm run dev
cd web && npm run build && npm run lint && npm run test
```

## 5. 环境事实（不要试图绕过）

- 开发机是**阿里云 Linux 服务器**：可构建 Android、共享逻辑、Web；**不能构建 iOS**。
- iOS 编译必须 macOS + Xcode，由 GitHub Actions `macos-15` runner 承担。
- Linux 上执行任何 `*Ios*` 的 Gradle 任务都会失败——**这是预期行为，不是 bug**。不要为此改 build 配置。
- 服务器访问 Google 服务可能不通；Play Console / Firebase 相关操作走 CI。

## 6. 两套 UI 的边界（最容易写坏的地方）

**必须放 `shared` 的**：
- 数据模型、序列化、API 调用与重试
- 业务规则：排序、分页、可见性、权限判断、上传队列状态机
- 校验与格式化（日期、尺寸、文件大小）

**可以各端各写的**：
- 布局、动画、交互手势
- 路由与导航
- 平台能力：相册权限、文件选择、分享、推送

**绝对禁止**：
- 在 `web/` 里重写一遍业务规则（这是三端不一致的头号原因）
- 在 `shared` 里 `import` Compose 或 React
- 用一个 `if (isWeb) ... else ...` 把两端行为糅在一个函数里

判断标准：**"这条规则如果 Web 和 App 不一致，用户会不会觉得是 bug？"** 会 → 放 `shared`。

## 7. Web 端硬性要求

- 每个公开页面必须有 **OG / Twitter Card meta**（标题、描述、封面图），否则分享出去是白板。
- 图片一律走 CDN + `next/image`，禁止 `background-image` 加载大图。
- 分享页必须 **SSR/SSG**，不能是纯客户端渲染。
- 首屏 LCP < 2.5s，超出视为未完成。
- 无障碍：语义标签、`alt`、键盘可达。

## 8. 完成定义（Definition of Done）

缺一项就如实报告"未完成"，**不许说"已完成"**：

1. `shared` 新增逻辑有 `commonTest` 覆盖，`./gradlew check` 通过；
2. Web 端 `npm run build` + `npm run lint` 通过；
3. Android 主路径在手/模拟器跑通（附截图）；
4. iOS 至少通过 `compileKotlinIosSimulatorArm64`（有 Mac 时附运行截图）；
5. 涉及公开页面时，验证过分享卡片的 meta 标签；
6. PR 描述写清：改了什么、为什么、怎么验证的。

## 9. 禁止事项

- ❌ 直接推 `main`、`git push --force`、改写已推送历史。
- ❌ 修改签名配置、keystore、`iosApp.xcodeproj` 的签名设置、`fastlane` 的密钥读取逻辑。
- ❌ 自动执行 `fastlane ios release` / `android promote`（提审与发布必须由人触发）。
- ❌ 把 `.p8`、`.jks`、service account JSON、`.env` 写进仓库或贴进对话。
- ❌ 引入新依赖不说明理由；引入 GPL/AGPL 类许可证的库。
- ❌ 为通过编译而删测试、`@Ignore`、注释掉断言。
- ❌ 未经确认改动数据库 schema 或 API 契约。
- ❌ `shared` 依赖 UI 框架。

## 10. 隐私与合规

- 权限（相册、相机、定位、通知）必须有具体用途文案，只在真正用到的界面请求。
- **EXIF 中的 GPS 坐标属于敏感数据**：上传前默认剥离，或在 UI 明确告知并提供开关。
- 收集数据前更新 `docs/privacy.md` 与隐私清单：收集什么、存哪、传给谁、怎么删。
- 有账号体系就必须有**账号删除**入口（Apple 5.1.1）。
- 有用户生成内容就必须有举报 + 屏蔽 + 联系方式（1.2）。
- 数字内容/订阅必须走 IAP（3.1.1），禁止引导外部支付。

## 11. 协作约定

- 一次只做一件事；大改动先出方案 + 文件清单，等人确认再动手。
- 改动前确认 Git 工作区干净。
- 多文件重构可 `delegate_task` 拆分，但**同一模块同一时间只允许一个 agent 写**。
- 不确定的产品决策用 `clarify` 提问，不要自己拍板。

## 12. 发版

App 流程见 `skills/kmp-release/SKILL.md`。
Web 部署见 `docs/deploy-web.md`，由人执行，agent 不自动上线。
