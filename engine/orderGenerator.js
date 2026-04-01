const { ITEMS, MIN_PRICE, MAX_PRICE } = require("./config");

let id = 1;

function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomPrice() {
  return Math.floor(Math.random() * (MAX_PRICE - MIN_PRICE + 1)) + MIN_PRICE;
}

function generateOrder() {
  return {
    id: id++,
    type: Math.random() < 0.5 ? "buy" : "sell",
    item: randomChoice(ITEMS),
    price: randomPrice(),
  };
}

module.exports = { generateOrder };
