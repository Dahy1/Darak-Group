import SiteScripts from "@/components/SiteScripts";
import { read, readJSON } from "@/lib/content";
export const dynamic = "force-static";
export default function Page(){
  const content = read("pages/blog.html");
  const style = read("pages/blog.style.html");
  const scripts = readJSON("pages/blog.scripts.json");
  return (
    <>
      {style ? <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: style }} /> : null}
      <div suppressHydrationWarning className="oh-page-content" dangerouslySetInnerHTML={{ __html: content }} />
      <SiteScripts scripts={scripts} k="page-blog" />
    </>
  );
}
