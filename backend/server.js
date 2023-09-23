// -----------------------------------------------------------------------------
// Import needed modules
// -----------------------------------------------------------------------------
const express = require("express");
const db = require("./db"); // local module for interacting with Database
const recutils = require("./recommendation_logic"); // local module w/ utilities
                                                    // to handle recommendations


const app = express();

// -----------------------------------------------------------------------------
// Routers for responding to client-side requets
// -----------------------------------------------------------------------------
app.get("/busca-tipo-produto", function (req, res) {
  /** 
   * Responds to requests where user types a generic product name
   * by sendind back a list of product types it can select from.
  */
  // ...
});

app.get("/recomendacao-mercados", function (req, res) {
  /** 
   * Responds to requests containing a shopping cart (a set of product types),
   * an address/location, and a maximum distance by sending back zero or more 
   * markets along with the product instances that match the shoppping cart etc.
   * 
   * Recommendations should do a tradeoff between minimizing total price in
   * that market and maximizing the number of cart items that are available.
   */
  // ...
});

app.get("/busca-instancias-prods-alternativas", function (req, res) {
  /**
   * Responds to a request containing a market id and a generic product name
   * by sending back alternative product instances form within that market
   * that may respond to the query.
   */
  // ...
});

//! ERASE-ME:
app.get("/", function (req, res) {
  res.send("Hello World!");
});

// -----------------------------------------------------------------------------
// Listen to requests coming through port 3000
// -----------------------------------------------------------------------------
const port = 3000;
function getHost() {
  // run in either "globally exposed" mode (for docker) or locally:
  return process.env.DEPLOY_MODE == 'docker' ? '0.0.0.0' : '127.0.0.1';
}
app.listen(port, getHost(), function () {
  console.log(`Example app listening on port ${port}!`);
});