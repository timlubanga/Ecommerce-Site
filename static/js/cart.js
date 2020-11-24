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
  console.log("you are not logged  in fucker ");
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
    setCookie("cart", JSON.stringify(cart, 200));
  } else {
    cart[itemIndex].quantity += 1;
    console.log(cart);
    setCookie("cart", JSON.stringify(cart, 200));
  }

  // for (item of cart) {
  //   if (item.productId == productId) {
  //     item.quantity = +1;
  //   } else {
  //     cookies["productId"] = productId;
  //     cookies["action"] = action;
  //     cookies["quantity"] = 1;
  //     cart.push(cookies);
  //   }
  //   console.log(cart);
  //   setCookie("cart", JSON.stringify(cart, 200));
  // }

  // setCookie("cart", JSON.stringify(cart, 200));
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
