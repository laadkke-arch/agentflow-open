// Bridge a test-only loopback port across a local Docker bind mount.
import net from "node:net";

function address(input) {
  const separator = input.indexOf(":");
  const kind = input.slice(0, separator);
  const value = input.slice(separator + 1);
  if (kind === "unix" && value.startsWith("/")) return { path: value };
  if (kind === "tcp" && /^\d+$/.test(value)) {
    return { host: "127.0.0.1", port: Number(value) };
  }
  throw new Error(`Invalid loopback relay address: ${input}`);
}

const [listener, destination] = process.argv.slice(2).map(address);
const server = net.createServer((client) => {
  const upstream = net.createConnection(destination);
  client.on("error", () => upstream.destroy());
  upstream.on("error", () => client.destroy());
  client.pipe(upstream).pipe(client);
});

server.on("error", (error) => {
  console.error(error.message);
  process.exit(1);
});
server.listen(listener);
