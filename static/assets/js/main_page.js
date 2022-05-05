function hashtag(url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);

    // 태그 출력 부모요소
    var box = document.getElementById('tag_output');
    var legend = document.getElementById('pieID');

    try{
        for (var i = 0; i < 20; i++) {
            document.querySelectorAll("#tag_output > span")[0].remove();
        }
        for (var i = 0; i < 5; i++) {
            document.querySelector("#pieID > li")[0].remove();
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
                for (tag in result['hashtag']) {
                    var tags = document.createElement('span');
                    box.appendChild(tags);
                    tags.innerHTML = result['hashtag'][tag];
                };
                for (tag in result['best_hash']) {
                    var li = document.createElement('li');
                    var tag_name = document.createElement('em');
                    var tag_cnt = document.createElement('span');
                    legend.appendChild(li);
                    li.appendChild(tag_name);
                    li.appendChild(tag_cnt);
                    tag_name.innerHTML = tag;
                    tag_cnt.innerHTML = result['best_hash'][tag];
                    createPie(".pieID.legend", ".pieID.pie");
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

