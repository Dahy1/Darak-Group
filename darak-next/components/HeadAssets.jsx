import { read } from "@/lib/content";
export default function HeadAssets(){
  return <div suppressHydrationWarning style={{ display: "contents" }} dangerouslySetInnerHTML={{ __html: read("_head.html") }} />;
}
