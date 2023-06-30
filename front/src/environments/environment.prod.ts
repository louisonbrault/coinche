export const environment = {
  production: true,
  //@ts-ignore
  apiUrl: window["env"]["apiUrl"] || "default",
  //@ts-ignore
  facebookAppId: window["env"]["facebookAppId"] || "default",
};
