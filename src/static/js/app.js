/* Theme Name: 115
  Author: Themesdesign
  Version: 1.0.0
  File Description: Main JS file of the template
*/

// Show password input value

document.getElementById('password-addon').addEventListener('click', function () {
	var passwordInput = document.getElementById("password-input");
	if (passwordInput.type === "password") {
		passwordInput.type = "text";
	} else {
		passwordInput.type = "password";
	}
});

// two-step move next
function moveToNext(elem, count) {
    if (elem.value.length > 0) {
        document.getElementById("digit" + count + "-input").focus();
    }
}