grecaptcha.ready(function () {
  // アクション名は英数字とスラッシュの範囲内で自由に設定できます。
  // 記事投稿には action: 'article', コメント投稿には action: 'comment' を指定するなど名前を分けることで、管理コンソールの中で各アクションの状況を区別することができます。
  grecaptcha
    .execute("6LdbF4EaAAAAAH4V9k15J9fWPE2q2RsYXbUHTSd-", { action: "submit" })
    .then(function (token) {
      // ここに元々あったデータ送信ロジックを書きます。送信データの中にtokenを追加することを忘れないでください。
      // XHRやfetchではなく<form />のPOSTを利用して送信する場合は、フォームの中にhiddenなinputを追加し、そのvalueにtokenを与えるような記述をすることになると思います。
    });
});
