import re, glob, os

FOOTER_OPEN = re.compile(r'<footer data-elementor-type="footer" data-elementor-id="738"[^>]*>')
EXISTING_STYLE = re.compile(r'\n?<style id="oh-footer-redesign">.*?</style>', re.S)

STYLE = '''<style id="oh-footer-redesign">
/* ===== Darak Group footer — light redesign ===== */
.elementor-738{background:#ffffff !important;color:#111111;position:relative;overflow:hidden;
  border-top:1px solid rgba(0,0,0,.10);font-family:'Helvetica Neue',Arial,sans-serif;}
.elementor-738 .elementor-element-c570aa1,
.elementor-738 .elementor-element-13b84fe{background:transparent !important;background-color:transparent !important;}
.elementor-738 .elementor-element-13b84fe{max-width:1520px;margin-left:auto;margin-right:auto;display:block !important;
  padding:clamp(30px,5vh,56px) clamp(22px,5vw,80px) clamp(20px,3vh,34px) !important;}

/* logo */
.elementor-738 .elementor-element-c570aa1{max-width:1520px;margin-left:auto;margin-right:auto;
  padding:clamp(54px,8vh,100px) clamp(22px,5vw,80px) 0 !important;}
.elementor-738 .elementor-element-c570aa1 .e-con-inner{align-items:center;text-align:center;}
.elementor-738 .elementor-element-71f9dc2{text-align:center;width:100% !important;}
.elementor-738 .elementor-element-71f9dc2 a{display:inline-block;}
.elementor-738 .elementor-element-71f9dc2 img{width:auto !important;height:clamp(38px,4.4vw,58px) !important;}

/* tagline — original size, centered (text-align scoped to the heading so columns stay left) */
.elementor-738 .elementor-element-6773913{max-width:none !important;align-items:center !important;}
.elementor-738 .elementor-element-3029788{align-self:center !important;margin-left:auto !important;margin-right:auto !important;}
.elementor-738 .elementor-element-3029788 .elementor-heading-title{
  font-family:'Gallient',Georgia,serif !important;font-weight:400 !important;
  color:#111111 !important;margin:0 auto;text-align:center !important;}
.elementor-738 .elementor-element-3029788 .elementor-heading-title span{color:#9a9a9a !important;}

/* divider */
.elementor-738 .elementor-element-344d8ac{margin:clamp(30px,4.5vh,52px) 0 0 !important;}
.elementor-738 .elementor-divider{padding:0 !important;}
.elementor-738 .elementor-divider-separator{border-top:1px solid rgba(0,0,0,.14) !important;}

/* columns grid */
.elementor-738 .elementor-element-fb9749f{display:grid !important;
  grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(26px,3vw,54px);
  padding:clamp(38px,6vh,66px) 0 0 !important;align-items:start;width:100%;text-align:left !important;}
.elementor-738 .elementor-element-fb9749f > .elementor-element{width:auto !important;}

/* column headings */
.elementor-738 h6.elementor-heading-title{font-family:'Helvetica Neue',Arial,sans-serif !important;
  font-size:11px !important;letter-spacing:.2em !important;text-transform:uppercase !important;
  color:rgba(17,17,17,.45) !important;margin:0 0 20px !important;font-weight:600 !important;}

/* lists & links */
.elementor-738 .elementor-icon-list-items{margin:0;padding:0;list-style:none;}
.elementor-738 .elementor-icon-list-item{margin:0 0 11px !important;padding:0 !important;border:none !important;}
.elementor-738 .elementor-icon-list-text{color:rgba(17,17,17,.74);font-size:15px;line-height:1.5;letter-spacing:.005em;}
.elementor-738 .elementor-icon-list-item > a{display:inline-block;text-decoration:none;}
.elementor-738 .elementor-icon-list-item > a .elementor-icon-list-text{
  background-image:linear-gradient(#111,#111);background-repeat:no-repeat;
  background-position:0 100%;background-size:0% 1px;padding-bottom:3px;
  transition:background-size .45s cubic-bezier(.16,1,.3,1),color .3s ease;}
.elementor-738 .elementor-icon-list-item > a:hover .elementor-icon-list-text{color:#111;background-size:100% 1px;}

/* social icons -> outlined circular buttons */
.elementor-738 .uc_social-buttons{display:flex;gap:12px;margin-top:24px;}
.elementor-738 .uc_social-button{width:44px !important;height:44px !important;border-radius:50% !important;
  border:1px solid rgba(0,0,0,.22) !important;background:#ffffff !important;box-shadow:none !important;
  color:#111111 !important;display:inline-flex !important;align-items:center;justify-content:center;
  transition:background .35s ease,border-color .35s ease,transform .35s ease,color .35s ease !important;}
.elementor-738 .uc_social-button::before{display:none !important;}
.elementor-738 .uc_social-button svg{width:18px;height:18px;fill:currentColor;display:block;}
.elementor-738 .uc_social-button:hover{background:#111111 !important;border-color:#111111 !important;transform:translateY(-2px);color:#ffffff !important;}

/* copyright bar (repurposed credit element) */
.elementor-738 .elementor-element-87e31c3{max-width:1520px;margin:clamp(30px,4.5vh,52px) auto 0 !important;
  padding:22px clamp(22px,5vw,80px) clamp(26px,4vh,40px) !important;border-top:1px solid rgba(0,0,0,.12);}
.elementor-738 .elementor-element-87e31c3 .elementor-heading-title{font-family:'Helvetica Neue',Arial,sans-serif !important;
  font-size:12px !important;letter-spacing:.16em !important;text-transform:uppercase !important;
  color:rgba(17,17,17,.46) !important;text-align:center !important;font-weight:400 !important;margin:0;}
.elementor-738 .elementor-element-87e31c3 .elementor-heading-title a{color:inherit !important;text-decoration:none;cursor:default;}

@media (max-width:900px){
  .elementor-738 .elementor-element-fb9749f{grid-template-columns:1fr 1fr;gap:34px 26px;}
}
@media (max-width:560px){
  .elementor-738 .elementor-element-fb9749f{grid-template-columns:1fr;gap:30px;}
}
</style>'''

