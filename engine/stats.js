let matched = 0;
let stored = 0;

function recordMatch() {
  matched++;
}

function recordStored() {
  stored++;
}

function printStats() {
  console.log("\n=== FINAL STATS ===");
  console.log("Matched Orders:", matched);
  console.log("Stored Orders:", stored);
}

module.exports = {
  recordMatch,
  recordStored,
  printStats,
};
