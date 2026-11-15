"""Constant metadata only: no user data or React-owned child manipulation."""
LOCALE_GUARD='''<script>
(() => {
  const root = document.documentElement;
  root.lang = "pt-BR";
  root.setAttribute("translate", "no");
  root.classList.add("notranslate");
  let meta = document.querySelector('meta[name="google"]');
  if (!meta) {
    meta = document.createElement("meta");
    meta.name = "google";
    document.head.appendChild(meta);
  }
  meta.content = "notranslate";
})();
</script>'''
