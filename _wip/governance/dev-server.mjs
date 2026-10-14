#!/usr/bin/env node
// Serves the built deck and rebuilds and reloads the browser when a source file changes.
//
//   node dev-server.mjs [--port 8765] [--presenter smitty] [--mode overview]
//
// Watches slides/, shell/, builder/ and presenters/, runs builder/build.py with --no-zip after
// each burst of changes, then tells every open page to reload. A failed build keeps the last
// good page and prints the error. The server refuses to start if the port is taken; it never
// stops another process.

import { createServer } from "node:http";
import { spawn } from "node:child_process";
import { watch, createReadStream, statSync, readFileSync } from "node:fs";
import { dirname, extname, join, normalize, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const WATCHED = ["slides", "shell", "builder", "presenters"];
const DEBOUNCE_MS = 300;

const argv = process.argv.slice(2);
const option = (name, fallback) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback;
};
const PORT = Number(option("port", "8765"));
const PRESENTER = option("presenter", "smitty");
const MODE = option("mode", "overview");
const OUT = join(ROOT, "generated", MODE);

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".mp4": "video/mp4",
};

const RELOAD_SNIPPET =
  "<script>new EventSource('/__reload').onmessage=()=>location.reload();</script>";

const clients = new Set();
let building = false;
let queued = false;
let timer = null;

function build() {
  if (building) {
    queued = true;
    return;
  }
  building = true;
  const started = Date.now();
  const args = ["builder/build.py", "--mode", MODE, "--no-zip"];
  if (PRESENTER) args.push("--presenter", PRESENTER);
  const child = spawn("python3", args, { cwd: ROOT });
  let output = "";
  child.stdout.on("data", (d) => (output += d));
  child.stderr.on("data", (d) => (output += d));
  child.on("close", (code) => {
    building = false;
    if (code === 0) {
      console.log(`built in ${Date.now() - started} ms, reloading ${clients.size} page(s)`);
      for (const res of clients) res.write("data: reload\n\n");
    } else {
      console.error(`build failed (exit ${code}), keeping the last good page:\n${output.split("\n").slice(-15).join("\n")}`);
    }
    if (queued) {
      queued = false;
      build();
    }
  });
}

function onChange(_event, name) {
  if (name && /(^|[\\/])\.DS_Store$|~$|\.swp$/.test(name)) return;
  clearTimeout(timer);
  timer = setTimeout(build, DEBOUNCE_MS);
}

function serve(req, res) {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname === "/__reload") {
    res.writeHead(200, {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    });
    res.write("retry: 1000\n\n");
    clients.add(res);
    req.on("close", () => clients.delete(res));
    return;
  }
  let rel = decodeURIComponent(url.pathname);
  if (rel.endsWith("/")) rel += "index.html";
  const file = normalize(join(OUT, rel));
  if (file !== OUT && !file.startsWith(OUT + sep)) {
    res.writeHead(403).end("Forbidden");
    return;
  }
  let st;
  try {
    st = statSync(file);
  } catch {
    res.writeHead(404).end("Not found");
    return;
  }
  if (!st.isFile()) {
    res.writeHead(404).end("Not found");
    return;
  }
  const type = TYPES[extname(file).toLowerCase()] ?? "application/octet-stream";
  if (extname(file) === ".html") {
    const html = readFileSync(file, "utf8");
    const body = html.includes("</body>")
      ? html.replace("</body>", `${RELOAD_SNIPPET}</body>`)
      : html + RELOAD_SNIPPET;
    res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store" });
    res.end(body);
    return;
  }
  res.writeHead(200, { "Content-Type": type, "Cache-Control": "no-store" });
  createReadStream(file).pipe(res);
}

const server = createServer(serve);
server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    console.error(`port ${PORT} is already in use; stop that server or pass --port`);
  } else {
    console.error(err.message);
  }
  process.exit(1);
});
server.listen(PORT, "127.0.0.1", () => {
  for (const dir of WATCHED) watch(join(ROOT, dir), { recursive: true }, onChange);
  console.log(`serving ${OUT}\n  http://127.0.0.1:${PORT}/index.html\nwatching ${WATCHED.join(", ")}`);
  build();
});
