function signup() {
    if(check()) {
        $.ajax({
            type: "POST",
            url: "/api/signup",
            data: {
                id_give: $('#id_give').val(),
                pw_give: $('#pw_give').val(),
                pwConfirm_give: $('#pwConfirm_give').val(),
                phone_give: $('#phone_give').val(),
                birthday_give: $('#birthday_give').val(),
                sex_give: $('#sex_give').val()
            },
            success: function (response) {
                if (response['result'] == 'success') {
                    alert('회원가입이 완료되었습니다.') 
                    $.cookie('mytoken', response['token']);
                    window.location.href = "/";
                } else {
                    alert(response['msg'])
                }
            }
        })
    }                
}
function check() {
    let id = $("#id_give").val()
    let password = $("#pw_give").val();
    let passwordConfirm = $("#pwConfirm_give").val();
    let phone = $("#phone_give").val();
    let birthday = $("#birthday_give").val();
    let sex = $("#sex_give").val();
    if (id == "") {
        alert("아이디 입력해주세요!")
        $("#id_give").focus()
        return false;
    }
    if (!is_id(id)) {
        $("#idHelp").text("다시 확인! 문자와 숫자로 5자 이상 25자 이내로 입력! 일부 특수문자(._-) 사용가능!").removeClass("text-muted").addClass("text-danger");
        $("#id_give").focus()
        return false;
    }
    if (password == "") {
        alert("패스워드 입력!");
        $("#pw_give").focus()
        return false;
    }
    if (!is_password(password)) {
        $("#passwordHelp").text("다시 확인! 문자와 숫자로 8자 이상 25자 이내로 입력! 일부 특수문자(._-) 사용가능!").removeClass("text-muted").addClass("text-danger");
        $("#pw_give").focus()
        return false;
    }
    if (passwordConfirm == "") {
        alert("패스워드를 한번 더 입력!");
        $("#pwConfirm_give").focus()
        return false;
    }
    if (!is_password(passwordConfirm)) {
        $("#passwordConfirmHelp").text("패스워드 불일치! 다시 확인!").removeClass("text-muted").addClass("text-danger");
        $("#pwConfirm_give").focus()
        return false;
    }
    if (phone == "") {
        alert("폰번호를 입력! XXX-XXXX-XXXX 형식!");
        $("#phone_give").focus()
        return false;
    }
    if (!is_phone(phone)) {
        $("#phone_Help").text("폰번호 형식을 확인해주세요. XXX-XXXX-XXXX!").removeClass("text-muted").addClass("text-danger");
        $("#phone_give").focus()
        return false;
    }
    if (sex == "") {
        alert("성별 선택!");
        $("#sex_give").focus()
        return false;
    }
    if (birthday == "") {
        alert("생년월일 선택!");
        $("#birthday_give").focus()
        return false;
    }
    return true;
}
function is_id(asValue) {
    let regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{5,25}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    let regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,25}$/;
    return regExp.test(asValue);
}
function is_phone(asValue) {
    let regPhone = /^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$/;
    return regPhone.test(asValue)
}