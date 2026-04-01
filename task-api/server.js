const express = require("express");
const app = express();

app.use(express.json());
app.use(express.static(__dirname));

const { randomUUID } = require("crypto");

const tasks = {};
const queue = [];

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
    queuedAt: null,
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
// PROCESS (NON-BLOCKING)
// =======================
app.post("/process", (req, res) => {
  console.log("=== ENQUEUE START ===");

  Object.values(tasks).forEach((task) => {
    if (task.status === "pending") {
      task.status = "queued";
      task.queuedAt = Date.now();
      queue.push(task);
    }
  });

  console.log(`QUEUE SIZE: ${queue.length}`);

  res.json({ message: "Tasks queued" });
});

// =======================
// WORKER FUNCTION
// =======================
function worker(workerId) {
  setInterval(() => {
    if (queue.length === 0) return;

    const task = queue.shift();

    task.status = "processing";
    task.startedAt = Date.now();

    // waiting = time spent before worker picks it
    task.waitingTime = task.startedAt - task.createdAt;

    console.log(
      `WORKER ${workerId} START: ${task.id} | Waiting: ${task.waitingTime}ms`,
    );

    // simulate heavy work
    setTimeout(() => {
      task.completedAt = Date.now();
      task.processingTime = task.completedAt - task.startedAt;
      task.totalTime = task.completedAt - task.createdAt;

      task.result = { output: "done" };
      task.status = "completed";

      console.log(
        `WORKER ${workerId} DONE: ${task.id} | Processing: ${task.processingTime}ms | Total: ${task.totalTime}ms`,
      );
    }, 5000);
  }, 100); // faster polling than before
}

// =======================
// WORKER POOL (KEY UPGRADE)
// =======================
const WORKER_COUNT = 4;

for (let i = 0; i < WORKER_COUNT; i++) {
  worker(i + 1);
}

// =======================
app.get("/", (req, res) => {
  res.send("AI Architecture Running");
});

app.listen(3000, () => {
  console.log("AI system running on 3000");
});

app.get("/metrics", (req, res) => {
  res.json(Object.values(tasks));
});
