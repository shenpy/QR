myapp.module({builder: function(myapp) {
    var modal = (function(){
        var
        method = {},
        $overlay,
        $modal,
        $content,
        $close;

        method.center = function () {
            var top, left;
            top = document.documentElement.clientHeight/2 -  $modal.height()/2;
            left = Math.max($(window).width() - $modal.width(), 0) / 2;
            $modal.css({
                "top": top ,
                "left": left
            });
        };

        method.open = function (settings) {
            $content.empty().append(settings.content);

          //  $modal.css({
          //      width: settings.width || 'auto',
          //      height: settings.height || 'auto'
          //  });

            method.center();
            $(window).bind('resize', method.center);
            $modal.fadeIn();
            $overlay.show();
        };

        method.close = function () {
            $modal.fadeOut(500, $content.empty);
            $overlay.hide();
            $(window).unbind('resize.modal');
        };

        $overlay = $('<div class="dismiss" id="mask"></div>');
        $modal = $('<div id="modal"></div>');
        $content = $('<div id="modal-content"></div>');
        $head = $('<div id="modal-head"><div id="modal-head-title">ask question</div><div class="dismiss" id="close" href="#">close</div></div>');

        $modal.hide();
        $overlay.hide();
        $modal.append($head, $content);

        $(document).ready(function(){
            $('body').append($overlay, $modal);
            $('.dismiss').click(function(e){
                e.preventDefault();
                method.close();
            });
            //$('#modal-head-title').click(function(e){
            //    e.preventDefault();
            //    $('#id_title').val($(document).height());
            //});
        });

        return method;
    }());


    $(document).ready(function(){
        $('.askquestion').click(function(e) {
            e.preventDefault();
            $(this).addClass('ajax-loading');
            $.ajax({
                type : "get",
                url : '/question/new/',
                dataType : "html",
                success: function(data) {
                    $('.askquestion').removeClass('ajax-loading');
                    modal.open({content: data});
                    $('#id_title').focus();
                },
                error : function() {
                    $('.askquestion').removeClass('ajax-loading');
                    alert("Sorry, try later!");
                }
            });
        });
    });

    myapp.modal = modal;
    }
});
