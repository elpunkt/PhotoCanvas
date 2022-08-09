const env = process.env.NODE_ENV;


let envApiUrl = '';
let envWSUrl = '';

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}${process.env.VUE_APP_API_PATH}`;
  envWSUrl = `ws://${process.env.VUE_APP_DOMAIN_PROD}/ws`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}${process.env.VUE_APP_API_PATH}`;
  envWSUrl = `wss://${process.env.VUE_APP_DOMAIN_STAG}/ws`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}${process.env.VUE_APP_API_PATH}`;
  envWSUrl = `wss://${process.env.VUE_APP_DOMAIN_DEV}/ws`;
}

export const wsUrl = envWSUrl;
export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
