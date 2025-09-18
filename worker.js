// Cloudflare Worker: scrape leilões e devolver JSON
const LEILAO_SITES = [
    "https://www.serpaleiloes.com.br/?tipo=leilao",
    "https://www.portalzuk.com.br/leilao-de-imoveis/u/todos-imoveis/sc",
    "https://www.brasilsulleiloes.com.br/",
  ];
  
  const BENS_INTERESSE = [
    "imovel urbano", "imoveis urbanos",
    "imovel rural", "imoveis rurais",
    "trator", "tratores",
    "carregadeira", "escavadeira",
    "leilao", "leiloes"
  ];
  
  function normalize(s = "") {
    return s
      .normalize("NFKD")
      .replace(/\p{M}/gu, "")
      .toLowerCase();
  }
  
  function linkInteressante(textoNorm) {
    return BENS_INTERESSE.some(b => textoNorm.includes(b)) && textoNorm.includes("leil");
  }
  
  // Extrai <a href="...">texto</a> com heurística simples (sem libs)
  function parseLinks(html) {
    const links = [];
    const regex = /<a\b[^>]*href\s*=\s*(['"])(.*?)\1[^>]*>(.*?)<\/a>/gims;
    let m;
    while ((m = regex.exec(html)) !== null) {
      const href = (m[2] || "").trim();
      let texto = (m[3] || "")
        .replace(/<[^>]+>/g, " ")
        .replace(/\s+/g, " ")
        .trim();
      links.push({ href, texto });
    }
    return links;
  }
  
  function urlJoin(base, href) {
    try { return new URL(href, base).toString(); }
    catch { return href; }
  }
  
  async function fetchSite(site) {
    const res = await fetch(site, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
      },
      cf: { cacheTtl: 0, cacheEverything: false }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status} em ${site}`);
    const html = await res.text();
    const anchors = parseLinks(html);
  
    const vistos = new Set();
    const agora = new Date();
    const dataColeta = `${agora.getFullYear()}-${String(agora.getMonth()+1).padStart(2,"0")}-${String(agora.getDate()).padStart(2,"0")} ${String(agora.getHours()).padStart(2,"0")}:${String(agora.getMinutes()).padStart(2,"0")}`;
  
    const editais = [];
    for (const a of anchors) {
      const textoNorm = normalize(a.texto);
      if (!textoNorm) continue;
      const fullUrl = urlJoin(site, a.href);
      const key = `${textoNorm}||${fullUrl}`;
      if (vistos.has(key)) continue;
      if (linkInteressante(textoNorm)) {
        vistos.add(key);
        editais.push({
          titulo: a.texto,
          link: fullUrl,
          site_origem: site,
          data_coleta: dataColeta
        });
      }
    }
    return editais;
  }
  
  export default {
    async fetch(req) {
      // CORS liberado
      const headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      };
      if (req.method === "OPTIONS") {
        return new Response(null, { headers });
      }
      try {
        const results = await Promise.allSettled(LEILAO_SITES.map(fetchSite));
        const editais = [];
        const erros = [];
        for (const r of results) {
          if (r.status === "fulfilled") editais.push(...r.value);
          else erros.push({ erro: String(r.reason) });
        }
        return new Response(JSON.stringify({ editais, erros }), {
          headers: { ...headers, "Content-Type": "application/json; charset=utf-8" },
        });
      } catch (e) {
        return new Response(JSON.stringify({ editais: [], erros: [{ erro: String(e) }] }), {
          status: 500,
          headers: { ...headers, "Content-Type": "application/json; charset=utf-8" },
        });
      }
    }
  };
  