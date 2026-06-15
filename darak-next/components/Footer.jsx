import { read } from "@/lib/content";
export default function Footer(){
  return <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: read("_footer.html") }} />;
}
