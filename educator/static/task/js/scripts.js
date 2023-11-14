$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('.like-button').click(function () {
        const button = $(this);
        const taskId = button.data('task-id');
        const csrftoken = getCookie('csrftoken');

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        });

        $.ajax({
            type: 'POST',
            url: '/toggle_like/' + taskId + '/',
            data: {task_id: taskId},
            success: function (response) {
                if ('liked' in response && 'like_count' in response) {
                    button.siblings('.likes-count').text(response.like_count);
                    console.log('Likes count updated:', response.like_count);
                } else {
                    console.error('Invalid response format:', response);
                }
            },
            error: function (error) {
                console.error('AJAX request error:', error);
            },
            complete: function (xhr) {
                console.log('XHR status:', xhr.status);
                console.log('XHR response:', xhr.responseText);
            }
        });
    });

    function toggleFullscreenImage() {
        const fullscreenImage = $('.fullscreen-image img');
        const isVisible = fullscreenImage.is(':visible');

        if (isVisible) {
            fullscreenImage.hide();
        } else {
            const imageUrl = fullscreenImage.attr('src');
            if (imageUrl) {
                fullscreenImage.attr('src', imageUrl);
                fullscreenImage.show();
            }
        }
    }
});

