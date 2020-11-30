const update_cart = document.getElementsByClassName("update-cart");
const update_array = Array.from(update_cart);

const handleAddItemclick = (e) => {
  console.log(user);
  const id = e.target.dataset.id;
  const action = e.target.dataset.action;
  if (user != "AnonymousUser") {
    console.log("logged in");
    sendOrderData(id, action);
  } else {
    handleCookies(id, action);
  }
};

const handleCookies = (productId, action) => {
  console.log("you are not logged  in ");
  const cart = JSON.parse(getCookie("cart"));
  const cookies = {};

  const itemIndex = cart.findIndex((el) => {
    return el.productId == productId;
  });

  if (itemIndex < 0) {
    cookies["productId"] = productId;
    cookies["action"] = action;
    cookies["quantity"] = 1;
    cart.push(cookies);
  } else if (itemIndex > -1 && action == "add") {
    cart[itemIndex].quantity += 1;
  } else if (
    itemIndex > -1 &&
    action == "remove" &&
    cart[itemIndex].quantity <= 1
  ) {
    cart.splice(itemIndex, 1);
    console.log(cart);
  } else if (itemIndex > -1 && action == "remove") {
    cart[itemIndex].quantity -= 1;
  }
  setCookie("cart", JSON.stringify(cart), 200);
  location.reload();
};
for (let i = 0; i < update_array.length; i++) {
  update_array[i].addEventListener("click", handleAddItemclick);
}

const sendOrderData = (productId, action) => {
  fetch("/updateorder/", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFtoken": csrftoken },
    body: JSON.stringify({ product_id: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      location.reload();
    })
    .catch((err) => {
      console.log(err);
    });
};

// const addItemFunct = (option, quantity) => {
//   if (option == "add") {
//     quantity += 1;
//     return quantity;
//   } else if (option == "remove") {
//     quantity += 1;
//   }
//   return quantity;
// };
