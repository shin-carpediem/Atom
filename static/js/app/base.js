"use strict";

const changeLangApp = () => {
  const changelang = document.getElementById("changeLangApp");
  const clickbtn = document.getElementById("langBtnApp");

  changelang.addEventListener("change", (e) => {
    clickbtn.click(e);
  });
};
changeLangApp();
