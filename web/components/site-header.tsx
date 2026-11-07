const NAV = [
  { href: "#catalogue", label: "探索与检索", en: "Explore & Search", current: true },
  { href: "#works", label: "IIIF 深度浏览", en: "Deep Zoom & Scrolls" },
  { href: "#taxonomy", label: "策展专论", en: "Curatorial Dossiers" },
];

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="wrap bar">
        <div style={{ display: "flex", alignItems: "center", gap: "3rem" }}>
          <a className="brand" href="#top" aria-label="Lumière Archive 首页">
            <strong>Lumière Archive</strong>
            <span>文化遗产数字典藏</span>
          </a>
          <nav className="nav" aria-label="主导航">
            {NAV.map((item) => (
              <a key={item.href} href={item.href} aria-current={item.current ? "page" : undefined}>
                {item.label} ({item.en})
              </a>
            ))}
          </nav>
        </div>

        <div className="tools">
          <span className="badge">
            <span className="dot" aria-hidden />
            IIIF v3.0
          </span>
          <button className="search-btn" type="button" aria-label="检索馆藏">
            检索 <kbd style={{ opacity: 0.6 }}>⌘K</kbd>
          </button>
          <span className="lang" aria-label="语言切换">
            <b>ZH</b> / EN
          </span>
        </div>
      </div>
    </header>
  );
}
