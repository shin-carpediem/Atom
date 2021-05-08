"use strict";

if (path == "/index") {
  const withdrawConfirm = () => {
    const logout = document.getElementById("withdraw");

    logout.addEventListener("click", () => {
      const answer = confirm(
        "再度ログインできなくなります。本当に退会しますか? / You will not be able to log in again. Are you sure withdraw this account?"
      );
      if (answer) {
        window.location.href = "/withdraw/";
      }
    });
  };
  withdrawConfirm();
}
