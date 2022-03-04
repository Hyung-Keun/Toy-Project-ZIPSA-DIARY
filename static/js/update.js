$(document).ready(function () {
    bsCustomFileInput.init();
});

function update() {
    let title = $('#title').val();
    let content = $('#content').val();
    let file = $('#file')[0].files[0];
    let idValue = window.location.pathname.split('/')[2];
    let name = $('#friend_name').val();
    let age = $('#friend_age').val();
    let sex = $('#friend_sex').val();
    let species = $('#friend_species').val();

    if (title === '') {
        alert('제목 추가!');
        $('#title').focus();
        return;
    } else if (friend_name === '') {
        alert('이름 추가!');
        $('#friend_name').focus();
        return;
    } else if (friend_sex === '') {
        alert('성별 추가!');
        $('#friend_sex').focus();
        return;
    } else if (friend_age === '') {
        alert('나이 추가!');
        $('#friend_age').focus();
        return;
    } else if (friend_species === '') {
        alert('주인공 추가!');
        $('#friend_species').focus();
        return;
    } else if (content === '') {
        alert('일기 추가!');
        $('#content').focus();
        return;
    }

    let form_data = new FormData();
    if (file === undefined) {
        form_data.append('title_give', title);
        form_data.append('content_give', content);
        form_data.append('friend_name_give', name);
        form_data.append('friend_age_give', age);
        form_data.append('friend_sex_give', sex);
        form_data.append('friend_species_give', species);
        form_data.append('id_give', idValue);
    } else {
        form_data.append('file_give', file);
        form_data.append('title_give', title);
        form_data.append('content_give', content);
        form_data.append('friend_name_give', name);
        form_data.append('friend_age_give', age);
        form_data.append('friend_sex_give', sex);
        form_data.append('friend_species_give', species);
        form_data.append('id_give', idValue);
    }

    $.ajax({
        type: 'PUT',
        url: '/api/diary',
        data: form_data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response['msg']);
            window.location.href = `/diary/${idValue}`;
        },
    });
}

function preview(input) {
    let imgfile = input.files;
    let filetype = imgfile[0].type.split('/').pop().toLowerCase();

    if (imgfile && imgfile[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            if ($.inArray(filetype, ['jpg', 'jpeg', 'png', 'gif']) == -1) {
                alert('jpg, jpeg, png, gif 파일만 업로드 해주세요.');
                $('#img-preview').attr('src', `../static/img/addimg.jpeg`);
                $('#posting-btn').attr('disabled', true);
                return;
            }

            $('#img-preview').attr('src', e.target.result);
            $('#posting-btn').removeAttr('disabled');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function deleteDiary() {
    let idValue = window.location.pathname.split('/')[2];
    $.ajax({
        type: 'DELETE',
        url: '/api/diary' + '?id_give=' + idValue,

        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response['msg']);
            window.location.href = '/diary';
        },
    });
}

function cancelBtn() {
    let idValue = window.location.pathname.split('/')[2];
    window.location.href = `/diary/${idValue}`;
}
