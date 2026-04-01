const { buyOrders, sellOrders, removeOrder } = require("./orderBook");

function matchOrder(order) {
  if (order.type === "buy") {
    // find lowest sell
    let match = null;

    for (let sell of sellOrders) {
      if (sell.item === order.item && sell.price <= order.price) {
        if (!match || sell.price < match.price) {
          match = sell;
        }
      }
    }

    if (match) {
      removeOrder(sellOrders, match.id);
      return { matched: true, matchedWith: match };
    }
  } else {
    // find highest buy
    let match = null;

    for (let buy of buyOrders) {
      if (buy.item === order.item && buy.price >= order.price) {
        if (!match || buy.price > match.price) {
          match = buy;
        }
      }
    }

    if (match) {
      removeOrder(buyOrders, match.id);
      return { matched: true, matchedWith: match };
    }
  }

  return { matched: false };
}

module.exports = { matchOrder };
