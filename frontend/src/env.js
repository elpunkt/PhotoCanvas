const env = process.env.VUE_APP_ENV;

let envApiUrl = '';

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}${process.env.VUE_APP_API_PATH}`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}${process.env.VUE_APP_API_PATH}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}${process.env.VUE_APP_API_PATH}`;
}

export const apiUrl = envApiUrl;
export const appName = process.env.VUE_APP_NAME;
