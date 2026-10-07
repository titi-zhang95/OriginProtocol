"""Fetch verified sources for Immunefi in-scope assets (+ proxy implementations) via Blockscout."""
import json, os, re, sys, time, urllib.request

SCOPE_HTML, OUT = sys.argv[1], sys.argv[2]
EXPLORERS = {"etherscan.io": ("ethereum", "https://eth.blockscout.com"),
             "basescan.org": ("base", "https://base.blockscout.com"),
             "arbiscan.io": ("arbitrum", "https://arbitrum.blockscout.com"),
             "hyperevmscan.io": ("hyperevm", None)}
CHAIN_ID = {"ethereum": 1, "base": 8453, "arbitrum": 42161, "hyperevm": 999}
RPC = {"ethereum": "https://ethereum-rpc.publicnode.com", "base": "https://base-rpc.publicnode.com",
       "arbitrum": "https://arbitrum-one-rpc.publicnode.com", "hyperevm": "https://rpc.hyperliquid.xyz/evm"}
IMPL_SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"


def rpc(chain, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for i in range(4):
        try:
            req = urllib.request.Request(RPC[chain], data=body, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r).get("result")
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def eip1967_impl(chain, addr):
    v = rpc(chain, "eth_getStorageAt", [addr, IMPL_SLOT, "latest"])
    if v and int(v, 16):
        return "0x" + v[-40:]
    return None


def from_blockscout(base, addr):
    d = get(f"{base}/api/v2/smart-contracts/{addr}") if base else None
    if not isinstance(d, dict) or not d.get("is_verified"):
        return None
    files = [{"file_path": d.get("file_path") or f"{d.get('name')}.sol", "source_code": d.get("source_code", "")}]
    files += d.get("additional_sources") or []
    meta = {k: d.get(k) for k in ("name", "file_path", "compiler_version", "evm_version", "optimization_enabled",
                                  "optimization_runs", "compiler_settings", "proxy_type", "implementations",
                                  "verified_at", "is_fully_verified", "constructor_args", "decoded_constructor_args",
                                  "external_libraries", "language")}
    impls = [i.get("address_hash") or i.get("address") for i in d.get("implementations") or []]
    return d.get("name") or "Unknown", files, meta, d.get("abi"), impls, "blockscout"


def from_sourcify(chain, addr):
    d = get(f"https://sourcify.dev/server/v2/contract/{CHAIN_ID[chain]}/{addr}?fields=all")
    if not isinstance(d, dict) or not d.get("sources"):
        return None
    c = d.get("compilation") or {}
    files = [{"file_path": k, "source_code": v.get("content", "")} for k, v in d["sources"].items()]
    meta = {"name": c.get("name"), "fullyQualifiedName": c.get("fullyQualifiedName"),
            "compiler_version": c.get("compilerVersion"), "compiler_settings": c.get("compilerSettings"),
            "match": d.get("match"), "verified_at": d.get("verifiedAt"), "proxy_resolution": d.get("proxyResolution"),
            "deployment": d.get("deployment")}
    pr = d.get("proxyResolution") or {}
    impls = [i.get("address") for i in pr.get("implementations") or []]
    return c.get("name") or "Unknown", files, meta, d.get("abi"), impls, "sourcify"


def get(url):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 * (i + 1))
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def assets():
    s = open(SCOPE_HTML).read().replace('\\"', '"')
    seen = []
    for m in re.finditer(r'\{[^{}]*"url":"(https://[^"]+)"[^{}]*\}', s):
        o = m.group(0)
        t = re.search(r'"type":"([^"]+)"', o)
        d = re.search(r'"description":"([^"]*)"', o)
        a = re.search(r'https://([a-z.]+)/address/(0x[0-9a-fA-F]{40})', m.group(1))
        if t and t.group(1) == "smart_contract" and a:
            k = (d.group(1).strip(), a.group(1), a.group(2))
            if k not in seen:
                seen.append(k)
    return seen


def safe(p):
    p = p.lstrip("/").replace("..", "__")
    return re.sub(r"[^A-Za-z0-9_./@-]", "_", p)


fetched = {}  # (chain, addr) -> info


def fetch(chain, base, addr, depth=0):
    key = (chain, addr.lower())
    if key in fetched:
        return fetched[key]
    info = {"address": addr, "chain": chain, "implementations": []}
    fetched[key] = info
    res = from_blockscout(base, addr) or from_sourcify(chain, addr)
    impls = []
    if res:
        name, files, meta, abi, impls, src = res
        dirn = os.path.join(OUT, chain, f"{addr}_{safe(name)}")
        for f in files:
            p = os.path.join(dirn, "src", safe(f["file_path"]))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write(f["source_code"])
        meta.update(address=addr, chain=chain, source=src)
        json.dump(meta, open(os.path.join(dirn, "metadata.json"), "w"), indent=2)
        json.dump(abi, open(os.path.join(dirn, "abi.json"), "w"), indent=2)
        info.update(status="ok", name=name, dir=os.path.relpath(dirn, OUT), files=len(files), source=src,
                    compiler=meta.get("compiler_version"))
    else:
        info["status"] = "unverified_or_unavailable"
    slot = eip1967_impl(chain, addr)
    if slot:
        info["eip1967_impl_onchain"] = slot
        if slot.lower() not in [i.lower() for i in impls if i]:
            impls.append(slot)
    if depth < 2:
        for ia in impls:
            if ia and ia.lower() != addr.lower():
                info["implementations"].append(fetch(chain, base, ia, depth + 1))
    return info


index = []
for name, host, addr in assets():
    chain, base = EXPLORERS[host]
    r = fetch(chain, base, addr)
    index.append({"asset": name, "chain": chain, "address": addr, "result": r})
    print(f"{chain:9} {addr} {name:45} {r.get('status')}/{r.get('source','-')} {r.get('name','')} "
          f"impl={[i.get('name', i.get('status')) for i in r.get('implementations', [])]}", flush=True)
json.dump(index, open(os.path.join(OUT, "index.json"), "w"), indent=2, default=str)
