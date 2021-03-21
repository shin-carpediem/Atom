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
