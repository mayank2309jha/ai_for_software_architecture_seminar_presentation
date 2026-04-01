const express = require("express");
const app = express();

app.use(express.json());
app.use(express.static(__dirname));

const tasks = {};
const { randomUUID } = require("crypto");

// =======================
// CREATE TASK
// =======================
app.post("/task", (req, res) => {
  const startApi = Date.now();

  const id = randomUUID();

  tasks[id] = {
    id,
    status: "pending",
    payload: req.body,
    result: null,

    createdAt: Date.now(),
    startedAt: null,
    completedAt: null,

    waitingTime: null,
    processingTime: null,
    totalTime: null,
  };

  const apiTime = Date.now() - startApi;

  console.log(`TASK CREATED: ${id} | API Time: ${apiTime}ms`);

  res.json({ id, status: "pending" });
});

// =======================
// GET TASKS
// =======================
app.get("/tasks", (req, res) => {
  res.json(Object.values(tasks));
});

// =======================
// PROCESS (BLOCKING)
// =======================
app.post("/process", (req, res) => {
  console.log("=== PROCESS STARTED ===");
  const processStart = Date.now();

  Object.values(tasks).forEach((task) => {
    if (task.status === "pending") {
      task.status = "processing";

      task.startedAt = Date.now();
      task.waitingTime = task.startedAt - task.createdAt;

      console.log(`START: ${task.id} | Waiting: ${task.waitingTime}ms`);

      // 🔴 BLOCKING CPU WORK
      const start = Date.now();
      while (Date.now() - start < 1000) {}

      task.completedAt = Date.now();
      task.processingTime = task.completedAt - task.startedAt;
      task.totalTime = task.completedAt - task.createdAt;

      task.result = { output: "done" };
      task.status = "completed";

      console.log(
        `DONE: ${task.id} | Processing: ${task.processingTime}ms | Total: ${task.totalTime}ms`,
      );
    }
  });

  const processTime = Date.now() - processStart;

  console.log("=== PROCESS COMPLETE ===");
  console.log(`TOTAL PROCESS TIME: ${processTime}ms`);

  res.json({ message: "All tasks processed", processTime });
});

app.listen(3001, () => {
  console.log("Baseline server running on 3001");
});

app.get("/metrics", (req, res) => {
  res.json(Object.values(tasks));
});
