const axios = require("axios");
const fs = require("fs");

// 🔁 CHANGE THIS
const BASE_URL = "http://localhost:3001"; // 3000 = AI, 3001 = baseline
const OUTPUT_FILE = BASE_URL.includes("3000")
  ? "ai_metrics.csv"
  : "baseline_metrics.csv";

async function runLoad() {
  const requests = [];

  console.time("TASK_CREATION");

  for (let i = 0; i < 100; i++) {
    requests.push(axios.post(`${BASE_URL}/task`, { num: i }));
  }

  await Promise.all(requests);

  console.timeEnd("TASK_CREATION");

  console.log("Tasks created");

  console.time("PROCESS_TRIGGER");

  await axios.post(`${BASE_URL}/process`);

  console.timeEnd("PROCESS_TRIGGER");

  console.log("Processing started");

  // ⏳ WAIT for tasks to finish
  console.log("Waiting for tasks to complete...");
  await new Promise((resolve) => setTimeout(resolve, 15000));

  // 📊 FETCH METRICS
  const res = await axios.get(`${BASE_URL}/metrics`);
  const tasks = res.data;

  // 📝 Convert to CSV
  const headers = [
    "id",
    "status",
    "createdAt",
    "queuedAt",
    "startedAt",
    "completedAt",
    "waitingTime",
    "processingTime",
    "totalTime",
  ];

  const rows = tasks.map((t) =>
    [
      t.id,
      t.status,
      t.createdAt,
      t.queuedAt || "",
      t.startedAt,
      t.completedAt,
      t.waitingTime,
      t.processingTime,
      t.totalTime,
    ].join(","),
  );

  const csv = [headers.join(","), ...rows].join("\n");

  fs.writeFileSync(OUTPUT_FILE, csv);

  console.log(`✅ Metrics saved to ${OUTPUT_FILE}`);
}

runLoad();
