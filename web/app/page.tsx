import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { WorkCard } from "@/components/work-card";
import { works, stats, eraCount, erasCn, erasWest, byMuseum } from "@/lib/content";

const nf = new Intl.NumberFormat("zh-CN");

export default function HomePage() {
  return (
    <>
      <SiteHeader />

      <main id="top">
        {/* ---------------- Hero ---------------- */}
        <section className="hero wrap" id="catalogue">
          <div className="kicker">
            <span className="eyebrow">Catalogue Raisonné Index</span>
            <span className="eyebrow" style={{ opacity: 0.5 }}>/</span>
            <span className="eyebrow">跨文明典藏索引系统</span>
          </div>

          <h1 className="display display-xl">
            二十五期
            <br />
            古代名人书画展卷
          </h1>

          <p className="lead">
            以 IIIF 深缩放呈现中国书画长卷与西方绘画原作。每一件均登记作者、现藏地、
            图像来源与许可协议；即使协议不强制，署名仍在此完整呈现。
          </p>

          <div className="stat-row">
            <div className="stat">
              <div className="num display">{nf.format(stats.total)}</div>
              <div className="cap">在册作品 / Works</div>
            </div>
            <div className="stat">
              <div className="num display">{nf.format(stats.artists)}</div>
              <div className="cap">艺术家 / Artists</div>
            </div>
            <div className="stat">
              <div className="num display">{nf.format(stats.museums)}</div>
              <div className="cap">收藏机构 / Institutions</div>
            </div>
            <div className="stat">
              <div className="num display">{nf.format(stats.ready)}</div>
              <div className="cap">已核验可发布</div>
            </div>
          </div>

          <div className="filters" aria-label="当前筛选条件">
            <span className="chip">
              期次 <i>第 {stats.episodes} 期 · 基石</i>
            </span>
            <span className="chip">
              开放协议 <i>CC0 / PDM / 待核验</i>
            </span>
            <span className="chip">
              状态 <i>{stats.pending} 件待核验</i>
            </span>
          </div>

          <div className="notice">
            <b>预览版</b>
            <span>
              本页为设计还原稿。工作状态为「待核验」的作品暂不对外发布，图像将在权利登记完成后接入。
            </span>
          </div>
        </section>

        {/* ---------------- Taxonomy ---------------- */}
        <section className="section wrap" id="taxonomy">
          <div className="section-head">
            <div>
              <span className="eyebrow">01 / Taxonomy Matrices</span>
              <h2 className="headline-lg">多维分类视域</h2>
            </div>
            <span className="eyebrow muted">点击切换维度</span>
          </div>

          <div className="taxonomy">
            <div className="tax-col">
              <h3>中国历代断代</h3>
              {eraCount(erasCn).map((e) => (
                <div className="tax-row" key={e.label}>
                  <span className="k">{e.label}</span>
                  <span className="v">{e.count} 件</span>
                </div>
              ))}
            </div>

            <div className="tax-col">
              <h3>西方艺术史分期</h3>
              {eraCount(erasWest).map((e) => (
                <div className="tax-row" key={e.label}>
                  <span className="k">{e.label}</span>
                  <span className="v">{e.count} 件</span>
                </div>
              ))}
            </div>

            <div className="tax-col">
              <h3>收藏机构源</h3>
              {byMuseum.map((m) => (
                <div className="tax-row" key={m.label}>
                  <span className="k">{m.label}</span>
                  <span className="v">{m.count} 件</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ---------------- Works ---------------- */}
        <section className="section wrap" id="works">
          <div className="section-head">
            <div>
              <span className="eyebrow">02 / Masterwork Archives</span>
              <h2 className="headline-lg">精选馆藏名作</h2>
            </div>
            <span className="eyebrow muted">
              {stats.total} 件 · 第 {stats.episodes} 期
            </span>
          </div>

          <div className="works">
            {works.map((w) => (
              <WorkCard key={w.id} work={w} />
            ))}
          </div>
        </section>

        {/* ---------------- Rights ---------------- */}
        <section className="section wrap" id="rights">
          <div className="section-head">
            <div>
              <span className="eyebrow">03 / Rights & Provenance</span>
              <h2 className="headline-lg">权利与来源</h2>
            </div>
          </div>
          <p className="lead" style={{ maxWidth: "60ch" }}>
            开放不等于无主。每件作品页面均标注作者、现藏地、图像来源链接与许可协议；
            CC0 作品亦保留署名，以尊重著作人身权。任何未完成权利登记的作品不进入发布内容。
          </p>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}
