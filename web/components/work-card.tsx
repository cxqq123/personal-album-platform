import type { Work } from "@/lib/content";

const REGION_LABEL: Record<string, string> = { CN: "中国", WEST: "西方" };

export function WorkCard({ work }: { work: Work }) {
  const verified = work.status === "ready";
  return (
    <article className="card">
      <div className="thumb" role="img" aria-label={`${work.titleZh} · 图像待接入`}>
        <span className="ph">
          图像待接入
          <br />
          {work.titleEn || work.titleZh}
        </span>
      </div>

      <div className="meta">
        <span>{work.era}</span>
        <span>{REGION_LABEL[work.region] ?? "—"}</span>
      </div>

      <h3>{work.titleZh}</h3>
      <span className="sub">{work.titleEn}</span>

      <div className="credit">
        <span>
          {work.artist}
          {work.artistYears ? `（${work.artistYears}）` : ""}
        </span>
        <span>{work.museum}</span>
      </div>

      <span className={`lic${verified ? "" : " pending"}`}>
        {verified ? work.licenseMarker || work.license : "权利待核验"}
      </span>
    </article>
  );
}
