#!/usr/bin/env python3
"""生成 web/preview.html —— 无需 Node 即可在浏览器查看版式。

与 Next 页面共用同一份 globals.css 与 artworks.json，
仅用于查看设计还原效果，不作为正式产物。
"""

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "web" / "data" / "artworks.json"
CSS = ROOT / "web" / "app" / "globals.css"
OUT = ROOT / "web" / "preview.html"

CN_ERAS = ["东晋", "隋", "北宋", "元"]
WEST_ERAS = ["文艺复兴早期", "盛期文艺复兴", "巴洛克", "荷兰黄金时代", "印象派", "后印象派"]


def esc(x: str) -> str:
    return html.escape(x or "", quote=True)


def main() -> None:
    works = json.loads(DATA.read_text(encoding="utf-8"))
    css = CSS.read_text(encoding="utf-8")

    total = len(works)
    artists = len({w["artist"] for w in works})
    museums = len({w["museum"] for w in works})
    ready = sum(1 for w in works if w["status"] == "ready")

    era_c = Counter(w["era"] for w in works)
    museum_c = Counter(w["museum"] for w in works)

    def tax(rows):
        return "".join(
            f'<div class="tax-row"><span class="k">{esc(k)}</span>'
            f'<span class="v">{v} 件</span></div>'
            for k, v in rows
        )

    cn_rows = [(e, era_c.get(e, 0)) for e in CN_ERAS]
    west_rows = [(e, era_c.get(e, 0)) for e in WEST_ERAS]
    museum_rows = museum_c.most_common()

    cards = "".join(f'''
      <article class="card">
        <div class="thumb"><span class="ph">图像待接入<br>{esc(w["titleEn"] or w["titleZh"])}</span></div>
        <div class="meta"><span>{esc(w["era"])}</span><span>{"中国" if w["region"] == "CN" else "西方"}</span></div>
        <h3>{esc(w["titleZh"])}</h3>
        <span class="sub">{esc(w["titleEn"])}</span>
        <div class="credit">
          <span>{esc(w["artist"])}{"（" + esc(w["artistYears"]) + "）" if w["artistYears"] else ""}</span>
          <span>{esc(w["museum"])}</span>
        </div>
        <span class="lic{" " if w["status"] == "ready" else " pending"}">{"已核验" if w["status"] == "ready" else "权利待核验"}</span>
      </article>''' for w in works)

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lumière Archive · 设计还原预览</title>
<style>
{css}
.preview-flag{{position:fixed;right:1rem;bottom:1rem;z-index:99;background:#1a1c1c;color:#f9f9f9;
font-size:.625rem;letter-spacing:.14em;text-transform:uppercase;padding:.375rem .625rem;opacity:.85}}
</style>
</head>
<body>
<header class="site-header">
  <div class="wrap bar">
    <div style="display:flex;align-items:center;gap:3rem">
      <a class="brand" href="#top"><strong>Lumière Archive</strong><span>文化遗产数字典藏</span></a>
      <nav class="nav">
        <a href="#catalogue" aria-current="page">探索与检索 (Explore &amp; Search)</a>
        <a href="#works">IIIF 深度浏览 (Deep Zoom &amp; Scrolls)</a>
        <a href="#taxonomy">策展专论 (Curatorial Dossiers)</a>
      </nav>
    </div>
    <div class="tools">
      <span class="badge"><span class="dot"></span>IIIF v3.0</span>
      <button class="search-btn" type="button">检索 <kbd style="opacity:.6">⌘K</kbd></button>
      <span class="lang"><b>ZH</b> / EN</span>
    </div>
  </div>
</header>

