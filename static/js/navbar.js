$(document).ready(function () {
    const url_string = window.location.search;
    if(url_string.includes('token_expired')) {
        $.removeCookie('mytoken', {path: '/'})
        const not_login_user_html = `<li class="nav-item">
                                            <a class="nav-link" href="/login"><img src="/static/img/loginlogin.svg" width="20" height="20" class="d-inline-block align-top" alt=""> 로그인</a>
                                        </li>
                                        <li class="nav-item">
                                            <a class="nav-link" href="/signup"><img src="/static/img/signupup.svg" width="25" height="25" class="d-inline-block align-top" alt=""> 회원가입</a>
                                        </li>`
        $("#show_user_by_token").empty().append(not_login_user_html);
        $("#show_posting_button_by_token").empty();
    }

    let token = $.cookie('mytoken');
    if (token !== undefined) {
        token = JSON.parse(atob(token.split('.')[1]));
        $("#user_id").text('😎' + token.id + ' 집사 로그인중')

    }
})

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/';
}