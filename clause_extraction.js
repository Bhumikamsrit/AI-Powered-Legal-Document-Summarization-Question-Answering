const nlp = require("compromise");

function extractEntities(text) {
  const doc = nlp(text);
  return doc.topics().out("array");
}

module.exports = { extractEntities };
