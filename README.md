# personal-album-platform

**25 期「古代名人 · 书画长卷」数字展卷** · Android + iOS + Web 三端。

> 当前状态：**工程骨架 + 内容准入机制**。业务代码尚未开始，内容清单与版权门禁已就位。

一期不做用户上传、不做账号、不做社交。内容由团队策展，**逐件登记版权后入库**。

**两套 UI，一套业务逻辑。** App 用 Compose 做沉浸式长卷浏览；Web 用 Next.js 做可被搜索引擎收录的展卷页面。业务规则只写在 `shared/` 里。

## 技术栈

- **共享逻辑**：Kotlin Multiplatform（domain / data / api，不依赖 UI 框架）
- **App UI**：Compose Multiplatform（Android + iOS）
- **Web UI**：Next.js（App Router）+ TypeScript
- **长卷浏览**：IIIF Image API + 瓦片加载
- Ktor · kotlinx.serialization · SQLDelight · Koin

## 目录

```
content/rights/            图像版权清单 + 来源机构登记（发布准入凭证）
tools/check_rights.py      清单校验脚本
shared/                    KMP 逻辑模块（唯一真相源）
composeApp/                Compose UI（Android + iOS）
web/                       Next.js Web 端
iosApp/                    Xcode 壳工程
.github/workflows/ci.yml   content / shared / web / android / ios 五个 job
fastlane/                  App 发版 lane
docs/                      路线图、Web 部署、第 1 期展卷计划
AGENTS.md                  项目契约
```

## 内容准入（硬性）

新增任何作品前，先在 `content/rights/artworks.csv` 登记，再跑：

```bash
python3 tools/check_rights.py            # 日常
python3 tools/check_rights.py --strict   # 发布前
```

只有 `status=ready` 且 `commercial_ok=yes` 的作品可以进入已发布内容。
判定规则见 [`content/rights/README.md`](content/rights/README.md)。

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

python3 tools/check_rights.py
./gradlew :shared:allTests
./gradlew :composeApp:assembleDebug
cd web && npm ci && npm run dev
```

## 发布

- App：见 [`skills/kmp-release/SKILL.md`](skills/kmp-release/SKILL.md)，**提审由人手动执行**
- Web：见 [`docs/deploy-web.md`](docs/deploy-web.md)，**部署由人手动执行**

## 许可

私有项目，未授权。
