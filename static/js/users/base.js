"use strict";

// 保護したい各アクションを呼び出す
function onClick(e) {
  e.preventDefault();
  grecaptcha.ready(function () {
    grecaptcha.execute(
      "6LdbF4EaAAAAAH4V9k15J9fWPE2q2RsYXbUHTSd-",
      { action: "submit" }.then(function (token) {
        // const loginBtn = document.getElementById("loginBtn");
        const reCaptcha = document.getElementById("reCaptcha");
        // if (token !== "") {
        //   loginBtn.removeAttribute("disabled");
        // }
        reCaptcha.value = "token";
      })
    );
  });
}
onClick();
