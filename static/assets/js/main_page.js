function hashtag(url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);

    // 태그 출력 부모요소
    var box = document.getElementById('tag_output');

    try{
        for (var i = 0; i < 20; i++) {
            document.querySelectorAll("#tag_output > span")[0].remove();
        }
    } catch (error) {
    } finally {
        $.ajax({
            type: "POST",
            url: "hashtag/",
            async: true,
            headers: { 'X-CSRFToken': csrftoken },
            enctype: "multipart/form-data",
            data: myformData,
            processData: false,
            contentType: false,
    
            error: function () {
                alert("fail!");
            },
            success: function (result) {
                console.log(result['hashtag']);

                for (tag in result['hashtag']) {
                    var tags = document.createElement('span');
                    box.appendChild(tags);
                    tags.innerHTML = result['hashtag'][tag];
                };
            }
        });
    }
};

function image_upload() {
    var fileInput = document.querySelector("#file-id");
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("attachedImage", fileInput.files[0]);

    $.ajax({
        type: "POST",
        url: "image/",
        async: true,
        headers: { 'X-CSRFToken': csrftoken },
        enctype: "multipart/form-data",
        data: myformData,
        processData: false,
        contentType: false,

        error: function () {
            alert("fail!");
        },
        success: function (result) {
            console.log(result);
            hashtag(result['l_url'])
        }
    });
};

