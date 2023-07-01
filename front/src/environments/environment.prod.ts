export const environment = {
  production: true,
  //@ts-ignore
  apiUrl: window["env"]["apiUrl"] || "default",
  //@ts-ignore
  googleAppId: window["env"]["googleAppId"] || "default",
};