<main id="top">
  <section class="hero wrap" id="catalogue">
    <div class="kicker">
      <span class="eyebrow">Catalogue Raisonné Index</span>
      <span class="eyebrow" style="opacity:.5">/</span>
      <span class="eyebrow">跨文明典藏索引系统</span>
    </div>
    <h1 class="display display-xl">二十五期<br>古代名人书画展卷</h1>
    <p class="lead">以 IIIF 深缩放呈现中国书画长卷与西方绘画原作。每一件均登记作者、现藏地、图像来源与许可协议；即使协议不强制，署名仍在此完整呈现。</p>
    <div class="stat-row">
      <div class="stat"><div class="num display">{total}</div><div class="cap">在册作品 / Works</div></div>
      <div class="stat"><div class="num display">{artists}</div><div class="cap">艺术家 / Artists</div></div>
      <div class="stat"><div class="num display">{museums}</div><div class="cap">收藏机构 / Institutions</div></div>
      <div class="stat"><div class="num display">{ready}</div><div class="cap">已核验可发布</div></div>
    </div>
    <div class="filters">
      <span class="chip">期次 <i>第 1 期 · 基石</i></span>
      <span class="chip">开放协议 <i>CC0 / PDM / 待核验</i></span>
      <span class="chip">状态 <i>{total - ready} 件待核验</i></span>
    </div>
    <div class="notice"><b>预览版</b><span>本页为设计还原稿。工作状态为「待核验」的作品暂不对外发布，图像将在权利登记完成后接入。</span></div>
  </section>

  <section class="section wrap" id="taxonomy">
    <div class="section-head">
      <div><span class="eyebrow">01 / Taxonomy Matrices</span><h2 class="headline-lg">多维分类视域</h2></div>
      <span class="eyebrow muted">点击切换维度</span>
    </div>
    <div class="taxonomy">
      <div class="tax-col"><h3>中国历代断代</h3>{tax(cn_rows)}</div>
      <div class="tax-col"><h3>西方艺术史分期</h3>{tax(west_rows)}</div>
      <div class="tax-col"><h3>收藏机构源</h3>{tax(museum_rows)}</div>
    </div>
  </section>

  <section class="section wrap" id="works">
    <div class="section-head">
      <div><span class="eyebrow">02 / Masterwork Archives</span><h2 class="headline-lg">精选馆藏名作</h2></div>
      <span class="eyebrow muted">{total} 件 · 第 1 期</span>
    </div>
    <div class="works">{cards}</div>
  </section>

  <section class="section wrap" id="rights">
    <div class="section-head"><div><span class="eyebrow">03 / Rights &amp; Provenance</span><h2 class="headline-lg">权利与来源</h2></div></div>
    <p class="lead" style="max-width:60ch">开放不等于无主。每件作品页面均标注作者、现藏地、图像来源链接与许可协议；CC0 作品亦保留署名，以尊重著作人身权。任何未完成权利登记的作品不进入发布内容。</p>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <span class="headline-sm" style="letter-spacing:.14em;text-transform:uppercase">Lumière Archive Foundation</span>
        <p>以 IIIF 光栅流式传输与学术级考据，保存并开放世界文化遗产的影像与文献。所有入藏影像均逐件登记权利状态，署名与来源在前台完整可见。</p>
      </div>
      <div class="footer-col"><h4>学术标准</h4><ul>
        <li>IIIF Presentation API 3.0</li><li>CIDOC CRM Ontologies</li>
        <li>Getty AAT / ULAN Linked Data</li><li>Dublin Core Metadata Standard</li>
      </ul></div>
      <div class="footer-col"><h4>合作机构</h4><ul>
        <li>The Metropolitan Museum of Art</li><li>Cleveland Museum of Art</li>
        <li>Art Institute of Chicago</li><li>Rijksmuseum Amsterdam</li><li>国立故宫博物院</li>
      </ul></div>
    </div>
    <div class="footer-base">
      <span>© 2026 Lumière Archive · Open Access CC0 / PDM</span>
      <span class="footer-links"><a href="#rights">权利与来源</a><a href="#catalogue">IIIF Manifest Registry</a></span>
    </div>
  </div>
</footer>
<div class="preview-flag">设计还原预览 · 无数据核验</div>
</body>
</html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"→ {OUT.relative_to(ROOT)}（{len(doc)//1024} KB）")


if __name__ == "__main__":
    main()
