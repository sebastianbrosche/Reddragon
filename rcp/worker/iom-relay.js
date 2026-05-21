/**
 * IOM WebSocket Relay Worker
 * Bridges browser WebSocket clients to Islands of Myth via TCP
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Health check
    if (url.pathname === "/") {
      return new Response(JSON.stringify({
        status: "IOM WebSocket Relay",
        version: "1.0",
        endpoints: {
          websocket: "/ws",
          health: "/"
        }
      }), { headers: { "Content-Type": "application/json" }});
    }
    
    // WebSocket upgrade endpoint
    if (url.pathname === "/ws") {
      return handleWebSocket(request, env);
    }
    
    return new Response("Not found", { status: 404 });
  }
};

async function handleWebSocket(request, env) {
  const upgradeHeader = request.headers.get("Upgrade");
  if (upgradeHeader !== "websocket") {
    return new Response("Expected websocket", { status: 400 });
  }
  
  const [clientSocket, serverSocket] = Object.values(new WebSocketPair());
  
  serverSocket.accept();
  
  // Connect to Islands of Myth via TCP
  const iomHost = "islandsofmyth.org";
  const iomPort = 3000;
  
  try {
    console.log(`Connecting to ${iomHost}:${iomPort}...`);
    const tcpSocket = await connectToIOM(iomHost, iomPort, serverSocket, env);
    console.log("TCP connection established");
    
    // Forward client → IOM
    serverSocket.addEventListener("message", async (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.cmd === "input" && tcpSocket) {
          const text = data.text + "\n";
          console.log(`Forwarding command: ${data.text}`);
          await tcpSocket.write(new TextEncoder().encode(text));
        }
      } catch (e) {
        console.error("Error forwarding message:", e);
        // Raw text, forward as-is
        if (tcpSocket) {
          await tcpSocket.write(new TextEncoder().encode(event.data + "\n"));
        }
      }
    });
    
    serverSocket.addEventListener("close", () => {
      console.log("WebSocket closed");
      if (tcpSocket) tcpSocket.close();
    });
    
    serverSocket.send(JSON.stringify({
      type: "status",
      msg: "Connected to Islands of Myth"
    }));
    
  } catch (err) {
    console.error("Connection failed:", err);
    serverSocket.send(JSON.stringify({
      type: "status",
      msg: "Connection failed: " + err.message
    }));
    serverSocket.close();
  }
  
  return new Response(null, {
    status: 101,
    webSocket: clientSocket
  });
}

async function connectToIOM(host, port, wsSocket, env) {
  const socket = connect({ hostname: host, port: port });
  const writer = socket.writable.getWriter();
  const reader = socket.readable.getReader();
  
  // Read loop: IOM → browser
  const readLoop = async () => {
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const text = new TextDecoder().decode(value);
        
        // Log to KV if available
        if (env.IOM_LOGS) {
          const timestamp = Date.now();
          const key = `log_${timestamp}_${Math.random().toString(36).slice(2, 8)}`;
          await env.IOM_LOGS.put(key, text, { expirationTtl: 86400 });
        }
        
        wsSocket.send(JSON.stringify({
          type: "output",
          data: text
        }));
      }
    } catch (e) {
      wsSocket.send(JSON.stringify({
        type: "status",
        msg: "IOM connection closed"
      }));
    }
  };
  
  // Start read loop in background
  readLoop();
  
  return {
    write: (data) => writer.write(data),
    close: () => {
      writer.releaseLock();
      reader.releaseLock();
      socket.close();
    }
  };
}
