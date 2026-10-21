/* glossary-link.js - DOM-safe auto-linker for research pages (#108-style).
   Fetches glossary-terms.json and wraps the FIRST occurrence of each glossary term (once per page)
   in a link to glossary.html#<anchor>, with the definition as a tooltip. Operates only on text
   nodes inside <main>, skipping links/code/headings/scripts, so it never mangles HTML. No network
   egress beyond the same-origin glossary file. */
(function () {
  var SKIP = {A:1, CODE:1, PRE:1, SCRIPT:1, STYLE:1, H1:1, H2:1, H3:1, TEXTAREA:1, BUTTON:1};
  function esc(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function build(terms){
    var rules = [];
    terms.forEach(function (g) {
      (g.k || []).forEach(function (key) {
        var acronym = /^[A-Z0-9][A-Z0-9-]*[A-Z0-9]$/.test(key) && key === key.toUpperCase();
        var flags = acronym ? "" : "i";
        // word-ish boundaries that tolerate hyphens (U-3) and parens
        var re = new RegExp("(^|[^A-Za-z0-9])(" + esc(key) + ")(?![A-Za-z0-9])", flags);
        rules.push({re: re, a: g.a, d: g.d, len: key.length});
      });
    });
    rules.sort(function (a, b) { return b.len - a.len; });  // longest first
    return rules;
  }
  function run(terms){
    var rules = build(terms);
    var used = {};                       // link each glossary anchor at most once per page
    var main = document.querySelector("main") || document.body;
    var walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT, null);
    var textnodes = [], n;
    while ((n = walker.nextNode())) {
      var p = n.parentNode, skip = false;
      for (var el = p; el && el !== main.parentNode; el = el.parentNode) {
        if (el.nodeType === 1 && (SKIP[el.tagName] || el.classList.contains("gl-term"))) { skip = true; break; }
      }
      if (!skip && n.nodeValue && n.nodeValue.trim().length > 2) textnodes.push(n);
    }
    textnodes.forEach(function (node) {
      for (var i = 0; i < rules.length; i++) {
        var r = rules[i];
        if (used[r.a]) continue;
        var m = r.re.exec(node.nodeValue);
        if (!m) continue;
        var pre = m[1], hit = m[2], at = m.index + pre.length;
        var after = node.splitText(at);
        after.nodeValue = after.nodeValue.slice(hit.length);
        var a = document.createElement("a");
        a.className = "gl-term"; a.href = "glossary.html#" + r.a; a.title = r.d;
        a.textContent = hit;
        node.parentNode.insertBefore(a, after);
        used[r.a] = 1;
        return;                         // one link per text node, keeps it clean
      }
    });
    if (!document.getElementById("gl-term-style")) {
      var s = document.createElement("style"); s.id = "gl-term-style";
      s.textContent = "a.gl-term{color:inherit;text-decoration:none;border-bottom:1px dotted #9a8f78;cursor:help}a.gl-term:hover{border-bottom-color:#7b2d26;color:#7b2d26}";
      document.head.appendChild(s);
    }
  }
  fetch("glossary-terms.json").then(function (r) { return r.json(); }).then(run).catch(function () {});
})();
