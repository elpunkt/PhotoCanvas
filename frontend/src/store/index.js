import { Api } from '@/api/api'
import router from '@/router';
import { createStore } from 'vuex'
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';

const store = createStore({
  state: {
    token: "",
    isLoggedIn: false,
    userProfile: null,
    notifications: new  Array(),
    backendTasks: new Array()
  },
  getters: {
    hasAdminAccess(state) {
        return (
            state.userProfile &&
            state.userProfile.is_superuser && state.userProfile.is_active);
    },
    isLoggedIn(state) {
      return (state.userProfile && state.isLoggedIn)
    },
    latestNotification(state) {
      if (state.notifications.length > 0) {
        return state.notifications[0]
      }
    },
  },
  mutations: {
    setToken(state, payload)  {
      state.token = payload;
    },
    setLoggedIn(state, payload) {
      state.isLoggedIn = payload;
    },
    setUserProfile(state, payload) {
      state.userProfile = payload;
    },
    addNotification(state, payload) {
      payload.timestamp = Date.now()
      state.notifications.unshift(payload)
    },
    removeNotification(state, payload) {
      state.notifications = state.notifications.filter((notification) => notification !== payload);
    }
  },
  actions: {
    async logIn(context, payload) {
      try {
        const response = await Api.logInGetToken(payload.username, payload.password);
        const token = response.data.access_token;
        if (token) {
          saveLocalToken(token);
          context.commit('setToken', token);
          context.commit('setLoggedIn', true);
          await context.dispatch('getUserProfile')
          context.commit('addNotification', { content: 'Eingeloggt.', color: 'success' })
          router.push({name: 'Home'});
        } else {
          await context.dispatch('logOut');
        }
      } catch (err) {
          console.log(err);
          // context.commit('addNotification', { content: err.response.data.detail, color: 'warning'})
          removeLocalToken();
          context.commit('setToken', '');
          context.commit('setLoggedIn', false);
      }
    },
    async logOut(context) {
      removeLocalToken();
      context.commit('setToken', '');
      context.commit('setLoggedIn', false);
      context.commit('addNotification', { content: 'Ausgeloggt', color: 'success' })
      if (router.currentRoute.path !== '/login') {
          router.push({name: 'Login'});
      }
    },
    async checkLoggedIn(context) {
      if (!context.state.isLoggedIn) {
        let token = context.state.token;
        if (!token) {
          const localToken = getLocalToken();
          if (localToken) {
            context.commit('setToken', localToken)
            token = localToken;
          }
        }
        if (token) {
          try {
            context.commit('setLoggedIn', true);
            //Immidiately setting dummy profile, so that client can begin to browse protectedd routes.
            // TODO: fix this ugly workaround
            context.commit('setUserProfile', {email: '...loading', is_superuser: true, is_active: true})
            await context.dispatch('getUserProfile')
          } catch (error) {
            removeLocalToken();
            context.commit('setToken', '');
            context.commit('setLoggedIn', false);
          }
        }
      }
    },
    async getUserProfile(context) {
      try {
        const response = await Api.getMe(context.state.token)
        context.commit('setUserProfile', response.data)
      } catch (error) {
        context.commit('addNotification', { content: "Couldn't fetch your profile, please login again.", color: "warning"})
      }
    },
    async updateUserProfile(context, payload) {
      try {
        const response = await Api.updateMe(context.state.token, payload)
        context.commit('addNotification' , { content: 'Profile successfully updated', color: 'success' });
        context.commit('setUserProfile', response.data)
        router.push('/profile/view')
      } catch (err) {
        err.response.data.detail.map((e) => {
          context.commit('addNotification', { content: e.msg, color: 'error'})
        })
      }
    },
    async changeUserPassword(context, payload) {
      try {
        await Api.updatePasswordMe(context.state.token, payload)
        context.commit('addNotification', { content: "Password updated.", color: 'success'})
        router.push('/profile/view')
      } catch (error) {
        context.commit('addNotification', { content: "Couldn't update your password", color: 'warning'})
      }
    },
    async passwordRecovery(context, username) {
      try {
        Api.passwordRecovery(username)
        context.commit('addNotification', { content: "Password recovery email sent", color: 'success'})
      } catch (error) {
        context.commit('addNotification', { content: "Couldn't send recovery email", color: 'warning'})
      }
    },
    async resetPassword(context, payload) {
      try {
        Api.resetPassword(payload, payload)
        context.commit('addNotification', { content: 'Password successfully reset', color: 'success' });
        router.push({name:'Login'})
      } catch (err) {
        context.commit('addNotification', { color: 'error', content: 'Error resetting password' });
      }
    }
  },
  modules: {
  }
})

export default store
