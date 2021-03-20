"use strict";

{
  async function assignChore() {
    const res = await fetch("http://127.0.0.1:8000/api/housechore/");

    const assignChore = document.getElementById("assignChore");
    assignChore.addEventListener("click", () => {
      const housechore = await res.json();
      console.log(housechore)
    });
  }

  assignChore();
}
