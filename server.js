const express = require("express");

const path = require("path");
const multer = require("multer");
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
//Configuration for Multer
const multerStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, "uploads");
  },
  filename: (req, file, cb) => {
    const ext = file.mimetype.split("/")[1];
    cb(null, `${file.originalname}-${Date.now()}.${ext}`);
  },
});
const upload = multer({
  storage: multerStorage,
});
server.get("/", function (req, res) {
  res.render("index");
});
server.post("/upload", upload.single("file"), async (req, res) => {
  console.log(req.file);
  // var spawn = require("child_process").spawn;
  // var ip_path = __dirname + "\\" + newFile.file_path;
  // const childPython = spawn("python", [
  //   "borb-master/extract_files.py",
  //   ip_path,
  // ]);
  // childPython.stdout.on("data", (data) => {
  //   console.log(data.toString());
  //   output_files.push(data.toString().trimEnd());
  // });
  // childPython.stderr.on("data", (data) => {
  //   console.log(`stderr:${data}`);
  // });
  // childPython.on("close", (code) => {
  //   console.log(output_files);
  //   res.status(200);
  //   res.redirect("http://localhost:3000/home/filesresult");
  //   console.log(`exited with code:${code}`);
  // });
});

server.listen(5000, function () {
  console.log("Listening on port", port);
});
