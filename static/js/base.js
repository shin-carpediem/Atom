"use strict";

// default
let path = window.location.pathname;

const changeLangUsers = () => {
  const changelang = document.getElementById("changeLangUsers");
  const clickbtn = document.getElementById("langBtnUsers");

  changelang.addEventListener("change", (e) => {
    clickbtn.click(e);
  });
};
changeLangUsers();

if (path !== "/") {
  const logOutConfirm = () => {
    const logout = document.getElementById("logout");

    logout.addEventListener("click", () => {
      const answer = confirm("ログアウトしますか? / Are you sure log out?");
      if (answer) {
        window.location.href = "/logout/";
      }
    });
  };
  logOutConfirm();
}

const breadCrumb = () => {
  const loginLi = document.getElementById("login_page");
  const indexLi = document.getElementById("index_page");
  const roomLi = document.getElementById("room_page");
  console.log(path);

  if (path == "/") {
    loginLi.classList.add("breadcrumb_current");

    indexLi.classList.add("breadcrumb_hide");

    roomLi.classList.add("breadcrumb_hide");
  }
  if (path == "/index") {
    loginLi.classList.remove("breadcrumb_current");
    loginLi.classList.add("breadcrumb_active");

    indexLi.classList.remove("breadcrumb_hide");
    indexLi.classList.add("breadcrumb_current");

    roomLi.classList.remove("breadcrumb_current");
    roomLi.classList.add("breadcrumb_hide");
  }
  if (path == "/room") {
    loginLi.classList.remove("breadcrumb_current");
    loginLi.classList.add("breadcrumb_active");

    indexLi.classList.remove("breadcrumb_hide");
    indexLi.classList.remove("breadcrumb_current");
    indexLi.classList.add("breadcrumb_active");

    roomLi.classList.remove("breadcrumb_hide");
    roomLi.classList.add("breadcrumb_current");
  }
};
breadCrumb();
