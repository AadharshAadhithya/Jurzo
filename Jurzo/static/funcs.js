function CopyText() {
  /* Get the text field */
  var copyText = document.getElementById("form7");

  /* Select the text field */
  copyText.select();

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("copied to clipboard: " + copyText.value);
}
