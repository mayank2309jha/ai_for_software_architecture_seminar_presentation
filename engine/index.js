const fs = require("fs");

const { TOTAL_ORDERS } = require("./config");
const { generateOrder } = require("./orderGenerator");
const { matchOrder } = require("./matcher");
const { addOrder } = require("./orderBook");
const { recordMatch, recordStored, printStats } = require("./stats");
const { initCSV, record } = require("./analytics");

// Redirect console logs to file
const logStream = fs.createWriteStream("mono_results.txt", { flags: "w" });
console.log = function (message) {
  logStream.write(message + "\n");
};

initCSV();

console.log("Starting Order Matching Simulation...\n");

for (let i = 0; i < TOTAL_ORDERS; i++) {
  const order = generateOrder();

  // ⏱️ Timing
  const arrivalTime = Date.now();

  const startProcessTime = Date.now();

  const result = matchOrder(order);

  const endProcessTime = Date.now();

  const times = {
    arrivalTime,
    startProcessTime,
    endProcessTime,
  };

  if (result.matched) {
    console.log(
      `MATCH: Order ${order.id} (${order.type} ${order.item} @${order.price}) matched`,
    );
    recordMatch();

    record(order, times, "MATCHED");
  } else {
    addOrder(order);

    console.log(
      `STORE: Order ${order.id} (${order.type} ${order.item} @${order.price}) added`,
    );
    recordStored();

    record(order, times, "STORED");
  }
}

printStats();

logStream.end();
