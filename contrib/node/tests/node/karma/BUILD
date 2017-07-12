node_module(
  name='karma',
  sources=globs(
    'package.json',
    'yarn.lock',
    'test/*.js',
    'test/spec/*.js',
    'karma.conf.js'),
  package_manager='yarn',
)

node_karma_tests(
  name='karma_test',
  dependencies=[
    ':karma'
  ]
)
