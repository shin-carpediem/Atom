"use strict";

const changeLangUsers = () => {
  const changelang = document.getElementById("changeLangUsers");
  const clickbtn = document.getElementById("langBtnUsers");

  changelang.addEventListener("change", (e) => {
    clickbtn.click(e);
  });
};
changeLangUsers();

const logOutConfirm = () => {
  const logout = document.getElementById("logout");

  logout.addEventListener("click", () => {
    const answer = confirm("ログアウトしますか? / Do you want to log out?");
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
    const answer = confirm(
      "アカウントが削除されます。本当に退会しますか? / Your account will be deleted. Do you really want to unsubscribe?"
    );
    console.log(answer);
    if (answer) {
      window.location.href = "/withdraw/";
    }
  });
};
withdrawConfirm();
