myapp.module({builder: function(myapp) {
    var requireLogin = function() {
            if(!CURRENT_USER_ID){
                modal.open({content: $('#login-form').html()});
                return false;
            }
            return true;
        };
    var modal = (function(){
        var
        method = {},
        $overlay,
        $modal,
        $close,
        $content;
        method.center = function () {
            var top, left;
            top = document.documentElement.clientHeight/2 -  $modal.height()/2;
            left = Math.max($(window).width() - $modal.width(), 0) / 2;
            $modal.css({
                "top": top + $(document).scrollTop() ,
                "left": left
            });
        };

        method.open = function (settings) {
            $content.empty().append(settings.content);
            $('.dismiss').bind('click', method.close);
            method.center();
            $(window).bind('resize', method.center);
            $modal.fadeIn();
            $overlay.show();
        };

        method.close = function () {
            $modal.fadeOut();
            $overlay.hide();
            $(window).unbind('resize');
        };

        $overlay = $('<div class="dismiss" id="mask"></div>');
        $modal = $('<div id="modal"></div>');
        $content = $('<div ></div>');

        $modal.append($content);

        $modal.hide();
        $overlay.hide();

        $(document).ready(function(){
            $('body').append($overlay, $modal);
            $('.dismiss').click(function(){
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
            if(!myapp.requireLogin())return false;
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

    myapp.requireLogin = requireLogin;
    myapp.modal = modal;
    }
});
