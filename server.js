const express = require("express");

const path = require("path");

const port = process.env.PORT || 5000;

const server = express();
server.use(express.json());
server.use(express.static("./public"));
server.set("view engine", "ejs");
server.set("views", "./src/views");
server.use(
  express.urlencoded({
    extended: true,
  })
);
server.get("/", function (req, res) {
  res.render("index");
});

server.listen(5000, function () {
  console.log("Listening on port", port);
});
