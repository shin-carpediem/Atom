"use strict";

// default
let path = window.location.pathname;
const loading_icon = document.getElementById("loading_icon");

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

if (path == "/room") {
  const weeklyTapHouseChore = () => {
    const weeklyCard = document.getElementById("weekly__card");
    const weeklyCheck = document.getElementById("weekly__check");

    weeklyCard.addEventListener("click", () => {
      if (weeklyCheck.hasAttribute("checked")) {
        weeklyCard.classList.remove("tapped_housechore");
        weeklyCheck.removeAttribute("checked", "checked");
      } else {
        weeklyCard.classList.add("tapped_housechore");
        weeklyCheck.setAttribute("checked", "checked");
      }
    });
  };
  weeklyTapHouseChore();

  const monthlyTapHouseChore = () => {
    const monthlyCard = document.getElementById("monthly__card");
    const monthlyCheck = document.getElementById("monthly__check");
    monthlyCard.addEventListener("click", () => {
      if (monthlyCheck.hasAttribute("checked")) {
        monthlyCard.classList.remove("tapped_housechore");
        monthlyCheck.removeAttribute("checked", "checked");
      } else {
        monthlyCard.classList.add("tapped_housechore");
        monthlyCheck.setAttribute("checked", "checked");
      }
    });
  };
  monthlyTapHouseChore();
}

const breadCrumb = () => {
  const loginLi = document.getElementById("login_page");
  const indexLi = document.getElementById("index_page");
  const roomLi = document.getElementById("room_page");

  if (path == "/") {
    loginLi.classList.add("breadcrumb_current");

    indexLi.classList.add("prop_hide");

    roomLi.classList.add("prop_hide");
  }
  if (path == "/index") {
    loginLi.classList.remove("breadcrumb_current");
    loginLi.classList.add("breadcrumb_active");

    indexLi.classList.remove("prop_hide");
    indexLi.classList.add("breadcrumb_current");

    roomLi.classList.remove("breadcrumb_current");
    roomLi.classList.add("prop_hide");
  }
  if (path == "/room") {
    loginLi.classList.remove("breadcrumb_current");
    loginLi.classList.add("breadcrumb_active");

    indexLi.classList.remove("prop_hide");
    indexLi.classList.remove("breadcrumb_current");
    indexLi.classList.add("breadcrumb_active");

    roomLi.classList.remove("prop_hide");
    roomLi.classList.add("breadcrumb_current");
  }
};
breadCrumb();

const loading_show = () => {
  loading_icon.classList.remove("prop_hide");
};
loading_show();

const loading_hide = () => {
  loading_icon.classList.add("prop_hide");
};
loading_hide();
