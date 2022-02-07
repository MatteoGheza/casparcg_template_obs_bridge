console.log("Running in " + (isProduction ? "production" : "development") + " mode");

export const SOCKET_ENDPOINT = isProduction
  ? undefined
  : 'http://localhost:5000/'