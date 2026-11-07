#!/usr/bin/env python3
"""把 content/rights/artworks.csv 转成 web/data/artworks.json。

Web 端不直接读 CSV：CSV 是给人维护的，JSON 是给构建用的。
每次改动清单后运行：python3 tools/build_web_content.py
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "rights" / "artworks.csv"
OUT = ROOT / "web" / "data" / "artworks.json"

# 编年与地域：入档元数据，不是统计口径
META = {
    "顾恺之（传）": ("东晋", "CN"), "展子虔（传）": ("隋", "CN"),
    "范宽": ("北宋", "CN"), "郭熙": ("北宋", "CN"), "张择端": ("北宋", "CN"),
    "王希孟": ("北宋", "CN"), "李公麟": ("北宋", "CN"), "赵佶（宋徽宗）": ("北宋", "CN"),
    "黄公望": ("元", "CN"), "倪瓒": ("元", "CN"),
    "波提切利": ("文艺复兴早期", "WEST"), "达·芬奇": ("盛期文艺复兴", "WEST"),
    "米开朗基罗": ("盛期文艺复兴", "WEST"), "拉斐尔": ("盛期文艺复兴", "WEST"),
    "伦勃朗": ("巴洛克", "WEST"), "维米尔": ("荷兰黄金时代", "WEST"),
    "鲁本斯": ("巴洛克", "WEST"), "委拉斯开兹": ("巴洛克", "WEST"),
    "莫奈": ("印象派", "WEST"), "梵高": ("后印象派", "WEST"),
}


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig")))
    out = []
    for r in rows:
        era, region = META.get(r["artist"].strip(), ("待定", "CN"))
        out.append({
            "id": r["id"],
            "episode": r["episode"],
            "artist": r["artist"],
            "artistYears": r.get("artist_years", ""),
            "titleZh": r["title_zh"],
            "titleEn": r.get("title_en", ""),
            "museum": r["museum"],
            "source": r["source"],
            "license": r["license"],
            "licenseMarker": r.get("license_marker", ""),
            "commercialOk": r.get("commercial_ok", ""),
            "status": r["status"],
            "era": era,
            "region": region,
            "imageUrl": r.get("image_url", ""),
            "creditLine": r.get("credit_line", ""),
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(out)} 件 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
