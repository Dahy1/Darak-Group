import SiteScripts from "@/components/SiteScripts";
import { read, readJSON } from "@/lib/content";
export const dynamic = "force-static";
export default function Page(){
  const content = read("pages/projects__1000-89-st-surfside.html");
  const style = read("pages/projects__1000-89-st-surfside.style.html");
  const scripts = readJSON("pages/projects__1000-89-st-surfside.scripts.json");
  return (
    <>
      {style ? <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: style }} /> : null}
      <div suppressHydrationWarning className="oh-page-content" dangerouslySetInnerHTML={{ __html: content }} />
      <SiteScripts scripts={scripts} k="page-projects__1000-89-st-surfside" />
    </>
  );
}
