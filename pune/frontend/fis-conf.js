fis.config.merge({
  modules : {
    spriter : 'csssprites'
  },
  roadmap : {
    path : [
      // admin css/js/fonts/images
      {
        reg : 'js/**',
        useDomain: false,
        release : 'static/$&'
      },
      {
        reg : 'css/**.css',
        useHash : true,
        useDomain: false,
        release : 'static/$&'
      },
      {
        reg : 'fonts/**',
        useHash : true,
        useDomain: false,
        release : 'static/$&'
      },
      {
        reg : 'lib/**',
        useHash : false,
        useOptimizer: false,
        isCssLike: false,
        useDomain: false,
        release : 'static/$&'
      },
      {
        reg : /^\/images\/(.*\.(?:png|jpg|jpeg|gif|ico|svg))/i,
        useDomain: false,
        release : 'static/images/$1',
      },
      {
        reg : /^^\/html\/(.*\.(?:html))/i,
        release : 'templates/$1',
      },
      {
        //前面规则未匹配到的其他文件编译的时候不要产出了
        reg : /.*/,
        release : false
      }
    ]
  }
});
