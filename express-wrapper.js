const express = require("express");
const app = express();

app.get("/healthz", (req, res) => {
  res.status(200).send("OK");
});

app.use((req, res) => {
  res.status(403).send("Forbidden");
});

module.exports = app;
EOF < /dev/null