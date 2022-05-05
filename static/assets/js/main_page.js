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
            },
        success: function (result) {
            for (tag in result) {
                var img = new Image();
                img.style = "width:100%; height: 100%; position:relative; display:none";
                img.id = tag
                img.src = "data:image/;base64,"+result[tag]
                imgbox.appendChild(img);
                }
            }
        });
        
}

function hashtag(url) {
    const myformData = new FormData();
    const csrftoken = getCookie('csrftoken');
    myformData.append("url", url);

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
            hashtag(result['l_url']);
            GAN_image(result['l_url']);
        }
    });
};

