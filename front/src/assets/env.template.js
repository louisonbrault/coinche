(function(window) {
  window.env = window.env || {};

  // Environment variables
  window["env"]["apiUrl"] = "${API_URL}";
  window["env"]["facebookAppId"] = "${FACEBOOK_APP_ID}";
})(this);
