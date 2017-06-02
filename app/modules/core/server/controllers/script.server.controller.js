'use strict';

var path = require('path'),
  config = require(path.resolve('./config/config'));

/**
 * Run Script
 */
exports.runScript = function (req, res) {
  return res.status(400).send({
    message: 'Script running'
  });
};
