const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const errorHandler = require('./controllers/error');
const { scrapper } = require('./controllers/scrapper');

const PORT = 5050;

app.use(cors());
app.use(bodyParser.json());

app.get('/', scrapper);

app.use(function(req, res, next) {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
});

app.use(errorHandler);

app.listen(PORT, function() {
  console.log(`Server is starting on port ${PORT}`);
});
