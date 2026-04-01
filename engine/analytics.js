const fs = require("fs");

const fileName = "analytics.csv";

// Write header once
function initCSV() {
  const header =
    "id,type,item,price,arrivalTime,startProcessTime,endProcessTime,latency,processingTime,status\n";
  fs.writeFileSync(fileName, header);
}

function record(order, times, status) {
  const row = [
    order.id,
    order.type,
    order.item,
    order.price,
    times.arrivalTime,
    times.startProcessTime,
    times.endProcessTime,
    times.endProcessTime - times.arrivalTime,
    times.endProcessTime - times.startProcessTime,
    status,
  ].join(",");

  fs.appendFileSync(fileName, row + "\n");
}

module.exports = {
  initCSV,
  record,
};