IG_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zm0 1.62c-3.15 0-3.5.01-4.74.07-.99.05-1.53.21-1.89.35-.47.18-.81.4-1.17.76-.36.36-.58.7-.76 1.17-.14.36-.3.9-.35 1.89-.06 1.24-.07 1.59-.07 4.74s.01 3.5.07 4.74c.05.99.21 1.53.35 1.89.18.47.4.81.76 1.17.36.36.7.58 1.17.76.36.14.9.3 1.89.35 1.24.06 1.59.07 4.74.07s3.5-.01 4.74-.07c.99-.05 1.53-.21 1.89-.35.47-.18.81-.4 1.17-.76.36-.36.58-.7.76-1.17.14-.36.3-.9.35-1.89.06-1.24.07-1.59.07-4.74s-.01-3.5-.07-4.74c-.05-.99-.21-1.53-.35-1.89a3.15 3.15 0 0 0-.76-1.17 3.15 3.15 0 0 0-1.17-.76c-.36-.14-.9-.3-1.89-.35-1.24-.06-1.59-.07-4.74-.07zm0 2.76a5.3 5.3 0 1 1 0 10.6 5.3 5.3 0 0 1 0-10.6zm0 1.62a3.68 3.68 0 1 0 0 7.36 3.68 3.68 0 0 0 0-7.36zm5.5-.9a1.24 1.24 0 1 1-2.48 0 1.24 1.24 0 0 1 2.48 0z"/></svg>')
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M.06 24l1.68-6.13A11.8 11.8 0 0 1 .16 11.9C.16 5.4 5.46.1 11.96.1c3.16 0 6.12 1.23 8.35 3.46a11.74 11.74 0 0 1 3.46 8.35c0 6.5-5.3 11.8-11.81 11.8-1.97 0-3.9-.5-5.62-1.43L.06 24zm6.6-3.8c1.66.99 3.25 1.58 5.3 1.58 5.4 0 9.8-4.4 9.8-9.79 0-2.62-1.02-5.08-2.87-6.93a9.74 9.74 0 0 0-6.92-2.88c-5.41 0-9.8 4.4-9.8 9.8 0 1.85.52 3.65 1.5 5.2l-.99 3.6 3.7-.97zm11.07-5.05c-.07-.12-.27-.2-.56-.34-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.61-.92-2.21-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.79.37-.27.3-1.04 1.01-1.04 2.47 0 1.46 1.06 2.87 1.21 3.07.15.2 2.09 3.2 5.07 4.49.71.3 1.26.49 1.69.62.71.23 1.36.2 1.87.12.57-.08 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41z"/></svg>')

SERVICES_LI = re.compile(
    r'<li class="elementor-icon-list-item">\s*'
    r'<a href="/careers/">\s*'
    r'<span class="elementor-icon-list-text">Services</span>\s*'
    r'</a>\s*</li>')

BANGLUXOR = re.compile(r'<a href="https://bangluxor\.com/"[^>]*>2026 Web design by Bangluxor</a>')
COPYRIGHT = '© 2026 Darak Group — Built in Miami, FL'

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    m = FOOTER_OPEN.search(html)
    if not m:
        return False
    orig = html

    # refresh the redesign stylesheet (replace if present, else inject)
    html = EXISTING_STYLE.sub('', html)
    m = FOOTER_OPEN.search(html)
    html = html[:m.end()] + '\n' + STYLE + html[m.end():]

    # real SVG social icons (Font Awesome glyphs were not rendering)
    html = html.replace('<i class="fab fa-whatsapp"></i>', WA_SVG)
    html = html.replace('<i class="fab fa-instagram"></i>', IG_SVG)

    # repurpose the external "Web design by Bangluxor" credit as our copyright line
    html = BANGLUXOR.sub(COPYRIGHT, html)

    # fix duplicate "Services" nav link: first -> "Careers", remove the second
    matches = list(SERVICES_LI.finditer(html))
    if len(matches) >= 2:
        first, second = matches[0], matches[1]
        html = html[:second.start()] + html[second.end():]
        relabeled = first.group(0).replace('>Services<', '>Careers<')
        html = html[:first.start()] + relabeled + html[first.end():]

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

def main():
    files = glob.glob('site/**/index.html', recursive=True) + ['site/index.html']
    files = sorted(set(os.path.normpath(p) for p in files))
    done = sum(1 for p in files if process(p))
    print(f'{done} pages updated')

if __name__ == '__main__':
    main()
