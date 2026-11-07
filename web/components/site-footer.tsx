const STANDARDS = [
  "IIIF Presentation API 3.0",
  "CIDOC CRM Ontologies",
  "Getty AAT / ULAN Linked Data",
  "Dublin Core Metadata Standard",
];

const PARTNERS = [
  "The Metropolitan Museum of Art",
  "Cleveland Museum of Art",
  "Art Institute of Chicago",
  "Rijksmuseum Amsterdam",
  "国立故宫博物院",
];

export function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="wrap">
        <div className="footer-grid">
          <div className="footer-col">
            <span className="headline-sm" style={{ letterSpacing: "0.14em", textTransform: "uppercase" }}>
              Lumière Archive Foundation
            </span>
            <p>
              以 IIIF 光栅流式传输与学术级考据，保存并开放世界文化遗产的影像与文献。
              所有入藏影像均逐件登记权利状态，署名与来源在前台完整可见。
            </p>
          </div>
          <div className="footer-col">
            <h4>学术标准</h4>
            <ul>
              {STANDARDS.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </div>
          <div className="footer-col">
            <h4>合作机构</h4>
            <ul>
              {PARTNERS.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          </div>
        </div>
        <div className="footer-base">
          <span>© 2026 Lumière Archive · Open Access CC0 / PDM</span>
          <span className="footer-links">
            <a href="#rights">权利与来源</a>
            <a href="#catalogue">IIIF Manifest Registry</a>
          </span>
        </div>
      </div>
    </footer>
  );
}
