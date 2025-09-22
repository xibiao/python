function getEmailCaptcha() {
    // 从register.html文件中根据id得到"获取验证码"的按钮id="captcha-btn"，当点击该按钮时会执行以下事件
    $("#captcha-btn").click(function (event) {
        // $this 代表的是当前按钮的jQuery对象
        var $this = $(this)
        // 阻止默认的事件(按钮默认的事件是提交)
        event.preventDefault();
        var email = $("input[name='email']").val();
        $.ajax({
            // 调用接口发送请求
            url: "/auth/email/captcha?email=" + email,
            method: "GET",
            success: function (result) {
                console.log('完整响应:', result); // 打印原始响应
                if (typeof result === 'undefined') {
                    alert('API返回空数据');
                    return;
                }
                var code = result['code'];
                if (code == 200) {
                    var countDown = 60;
                    // 点击获取"获取验证码"按钮之后，开始倒计时，此时需要取消按钮的点击事件，直到倒计时结束才可重新点击
                    $this.off("click");
                    var timer = setInterval(function () {
                        $this.text(countDown);
                        countDown -= 1;
                        if (countDown <= 0) {
                            // 清除掉定时器
                            clearInterval(timer);
                            // 将按钮的文字修改回原来的"获取验证码"
                            $this.text("获取验证码");
                            // 倒计时结束时需要重新绑定点击事件，可以再次点击按钮获取验证码
                            getEmailCaptcha();
                        }
                    }, 1000)
                    alert("验证码已经成功发送到邮箱！")
                } else {
                    alert(result['message']);
                }
                console.log(result);
            },
            fail: function (error) {
                console.log(error);
            }
        })
    });
}

// 对于使用register.js文件的HTML文件，等到整个HTML网页都加载完毕后再执行register.js文件中的内容
$(function () {
    getEmailCaptcha();
});