const buyOrders = [];
const sellOrders = [];

function addOrder(order) {
  if (order.type === "buy") {
    buyOrders.push(order);
  } else {
    sellOrders.push(order);
  }
}

function removeOrder(orderArray, orderId) {
  const index = orderArray.findIndex((o) => o.id === orderId);
  if (index !== -1) {
    orderArray.splice(index, 1);
  }
}

module.exports = {
  buyOrders,
  sellOrders,
  addOrder,
  removeOrder,
};
