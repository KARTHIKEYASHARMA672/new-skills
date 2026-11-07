// Tiny show-it visualization server.
// Serves frame.html at /, and the current screen fragment at /screen.
// The agent writes a fragment to $SCREEN_DIR/screen.html; the page polls /screen
// every 800ms and swaps it in. Run: SCREEN_DIR=... bun server.ts

const dir = process.env.SCREEN_DIR ?? ".";
const port = Number(process.env.PORT ?? 0); // 0 = pick a free port
const frame = await Bun.file(new URL("./frame.html", import.meta.url)).text();

const server = Bun.serve({
  port,
  async fetch(req) {
    const { pathname } = new URL(req.url);
    if (pathname === "/") return html(frame);
    if (pathname === "/screen") {
      const f = Bun.file(`${dir}/screen.html`);
      const body = (await f.exists())
        ? await f.text()
        : "Waiting for the agent to push a screen...";
      return html(body);
    }
    return new Response("not found", { status: 404 });
  },
});

const html = (body: string) =>
  new Response(body, { headers: { "content-type": "text/html; charset=utf-8" } });

console.log(`show-it: visualization at http://localhost:${server.port}  (screen dir: ${dir})`);
