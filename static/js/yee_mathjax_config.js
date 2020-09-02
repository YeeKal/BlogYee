
// ref to : https://mathjax-chinese-doc.readthedocs.io/en/latest/configuration.html
MathJax.Hub.Config({
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
    processEscapes: true,
    skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
});

