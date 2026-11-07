> 本目录是**发布的准入凭证**，不是参考资料。
> 没有出现在 `artworks.csv` 里的作品，不得出现在任何一期内容中。

# 图像版权清单

## 为什么是 CSV

- 你可以在 Excel / Numbers 里直接维护，不用写代码
- Git 能看 diff，谁改了哪一行一目了然
- CI 能校验，漏填直接卡住合并

## 两个文件

| 文件 | 作用 |
| --- | --- |
| `artworks.csv` | 逐件作品的权利登记（**发布准入凭证**） |
| `sources.csv` | 来源机构登记：默认授权基调、条款地址 |

`artworks.csv` 的 `source` 列必须能在 `sources.csv` 里找到，否则 CI 报错。

## 字段说明

| 字段 | draft | ready | 说明 |
| --- | --- | --- | --- |
| `status` | ✅ | ✅ | `draft`（在研）/ `ready`（可发布） |
| `id` | ✅ | ✅ | 唯一标识，全小写 |
| `episode` | ✅ | ✅ | 期号，形如 `E01` |
| `artist` | ✅ | ✅ | ① 作者 |
| `artist_years` | | | 生卒年 |
| `title_zh` | ✅ | ✅ | ① 作品名 |
| `title_en` | | | 英文名（Web SEO） |
| `museum` | ✅ | ✅ | 现藏地（**必须逐件核对**） |
| `source` | ✅ | ✅ | 来源代码，须在 `sources.csv` 登记 |
| `license` | ✅ | ✅ | 见协议枚举 |
| `license_marker` | | ✅ | ③ 授权标识：`CC0` / `PDM` / `CC-BY-4.0` / `FAITHFUL_REPRO` / `INSTITUTIONAL` / `NONE` |
| `commercial_ok` | | ✅ | `yes` / `no` / `unknown` |
| `source_page_url` | | ✅ | ② 人可核验的作品页 |
| `image_url` | | ✅ | ② 图片直链 |
| `license_url` | | ✅ | ③ 协议原文 |
| `credit_line` | | ✅ | 署名文案，必须在前台可见 |
| `accessed_date` | | ✅ | ④ 获取日期 `YYYY-MM-DD` |
| `checked_by` | | ✅ | 核实人 |
| `notes` | | | 限制、待办、更正记录 |

## 许可协议枚举与判定

| 值 | 含义 | 可商用 | 可上架 |
| --- | --- | --- | --- |
| `PD` | 公有领域（作者逝世逾版权期） | ✅ | ✅ |
| `PDM` | Public Domain Mark | ✅ | ✅ |
| `CC0-1.0` | 放弃全部权利 | ✅ | ✅ |
| `CC-BY-4.0` | 署名即可 | ✅ | ✅（必须署名） |
| `CC-BY-SA-4.0` | 署名 + 相同方式共享 | ⚠️ | ✅（改编需同协议） |
| `CC-BY-NC-4.0` | 禁止商用 | ❌ | ❌ |
| `CC-BY-ND-4.0` | 禁止改编 | ⚠️ | ❌（裁切/缩放可能被视为改编） |
| `ARR` | 保留所有权利 | ❌ | ❌ |
| `UNKNOWN` | 未核实 | ❌ | ❌ |

**规则：`commercial_ok=yes` 只允许搭配 PD / PDM / CC0 / CC-BY / CC-BY-SA。** 其他组合会被 CI 判为矛盾。

## 来源风险分级

| 代码 | 机构 | 基调 |
| --- | --- | --- |
| `MET` `CMA` `AIC` `RIJKS` | 大都会 / 克利夫兰 / 芝加哥 / 荷兰国立 | 🟢 CC0 |
| `GETTY` | 盖蒂 | 🟡 逐件确认 |
| `NPM` | 台北故宫 | 🟡 政府资料开放授权（**非 CC0**），必须署名 |
| `DPM` `BM` | 北京故宫 / 大英博物馆 | 🔴 禁商用，须换来源或取得授权 |
| `LOUVRE` `UFFIZI` `VATICAN` `PRADO` `ACCADEMIA` `MAURITSHUIS` `TNM` | 各馆官网 | 🔴 条款受限 |
| `COMMONS` | 维基共享资源 | ⚪ 聚合层，**不是来源**，必须回溯馆方页面 |

> ⚠️ 古代画作本身是公有领域，**但博物馆拍摄的数字化照片可能另有权利**。清单记录的是"图像来源"，不是"作者"。

## 三种状态

- **`ready` + `commercial_ok=yes`**：可进正式内容
- **`draft`**：允许存在（方便登记在研作品），但**不得被任何一期引用**
- **`UNKNOWN`**：`ready` 状态下直接判错；`draft` 状态下视为不可发布

## 怎么加一条

1. 在 `sources.csv` 确认来源代码已登记
2. 打开作品页，找到版权声明区（通常页脚）
3. 核对**现藏地**——画错馆，许可判断就会跟着错
4. 按枚举判定 `license` 与 `commercial_ok`，填 `image_url` 与 `accessed_date`
5. 提交 PR，CI 会校验格式与矛盾

## CI 门禁

```bash
python3 tools/check_rights.py                  # 日常校验
python3 tools/check_rights.py --episode E01    # 只看某一期
python3 tools/check_rights.py --strict         # 发布前：必须全部 ready 且可商用
```
