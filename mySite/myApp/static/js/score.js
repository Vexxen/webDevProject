function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(".upvote").click(function(){
    $.ajax({
        type: "POST",
        dataType: 'json',
        url: $(this).attr("data-href"),
        complete(data) {
            $("[name=scoreText-"+data.responseJSON.id+"]").html(data.responseJSON.score)
            console.log(data.responseJSON.score)
        }
    })
})

$(".downvote").click(function(){
    $.ajax({
        type: "POST",
        dataType: 'json',
        url: $(this).attr("data-href"),
        complete(data) {
            $("[name=scoreText-"+data.responseJSON.id+"]").html(data.responseJSON.score)
            console.log(data.responseJSON.score)
        }
    })
})

// var scoreApp = new Vue({
//     el: '#score',
//     data: {
//         score: 0
//     },
//     created: function(){
//     this.fetchScore();
//     this.timer = setInterval(this.fetchScore)
//     },
//     methods: {
//         fetchScore: function() {
//             axios
//                 .get()
//         }
//     }
// })