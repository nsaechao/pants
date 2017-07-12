'use strict';

var tests = Object.keys(window.__karma__.files).filter(function (file) {
  return (/_spec\.js$/.test(file));
});

require.config({
  // Karma serves files under /base, which is the basePath from your config file
  baseUrl: '/base',

  // dynamically load all test files
  deps: tests,

  // kick off jasmine
  callback: window.__karma__.start
});