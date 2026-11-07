import raw from "@/data/artworks.json";

export type Work = {
  id: string;
  episode: string;
  artist: string;
  artistYears: string;
  titleZh: string;
  titleEn: string;
  museum: string;
  source: string;
  license: string;
  licenseMarker: string;
  commercialOk: string;
  status: "draft" | "ready";
  era: string;
  region: "CN" | "WEST";
  imageUrl: string;
  creditLine: string;
};

export const works: Work[] = raw as Work[];

export const stats = (() => {
  const artists = new Set(works.map((w) => w.artist));
  const museums = new Set(works.map((w) => w.museum));
  const ready = works.filter((w) => w.status === "ready");
  return {
    total: works.length,
    artists: artists.size,
    museums: museums.size,
    ready: ready.length,
    pending: works.length - ready.length,
    episodes: new Set(works.map((w) => w.episode)).size,
  };
})();

/** 按维度分组计数：只统计真实存在于清单中的条目 */
export function groupBy(pick: (w: Work) => string) {
  const map = new Map<string, number>();
  for (const w of works) {
    const key = pick(w);
    map.set(key, (map.get(key) ?? 0) + 1);
  }
  return [...map.entries()]
    .sort((a, b) => b[1] - a[1])
    .map(([label, count]) => ({ label, count }));
}

export const erasCn = ["东晋", "隋", "北宋", "元"];
export const erasWest = ["文艺复兴早期", "盛期文艺复兴", "巴洛克", "荷兰黄金时代", "印象派", "后印象派"];

export const byEra = groupBy((w) => w.era);
export const byMuseum = groupBy((w) => w.museum);

export function eraCount(list: string[]) {
  const m = new Map(byEra.map((e) => [e.label, e.count]));
  return list.map((label) => ({ label, count: m.get(label) ?? 0 }));
}
