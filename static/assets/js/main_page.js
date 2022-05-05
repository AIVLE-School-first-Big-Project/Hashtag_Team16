var cnt = 0

function last_func(url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);
    $.ajax({
        type: "POST",
        url: "",
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
            }
        });
}

function img_btn(id) {
    let img_list = ['img1', 'img2', 'img3', 'img4'];
    let index = img_list.indexOf(id);
    img_list.splice(index,1);
    const target_img = document.getElementById(id);
    target_img.style.display = 'block';
    for (exception in img_list) {
        const ex_img = document.getElementById(img_list[exception]);
        ex_img.style.display = 'none';
    }
}

function GAN_image(url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);
    const imgbox = document.getElementById('img1_output');
    
    while (imgbox.hasChildNodes() ) {	// 부모노드가 자식이 있는지 여부를 알아낸다
        imgbox.removeChild(imgbox.firstChild);
    };
    
    $.ajax({
        type: "POST",
        url: "gan_image/",
        async: true,
        headers: { 'X-CSRFToken': csrftoken },
        enctype: "multipart/form-data",
        data: myformData,
        processData: false,
        contentType: false,

        error: function () {
            alert("fail!");
            $('#noneDiv').hide();
            },
        success: function (result) {
            for (tag in result) {
                var img = new Image();
                img.style = "width:100%; height: 100%; position:relative; display:none";
                img.id = tag
                img.src = "data:image/;base64,"+result[tag]
                imgbox.appendChild(img);
                };
                cnt++;
                if (cnt == 3) {
                    $('#noneDiv').hide();
                    last_func(url);
                }
            }
        });
        
}

function likes(tags, url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("tags", tags);
    const box = document.getElementById('tag_likes');

    if (document.querySelector("#tag_likes > span")) {
        document.querySelector("#tag_likes > span").remove();
    }

    $.ajax({
        type: "POST",
        url: "likes/",
        async: true,
        headers: { 'X-CSRFToken': csrftoken },
        enctype: "multipart/form-data",
        data: myformData,
        processData: false,
        contentType: false,

        error: function () {
            alert("fail!");
            $('#noneDiv').hide();
        },
        success: function (result) {
            var tags_likes = document.createElement('span');
            box.appendChild( tags_likes );
            tags_likes.innerHTML = result['like'];
            cnt++;
            if (cnt == 3) {
                $('#noneDiv').hide();
                last_func(url);
            }
        }
    });
}

function influence(tags, url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("tags", tags);
    const box = document.getElementById('tag_influ');

    if (document.querySelector("#tag_influ > span")) {
        document.querySelector("#tag_influ > span").remove();
    }

    $.ajax({
        type: "POST",
        url: "influence/",
        async: true,
        headers: { 'X-CSRFToken': csrftoken },
        enctype: "multipart/form-data",
        data: myformData,
        processData: false,
        contentType: false,

        error: function () {
            alert("fail!");
            $('#noneDiv').hide();
        },
        success: function (result) {
            var tag_influ = document.createElement('span');
            box.appendChild( tag_influ );
            tag_influ.innerHTML = result['influence'];
            cnt++;
            if (cnt == 3) {
                $('#noneDiv').hide();
                last_func(url);
            }
        }
    });
}

function hashtag(url, url2) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);
    myformData.append("url2", url2);

    // 태그 출력 부모요소
    const box = document.getElementById('tag_output');
    const legend = document.getElementById('pieID');


    while (box.hasChildNodes() ) {	// 부모노드가 자식이 있는지 여부를 알아낸다
        box.removeChild(box.firstChild);
    };
    
    while (legend.hasChildNodes() ) {	// 부모노드가 자식이 있는지 여부를 알아낸다
        legend.removeChild(legend.firstChild);
    };

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
            $('#noneDiv').hide();
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

            likes(result['hashtag'], url)
            influence(result['hashtag'], url)
        }
    });
    
};

function image_upload() {
    cnt = 0
    var fileInput = document.querySelector("#file-id");
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("attachedImage", fileInput.files[0]);
    $('#noneDiv').show();
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
            $('#noneDiv').hide();
        },
        success: function (result) {
            hashtag(result['l_url'], result['url']);
            GAN_image(result['l_url'], result['url']);

        }
    });
};

