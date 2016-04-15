$(function(){
   tinymce.init({
      plugins: "image link textcolor colorpicker code preview",
      menubar: false,
      theme: 'modern',
      skin: 'light',
      toolbar: 'undo redo code preview | styleselect removeformat | forecolor backcolor | bold italic | alignleft aligncenter alignright alignfull | bullist numlist outdent indent | link image',
      mode: "specific_textareas",
      editor_selector : "mce-editor",
      convert_urls: false,
      keep_styles: true,
      entity_encoding : "named",
      style_formats: [
        {title: "Header 1(⌘+1)", format: "h1"},
        {title: "Header 2(⌘+2)", format: "h2"},
        {title: "Header 3(⌘+3)", format: "h3"},
        {title: "Header 4(⌘+4)", format: "h4"},
        {title: "Header 5(⌘+5)", format: "h5"},
        {title: "Header 6(⌘+6)", format: "h6"},
        {title: "Paragraph(⌘+7)", format: "p"}
      ],
      setup: function (editor) {
          editor.on('init', function(args) {
              this.getDoc().body.style.fontSize = '14px';
              editor = args.target;
              editor.on('NodeChange', function(e) {
                  if (e && e.element.nodeName.toLowerCase() == 'img') {
                      tinyMCE.DOM.setAttribs(e.element, {'width': null, 'height': null});
                  }
              });
          });
      }
   });
  window.onbeforeunload = function() {
      if (tinyMCE.activeEditor.isDirty()) {
          return "页面更改还没有保存，确定关闭？";
      }
  }
});
