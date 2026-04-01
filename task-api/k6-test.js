import http from "k6/http";

export default function () {
  http.post("http://localhost:3000/task", JSON.stringify({ a: 1 }), {
    headers: { "Content-Type": "application/json" },
  });
}
