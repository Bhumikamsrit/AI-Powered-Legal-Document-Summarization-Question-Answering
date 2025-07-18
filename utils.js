const nlp = require("compromise");

function preprocessText(text) {
  let doc = nlp(text);
  doc = doc.normalize().out("text");
  return doc;
}

module.exports = { preprocessText };