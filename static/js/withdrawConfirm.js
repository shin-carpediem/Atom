"use strict";

if (path == "/index") {
  const withdrawConfirm = () => {
    const logout = document.getElementById("withdraw");

    logout.addEventListener("click", () => {
      const answer = confirm(
        "アカウントが削除されます。本当に退会しますか? / Your account will be deleted. Are you sure withdraw this account?"
      );
      if (answer) {
        window.location.href = "/withdraw/";
      }
    });
  };
  withdrawConfirm();
}
