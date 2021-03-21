"use strict";

const logOutConfirm = () => {
  const logout = document.getElementById("logout");

  logout.addEventListener("click", () => {
    const answer = confirm("ログアウトしますか?");
    console.log(answer);
    if (answer) {
      window.location.href = "/logout/";
    }
  });
};
logOutConfirm();

const withdrawConfirm = () => {
  const logout = document.getElementById("withdraw");

  logout.addEventListener("click", () => {
    const answer = confirm("アカウントが削除されます。本当に退会しますか?");
    console.log(answer);
    if (answer) {
      window.location.href = "/withdraw/";
    }
  });
};
withdrawConfirm();
