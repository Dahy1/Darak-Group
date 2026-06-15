import { read } from "@/lib/content";
export default function Nav(){
  return <div suppressHydrationWarning dangerouslySetInnerHTML={{ __html: read("_nav.html") }} />;
}
