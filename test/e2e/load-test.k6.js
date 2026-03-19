import http from "k6/http";
import { check } from "k6";
function uuidv4() {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

const AGENT_GATEWAY_URL = __ENV.AGENT_GATEWAY_URL || "http://localhost:11002";
const AGENT_GATEWAY_API_KEY = __ENV.AGENT_GATEWAY_API_KEY || "";

export const options = {
  scenarios: {
    cross_selling: {
      executor: "constant-vus",
      vus: 10,
      duration: "2m",
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<30000"],
    http_req_failed: ["rate<0.1"],
  },
};

export default function () {
  const payload = JSON.stringify({
    jsonrpc: "2.0",
    id: 1,
    method: "message/send",
    params: {
      message: {
        role: "user",
        parts: [
          {
            kind: "text",
            text: "Bitte entwickle eine cross-selling-strategie für Kunde 'Anna Müller'",
          },
        ],
        messageId: uuidv4(),
        contextId: uuidv4(),
      },
      metadata: {},
    },
  });

  const headers = { "Content-Type": "application/json" };
  if (AGENT_GATEWAY_API_KEY) {
    headers["Authorization"] = `Bearer ${AGENT_GATEWAY_API_KEY}`;
  }

  const res = http.post(
    `${AGENT_GATEWAY_URL}/insurance-host-agent`,
    payload,
    { headers, timeout: "90s" },
  );

  check(res, {
    "status is 200": (r) => r.status === 200,
    "response contains insurance content": (r) =>
      r.body.toLowerCase().includes("versicherung"),
  });
}
