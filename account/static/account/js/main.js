$('#btn_followiing').click(function(){
    // django csrf token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });




    var user_id = $('#btn_followiing').attr('data-id')
    var status = $('#btn_followiing').text()

    if(status == 'follow'){
        var url = '/account/follow/'
        var btn_text = 'unfollow'
        var btn_class = 'btn btn-danger'
    }else{
        var url = '/account/unfollow/'
        var btn_text = 'follow'
        var btn_class = 'btn btn-primary'
    }

    $.ajax({
        url ,
        method: 'POST',
        data: {
            'user_id': user_id,
        },
        success : function(data){
            if(data['status'] == 'ok'){
                $('#btn_followiing').text(btn_text)
                $('#btn_followiing').attr({'class': btn_class})
            }
        }
    
    });
})